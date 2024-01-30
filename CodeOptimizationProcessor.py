from OptimizeChain import OptimizeChain
from lexer import Lexer
from Parser import Parser
from SemanticModule import SemanticModule
from SupportClasses import NodeProgram
from OptimizeChain import OptimizeChain, NotUsedVariableOptimize

class CodeOptimizationProcessor:
    
    def __init__(self, main_chain : OptimizeChain = None):
        self.__chain_head = main_chain

    def add_new_chain(self, chain : OptimizeChain):
        if self.__chain_head is None:
            self.__chain_head = chain
            return
        iter = self.__chain_head
        while iter.get_next() is not None:
            iter = iter.get_next()
        iter.set_next(chain)

    def start_optimization(self, program_node : NodeProgram) -> NodeProgram:
        return self.__chain_head.process_optimization(program_node)

if __name__ == '__main__':
    reader = open('comp/test.pas', 'r')
    code = reader.read()
    lexer = Lexer(code)
    semantic_module = SemanticModule()
    parser = Parser(lexer)
    parser.set_semantic_module(semantic_module)
    res = parser.parse()
    writer = open('Not optimized program.txt', 'w')
    writer.write(str(res))
    writer.flush()
    writer.close()
    # Цепочка оптимизации
    optimizer1 = NotUsedVariableOptimize()
    optimizer1.set_semantic_module(semantic_module) # Лайфхак с таблицей
    # Оптимизатор кода
    optimize_processor = CodeOptimizationProcessor()
    optimize_processor.add_new_chain(optimizer1)
    optimized_program = optimize_processor.start_optimization(res)
    writer = open('Optimized program.txt', 'w')
    writer.write(str(optimized_program))
    writer.flush()
    writer.close()
