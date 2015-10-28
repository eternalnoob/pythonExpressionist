"""
Module designed to be used for the generation of generative grammars that focuses entirely on
generating grammars as opposed to parsing them
"""
import random
import re
import itertools
import collections
import csv


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

    def __eq__(self, other):
        if isinstance(other, IntermediateDeriv):
            return self.markup == other.markup and self.expansion == other.expansion
        else:
            return False

    def __str__(self):
        return self.expansion.__str__()+" MARKUP"+self.markup.__str__()

    def __add__(self, other):
        return IntermediateDeriv(self.markup | other.markup, self.expansion + other.expansion)

    def __lt__(self, other):
        return self.expansion < other.expansion

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def mcm_derive(self, samplesscalar,  markup):
            return  self.expansion.mcm_derive(samplesscalar, markup)

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(( self.expansion))



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
        #add ourself to our markup

    def __eq__(self, other):
        if isinstance(other, Markup):
            return self.tag == other.tag and self.tagset == other.tagset
        else:
            return False

    def __str__(self):
        return self.tagset.__str__()+":"+self.tag.__str__()

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

    def __eq__(self, other):
        return self.tagset == other.tagset and self.markups == other.markups

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
    def __str__(self):
        return self.tagset


class NonterminalSymbol(object):
    """A non-terminal symbol in a grammar."""

    def __init__(self, tag, markup=set()):
        """Initialize a NonterminalSymbol object."""
        self.tag = tag
        self.rules = []  # Unordered list of rule objects
        self.rules_probability_distribution = {}
        self.markup = set()
        if markup:
            self.markup.add(markup)

    def __eq__(self, other):
        if isinstance(other, NonterminalSymbol):
        #equality depends on tag and rules
            return self.tag == other.tag and self.rules == other.rules
        else:
            return False

    def add_rule(self, derivation, application_rate=1):
        """Add a new production rule for this nonterminal symbol."""
        rule_object = Rule(symbol=self, derivation=derivation, application_rate=application_rate)
        self.rules.append(rule_object)
        self._fit_probability_distribution()

    def remove_rule(self, derivation):
        """remove a production rule for this nonterminal symbol."""
        rule_object = Rule(symbol=self, derivation=derivation)
        if rule_object in self.rules:
            self.rules.remove(rule_object)
            self._fit_probability_distribution()

    def expand(self):
        """Expand this nonterminal symbol by probabilistically choosing a production rule."""
        selected_rule = self._pick_a_production_rule()
        return selected_rule.derive()

    def add_markup(self, markup):
        """
        adds markup to a given nonterminalSymbol
        """
        if markup:
            self.markup.add(markup)

    def monte_carlo_expand(self, samplesscalar=1, markup=set()):
        """
        probabilistically expand our nonterminal
        samplesScalar*n times, where n is the number of productions rules
        at our particular level
        returns an array containing the n samples of the productions for self
        """
        #expand n times
        rule_choices = []
        ret_list = []
        if len(self.rules) != 0:
            times = len(self.rules)*samplesscalar
        else:
            times = 1

        #union the set of our markup and the markup we are called with
        new_markup = self.markup | markup
        chosen = []

        for _ in range(times):
            selected_rule = self._pick_a_production_rule()
            chosen.append(selected_rule)
            rule_choices.append(IntermediateDeriv(new_markup, selected_rule))

        #ensure each possible production occurs at least once

        for rule in self.rules:
            if rule not in chosen:
                rule_choices.append(IntermediateDeriv(new_markup, rule))

        for derivation in rule_choices:
            #expand the rule if possible
            ret_list.append(derivation.mcm_derive(samplesscalar, new_markup))

        #there has to be a better way to do this
        is_list = 1
        for derivations in ret_list:
            if not isinstance(derivations, list):
                is_list = 0

        if is_list:
            ret_list = list(itertools.chain(*ret_list))


        return ret_list

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
            #if there are no rules for the nonterminal, return empty string
            return Rule(self, [TerminalSymbol(self.__str__())])

    def __str__(self):
        return '[['+self.tag.__str__()+']]'

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
                probability = frequency/frequencies_sum
                probabilities[k] = probability
            fitted_probability_distribution = {}
            current_bound = 0.0
            for k in probabilities:
                probability = probabilities[k]
                probability_range_for_k = (current_bound, current_bound+probability)
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

    def expand(self, markup):
        """Return this terminal symbol."""
        return IntermediateDeriv(self.markup | markup, self.representation)

    def monte_carlo_expand(self, markup):
        """
        this is not a nonterminal, so the monte carlo_expand is the same as the normal expand
        """
        return self.expand(markup)

    def __str__(self):
        return "["+ self.representation.__str__()+"]"

    def __repr__(self):
        return self.__str__()

class SystemVar(TerminalSymbol):
    """
    class to handle systemVariables which are processed by game engine
    instead of Expressionist, seperate from TerminalSymbol so that
    we can provide a list of all systemVar easily
    """

    def __init__(self, representation):
        TerminalSymbol.__init__(self, representation)

    def __str__(self):
        return "[" + self.representation + "]"

    def __repr__(self):
        return self.__str__()

    def expand(self, markup):
        """Return systemVar"""
        return IntermediateDeriv(self.markup | markup, self.__str__())

    def monte_carlo_expand(self, markup):
        return self.expand( markup )


class Rule(object):
    """A production rule in a grammar."""

    def __init__(self, symbol, derivation, application_rate=1):
        """Initialize a Rule object.
        :param symbol: Nonterminal symbol(lhs) for this rule
        :type symbol: NonterminalSymbol
        :param derivation: Derivation of the NonterminalSymbol
        :type derivation: list()
        :param application_rate: application_rate(probability) for this rule
        """
        self.symbol = symbol # NonterminalSymbol that is lhs of rule
        self.derivation = derivation  # An ordered list of nonterminal and terminal symbols
        self.application_rate = application_rate

    def __eq__(self, other):
        #equality does not consider application_rate
        if isinstance(other, Rule):
            return self.symbol.tag == other.symbol.tag and self.derivation == other.derivation
        else:
            return False

    def modify_application_rate(self, application_rate):
        """
        change the application rate for this rule
        """
        self.application_rate = application_rate

    def derive(self):
        """Carry out the derivation specified for this rule."""
        return ''.join(symbol.expand() for symbol in self.derivation)

    def mcm_derive(self, samplesscalar, markup):
        """carry out montecarlo derivation for this rule"""
        ret_list = []
        #for each value in derivation side of the rule
        for symbol in self.derivation:
            #if the symbol is a nonterminal, monte_carlo_expand returns an array
            if isinstance(symbol, NonterminalSymbol):
                #List containing the mcm expansions for a given symbol
                ret_list.append(symbol.monte_carlo_expand(samplesscalar, markup))
                    #samples should be intermediate derivations
            else:
                toadd = []
                toadd.append(symbol.monte_carlo_expand(markup))
                ret_list.append(toadd)

        #nothing from here on to end of funct
        #ret list should be a list of lists
        #either TerminalSymbols or Nonterminals Symbols
        #take this and construct a list of TerminalSymbols and singleNonterminalSymbols
        #this means represent each possible combination of NonterminalSymbols

        #ret list contains the cartesian product of its subsets, representing all possible
        #combinations of derivations
        ret_list = list(itertools.product(*ret_list))

        final = []
        for values in ret_list:
            final.append(sum(values))

        #at this point, ret list should be a list of the Intermediate derivations
        #ret_list = list(itertools.chain.from_iterable(ret_list))


        return final




    def __str__(self):
        return self.symbol.__str__()+ ' -> ' + self.derivation.__str__()

    def __repr__(self):
        return self.__str__()

def parse_rule(rule_string):
    """
    function parses a string and returns the generation represented by that string
    :param rule_string: the string representing the rule to be parsed
    :type rule_string: string
    :returns: list[symbols]
    """

    #this regex is a pain but it matches strings of either [[...]] or [...]
    split_list = re.split('(\[\[[^\[{2}]+\]\]|\[[^\]]+])', rule_string)
    #remove all empty strings
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

    def __init__(self):
        self.nonterminals = []
        self.system_vars = []
        self.markup_class = set()

    def add_nonterminal(self, nonterminal):
        """ add a nonterminal to our grammar"""
        if nonterminal not in self.nonterminals:
            self.nonterminals.append(nonterminal)
        for markups in nonterminal.markup:
            if markups.tagset not in self.markup_class:
                self.markup_class.add(markups.tagset)


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
        nonterm_add = self.nonterminal(nonterminal)
        new_derivation = []
        for token in derivation:
            if isinstance(token, NonterminalSymbol):
                if any(token.tag == nt.tag for nt in self.nonterminals):
                    new_derivation.append(self.nonterminal(token))
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
        self.nonterminal(nonterminal).remove_rule(derivation)

    def expand(self, nonterminal):
        """expand a given nonterminal"""
        return self.nonterminal(nonterminal).expand()

    def nonterminal(self, nonterminal):
        """handles weirdness, this works kind of in the place of a dictionary which I will implement
        when I have more time and sanity"""
        for inner_nonterminal in self.nonterminals:
            if nonterminal.tag == inner_nonterminal.tag:
                return inner_nonterminal

    def modify_application_rate(self, nonterminal, derivation, application_rate):
        """modify application_rate for the given nonterminal and derivation"""
        rules = self.nonterminal(nonterminal).rules
        for rule in rules:
            if rule.derivation == derivation:
                rule.modify_application_rate(application_rate)
                self.nonterminal(nonterminal)._fit_probability_distribution()

    def monte_carlo_expand(self, nonterminal, samplesscalar=1):

        """
        performs monte_carlo_expand on a given nonterminal
        returns a list of size len(nonterminal.rules)*samplesscalar(no longer true, now size can
        very depending on if every possible production was sampled
        """

        return self.nonterminal(nonterminal).monte_carlo_expand(samplesscalar)

    def add_markup(self, nonterminal, markup):
        """
        add markup to an existing nonterminal
        :type markup: Markup
        """
        if markup.tagset not in self.markup_class:
            self.markup_class.add(markup.tagset)
        self.nonterminal(nonterminal).add_markup(markup)

    def export(self, nonterminal, samplesscalar=1):
        """
        returns a tab seperated value list of productions, duplicates removed.
        one thing I need to change is to output the set of markup in a nicer fashion
        """
        expansion = collections.Counter(sorted(self.monte_carlo_expand(nonterminal,samplesscalar)))
        with open('output.tsv', 'w') as csvfile:
            row_writer = csv.writer( csvfile, delimiter='\t', quotechar='|', quoting =
                    csv.QUOTE_MINIMAL)
            row_writer.writerow( ['Deep Meaning', 'Expansion','Markup', 'Probability'] )
            for deriv in expansion:
                row_writer.writerow( [nonterminal, str(deriv.expansion),  deriv.markup,
                        float(expansion[deriv])/sum(expansion.values())])

