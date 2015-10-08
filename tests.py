"""import unittest for running tests"""
import unittest
from grammar import NonterminalSymbol, Rule, parse_rule, PCFG, TerminalSymbol

class TestNonterminalEquivalency(unittest.TestCase):
    """
    Testing Equivalency of NonterminalSymbols
    """
    def setUp(self):
        self.a_nonterminal = NonterminalSymbol('A')
        self.b_nonterminal = NonterminalSymbol('A')
        self.aaa = NonterminalSymbol('AAA')
        self.bbb = NonterminalSymbol('BBB')

    def test_should_eq_each_other(self):
        """identical nonterminals should equal eachother"""
        self.assertEqual(self.a_nonterminal, self.b_nonterminal)

    def test_different_not_eq(self):
        """nonidentical nonterminals should not equal eachother"""
        self.assertNotEqual(self.aaa, self.bbb)

    def test_different_rules_not_eq(self):
        """Nonterminals with the same tag but different rules should not equal eachother"""
        a_rule = parse_rule("[[Test of]] rule parsing")
        self.a_nonterminal.add_rule(a_rule)
        self.assertEqual(self.a_nonterminal.tag, self.b_nonterminal.tag)
        self.assertNotEqual(self.a_nonterminal, self.b_nonterminal)


class TestRuleEquivalency(unittest.TestCase):
    """
    Test equivalency of Rules
    """
    def setUp(self):
        self.a_derivation = parse_rule("[[Test]] of [rule] {parsing}")
        self.a_nonterminal = NonterminalSymbol('A')
        self.a_rule = Rule(self.a_nonterminal, self.a_derivation, application_rate=1)
        self.b_rule = Rule(self.a_nonterminal, self.a_derivation, application_rate=1)

    def test_equal_rules(self):
        """Identical Rules Should equal eachother"""
        self.assertEqual(self.a_rule, self.b_rule)

    def test_different_app_rates(self):
        """Identical Rules with different application_rates should eq"""
        self.b_rule.application_rate = 3
        self.assertNotEqual(self.a_rule.application_rate, self.b_rule.application_rate)
        self.assertEqual(self.a_rule, self.b_rule)

    def test_different_derivations(self):
        """
        Rules with identical symbols but different derivations should not eq
        """
        c_derivation = parse_rule("[[haha]] we're testing it again")
        c_nonterminal = self.a_nonterminal
        c_rule = Rule(c_nonterminal, c_derivation)
        self.assertNotEqual(c_rule, self.a_rule)

    def test_different_symbols(self):
        """
        Rules with identical derivations but different symbols should not eq
        """
        c_nonterminal = NonterminalSymbol('c')
        c_rule = Rule(c_nonterminal, self.a_derivation)
        self.assertNotEqual(c_rule, self.a_rule)

class TestPcfgOperations(unittest.TestCase):
    """
    Testing operations on a PCFG
    """
    def setUp(self):
        self.test_gram = PCFG()
        self.nonterminal = NonterminalSymbol('a')

    def test_add_nonterminal(self):
        """
        test adding a nonterminal to a PCFG
        """
        nonterminal = NonterminalSymbol('a')
        self.test_gram.add_nonterminal(nonterminal)
        test_nonterminals = [NonterminalSymbol('a')]
        self.assertEqual(self.test_gram.nonterminals, test_nonterminals)

    def test_add_rule(self):
        """
        test adding a rule to an existing nonterminal in PCFG
        """
        self.test_gram.add_nonterminal(self.nonterminal)
        test_derivation = [NonterminalSymbol('b'), "aaaaade"]
        self.test_gram.add_rule(self.nonterminal, test_derivation)
        test_rules = [Rule(self.nonterminal, test_derivation)]
        self.assertEqual(self.test_gram.nonterminal(self.nonterminal).rules, test_rules)

    def test_remove_rule(self):
        """
        test that it successfully removes an implemented rule
        """
        self.test_gram.add_nonterminal(self.nonterminal)
        test_derivation = [NonterminalSymbol('b'), "aaaaade"]
        self.test_gram.remove_rule(self.nonterminal, test_derivation)
        self.assertEqual(self.test_gram.nonterminal(self.nonterminal).rules, [])

    def test_expansion(self):
        """
        test expansions of our grammar
        """
        self.test_gram.add_nonterminal(self.nonterminal)
        a_prod = parse_rule("[[b]], this is a test of expansion")
        self.test_gram.add_rule(self.nonterminal, a_prod)
        self.test_gram.add_nonterminal(a_prod[0])
        b_prod = parse_rule("Wow")
        self.test_gram.add_rule(a_prod[0], b_prod)
        test_string = "Wow, this is a test of expansion"
        self.assertEqual(self.test_gram.expand(NonterminalSymbol('a')), test_string)

    def test_recursive_nt_addition(self):
        """
        add_rule should add all nonterminals present in derivation
        that are not in the grammar to the grammar
        """
        self.test_gram.add_nonterminal(self.nonterminal)
        a_prod = parse_rule("[[b]], this is a test of expansion")
        self.test_gram.add_rule(self.nonterminal, a_prod)
        self.assertEqual(2, len(self.test_gram.nonterminals))


    def test_empty_expansion(self):
        """
        test that expansions of nonterminals with no productions works correctly
        """
        self.test_gram.add_nonterminal(self.nonterminal)
        a_prod = parse_rule("[[b]], this is a test of expansion")
        self.test_gram.add_rule(self.nonterminal, a_prod)
        self.test_gram.add_nonterminal(a_prod[0])
        test_string = ", this is a test of expansion"
        self.assertEqual(self.test_gram.expand(NonterminalSymbol('a')), test_string)


    def test_modify_app_rate(self):
        """
        test that application rates are correctly modified
        """
        self.test_gram.add_nonterminal(self.nonterminal)
        a_prob = parse_rule("test of application_rate")
        self.test_gram.add_rule(self.nonterminal, a_prob)
        old_app = self.test_gram.nonterminal(self.nonterminal).rules[0].application_rate
        self.test_gram.modify_application_rate(self.nonterminal, a_prob, 5)
        new_app = self.test_gram.nonterminal(self.nonterminal).rules[0].application_rate
        self.assertNotEqual(old_app, new_app)
        self.assertEqual(new_app, 5)







if __name__ == '__main__':
    unittest.main()

