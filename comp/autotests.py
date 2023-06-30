from lexer import Lexer as lex
import unittest
import re


class TestLexer(unittest.TestCase):
    def test_empty_input(self):
        code = ''
        expected_tokens = [('EOF', '')]
        self.assertEqual(lex.tokenize(self,code), expected_tokens)

    def test_identifier(self):
        code = 'foo'
        expected_tokens = [('IDENTIFIER', 'foo'),
                           ('EOF', '')]
        self.assertEqual(lex.tokenize(self,code), expected_tokens)

    def test_integer(self):
        code = '1'
        expected_tokens = [('NUMBER', '1'),
                           ('EOF', '')]
        self.assertEqual(lex.tokenize(self,code), expected_tokens)

    def test_float(self):
        code = '1.1'
        expected_tokens = [('NUMBER', '1'),
                           ('DOT', '.'),
                           ('NUMBER', '1'),
                           ('EOF', '')]
        self.assertEqual(lex.tokenize(self,code), expected_tokens)

    def test_string(self):
        code = "'aa'"
        expected_tokens = [('QUOTES', "'"),
                           ('IDENTIFIER', 'aa'),
                           ('QUOTES', "'"),
                           ('EOF', '')]
        self.assertEqual(lex.tokenize(self,code), expected_tokens)

    def test_invalid_identifier(self):
        code = '123foo'
        with self.assertRaises(ValueError):
            lex.tokenize(self,code)

    def test_integer_overflow(self):
        code = '32768'
        with self.assertRaises(ValueError):
            lex.tokenize(self,code)

    def test_valid_keywords(self):
        code = 'PROGRAM begin end if then else while do repeat until for to FUNCTION PROCEDURE VAR integer real boolean char array of read readln write writeln'
        expected_tokens = [('PROGRAM', 'PROGRAM'),
                           ('BEGIN', 'begin'),
                           ('END', 'end'),
                           ('IF', 'if'),
                           ('THEN', 'then'),
                           ('ELSE', 'else'),
                           ('WHILE', 'while'),
                           ('DO', 'do'),
                           ('REPEAT', 'repeat'),
                           ('UNTIL', 'until'),
                           ('FOR', 'for'),
                           ('TO', 'to'),
                           ('FUNCTION', 'FUNCTION'),
                           ('PROCEDURE', 'PROCEDURE'),
                           ('VAR', 'VAR'),
                           ('INTEGER', 'integer'),
                           ('REAL', 'real'),
                           ('BOOLEAN', 'boolean'),
                           ('CHAR', 'char'),
                           ('ARRAY', 'array'),
                           ('OF', 'of'),
                           ('READ', 'read'),
                           ('READLN', 'readln'),
                           ('WRITE', 'write'),
                           ('WRITELN', 'writeln'),
                           ('EOF', '')]
        self.assertEqual(lex.tokenize(self,code), expected_tokens)

    def test_invalid_keywords(self):
        code = 'begin2 end4 if-then while_2 do# repeat^until 5for goto'
        with self.assertRaises(ValueError):
            lex.tokenize(self,code)

    def test_multiple_tokens(self):
        code = 'VAR x : integer ; x := 42 ; writeln (            x )'
        expected_tokens = [('VAR', 'VAR'),
                           ('IDENTIFIER', 'x'),
                           ('COLON', ':'),
                           ('INTEGER', 'integer'),
                           ('SEMICOLON', ';'),
                           ('IDENTIFIER', 'x'),
                           ('ASSIGN', ':='),
                           ('NUMBER', '42'),
                           ('SEMICOLON', ';'),
                           ('WRITELN', 'writeln'),
                           ('LPAREN', '('),
                           ('IDENTIFIER', 'x'),
                           ('RPAREN', ')'),
                           ('EOF', '')]
        self.assertEqual(lex.tokenize(self,code), expected_tokens)

    def test_simple_assignment(self):
        code = "x := 10;"
        expected_tokens = [
            ('IDENTIFIER', 'x'),
            ('ASSIGN', ':='),
            ('NUMBER', '10'),
            ('SEMICOLON', ';'),
            ('EOF', '')]
        self.assertEqual(lex.tokenize(self,code), expected_tokens)

    def test_variable_declaration(self):
        code = "VAR x: integer;"
        expected_tokens = [
            ('VAR', 'VAR'),
            ('IDENTIFIER', 'x'),
            ('COLON', ':'),
            ('INTEGER', 'integer'),
            ('SEMICOLON', ';'),
            ('EOF', '')
        ]
        self.assertEqual(lex.tokenize(self,code), expected_tokens)

    def test_function_declaration(self):
        code = "FUNCTION add(a, b: integer): integer;\nbegin\n  add := a + b;\nend;"
        expected_tokens = [
            ('FUNCTION', 'FUNCTION'),
            ('IDENTIFIER', 'add'),
            ('LPAREN', '('),
            ('IDENTIFIER', 'a'),
            ('COMMA', ','),
            ('IDENTIFIER', 'b'),
            ('COLON', ':'),
            ('INTEGER', 'integer'),
            ('RPAREN', ')'),
            ('COLON', ':'),
            ('INTEGER', 'integer'),
            ('SEMICOLON', ';'),
            ('BEGIN', 'begin'),
            ('IDENTIFIER', 'add'),
            ('ASSIGN', ':='),
            ('IDENTIFIER', 'a'),
            ('PLUS', '+'),
            ('IDENTIFIER', 'b'),
            ('SEMICOLON', ';'),
            ('END', 'end'),
            ('SEMICOLON', ';'),
            ('EOF', '')
        ]
        self.assertEqual(lex.tokenize(self,code), expected_tokens)

    def test_invalid_variable_name(self):
        code = "2x := 10;"
        with self.assertRaises(ValueError):
            lex.tokenize(self,code)

    # def test_single_line_comment(self):
    #     code = "x := 5; {this is a comment} y := 7;"
    #     expected_tokens = [
    #         ('IDENTIFIER', 'x'),
    #         ('ASSIGN', ':='),
    #         ('NUMBER', '5'),
    #         ('SEMICOLON', ';'),
    #         ('IDENTIFIER', 'y'),
    #         ('ASSIGN', ':='),
    #         ('NUMBER', '7'),
    #         ('SEMICOLON', ';'),
    #         ('EOF', '')
    #     ]
    #     self.assertEqual(lex.tokenize(self,code), expected_tokens)

    # def test_multi_line_comment(self):
    #     code = """
    #         (*
    #         This is a
    #         multi-line
    #         comment
    #         *)
    #         x := 5;
    #     """
    #     expected_tokens = [
    #         ('IDENTIFIER', 'x'),
    #         ('ASSIGN', ':='),
    #         ('NUMBER', '5'),
    #         ('SEMICOLON', ';'),
    #         ('EOF', '')
    #     ]
    #     self.assertEqual(lex.tokenize(self,code), expected_tokens)

    def test_a_identifier(self):
        code = 'x y1 _z abc_123'
        tokens = lex.tokenize(self,code)
        expected_tokens = [('IDENTIFIER', 'x'),
                           ('IDENTIFIER', 'y1'),
                           ('IDENTIFIER', '_z'),
                           ('IDENTIFIER', 'abc_123'),
                           ('EOF', '')
                            ]
        self.assertEqual(tokens, expected_tokens)

    def test_invalid_identifier2(self):
        code = '1x abc.def'
        with self.assertRaises(ValueError) as cm:
            lex.tokenize(self,code)
        self.assertEqual(str(cm.exception), 'SyntaxError: Invalid variable name "1x" on line 1')

    def test_invalid_identifier3(self):
        code = 'x.y'
        with self.assertRaises(ValueError) as cm:
            lex.tokenize(self,code)
        self.assertEqual(str(cm.exception), 'SyntaxError: Invalid variable name "x.y" on line 1')

    def test_number(self):
        code = '123 456'
        tokens = lex.tokenize(self,code)
        expected_tokens = [('NUMBER', '123'),
                           ('NUMBER', '456'),
                           ('EOF', '')]
        self.assertEqual(tokens, expected_tokens)

    def test_overflow_number_2(self):
        code = '999999999999999999999999999999999999999999999999999999999999999'
        with self.assertRaises(ValueError) as cm:
            lex.tokenize(self,code)
        self.assertEqual(str(cm.exception),
                         'ValueError: Integer overflow "999999999999999999999999999999999999999999999999999999999999999" on line 1')

    def test_keywords(self):
        code = 'begin while do end if then else'
        tokens = lex.tokenize(self,code)
        expected_tokens = [('BEGIN', 'begin'),
                           ('WHILE', 'while'),
                           ('DO', 'do'),
                           ('END', 'end'),
                           ('IF', 'if'),
                           ('THEN', 'then'),
                           ('ELSE', 'else'),
                           ('EOF', '')]
        self.assertEqual(tokens, expected_tokens)

    def test_operators(self):
        code = '+ - * / := ; ( ) . , :'
        tokens = lex.tokenize(self,code)
        expected_tokens = [('PLUS', '+'),
                           ('MINUS', '-'),
                           ('MULTIPLY', '*'),
                           ('DIVIDE', '/'),
                           ('ASSIGN', ':='),
                           ('SEMICOLON', ';'),
                           ('LPAREN', '('),
                           ('RPAREN', ')'),
                           ('DOT', '.'),
                           ('COMMA', ','),
                           ('COLON', ':'),
                           ('EOF', '')]
        self.assertEqual(tokens, expected_tokens)


if __name__ == '__main__':
    unittest.main()

def main():
    pass