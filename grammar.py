import random


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

    def expand(self):
        """Expand this nonterminal symbol by probabilistically choosing a production rule."""
        selected_rule = self._pick_a_production_rule()
        return selected_rule.derive()

    def _pick_a_production_rule(self):
        """Probabilistically select a production rule."""
        x = random.random()
        selected_rule = next(
            rule for rule in self.rules_probability_distribution if
            self.rules_probability_distribution[rule][0] < x < self.rules_probability_distribution[rule][1]
        )
        return selected_rule

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


class Rule(object):
    """A production rule in a grammar."""

    def __init__(self, symbol, derivation, application_rate):
        """Initialize a Rule object."""
        self.symbol = symbol
        self.derivation = derivation  # An ordered list of nonterminal and terminal symbols
        self.application_rate = application_rate

    def derive(self):
        """Carry out the derivation specified for this rule."""
        return ''.join(symbol.expand() for symbol in self.derivation)


