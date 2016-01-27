"""
Module designed to be used for the generation of generative grammars that focuses entirely on
generating grammars as opposed to parsing them
"""
import random
import re
import itertools
import collections
import csv
import json

import operator
# from IPython import embed


N_RULES_FIRED = 0


class IntermediateDeriv(object):
    """
    This class is used in the probabilistic Monte Carlo Expansions to associate markup with
    productions
    markup contains all markup which led to a particular string being formed
    expansion contains that string
    these are then joined at the end
    """

    def __init__(self, markup, expansion):
        self.markup = markup
        self.expansion = expansion
        self.probability = 1

    def __eq__(self, other):
        if isinstance(other, IntermediateDeriv):
            return self.__str__() == other.__str__()
        else:
            return False

    def __str__(self):
        return self.expansion.__str__() + " MARKUP" + self.markup.__str__()

    def __add__(self, other):
        # if adding two derivations together, add them
        if isinstance(other, IntermediateDeriv):

            return IntermediateDeriv(self.markup | other.markup, self.expansion + other.expansion)
        # if adding markup to a derivation, only add markup, preserve expansion
        else:
            return IntermediateDeriv(self.markup | other, self.expansion)

    def __lt__(self, other):
        return self.expansion < other.expansion

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash((self.expansion))

    def to_json(self):

        def set_default(obj):
            if isinstance(obj, Markup):
                return obj.__str__()

        return json.dumps({"derivation": self.expansion.__str__(), "markup": list(self.markup)}, default=set_default)

    def mcm_derive(self, samplesscalar, markup):
        return self.expansion.mcm_derive(samplesscalar, markup)

    def exhaustively_and_nonprobabilistically_derive(self, markup):
        """"""
        return self.expansion.exhaustively_and_nonprobabilistically_derive(markup=markup)


class Markup(object):
    """
    individual instance of markup, found as a list within NonterminalSymbol
    note:nonterminals do not have markup associated by default,
    add it using nonterminal.add_Markup
    """

    def __init__(self, tag, tagset):
        """
        create new markup belonging to tagset with given tag
        :type tag: str
        :type tagset: MarkupSet
        """
        self.tag = tag
        self.tagset = tagset
        self.time_of_definition_index = tagset.assign_time_of_definition_index()
        #add ourself to our markup

    def __eq__(self, other):
        if isinstance(other, Markup):
            return str(self.tag) == str(other.tag) and str(self.tagset) == str(other.tagset)
        else:
            return False

    def __str__(self):
        return self.tagset.__str__() + ":" + self.tag.__str__()

    def __repr__(self):
        return self.__str__()


class MarkupSet(object):
    """
    Each MarkupSet has many Markup objects
    stored in a set
    """

    def __init__(self, tagset):
        self.tagset = tagset
        self.markups = set()
        # This increments as new tags are defined to allow sorting of drop-down
        # menus in the authoring interface by time of tag definition, e.g.,
        # an ordering with the most recently defined tags listed first
        self.current_time_of_definition_index = -1

    def __eq__(self, other):
        if isinstance(other, MarkupSet):
            return str(self.tagset) == str(other.tagset)
        else:
            return False

    def add_markup(self, markup):
        """
        add a markup to ourself
        """
        if markup.tagset == self.tagset:
            self.markups.add(markup)

    def remove_markup(self, markup):
        """
        remove a markup from our set
        """
        if markup.tagset == self.tagset and markup in self.markups:
            self.markups.remove(markup)

    def assign_time_of_definition_index(self):
        """Increment the current time-of-definition index and then return the result."""
        self.current_time_of_definition_index += 1
        return self.current_time_of_definition_index

    def __str__(self):
        return self.tagset.__str__()

    def __repr__(self):
        return self.__str__()


class NonterminalSymbol(object):
    """A non-terminal symbol in a grammar."""

    def __init__(self, tag, markup=None, deep=False):
        """Initialize a NonterminalSymbol object."""
        if markup is None:
            markup = set()
        self.tag = tag
        self.rules = []  # Unordered list of rule objects
        self.rules_probability_distribution = {}
        self.markup = set()
        self.deep = deep
        self.complete = False
        for markups in list(markup):
            if markups not in list(self.markup):
                self.markup.add(markups)
        # This attribute holds a list containing all possible expansions of this symbol (each being represented by
        # an agglomerated IntermediateDerivation object); it's built once and only once the first time
        # self.exhaustively_and_nonprobabilistically_expand() is called
        self.all_possible_expansions = None

    def __eq__(self, other):
        if isinstance(other, NonterminalSymbol):
            # equality depends on tag and rules
            return self.tag == other.tag and self.rules == other.rules
        else:
            return False

    def add_rule(self, derivation, application_rate=1):
        """Add a new production rule for this nonterminal symbol."""
        rule_object = Rule(symbol=self, derivation=derivation, application_rate=application_rate)
        if rule_object not in self.rules:
            self.rules.append(rule_object)
            self._fit_probability_distribution()
            return True
        else:
            return False

    def add_rule_object(self, rule_object):
        if rule_object not in self.rules:
            self.rules.append(rule_object)
            self._fit_probability_distribution()
            return True
        else:
            return False

    def remove_rule(self, derivation):
        """remove a production rule for this nonterminal symbol."""
        rule_object = Rule(symbol=self, derivation=derivation)
        if rule_object in self.rules:
            self.rules.remove(rule_object)
            self._fit_probability_distribution()

    def remove_by_index(self, index):
        self.rules.remove(self.rules[index])
        self._fit_probability_distribution()

    def expand(self, markup=None):
        if markup is None:
            markup = set()

        """Expand this nonterminal symbol by probabilistically choosing a production rule."""
        new_markup = markup | self.markup
        selected_rule = self._pick_a_production_rule()
        return selected_rule.derive(new_markup)

    def set_deep(self, truthy):
        self.deep = truthy

    def add_markup(self, markup):
        """
        adds markup to a given nonterminalSymbol
        """
        if markup and markup not in list(self.markup):
            self.markup.add(markup)

    def remove_markup(self, markup):
        for markup_tags in list(self.markup):
            if markup == markup_tags:
                self.markup.remove(markup_tags)

    def monte_carlo_expand(self, samplesscalar=1, markup=None):
        """
        probabilistically expand our nonterminal
        samplesScalar*n times, where n is the number of productions rules
        at our particular level
        returns an array containing the n samples of the productions for self
        """
        if markup is None:
            markup = set()
        # expand n times
        rule_choices = []
        ret_list = []
        if len(self.rules) != 0:
            times = len(self.rules) * samplesscalar
        else:
            times = 1

        # union the set of our markup and the markup we are called with
        new_markup = self.markup | markup
        chosen = []

        for _ in range(times):
            selected_rule = self._pick_a_production_rule()
            chosen.append(selected_rule)
            rule_choices.append(IntermediateDeriv(new_markup, selected_rule))

        # ensure each possible production occurs at least once

        for rule in self.rules:
            if rule not in chosen:
                rule_choices.append(IntermediateDeriv(new_markup, rule))

        for derivation in rule_choices:
            # expand the rule if possible
            ret_list.append(derivation.mcm_derive(samplesscalar, new_markup))

        # there has to be a better way to do this
        is_list = 1
        for derivations in ret_list:
            if not isinstance(derivations, list):
                is_list = 0

        if is_list:
            ret_list = list(itertools.chain(*ret_list))

        return ret_list

    def exhaustively_and_nonprobabilistically_expand(self, markup=None):
        """Exhaustively expand this nonterminal symbol using each of its production rules once and only once.

        If a production rule includes an embedded nonterminal symbol that has not been expanded yet,
        this method will make a call to this same method for that nonterminal symbol to recursively
        expand it. In this way, another symbol may call this method for this symbol if it needs to expand
        it for one of its production rules. Because we don't care about probabilities, but rather
        exhaustive expansion, we can just save the results from the first time this method is called so
        that we never do the computation more than once.
        """
        if not self.all_possible_expansions:
            # Collect all of the mark-up that we have accumulated at this point
            accumulated_markup = self.markup if markup is None else self.markup | markup
            # Prepare intermediate derivations for each of the production rules associated
            # with this symbol
            intermediate_derivations = [
                IntermediateDeriv(markup=accumulated_markup, expansion=rule) for rule in self.rules
                ]
            # Fire the production rules associated with these intermediate derivations
            expanded_intermediate_derivations = []
            for intermediate_derivation in intermediate_derivations:
                expanded_intermediate_derivations.append(
                        intermediate_derivation.exhaustively_and_nonprobabilistically_derive(markup=accumulated_markup)
                )
            # Flatten out the list (JOR: not sure why exactly)
            flattened_list_of_expanded_intermediate_derivations = list(
                    itertools.chain(*expanded_intermediate_derivations)
            )
            self.all_possible_expansions = flattened_list_of_expanded_intermediate_derivations
        return self.all_possible_expansions

    def _pick_a_production_rule(self):
        """Probabilistically select a production rule."""
        if self.rules:
            x = random.random()
            selected_rule = next(
                    rule for rule in self.rules_probability_distribution if (
                        self.rules_probability_distribution[rule][0] < x <
                        self.rules_probability_distribution[rule][1])
            )
            return selected_rule
        else:
            # if there are no rules for the nonterminal, return empty string
            return Rule(self, [TerminalSymbol(self.__str__())])

    def n_terminal_expansions(self):
        """Return the number of possible terminal expansions of this symbol."""
        return sum(rule.n_terminal_expansions() for rule in self.rules)

    def __str__(self):
        return '[[' + self.tag.__str__() + ']]'

    def __repr__(self):
        return self.__str__()

    def _fit_probability_distribution(self):
        """Return a probability distribution fitted to the given application-rates dictionary."""
        if self.rules:
            application_rates_dictionary = {rule: rule.application_rate for rule in self.rules}
            frequencies_sum = float(sum(application_rates_dictionary.values()))
            probabilities = {}
            for k in application_rates_dictionary.keys():
                frequency = application_rates_dictionary[k]
                probability = frequency / frequencies_sum
                probabilities[k] = probability
            fitted_probability_distribution = {}
            current_bound = 0.0
            for k in probabilities:
                probability = probabilities[k]
                probability_range_for_k = (current_bound, current_bound + probability)
                fitted_probability_distribution[k] = probability_range_for_k
                current_bound += probability
            # Make sure the last bound indeed extends to 1.0
            last_bound_attributed = list(probabilities)[-1]
            fitted_probability_distribution[last_bound_attributed] = (
                fitted_probability_distribution[last_bound_attributed][0], 1.0
            )
            self.rules_probability_distribution = fitted_probability_distribution


class TerminalSymbol(object):
    """A terminal symbol in a grammar."""

    def __init__(self, representation):
        """Initialize a NonterminalSymbol object.
        :param representation: string value of Terminal
        :type representation: string
        """
        self.representation = representation
        self.markup = set()

    def __eq__(self, other):
        if isinstance(other, TerminalSymbol):
            return self.representation == other.representation
        else:
            return False

    def expand(self, markup=None):
        """Return this terminal symbol."""
        if markup is None:
            markup = set()
        return IntermediateDeriv(self.markup | markup, self.representation)

    def monte_carlo_expand(self, markup):
        """
        this is not a nonterminal, so the monte carlo_expand is the same as the normal expand
        """
        return self.expand(markup)

    def exhaustively_and_nonprobabilistically_expand(self, markup):
        return self.expand(markup=markup)

    def n_terminal_expansions(self):
        """Return the number of possible terminal expansions of this symbol."""
        return 1

    def __str__(self):
        return self.representation.__str__()

    def __repr__(self):
        return self.__str__()


class SystemVar(TerminalSymbol):
    """
    class to handle systemVariables which are processed by game engine
    instead of Expressionist, separate from TerminalSymbol so that
    we can provide a list of all systemVar easily
    """

    def __init__(self, representation):
        TerminalSymbol.__init__(self, representation)

    def __str__(self):
        return "[" + str(self.representation) + "]"

    def __repr__(self):
        return self.__str__()

    def __cmp__(self, other):
        # ughhh
        if isinstance(other, SystemVar):
            if str(self) < str(other):  # compare name value (should be unique)
                return -1
            elif str(self) > str(other):
                return 1
            else:
                return 0  # should mean it's the same instance
        else:
            return 0

    def expand(self, markup):
        """Return systemVar"""
        return IntermediateDeriv(self.markup | markup, self.__str__())

    def monte_carlo_expand(self, markup):
        return self.expand(markup)


class Rule(object):
    """A production rule in a grammar."""

    def __init__(self, symbol, derivation, application_rate=1, markup=None):
        """Initialize a Rule object.
        :param symbol: Nonterminal symbol(lhs) for this rule
        :type symbol: NonterminalSymbol
        :param derivation: Derivation of the NonterminalSymbol
        :type derivation: list()
        :param application_rate: application_rate(probability) for this rule
        """
        if markup is None:
            markup = set()
        self.symbol = symbol  # NonterminalSymbol that is lhs of rule
        self.derivation = derivation  # An ordered list of nonterminal and terminal symbols
        self.application_rate = application_rate
        # specific rules can have markup to represent variation within nonterminal that does not warrant a new nonterminal
        self.markup = markup
        # This attribute holds a list containing all possible derivations of this rule (each being represented by
        # an agglomerated IntermediateDerivation object); it's built once and only once the first time
        # self.exhaustively_and_nonprobabilistically_derive() is called
        self.all_possible_derivations = None

    def __eq__(self, other):
        # equality does not consider application_rate
        if isinstance(other, Rule):
            return self.symbol.tag == other.symbol.tag and self.derivation == other.derivation
        else:
            return False

    def __str__(self):
        return self.symbol.__str__() + ' -> ' + self.derivation.__str__()

    def __repr__(self):
        return self.__str__()

    def modify_application_rate(self, application_rate):
        """
        change the application rate for this rule
        """
        self.application_rate = application_rate

    def derive(self, markup=None):
        """Carry out the derivation specified for this rule."""
        if markup is None:
            markup = set()
        return (sum(symbol.expand(markup=markup) for symbol in self.derivation)) + self.markup

    def derivation_json(self):
        def stringify(x): return x.__str__()

        return map(stringify, self.derivation)

    def mcm_derive(self, samplesscalar, markup):
        """carry out montecarlo derivation for this rule"""
        ret_list = []
        # for each value in derivation side of the rule
        for symbol in self.derivation:
            # if the symbol is a nonterminal, monte_carlo_expand returns an array
            if isinstance(symbol, NonterminalSymbol):
                # List containing the mcm expansions for a given symbol
                ret_list.append(symbol.monte_carlo_expand(samplesscalar, markup))
                # samples should be intermediate derivations
            else:
                toadd = []
                toadd.append(symbol.monte_carlo_expand(markup))
                ret_list.append(toadd)

        # ret list should be a list of lists
        # either TerminalSymbols or Nonterminals Symbols
        # take this and construct a list of TerminalSymbols and singleNonterminalSymbols
        # this means represent each possible combination of NonterminalSymbols

        # ret list contains the cartesian product of its subsets, representing all possible
        # combinations of derivations
        ret_list = list(itertools.product(*ret_list))

        final = []
        for values in ret_list:
            final.append(sum(values) + self.markup)

        # at this point, ret list should be a list of the Intermediate derivations
        # ret_list = list(itertools.chain.from_iterable(ret_list))
        return final

    def exhaustively_and_nonprobabilistically_derive(self, markup):
        global N_RULES_FIRED
        N_RULES_FIRED += 1
        print "{}: {}".format(N_RULES_FIRED, self)
        if not self.all_possible_derivations:
            # Build up a list containing all the possible intermediate derivations for each
            # symbol that is used in this rule
            intermediate_derivations = []
            for symbol in self.derivation:
                if isinstance(symbol, NonterminalSymbol):
                    # If a symbol is nonterminal, then calling exhaustively_and_nonprobabilistically_expand()
                    # for it will return a list of IntermediateDerivation objects
                    intermediate_derivations.append(symbol.exhaustively_and_nonprobabilistically_expand(markup=markup))
                else:
                    # If a symbol is terminal, calling exhaustively_and_nonprobabilistically_expand() for it
                    # will return a single IntermediateDerivation that expands to the string representing the
                    # nonterminal symbol; as such, we need to wrap this object up in a list before we append it
                    intermediate_derivations.append(
                            [symbol.exhaustively_and_nonprobabilistically_expand(markup=markup)]
                    )
            # To exhaustively compute all possible intermediate derivations for this symbol, we
            # simply take the Cartesian product of the list of lists that we have just built
            all_possible_combinations_of_intermediate_derivations = list(itertools.product(*intermediate_derivations))
            # Now we can yield new intermediate derivations for each of these combinations
            # that combines the string expansions and annotations of all the intermediate derivations
            # in the combination
            new_combined_intermediate_derivations = [
                sum(combination_of_intermediate_derivations) + self.markup for
                combination_of_intermediate_derivations in all_possible_combinations_of_intermediate_derivations
                ]
            self.all_possible_derivations = new_combined_intermediate_derivations
        return self.all_possible_derivations

    def add_markup(self, markup):
        if markup not in self.markup:
            self.markup.add(markup)

    def remove_markup(self, markup):
        # this is pretty gross, but it's working, I suppose
        if markup in list(self.markup):
            a = list(self.markup)
            a.remove(markup)
            self.markup = set(a)

    def n_terminal_expansions(self):
        """Return the number of possible terminal expansions of this rule."""
        # Since there's no product() built-in function in Python that works like sum()
        # does, we have to use this ugly reduce thing
        n_terminal_expansions = (
            reduce(operator.mul, (symbol.n_terminal_expansions() for symbol in self.derivation), 1)
        )
        return n_terminal_expansions


def parse_rule(rule_string):
    """
    function parses a string and returns the generation represented by that string
    :param rule_string: the string representing the rule to be parsed
    :type rule_string: string
    :returns: list[symbols]
    """

    # this regex is a pain but it matches strings of either [[...]] or [...]
    split_list = re.split('(\[\[[^\[{2}]+\]\]|\[[^\]]+])', rule_string)
    # remove all empty strings
    split_list = filter(None, split_list)

    derivation = []
    for token in split_list:
        brackets = token.count("[")
        stripped = token.lstrip("[").rstrip("]")

        if brackets == 2:
            derivation.append(NonterminalSymbol(stripped))
        elif brackets == 1:
            derivation.append(SystemVar(stripped))
        else:
            derivation.append(TerminalSymbol(stripped))
    return derivation


class PCFG(object):
    """
    Driver class for our PCFG, allows us to index our nonterminals and
    system variables so that the user can more easily modify them in real time
    Also allows us to selectively expand NonterminalSymbols to see all of their productions
    """

    def __init__(self, monte_carlo=False):
        self.nonterminals = {}
        self.system_vars = []
        self.markup_class = {}
        self.monte_carlo = monte_carlo  # Whether export will rely on a Monte Carlo derivation procedure

    def add_nonterminal(self, nonterminal):
        """ add a nonterminal to our grammar"""
        if not self.nonterminals.get(str(nonterminal.tag)):
            self.nonterminals[str(nonterminal.tag)] = nonterminal
        # this accomodates the recursive definition of nonterminals
        for markups in list(nonterminal.markup):
            self.add_markup(nonterminal, markups)

    def add_rule(self, nonterminal, derivation, application_rate=1):
        """
        add a rule to a nonterminal
        recursion makes this a paaaain
        problems arise with associating nonterminals that have the same tag with their correct
        nonterminal representation within the PCFG class nonterminals[] list
        so we have to do this manually with each token in derivation
        or else we end up with nonterminals that have the same tag but do not have the same
        productions associated with them
        """
        nonterm_add = self.nonterminals.get(str(nonterminal.tag))
        if nonterm_add:
            new_derivation = []
            for token in derivation:
                if isinstance(token, NonterminalSymbol):
                    if self.nonterminals.get(token.tag):
                        new_derivation.append(self.nonterminals.get(token.tag))
                    else:
                        self.add_nonterminal(token)
                        new_derivation.append(token)
                elif isinstance(token, SystemVar) and token not in self.system_vars:
                    self.system_vars.append(token)
                    new_derivation.append(token)
                else:
                    new_derivation.append(token)

            nonterm_add.add_rule(new_derivation, application_rate)

    def remove_rule(self, nonterminal, derivation):
        """remove a rule from a nonterminal"""
        self.nonterminals.get(str(nonterminal.tag)).remove_rule(derivation)

    def remove_rule_by_index(self, nonterminal, rule_index):
        """ remove a rule from a nonterminal by its index"""
        self.nonterminals.get(str(nonterminal.tag)).remove_by_index(rule_index)

    def expand(self, nonterminal):
        """expand a given nonterminal"""
        return self.nonterminals.get(str(nonterminal.tag)).expand(markup=set())

    def modify_application_rate(self, nonterminal, rule_index, application_rate):
        """modify application_rate for the given nonterminal and derivation"""
        rules = self.nonterminals.get(str(nonterminal.tag)).rules
        rules[rule_index].modify_application_rate(application_rate)
        self.nonterminals.get(str(nonterminal.tag))._fit_probability_distribution()

    def monte_carlo_expand(self, nonterminal, samplesscalar=1):
        """
        performs monte_carlo_expand on a given nonterminal
        returns a list of size len(nonterminal.rules)*samplesscalar(no longer true, now size can
        vary depending on if every possible production was sampled
        """
        return self.nonterminals[nonterminal.tag].monte_carlo_expand(samplesscalar)

    def exhaustively_and_nonprobabilistically_expand(self, nonterminal):
        """Exhaustively and nonprobabilistically expands a nonterminal, producing one of each possible derivation."""
        return self.nonterminals[nonterminal.tag].exhaustively_and_nonprobabilistically_expand()

    def set_deep(self, nonterminal, truthy):
        self.nonterminals[str(nonterminal.tag)].set_deep(truthy)

    def add_markup(self, nonterminal, markup):
        """
        add markup to an existing nonterminal
        :type markup: Markup
        """
        if self.nonterminals.get(str(nonterminal.tag)):
            if not self.markup_class.get(str(markup.tagset)):
                self.markup_class[str(markup.tagset)] = set()
            self.markup_class[str(markup.tagset)].add(markup)
            self.nonterminals.get(str(nonterminal.tag)).add_markup(markup)

    def add_rule_markup(self, nonterminal, rule, markup):
        """
        add a markup to a specific rule in a nonterminal
        will add it to the PCFG's markup_class as well
        nonterminal is the nonterminal we are going to change,
        rule holds the index of the rule we are changing
        markup holds the markup we are adding
        """
        self.add_unused_markup(markup)
        self.nonterminals.get(str(nonterminal.tag)).rules[rule].add_markup(markup)

    def remove_rule_markup(self, nonterminal, rule, markup):
        """
        remove occurence of markup from a given rule
        """
        self.nonterminals.get(str(nonterminal.tag)).rules[rule].remove_markup(markup)

    def toggle_rule_markup(self, nonterminal, rule, markup):
        if markup in list(self.nonterminals.get(str(nonterminal.tag)).rules[rule].markup):
            print("removing rule markup")
            self.remove_rule_markup(nonterminal, rule, markup)
        else:
            print("adding rule markup")
            self.add_rule_markup(nonterminal, rule, markup)

    def remove_markup(self, nonterminal, markup):
        """
        add markup to an existing nonterminal
        :type markup: Markup
        """
        nonterminal = self.nonterminals.get(str(nonterminal.tag))
        if nonterminal:
            nonterminal.remove_markup(markup)

    def toggle_markup(self, nonterminal, markup):
        if markup in list(self.nonterminals.get(str(nonterminal.tag)).markup):
            self.remove_markup(nonterminal, markup)
            print "removing markup"
        else:
            if str(nonterminal.tag) in self.nonterminals:
                print "adding markup"
                self.add_markup(nonterminal, markup)
            else:
                print('nonterminal not found!')

    def add_unused_markup(self, markup):

        if not self.markup_class.get(str(markup.tagset)):
            self.markup_class[str(markup.tagset)] = set()

        self.markup_class[str(markup.tagset)].add(markup)

    def add_new_markup_set(self, markupSet):

        if not self.markup_class.get(str(markupSet.tagset)):
            self.markup_class[str(markupSet.tagset)] = set()

    def monte_carlo_export(self, nonterminal, filename, samplesscalar=1, ):
        """
        returns a tab seperated value list of productions, duplicates removed.
        one thing I need to change is to output the set of markup in a nicer fashion
        """
        expansion = collections.Counter(sorted(self.monte_carlo_expand(nonterminal, samplesscalar)))
        with open(filename, 'a') as csvfile:
            row_writer = csv.writer(csvfile, delimiter='\t', quotechar='|', quoting=
            csv.QUOTE_MINIMAL)
            prob_range = 0
            for deriv in expansion:
                rng_interval = float(expansion[deriv]) / sum(expansion.values())
                rng_max = prob_range + rng_interval
                temp_prob = [prob_range, rng_max]
                row_writer.writerow(
                        [nonterminal, str(deriv.expansion),
                         '^'.join(str(annotation) for annotation in list(deriv.markup)),
                         [prob_range, rng_max]]
                )
                prob_range += rng_interval

    def exhaustively_and_nonprobabilistically_export(self, nonterminal, filename):
        """Append to a tab-separated file lines specifying each of the templated lines of dialogue that
        may be yielded by each of the possible terminal expansions of nonterminal.
        """
        all_possible_expansions_of_this_symbol = (
            self.exhaustively_and_nonprobabilistically_expand(nonterminal=nonterminal)
        )
        with open(filename, 'a') as export_tsv_file:
            row_writer = csv.writer(
                    export_tsv_file, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL
            )
            for intermediate_derivation_object in all_possible_expansions_of_this_symbol:
                row_writer.writerow(
                        [nonterminal, str(intermediate_derivation_object.expansion),
                         '^'.join(str(annotation) for annotation in list(intermediate_derivation_object.markup)),
                         ['N/A', 'N/A']]  # We write 'N/A' here to indicate that we did not expand probabilistically
                )

    def export_all(self, filename):
        with open(filename, 'w') as tsv_export_file:
            row_writer = csv.writer(
                    tsv_export_file, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL
            )
            header = ['Top-level Symbol', 'Expansion', 'Markup', 'Probability']
            row_writer.writerow(header)
        for nonterminal in self.nonterminals.itervalues():
            if nonterminal.deep:
                print "Expanding top-level symbol {}".format(nonterminal)
                if self.monte_carlo:
                    self.monte_carlo_export(nonterminal, filename)
                else:
                    self.exhaustively_and_nonprobabilistically_export(nonterminal=nonterminal, filename=filename)

    def to_json(self):
        # total represents our final dictionary we will conver to JSON
        total = {}
        # use defaultdict as it allows us to assume they are sets
        markups = collections.defaultdict(set)
        # nonterminals are their own dictionaries
        nonterminals = {}
        for key, value in self.nonterminals.iteritems():
            temp = {}
            if len(value.rules) != 0:
                value.complete = True
            else:
                value.complete = False
            temp['deep'] = value.deep
            temp['complete'] = value.complete
            rules_list = []
            for rules in value.rules:
                rule_mu_dict = collections.defaultdict(set)

                # createJSON representation for individual rule markup
                for markup in rules.markup:
                    rule_mu_dict[markup.tagset.__str__()] |= {markup.tag}
                    markups[markup.tagset.__str__()] |= {markup.tag}

                rules_list.append({'expansion': rules.derivation_json(), 'app_rate': rules.application_rate,
                                   'markup': rule_mu_dict})
            temp['rules'] = rules_list

            markup_dict = collections.defaultdict(set)
            for markup in value.markup:
                markup_dict[markup.tagset.__str__()] |= {markup.tag}
                markups[markup.tagset.__str__()] |= {markup.tag}

            temp['markup'] = markup_dict
            nonterminals[value.tag.__str__()] = temp

        total['nonterminals'] = nonterminals

        total['markups'] = {}
        for markupset in self.markup_class:
            total['markups'][str(markupset)] = set()
            for tag_object in self.markup_class[markupset]:
                if total['markups'].get(str(markupset)):
                    total['markups'][str(markupset)] |= {tag_object}
                else:
                    total['markups'][str(markupset)] = {tag_object}
            # Sort these in reverse order of definition time, meaning the most recently
            # defined mark-up shows up at the top of the drop-down; this makes it easy
            # to find and attribute a new tag that you've just defined in the case of
            # a very large tagset
            total['markups'][str(markupset)] = sorted(
                total['markups'][str(markupset)],
                key=lambda tag: tag.time_of_definition_index, reverse=True
            )
            # Just save the strings for the tags for each of the tag objects
            total['markups'][str(markupset)] = [
                str(tag_object.tag) for tag_object in total['markups'][str(markupset)]
            ]
            
        total['system_vars'] = sorted(self.system_vars)

        def set_default(obj):
            if isinstance(obj, set):
                return list(obj)
            if isinstance(obj, SystemVar):
                return str(obj)
            raise TypeError

        return json.dumps(total, default=set_default, sort_keys=True)
        # create the nonterminal dictonary

    def n_possible_derivations(self):
        """Return the number of possible terminal derivations that may yielded by this grammar."""
        return sum(symbol.n_terminal_expansions() for symbol in self.nonterminals.values() if symbol.deep)


def from_json(json_in):
    gram_res = PCFG()
    dict_rep = json.loads(json_in)
    nonterminals = dict_rep.get('nonterminals')
    for tag, nonterminal in nonterminals.iteritems():
        rules = nonterminal['rules']
        markup = nonterminal['markup']

        # translate UI markup rep into data markup rep
        tmp_markups = []
        for markup_set, tags in markup.iteritems():
            tmp_set = MarkupSet(markup_set)
            for i in tags:
                new_mark = Markup(i, tmp_set)
                tmp_markups.append(new_mark)

        temp_nonterm = NonterminalSymbol(tag, markup=set(tmp_markups), deep=nonterminal['deep'])
        gram_res.add_nonterminal(temp_nonterm)

        for ruleindex, rule in enumerate(rules):
            # rule is an object
            expansion = parse_rule(''.join(rule['expansion']))
            application_rate = rule['app_rate']
            markup = rule['markup']
            tmp_markups = []
            for markup_set, tags in markup.iteritems():
                tmp_set = MarkupSet(markup_set)
                for i in tags:
                    new_mark = Markup(i, tmp_set)
                    tmp_markups.append(new_mark)

            gram_res.add_rule(temp_nonterm, expansion, application_rate)
            for markups in tmp_markups:
                gram_res.add_rule_markup(temp_nonterm, ruleindex, markups)
    for markupSet in dict_rep.get('markups'):
        gram_res.add_new_markup_set(MarkupSet(markupSet))

    return gram_res
