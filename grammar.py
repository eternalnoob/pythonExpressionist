"""
Module designed to be used for the generation of generative grammars that focuses entirely on
generating grammars as opposed to parsing them
"""
import random
import re
import itertools




class NonterminalSymbol(object):
    """A non-terminal symbol in a grammar."""

    def __init__(self, tag):
        """Initialize a NonterminalSymbol object."""
        self.tag = tag
        self.rules = []  # Unordered list of rule objects
        self.rules_probability_distribution = {}

    def __eq__(self, other):
        #equality depends on tag and rules
        return self.tag == other.tag and self.rules == other.rules

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

    def monte_carlo_expand(self, samplesscalar=1):
        """
        probabilistically expand our nonterminal
        samplesScalar*n times, where n is the number of productions rules
        at our particular level
        returns an array containing the n samples of the productions for self
        """
        #expand n times
        ret_list = []
        times = len(self.rules)*samplesscalar

        for _ in range(times):
            selected_rule = self._pick_a_production_rule()
            ret_list.append(selected_rule.mcm_derive())

        return ret_list

    def full_monte(self):
        """
        This returns the flattened monte_carlo_expand for this nonterminal.
        due to the recursive nature of it, monte_carlo_expand returns a list whose size is
        len(self.rules)*samplesScalar, to represent each initial sample of our initial Nonterminal
        """

        #flatten the result of monte carlo expansion
        return list(itertools.chain.from_iterable(self.monte_carlo_expand()))



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
            return Rule(self, [TerminalSymbol("")])

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
    def __eq__(self, other):
        return self.representation == other.representation

    def expand(self):
        """Return this terminal symbol."""
        return self.representation

    def monte_carlo_expand(self):
        return self.expand()

    def __str__(self):
        return self.representation.__str__()

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

    def expand(self):
        """Return this terminal symbol."""
        return self.__str__()

    def monte_carlo_expand(self):
        return self.expand()


class Rule(object):
    """A production rule in a grammar."""

    def __init__(self, symbol, derivation, application_rate=1):
        """Initialize a Rule object.
        :param symbol: Nonterminal symbol(lhs) for this rule
        :type symbol: NonterminalSymbol
        :param derivation: Derivation of the NonterminalSymbol
        :type derivation: list()
        :param application_rate: application_rate(probability) for this rule
        :type application_rate: int
        """
        self.symbol = symbol # NonterminalSymbol that is lhs of rule
        self.derivation = derivation  # An ordered list of nonterminal and terminal symbols
        self.application_rate = application_rate

    def __eq__(self, other):
        #equality does not consider application_rate
        return self.symbol.tag == other.symbol.tag and self.derivation == other.derivation

    def modify_application_rate(self, application_rate):
        """
        change the application rate for this rule
        """
        self.application_rate = application_rate

    def derive(self):
        """Carry out the derivation specified for this rule."""
        return ''.join(symbol.expand() for symbol in self.derivation)

    def mcm_derive(self):
        """carry out montecarlo derivation for this rule"""
        ret_list = []
        #for each value in derivation side of the rule
        for symbol in self.derivation:
            symbol_arr = []
            #if the symbol is a nonterminal, monte_carlo_expand returns an array
            if isinstance(symbol, NonterminalSymbol):
                #List containing the mcm expansions for a given symbol
                for sample in symbol.monte_carlo_expand():
                    symbol_arr.append(sample)
            else:
                #other wise append the 
                symbol_arr.append(symbol.monte_carlo_expand())

            ret_list.append(symbol_arr)

        #ret list should be a list of lists
        #either TerminalSymbols or Nonterminals Symbols
        #take this and construct a list of TerminalSymbols and singleNonterminalSymbols
        #this means represent each possible combination of NonterminalSymbols

        #ret list contains the cartesian product of its subsets, representing all possible
        #combinations of nonterminal choices to be made
        ret_list = itertools.product(*ret_list)

        joined = []
        for productions in ret_list:
            joined.append(''.join(itertools.chain.from_iterable(list(productions))))


        return joined

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

    def add_nonterminal(self, nonterminal):
        """ add a nonterminal to our grammar"""
        if nonterminal not in self.nonterminals:
            self.nonterminals.append(nonterminal)


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

    def expand(self, nonterminal, nTimes=1):
        """expand a given nonterminal"""
        return self.nonterminal(nonterminal).expand()

    def nonterminal(self, nonterminal):
        """handles weirdness"""
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

    def monte_carlo_expand(self, nonterminal, samplesScalar = 2):
        return self.nonterminal(nonterminal).monte_carlo_expand(samplesScalar=2)

    def full_monte(self, nonterminal):
        return self.nonterminal(nonterminal).full_monte()

