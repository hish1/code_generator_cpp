import sys


class Token:
    def __init__(self, row, col, type, value):
        self.row, self.col, self.type, self.value = row, col, type, value

    def __repr__(self):
        return f"Type: {Lexer.PRESENTATION[self.type]}; Value: <{self.value}>"

    def __str__(self):
        return f"-{Lexer.PRESENTATION[self.type]}\t'{self.value}'"


class Lexer:
    def __init__(self, input_string):
        self.input_string = input_string
        self.input_length = len(input_string)
        self.current_pos = 0
        self.current_char = None
        self.row, self.col = 1, 0

    PROGRAM, VAR, BEGIN, INTEGER, REAL, NUMBER, \
        BOOLEAN, CHAR, STRING, STRING_VAL, IF, THEN, ELSE, \
        WHILE, DO, REPEAT, UNTIL, WRITE, READ, \
        WRITELN, READLN, FUNCTION, PROCEDURE, \
        NOT, IDENTIFIER, FOR, LPAREN, RPAREN, \
        TRUE, FALSE, RBR, LBR, RCBR, LCBR, LESS, GREATER, \
        TAB, DOT, COMMA, COLON, SEMICOLON, \
        SINGLE_QUOTE, DOUBLE_QUOTE, COMMENT,\
        PLUS, MINUS, MULTIPLY, ASSIGN, DIVIDE, END, EOF, \
        AND, IN, NEWLINE, RESULT, EQUAL, ARRAY, TO, \
        OF, LE, GE, SLASH, NOTEQ, ARRDOT, \
        BYTE, WORD, LONGWORD, UINT64, SHORTINT, SMALLINT, \
        INT64, SINGLE, DOUBLE, DECIMAL, TYPE, CONST = range(76)

    PRESENTATION = {
        PROGRAM: "program",
        VAR: "var",
        BEGIN: "begin",
        INTEGER: "integer",
        REAL: "real",
        NUMBER: "number",
        BOOLEAN: "boolean",
        ARRAY: "array",
        CHAR: "char",
        STRING: "string",
        STRING_VAL: "string_val",
        IF: "if",
        THEN: "then",
        ELSE: "else",
        EQUAL: "equal",
        WHILE: "while",
        DO: "do",
        REPEAT: "repeat",
        UNTIL: "until",
        FUNCTION: "function",
        PROCEDURE: "procedure",
        WRITE: "write",
        READ: "read",
        TO: "to",
        ARRDOT: "doubleDot",
        WRITELN: "writeln",
        READLN: "readln",
        FOR: "for",
        LPAREN: "lparen",
        RPAREN: "rparen",
        TRUE: "true",
        FALSE: "false",
        RBR: "rbr",
        LBR: "lbr",
        RCBR: "rcbr",
        LCBR: "lcbr",
        LESS: "less",
        GREATER: "greater",
        TAB: "tab",
        DOT: "dot",
        COMMA: "comma",
        COLON: "colon",
        SEMICOLON: "semicolon",
        SINGLE_QUOTE: "singleQuote",
        DOUBLE_QUOTE: "doubleQuote",
        PLUS: "plus",
        MINUS: "minus",
        MULTIPLY: "multiply",
        ASSIGN: "assign",
        DIVIDE: "divide",
        END: "end",
        EOF: "eof",
        AND: "and",
        NOT: "not",
        IN: "in",
        NEWLINE: "newline",
        RESULT: "result",
        LE: "le",
        GE: "ge",
        SLASH: "slash",
        NOTEQ: "noteq",
        IDENTIFIER: "identifier",
        COMMENT: "comment"
    }

    KEYWORDS = {
        'if': 'IF',
        'else': 'ELSE',
        'while': 'WHILE',
        'for': 'FOR',
        'do': 'DO',
        'function': 'FUNCTION',
        'procedure': 'PROCEDURE',
        'array': 'ARRAY',
        'repeat': 'REPEAT',
        'number': 'NUMBER',
        'and': 'AND',
        'in': 'IN',
        'end': 'END',
        'then': 'THEN',
        'begin': 'BEGIN',
        'var': 'VAR',
        'type': 'TYPE',
        'const': 'CONST',
        'program': 'PROGRAM',
        'true': 'TRUE',
        'to': 'TO',
        'false': 'FALSE',
        'until': 'UNTIL',
        'of': 'OF',
        'case' : 'CASE',
        'div' : 'DIV',
        'mod' : 'MOD'
    }

    TYPES = {
        'byte': 'BYTE',
        'word': 'WORD',
        'longword': 'LONGWORD',
        'uint64': 'UINT64',
        'shortint': 'SHORTINT',
        'smallint': 'SMALLINT',
        'integer': 'INTEGER',
        'int64': 'INT64',
        'boolean': 'BOOLEAN',
        'char': 'CHAR',
        'string': 'STRING',
        'real': 'REAL',
        'double': 'DOUBLE'
    }

    n_tabs = 4
    SYMBOLS = {
        ':=': 'ASSIGN',
        '=': 'EQUALITY',
        '+': 'PLUS',
        '-': 'MINUS',
        '*': 'MULTIPLY',
        '/': 'DIVIDE',
        '(': 'LPAREN',
        ')': 'RPAREN',
        '[': 'LBR',
        ']': 'RBR',
        '{': 'LCBR',
        '}': 'RCBR',
        '\t': 'TAB',
        '<=': 'GREATER_OR_EQUAL',
        '>=': 'SMALLER_OR_EQUAL',
        '<>': 'NONEQUALITY',
        ' ' * n_tabs: 'TAB',
        ',': 'COMMA',
        ':': 'COLON',
        ';': 'SEMICOLON',
        '<': 'LESS',
        '>': 'GREATER',
        "'": 'SINGLE_QUOTE',
        '"': 'DOUBLE_QUOTE',
        '.': 'DOT',
        '..': 'ARRDOT',
        '\n': 'NEWLINE'
    }

    def error(self, message):
        print("Lexer error:", message, f"at line {self.row}, index {self.col - 1}")
        sys.exit(1)

    def get_next_char(self):
        if self.current_char == '\n':
            self.row += 1
            self.col = 0
        if self.current_pos < self.input_length:
            self.current_char = self.input_string[self.current_pos]
            self.current_pos += 1
            self.col += 1
        else:
            self.current_char = ''

    def get_next_token(self):
        self.state = None
        self.value = None
        while self.state is None:
            if self.current_char is None:
                self.get_next_char()

            # end of file
            if self.current_char == '':
                self.state = 'EOF'
                self.value = 'eof'

            # whitespaces and tabulation
            elif self.current_char in [' ', '\t', '\n']:
                self.get_next_char()

            # string quote1
            elif self.current_char == "'":
                self.value = ""
                self.get_next_char()
                while self.current_char != "'":
                    self.value += self.current_char
                    self.get_next_char()
                self.get_next_char()
                if self.current_char == "'":
                    self.value += "'"
                    self.get_next_char()
                    while self.current_char != "'":
                        self.value += self.current_char
                        self.get_next_char()
                    self.get_next_char()
                if len(self.value) == 1:
                    self.state = 'CHAR_VAL'
                else:
                    self.state = 'STRING_VAL'

            # symbols
            elif self.current_char in Lexer.SYMBOLS:

                # assign :=
                if self.current_char == ':':
                    self.get_next_char()
                    if self.current_char == '=':
                        self.state = 'ASSIGN'
                        self.value = ':='
                        self.get_next_char()
                    else:
                        self.state = 'COLON'
                        self.value = ':'
                        self.get_next_char()
                
                # <= >= and <>
                elif self.current_char in ('>', '<'):
                    val = self.current_char
                    self.get_next_char()
                    if self.current_char in ('=', '>'):
                        val += self.current_char
                        self.get_next_char()
                    self.state = Lexer.SYMBOLS[val]
                    self.value = val

                #  array dot ..
                elif self.current_char == '.':
                    self.get_next_char()
                    if self.current_char == '.':
                        self.state = 'ARRDOT'
                        self.value = '..'
                        self.get_next_char()
                    else:
                        self.state = 'DOT'
                        self.value = '.'
                        self.get_next_char()

                # comment (* *)
                elif self.current_char == '(':
                    prev = self.current_char
                    self.get_next_char()
                    if self.current_char == '*':
                        self.state = 'COMMENT'
                        self.value = '(*'
                        while self.current_char != "*":
                            self.value += self.current_char
                            self.get_next_char()
                        self.get_next_char()
                        if self.current_char != ")":
                            self.value += self.current_char
                            self.get_next_char()
                            while self.current_char != ")":
                                self.value += self.current_char
                                self.get_next_char()
                            self.value += ')'
                            self.get_next_char()
                    else:
                        self.state = 'LPAREN'
                        self.value = prev

                else:
                    self.state = Lexer.SYMBOLS[self.current_char]
                    self.value = self.current_char  # ?
                    self.get_next_char()  # ?

            # numbers float and integer
            elif self.current_char != None and self.current_char.isdigit():
                number = 0
                while self.current_char.isdigit():
                    number = number * 10 + int(self.current_char)
                    self.get_next_char()
                if self.current_char.isalpha() or self.current_char == "_":
                    self.error(f'Invalid identifier')
                if self.current_char == '.':
                    number = str(number)
                    number += '.'
                    self.get_next_char()
                    while self.current_char.isdigit():
                        number += self.current_char
                        self.get_next_char()
                    if self.current_char == '.':
                        number = number[:-1]
                        self.current_char += '.'
                    elif number[len(number) - 1] == '.':
                        self.error(f'Invalid number ')
                number = str(number)
                self.state = 'NUMBER'
                self.value = str(number)

            # identifiers, keywords and reserved names
            elif self.current_char != None and self.current_char.isalpha() or self.current_char == '_':
                identifier = ""
                while self.current_char.isalpha() or self.current_char.isdigit() or self.current_char == '_':
                    identifier += self.current_char
                    self.get_next_char()
                if identifier.lower() in Lexer.KEYWORDS:
                    self.state = Lexer.KEYWORDS[identifier.lower()]
                    self.value = identifier  # ?
                elif identifier.lower() in Lexer.TYPES:
                    self.state = Lexer.TYPES[identifier.lower()]
                    self.value = identifier
                else:
                    self.state = 'IDENTIFIER'
                    self.value = identifier
            else:
                self.error(f'Unexpected symbol: {self.current_char}')

        token = (self.state, self.value, self.row, self.col)
        return token

if __name__ == '__main__':
    reader = open('comp/test.pas', 'r')
    code = reader.read()
    lexer = Lexer(code)
    token = lexer.get_next_token()
    while token[0] != 'EOF':
        print(token)
        token = lexer.get_next_token()