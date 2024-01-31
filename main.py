from lexer import Lexer
from Parser import Parser
from SemanticModule import SemanticModule
from CodeOptimizationProcessor import CodeOptimizationProcessor as Optimizator
from other.OptimizeChain import NotUsedVariableOptimize as NotUsedChain

lexer = Lexer()
parser = Parser()
semantic_module = SemanticModule()
optimizator = Optimizator()
optimizator.add_new_chain(NotUsedChain(semantic_module= semantic_module))

def main():
    lexer.add_file('test/test pascal file.pas')
    parser.set_lexer(lexer)
    parser.set_semantic_module(semantic_module)
    before = parser.parse()
    writer = open('output/before.txt', 'w')
    writer.write(str(before))
    writer.flush()
    writer.close()
    after = optimizator.start_optimization(before)
    writer = open('output/after.txt', 'w')
    writer.write(str(after))
    writer.flush()
    writer.close()

if __name__ == '__main__':
    main()