import re
import enum

# Define regular expressions for each token
regex_patterns = {
    'VAR': r'VAR',
    'PROGRAM': r'PROGRAM',
    'TYPE': r'TYPE',
    'CONST': r'CONST',
    'BEGIN': r'begin',
    'END': r'end',
    'INTEGER': r'integer',
    'REAL': r'real',
    'BOOLEAN': r'boolean',
    'CHAR': r'char',
    'STRING': r'string',
    'ARRAY': r'array',
    'OF': r'of',
    'IF': r'if',
    'THEN': r'then',
    'ELSE': r'else',
    'WHILE': r'while',
    'DO': r'do',
    'REPEAT': r'repeat',
    'UNTIL': r'until',
    'FOR': r'for',
    'TO': r'to',
    'DOWNTO': r'downto',
    'LSBR': r'\[',
    'RSBR': r'\]',   
    # 'WRITELN': r'writeln',
    # 'WRITE': r'write',
    # 'READLN': r'readln',
    # 'READ': r'read',
    'FUNCTION': r'FUNCTION',
    'PROCEDURE': r'PROCEDURE',
    'FORWARD': r'FORWARD',
    'RETURN': r'return',
    'NOT': r'not',
    'IDENTIFIER': r'[a-zA-Z][a-zA-Z0-9_]*|(?<![0-9])[0-9]+[a-zA-Z_]+',
    'NUMBER': r'[0-9]+',
    'PLUS': r'\+',
    'QUOTES': r'\'',
    'MINUS': r'\-',
    'EQUALITY': r'=',
    'NONEQUALITY': r'<>',
    'GREATER': r'>',
    'SMALLER': r'<',
    'MULTIPLY': r'\*',
    'DIVIDE': r'\/',
    'ASSIGN': r':=',
    'SEMICOLON': r';',
    'LPAREN': r'\(',
    'RPAREN': r'\)',
    'DOT': r'\.',
    'COMMA': r',',
    'COLON': r':',
}

# Combine all the regex patterns into one regular expression
token_regex = re.compile('|'.join('(?P<%s>%s)' % pair for pair in regex_patterns.items()))

class Lexer:

    def __init__(self, code):
        self.lexem_list = self.tokenize(code)
        self.current_pos = 0
    
    def has_next(self):
        return self.current_pos != len(self.lexem_list)
    
    def next_token(self):
        if self.current_pos < len(self.lexem_list):
            token = self.lexem_list[self.current_pos]
            self.current_pos += 1
            return token

    def tokenize(self, code):
        tokens = []
        line_number = 1
        for match in token_regex.finditer(code):
            token_type = match.lastgroup
            token_value = match.group(token_type)
            if token_type == 'IDENTIFIER':
                if not re.match(r'^[a-zA-Z][a-zA-Z0-9]*$', token_value):
                    raise ValueError(f'SyntaxError: Invalid variable name "{token_value}" on line {line_number}')
            elif token_type == 'NUMBER':
                if not re.match(r'^[0-9]+$', token_value):
                    raise ValueError(f'SyntaxError: Invalid number "{token_value}" on line {line_number - 1}')
                try:
                    int_value = int(token_value)
                except ValueError:
                    raise ValueError(f'SyntaxError: Invalid integer "{token_value}" on line {line_number - 1}')
                if not -32768 <= int_value <= 32767:
                    raise ValueError(f'ValueError: Integer overflow "{token_value}" on line {line_number}')
            elif token_type == 'SEMICOLON':
                line_number += 1
            tokens.append((token_type, token_value))
        tokens.append(('EOF', ''))
        return tokens

def main():
    with open('python_module/parser/test.pas', 'r') as file:
        code = file.read()

    try:
        lexer = Lexer(code)
        while lexer.has_next():
            print(lexer.next_token())
    except ValueError as e:
        print('Error:', str(e))
        return

if __name__ == '__main__':
    main()

