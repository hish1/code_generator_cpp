import unittest
from Parser import *
from SemanticTools import get_value_type


class ParserTestCase(unittest.TestCase):

    def test_var(self):
        reader = open('parserTestsPas/var', 'r')
        input_code = reader.read()
        reader.close()
        reader2 = open('parserTestsTrees/var_tree', 'r')
        expected_tree = reader2.read()
        reader2.close()
        self.assertTreesEqual(input_code, expected_tree)

    def test_type(self):
        reader = open('parserTestsPas/type', 'r')
        input_code = reader.read()
        reader.close()
        reader2 = open('parserTestsTrees/type_tree', 'r')
        expected_tree = reader2.read()
        reader2.close()
        self.assertTreesEqual(input_code, expected_tree)

    def test_2d_array(self):
        reader = open('parserTestsPas/2d_array', 'r')
        input_code = reader.read()
        reader.close()
        reader2 = open('parserTestsTrees/2d_array_tree', 'r')
        expected_tree = reader2.read()
        reader2.close()
        self.assertTreesEqual(input_code, expected_tree)

    def test_const(self):
        reader = open('parserTestsPas/const', 'r')
        input_code = reader.read()
        reader.close()
        reader2 = open('parserTestsTrees/const_tree', 'r')
        expected_tree = reader2.read()
        reader2.close()
        self.assertTreesEqual(input_code, expected_tree)

    def test_case(self):
        reader = open('parserTestsPas/case', 'r')
        input_code = reader.read()
        reader.close()
        reader2 = open('parserTestsTrees/case_tree', 'r')
        expected_tree = reader2.read()
        reader2.close()
        self.assertTreesEqual(input_code, expected_tree)

    def test_function(self):
        reader = open('parserTestsPas/function', 'r')
        input_code = reader.read()
        reader.close()
        reader2 = open('parserTestsTrees/function_tree', 'r')
        expected_tree = reader2.read()
        reader2.close()
        self.assertTreesEqual(input_code, expected_tree)

    def test_procedure(self):
        reader = open('parserTestsPas/procedure', 'r')
        input_code = reader.read()
        reader.close()
        reader2 = open('parserTestsTrees/procedure_tree', 'r')
        expected_tree = reader2.read()
        reader2.close()
        self.assertTreesEqual(input_code, expected_tree)

    def test_if_then(self):
        reader = open('parserTestsPas/if_then', 'r')
        input_code = reader.read()
        reader.close()
        reader2 = open('parserTestsTrees/if_then_tree', 'r')
        expected_tree = reader2.read()
        reader2.close()
        self.assertTreesEqual(input_code, expected_tree)

    def test_if_then_else(self):
        reader = open('parserTestsPas/if_then_else', 'r')
        input_code = reader.read()
        reader.close()
        reader2 = open('parserTestsTrees/if_then_else_tree', 'r')
        expected_tree = reader2.read()
        reader2.close()
        self.assertTreesEqual(input_code, expected_tree)

    def test_if_then_else_extended(self):
        reader = open('parserTestsPas/if_then_else_extended', 'r')
        input_code = reader.read()
        reader.close()
        reader2 = open('parserTestsTrees/if_then_else_extended_tree', 'r')
        expected_tree = reader2.read()
        reader2.close()
        self.assertTreesEqual(input_code, expected_tree)

    def test_while(self):
        reader = open('parserTestsPas/while', 'r')
        input_code = reader.read()
        reader.close()
        reader2 = open('parserTestsTrees/while_tree', 'r')
        expected_tree = reader2.read()
        reader2.close()
        self.assertTreesEqual(input_code, expected_tree)

    def test_while_extended(self):
        reader = open('parserTestsPas/while_extended', 'r')
        input_code = reader.read()
        reader.close()
        reader2 = open('parserTestsTrees/while_extended_tree', 'r')
        expected_tree = reader2.read()
        reader2.close()
        self.assertTreesEqual(input_code, expected_tree)

    def test_for(self):
        reader = open('parserTestsPas/for', 'r')
        input_code = reader.read()
        reader.close()
        reader2 = open('parserTestsTrees/for_tree', 'r')
        expected_tree = reader2.read()
        reader2.close()
        self.assertTreesEqual(input_code, expected_tree)

    def test_for_extended(self):
        reader = open('parserTestsPas/for_extended', 'r')
        input_code = reader.read()
        reader.close()
        reader2 = open('parserTestsTrees/for_extended_tree', 'r')
        expected_tree = reader2.read()
        reader2.close()
        self.assertTreesEqual(input_code, expected_tree)

    def test_repeat_until(self):
        reader = open('parserTestsPas/repeat_until', 'r')
        input_code = reader.read()
        reader.close()
        reader2 = open('parserTestsTrees/repeat_until_tree', 'r')
        expected_tree = reader2.read()
        reader2.close()
        self.assertTreesEqual(input_code, expected_tree)

    def test_repeat_until_extended(self):
        reader = open('parserTestsPas/repeat_until_extended', 'r')
        input_code = reader.read()
        reader.close()
        reader2 = open('parserTestsTrees/repeat_until_extended_tree', 'r')
        expected_tree = reader2.read()
        reader2.close()
        self.assertTreesEqual(input_code, expected_tree)

    def test_writeln_readln(self):
        reader = open('parserTestsPas/writeln_readln', 'r')
        input_code = reader.read()
        reader.close()
        reader2 = open('parserTestsTrees/writeln_readln_tree', 'r')
        expected_tree = reader2.read()
        reader2.close()
        self.assertTreesEqual(input_code, expected_tree)

    def test_invalid_declaration_part(self):
        reader = open('parserTestsPas/invalid_declaration_part', 'r')
        input_code = reader.read()
        reader.close()
        with self.assertRaises(AttributeError):
            self.get_tree(input_code)

    def get_tree(self, input_code):
        lexer = Lexer(input_code)
        parser = Parser(lexer)
        res = parser.parse()
        return str(res)

    def assertTreesEqual(self, input_code, expected_tree):
        self.assertEqual(expected_tree, self.get_tree(input_code))


class SemanticTestCase(unittest.TestCase):

    def test_a(self):
        self.assertTreesEqual(str(254), 'BYTE')
    def test_b(self):
        self.assertTreesEqual(str(254/128), 'REAL')

    def get_result(self, input_code):
        return get_value_type(input_code)

    def assertTreesEqual(self, input_code, expected_result):
        self.assertEqual(expected_result, self.get_result(input_code))

if __name__ == "__main__":
    unittest.main()
