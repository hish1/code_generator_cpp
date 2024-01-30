from Node import Node
from typing import final
from typing import abstractmethod
from SupportClasses import *
from enum import Enum
from lexer import Lexer
from Parser import Parser
from SemanticModule import SemanticModule

class OptimizeChain:

    def __init__(self, 
                 next = None):
        self.__next = None

    @final
    def set_next(self, next):
        self.__next = next

    @final
    def get_next(self):
        return self.__next

    @final
    def process_optimization(self, node_program : NodeProgram) -> NodeProgram:
        result = self._optimize(node_program)
        if self.__next is not None:
            return self.__next.process_optimization(result)
        else:
            return result
    
    @abstractmethod
    def _optimize(self, tree_node : Node) -> Node:
        pass 

class NotUsedVariableOptimize(OptimizeChain):

    def __init__(self, 
                 next = None):
        super().__init__(next)
        self.__semantic_module = None
        self.__current_scope = list()

    def set_semantic_module(self, module):
        self.__semantic_module = module
    
    def _optimize(self, tree_node : NodeProgram) -> Node:
        unused_names = self.__semantic_module.get_unused_variable_names()
        declaration = tree_node.global_declaration
        tree_node.global_declaration = self.__cut_declarations(declaration, unused_names)
        return tree_node
        
    def __cut_declarations(self, 
                           declaration_part: NodeDeclarationPart, 
                           unused_names : list[str]):
        filtered_declarations = list()
        for declaration in declaration_part.declaration_list:
            if isinstance(declaration, NodeSubroutine):
                self.__current_scope.append(declaration.identifier)
                subroutine = self.__cut_subroutine(declaration, unused_names)
                self.__current_scope.pop()
                filtered_declarations.append(subroutine)
            else:
                full_name = self.__semantic_module.convert_to_name(self.__current_scope, declaration.identifier)
                if full_name not in unused_names:
                    filtered_declarations.append(declaration)
        return NodeDeclarationPart(filtered_declarations)


    def __cut_subroutine(self, 
                         subroutine : NodeSubroutine, 
                         unused_names : list[str]):
        declaration = subroutine.declaration_part
        subroutine.declaration_part = self.__cut_declarations(declaration, unused_names)
        return subroutine
        
    def __cut_statement_part(self, 
                             statement_part : NodeStatementPart, 
                             unused_names : list[str]):
        '''
            Метод не определён т.к. нет никаких объявлений в блоке statement_part
            (Но возможно будут)
        ''' 
        pass