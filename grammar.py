
"""
Module designed to be used for the generation of generative grammars that focuses entirely on
generating grammars as opposed to parsing them
"""
import random
import re

class NonterminalSymbol(object):
    """A non-terminal symbol in a grammar."""

    def __init__(self, tag):
        """Initialize a NonterminalSymbol object."""
        self.tag = tag
        self.rules = []  # Unordered list of rule objects
        self.rules_probability_distribution = {}

    def add_rule(self, derivation, application_rate):
        """Add a new production rule for this nonterminal symbol."""
        rule_object = Rule(symbol=self, derivation=derivation, application_rate=application_rate)
        self.rules.append(rule_object)
        self._fit_probability_distribution()

    def remove_rule(self, derivation, application_rate):
        """remove a production rule for this nonterminal symbol."""
        rule_object = Rule(symbol=self, derivation=derivation, application_rate=application_rate)
        if rule_object in self.rules:
            self.rules.remove(rule_object)
            self._fit_probability_distribution()

    def expand(self):
        """Expand this nonterminal symbol by probabilistically choosing a production rule."""
        selected_rule = self._pick_a_production_rule()
        return selected_rule.derive()

    def _pick_a_production_rule(self):
        """Probabilistically select a production rule."""
        x = random.random()
        selected_rule = next(
                rule for rule in self.rules_probability_distribution if (
                self.rules_probability_distribution[rule][0] < x <
                self.rules_probability_distribution[rule][1])
                )
        return selected_rule

    def __str__(self):
        return '[['+self.tag.__str__()+']]'

    def __repr__(self):
        return self.__str__()

    def _fit_probability_distribution(self):
        """Return a probability distribution fitted to the given application-rates dictionary."""
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
        """Initialize a NonterminalSymbol object."""
        self.representation = representation

    def expand(self):
        """Return this terminal symbol."""
        return self.representation

    def __str__(self):
        return "\"" + self.representation.__str__() + "\""

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
        return "\[" + self.representation + "\]"

    def __repr__(self):
        return self.__str__


class Rule(object):
    """A production rule in a grammar."""

    def __init__(self, symbol, derivation, application_rate=1):
        """Initialize a Rule object."""
        self.symbol = symbol # NonterminalSymbol that is lhs of rule
        self.derivation = derivation  # An ordered list of nonterminal and terminal symbols
        self.application_rate = application_rate

    def __eq__(self, other):
        return self.symbol == other.symbol and self.derivation == other.derivation and self.application_rate == other.application_rate

    def modify_application_rate(self, application_rate):
        """
        change the application rate for a given Rule
        """
        self.application_rate = application_rate

    def derive(self):
        """Carry out the derivation specified for this rule."""
        return ''.join(symbol.expand() for symbol in self.derivation)

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
    #
    rhs = []
    for token in split_list:
        brackets = token.count("[")
        stripped = token.lstrip("[").rstrip("]")

        if brackets == 2:
            rhs.append(NonterminalSymbol(stripped))
        elif brackets == 1:
            rhs.append(SystemVar(stripped))
        else:
            rhs.append(TerminalSymbol(stripped))
    return rhs

class PCFG(object):
    """
    Driver class for our PCFG, allows us to index our nonterminals and
    system variables so that the user can more easily modify them in real time
    Also allows us to selectively expand NonterminalSymbols to see all of their productions
    """

    def __init__(self):
        self.nonterminals = []

    def add_nonterminal(self, nonterminal):
        """ add a nonterminal to our grammar"""
        if nonterminal not in self.nonterminals:
            self.nonterminals.append(nonterminal)













