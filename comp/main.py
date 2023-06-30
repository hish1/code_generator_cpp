# from parserV2 import Parser
import parserV2 as p
from lexer import Lexer
import gen as g
from pathlib import Path

with open('test.pas', 'r') as file:
        code = file.read()

lex = Lexer(code)
pars = p.Parser(lex)

head = pars.parse_prog()
gener = g.Gen()
gener.generate(head)
gen = gener.code
f2 = open('gen.txt', 'w')
f2.write(str(gen))
f2.flush()
f2.close()

f1 = open('result.txt', 'w')
f1.write(str(head))
f1.flush()
f1.close()



