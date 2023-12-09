from Node import Node
from enum import StrEnum

class ProgramType(StrEnum):
    PROGRAM = 'PROGRAM'; MODULE = 'MODULE'

# Тип функции
class SubroutineType(StrEnum):
    PROCEDURE = 'PROCEDURE'; FUNCTION = 'FUNCTION'

class UnaryOperatorType(StrEnum):
    UNARY_PLUS = 'PLUS'; UNARY_MINUS = 'MINUS'; NOT = 'NOT'; 

# https://pascalabc.net/downloads/pabcnethelp/index.htm?page=LangGuide/Operations_Expressions/oppriority.html
class BinaryOperatorType(StrEnum):
    PLUS = 'PLUS'; MINUS = 'MINUS'; MULTIPLY = 'MULTIPLY'; DIVIDE = 'DIVIDE'
    EQUALITY = 'EQUALITY'; NONEQUALITY = 'NONEQUALITY'; GREATER = 'GREATER'; SMALLER = 'SMALLER';
    MOD = 'MOD'; DIV = 'DIV'; IN = 'IN'; SHL = 'SHL'; SHR = 'SHR'; ASSIGN = 'ASSIGN';
    ARRAY_CALL = 'ARRAY_CALL'; SUBROUTINE_CALL = 'SUBROUTINE_CALL'; 
    OBJECT_CALL = 'OBJECT_CALL'

class PrimitiveType(StrEnum):
    UNDEFINED = 'UNDEFINED'; BYTE = 'BYTE'; SHORTINT = 'SHORTINT'; WORD = 'WORD'
    INTEGER = 'INTEGER'; LONGINT = 'LONGINT'; REAL = 'REAL'; SINGLE = 'SINGLE'
    DOUBLE = 'DOUBLE'; EXTENDED = 'EXTENDED'; BOOLEAN = 'BOOLEAN'; CHAR = 'CHAR'
    @classmethod
    def __contains__(cls, item):
        return item in cls.__members__

class NodeStatementPart(Node):
    def __init__(self, statements = list()):
        self.statements = statements
    def append(self, statement):
        self.statements.append(statement)

# Основная программа
class MainNode(Node):
    def __init__(self, program_type = ProgramType.PROGRAM, node_body = None):
        self.program_type = program_type
        self.node_body = node_body

class NodeProgram(Node):
    def __init__(self, identifier= '', global_declaration= None, statement_part = NodeStatementPart()):
        self.identifier = identifier
        self.global_declaration = global_declaration
        self.statement_part = statement_part

class NodeDeclarationPart(Node):
    def __init__(self, declaration_list = list()):
        self.declaration_list = declaration_list

# Классы для подпрограмм
class NodeSubroutineFormalParams(Node):
    def __init__(self, params = list()):
        self.params = params
    def append(self, param):
        self.params.append(param)
class NodeSubroutine(Node):
    def __init__(self, 
                 subroutine_type = SubroutineType.PROCEDURE, 
                 identifier = '',
                 retunr_type = None,
                 formal_params = NodeSubroutineFormalParams(),
                 declaration_part = NodeDeclarationPart(),
                 statement_part = NodeStatementPart(),
                 is_forward_declaration = False):
        self.identifier = identifier
        self.subroutine_type = subroutine_type
        self.retunr_type = retunr_type
        self.formal_params = formal_params
        self.declaration_part = declaration_part
        self.statement_part = statement_part
        self.is_forward_declaration = is_forward_declaration

class NodeType(Node):
    def __init__(self, identifier = None, _type = None):
        self.identifier = identifier
        self.type = _type

class NodeArrayType(Node):
    def __init__(self, left_bound = None, right_bound = None, _type = None):
        self.left_bound = left_bound
        self.right_bound = right_bound
        self.type = _type

class NodeConst(Node):
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

class NodeVariableDeclaration(Node):
    def __init__(self, identifier, _type):
        self.identifier = identifier
        self.type = _type
class NodeVariable(Node):
    def __init__(self, identifier):
        self.identifier = identifier
class NodeValue(Node):
    def __init__(self, value):
        self.value = value
class NodeCallParams(Node):
    def __init__(self, params = list()):
        self.params = params
    def append(self, param):
        self.params.append(param)

class NodeUnaryOperator(Node):
    def __init__(self, 
                 left, 
                 operation_type = UnaryOperatorType.UNARY_PLUS):
        self.left = left
        self.operation_type = operation_type

class NodeBinaryOperator(Node):
    def __init__(self, left, right, operation_type = BinaryOperatorType.PLUS):
        self.left = left
        self.right = right
        self.operation_type = operation_type

class NodeIfStatement(Node):
    def __init__(self, 
                 condition = None, 
                 then_statement_part = NodeStatementPart(), 
                 else_statement_part = NodeStatementPart()):
        self._condition = condition
        self.then_statement_part = then_statement_part
        self.else_statement_part = else_statement_part       

class NodeWhileStatement(Node):
    def __init__(self, condition = None, statement_part = NodeStatementPart()):
        self.condition = condition
        self.statement_part = statement_part

class NodeForStatement(Node):
    def __init__(self, 
                 variable = None, 
                 initial_expression = None, 
                 end_expression = None, 
                 statement_part = NodeStatementPart(), 
                 is_increase = False):
        self.variable = variable
        self.initial_expression = initial_expression
        self.end_expression = end_expression
        self.statement_part = statement_part
        self.is_increase = is_increase
