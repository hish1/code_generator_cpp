from lexer import Lexer
from lexer import regex_patterns as Token
from SupportClasses import *
from SemanticModule import SemanticModule

class Parser:

    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = lexer.next_token()
        self._scope_type_dict = dict() 
        self.current_scope = list()
        self.__semantic_module = SemanticModule()

    def __next_token(self):
        self.current_token = self.lexer.next_token()
    
    def __expect(self, _expected):
        if self.current_token[0] != _expected:
            self.__raise_exception(f'Unexpected token: {self.current_token}')
        return True

    def __expect_and_move(self, _expected):
        self.__expect(_expected)
        self.__next_token()
        return True
    
    def __check(self, _expected):
        return self.current_token[0] == _expected
    
    def __check_all(self, _expected_list):
        return self.current_token[0] in _expected_list

    def __pop_token(self):
        token = self.current_token[0]
        self.__next_token()
        return token

    def __pop_value(self):
        identifier = self.current_token[1]
        self.__next_token()
        return identifier

    def __get_current_scope_str(self):
        return '.'.join(self.current_scope)

    def __raise_exception(self, message):
        raise AttributeError(f'Parse error: {message}')
    
    def parse(self):
        if not self.__check('EOF'):
            main_node = self._parse_prog()
        else:
            main_node = MainNode()
        return main_node
    
    def _parse_prog(self):
        node = NodeProgram()
        if self.__check('PROGRAM'):
            self.__next_token()
            node.identifier = self.__pop_value()
            self.__expect_and_move('SEMICOLON')
        node.global_declaration = self._parse_declaration_part()
        self.current_scope.append(node.identifier)
        node.statement_part = self.__parse_STATEMENT_BLOCK()
        self.__expect_and_move('DOT')
        return node

    def _parse_declaration_part(self):
        declaration_list = list()
        while not self.__check('BEGIN'):
            match self.current_token[0]:
                case 'VAR':
                    self.__next_token()
                    while self.__check('IDENTIFIER'):
                        declaration_list.extend(self.__parse_VAR_statement())
                        self.__expect_and_move('SEMICOLON')
                case 'TYPE':
                    self.__next_token()
                    while self.__check('IDENTIFIER'):
                        declaration_list.append(self.__parse_TYPE_statement())
                        self.__expect_and_move('SEMICOLON')
                case 'CONST':
                    self.__next_token()
                    while self.__check('IDENTIFIER'):
                        declaration_list.append(self.__parse_CONST_statement())
                        self.__expect_and_move('SEMICOLON')
                case 'PROCEDURE' | 'FUNCTION':
                    declaration_list.append(self.__parse_SUBROUTINE())
                case _:
                    self.__raise_exception('Impossible to parse declaration part. Infinity loop')
        return NodeDeclarationPart(declaration_list)

    # Parsing VAR declaration
    def __parse_VAR_statement(self):
        identifiers = []
        while not self.__check('COLON'):
            identifiers.append(self.__pop_value())
            if self.__check('COMMA'):
                self.__next_token()
        self.__next_token()
        _type = self.__parse_type()
        if self.__check('ASSIGN'):
            raise Error('Not implement Variable assign')
        for identifier in identifiers:
            self.__semantic_module.add_variable(self.current_scope, identifier, _type)
        if not isinstance(_type, NodeArrayType):
            _type = str(_type)
        variables = [NodeVariableDeclaration(identifier, _type) for identifier in identifiers]
        # Add declaration to scope
        return variables
    
    # Parsing CONST declaration
    def __parse_CONST_statement(self):
        node = NodeConstantDeclaration()
        self.__expect('IDENTIFIER')
        node.identifier = self.__pop_value()
        self.__expect_and_move('EQUALITY')
        node.expression = self.__parse_condition()
        node.type = self.__semantic_module.predict_condition_type(node.expression, self.current_scope)
        if isinstance(node.type, NodeType):
            node.type = node.type.identifier
        else:
            node.type = node.type.value
        self.__semantic_module.add_variable(self.current_scope, node.identifier, node, True)
        return node

    # Parsing TYPE declaration
    def __parse_TYPE_statement(self):
        node = NodeTypeDeclaration()
        self.__expect('IDENTIFIER')
        node.identifier = self.__pop_value()
        self.__expect_and_move('EQUALITY')
        node.type = self.__parse_type()
        self.__semantic_module.add_type(self.current_scope, node.identifier, node.type)
        if not isinstance(node.type, NodeArrayType):
            node.type = str(node.type)
        return node

    def __parse_SUBROUTINE(self):
        node = NodeSubroutine()
        node.subroutine_type = SubroutineType(self.__pop_token())
        self.__expect('IDENTIFIER')
        node.identifier = self.__pop_value()
        self.__expect_and_move('LPAREN')
        self.current_scope.append(node.identifier)
        node.formal_params = self.__parse_SUBROUTINE_FORMAL_PARAMS()
        self.__expect_and_move('RPAREN')
        if node.subroutine_type == SubroutineType.FUNCTION:
            self.__expect_and_move('COLON')
            node.type = self.__parse_type()
        else:
            node.type = PrimitiveType.UNDEFINED
        self.__semantic_module.add_subroutine(self.current_scope[:-1], node.identifier, node.type, node.formal_params)
        if not isinstance(node.type, NodeArrayType):
            node.type = str(node.type)
        self.__expect_and_move('SEMICOLON')
        if self.__check('FORWARD'):
            self.__next_token()
            node.is_forward_declaration = True
        else:
            node.declaration_part = self._parse_declaration_part()
            self.__expect('BEGIN')
            node.statement_part = self.__parse_STATEMENT_BLOCK()
            self.__expect_and_move('SEMICOLON')
        self.current_scope.pop()
        return node

    def __parse_SUBROUTINE_FORMAL_PARAMS(self):
        node = NodeSubroutineFormalParams(list())
        while not self.__check('RPAREN'):
            node.extend(self.__parse_VAR_statement())
            if self.__check('SEMICOLON'):
                self.__next_token()
        return node
            
    def __parse_type(self):
        if self.__check('ARRAY'):
            self.__next_token()
            return self.__parse_ARRAY_TYPE()
        elif self.__check('RECORD'):
            self.__next_token()
            raise NotImplementedError('ИМПЛЕМЕНТИРУЙ RECORD')
        elif PrimitiveType.__contains__(self.current_token[0]):
            return PrimitiveType[self.__pop_token()]
        else:
            self.__expect('IDENTIFIER')
            custom_type = self.__pop_value()
            return self.__semantic_module.get_type(self.current_scope, custom_type)
    
    def __parse_ARRAY_TYPE(self):
        node = NodeArrayType()
        self.__expect_and_move('LSBR')
        while not self.__check('RSBR'):
            array_range = NodeArrayRange()
            array_range.left_bound = self.__parse_factor()
            self.__expect_and_move('DOT')
            self.__expect_and_move('DOT')
            array_range.right_bound = self.__parse_factor()
            if self.__check('COMMA'):
                self.__next_token()
            node.append(array_range)            
        self.__next_token()
        self.__expect_and_move('OF')
        node.type = self.__parse_type()
        return node
    
    # Parsing condition expression
    def __parse_condition(self):
        left = self.__parse_expression()
        while self.__check_all(('EQUALITY', 'NONEQUALITY', 'GREATER', 'SMALLER')):
            operator = Operator(self.__pop_token())
            right = self.__parse_expression()
            left = NodeBinaryOperator(left, right, operator)
        return left

    # Prasing expression
    def __parse_expression(self):
        left = self.__parse_term()
        while self.__check_all(('PLUS', 'MINUS', 'OR', 'XOR')):
            operator = Operator(self.__pop_token())
            right = self.__parse_term()
            left = NodeBinaryOperator(left, right, operator)
        return left

    # Parsing term
    def __parse_term(self):
        left = self.__parse_factor()
        while self.__check_all(('MULTIPLY', 'DIVIDE','DIV', 'MOD', 'AND', 'SHL', 'SHR')):
            operator = Operator(self.__pop_token())
            right = self.__parse_factor()
            left = NodeBinaryOperator(left, right, operator)
        return left

    # Parsing factor
    def __parse_factor(self):
        match self.current_token[0]:
            case 'NUMBER':
                possible_number = self.__pop_value()
                _type = self.__semantic_module.return_value_type(possible_number)
                return NodeValue(possible_number, _type)
            case 'TRUE' | 'FALSE':
                return NodeValue(self.__pop_value(), PrimitiveType.BOOLEAN)
            case 'QUOTES':
                return self.__parse_STRING()
            case 'LPAREN':
                self.__next_token()
                condition = self.__parse_condition()
                self.__expect_and_move('RPAREN')
                return condition
            case 'MINUS':
                self.__next_token()
                condition = self.__parse_condition()
                if isinstance(condition, NodeValue):
                    new_value = f'-{condition.value}'
                    _type = self.__semantic_module.return_value_type(new_value)
                    return NodeValue(new_value, _type)
                else:
                    return NodeUnaryOperator(condition, Operator.UNARY_MINUS)
            case 'PLUS':
                self.__next_token()
                condition = self.__parse_condition()
                return condition
            case _:
                self.__expect('IDENTIFIER')
                return self.__parse_IDENTIFIER_STATEMENT()

    # Parinsg variable or Subroutine/array call
    def __parse_IDENTIFIER_STATEMENT(self):    
        self.__expect('IDENTIFIER')
        left = NodeVariable(self.__pop_value())
        # Проверка на существование переменной
        self.__semantic_module.get_variable(self.current_scope, left.identifier)
        while self.__check_all(('ASSIGN', 'LPAREN', 'LSBR', 'DOT')):
            match self.current_token[0]:
                case 'ASSIGN':
                    self.__next_token()
                    right = self.__parse_condition()
                    variable = left
                    while not isinstance(variable, NodeVariable):
                        variable = variable.left
                    self.__semantic_module.check_assign(self.current_scope, variable.identifier, right)
                    left = NodeBinaryOperator(left, right, Operator.ASSIGN)
                case 'LPAREN':
                    self.__next_token()
                    right = self.__parse_SUBROUTINE_CALL_PARAMS()
                    self.__semantic_module.check_subroutine_call(self.current_scope, left.identifier, right)
                    left = NodeBinaryOperator(left, right, Operator.SUBROUTINE_CALL)
                case 'LSBR':
                    self.__next_token()
                    right = self.__parse_ARRAY_CALL()
                    self.__semantic_module.check_array_access(self.current_scope, left.identifier, right)
                    left = NodeBinaryOperator(left, right, Operator.ARRAY_CALL)
                case 'DOT':
                    raise NotImplementedError('ИМПЛЕМЕНТИРУЙ ОБРАЩЕНИЕ К ОБЪЕКТУ')
        return left

    # Parsing subroution call params
    def __parse_SUBROUTINE_CALL_PARAMS(self):
        node = NodeCallParams(list())
        while not self.__check('RPAREN'):
            node.append(self.__parse_condition())
            if self.__check('COMMA'):
                self.__next_token()
        self.__next_token()
        return node

    def __parse_ARRAY_CALL(self):
        node = NodeCallParams(list())
        while not self.__check('RSBR'):
            node.append(self.__parse_expression())
            if self.__check('COMMA'):
                self.__next_token()
        self.__next_token()
        return node

    # Parsing statement block
    def __parse_STATEMENT_BLOCK(self):
        statement_block = NodeStatementPart(list())
        if self.__check('BEGIN'):
            self.__next_token()
            while not self.__check('END'):
                statement_block.append(self.__parse_STATEMENT())
                if self.__check('SEMICOLON'):
                    self.__next_token()
            self.__next_token()
        else:
            statement_block.append(self.__parse_STATEMENT())
        return statement_block

    def __parse_STATEMENT(self):
        match self.current_token[0]:
            case 'LCOM':
                self.__next_token()
                pass
            case 'IF':
                self.__next_token()
                node = self.__parse_IF_STATEMENT()
            case 'CASE':
                self.__next_token()
                pass
            case 'FOR':
                self.__next_token()
                node = self.__parse_FOR_STATEMENT()
            case 'WHILE':
                self.__next_token()
                node = self.__parse_WHILE_STATEMENT()
            case 'REPEAT':
                self.__next_token()
                node = self.__parse_REPEAT_STATEMENT()
            case 'IDENTIFIER':
                node = self.__parse_IDENTIFIER_STATEMENT()
        return node

    def __parse_IF_STATEMENT(self):
        node = NodeIfStatement()
        node.condition = self.__parse_condition()
        self.__expect_and_move('THEN')
        node.then_statement_part = self.__parse_STATEMENT_BLOCK()
        if self.__check('ELSE'):
            node.else_statement_part = self.__parse_STATEMENT_BLOCK()
        return node

    def __parse_FOR_STATEMENT(self):
        node = NodeForStatement()
        self.__expect('IDENTIFIER')
        node.variable = NodeVariable(self.__pop_value())
        self.__semantic_module.get_variable(self.current_scope, node.variable.identifier)
        if self.__check('ASSIGN'):
            self.__next_token()
            expression = self.__parse_expression()
            self.__semantic_module.check_assign(self.current_scope, node.variable.identifier, expression)
            node.initial_expression = expression
        self.__expect_and_move('TO')
        node.end_expression = self.__parse_expression()
        self.__expect_and_move('DO')
        node.statement_part = self.__parse_STATEMENT_BLOCK()
        return node

    def __parse_WHILE_STATEMENT(self):
        node = NodeWhileStatement()
        node.condition = self.__parse_condition()
        self.__expect_and_move('DO')
        node.statement_block = self.__parse_STATEMENT_BLOCK()
        return node       

    def __parse_REPEAT_STATEMENT(self):
        node = NodeRepeatUntilStatement(None, NodeStatementPart(list()))
        while not self.__check('UNTIL'):
            node.statement_part.append(self.__parse_STATEMENT())
            self.__expect_and_move('SEMICOLON')
        self.__next_token()
        node.condition = self.__parse_condition()
        return node
            
if __name__ == '__main__':
    reader = open('comp/test.pas', 'r')
    code = reader.read()
    lexer = Lexer(code)
    parser = Parser(lexer)
    res = parser.parse()
    writer = open('parser.txt', 'w')
    writer.write(str(res))
    writer.flush()
    writer.close()