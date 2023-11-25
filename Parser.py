from lexer import Lexer
from lexer import regex_patterns as Token
from SupportClasses import *

class Parser:

    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = lexer.next_token()
        self._scope_type_dict = dict() 
        self.current_scope = list()

    def _next_token(self):
        self.current_token = self.lexer.next_token()
    
    def _expect(self, _expected):
        if self.current_token[0] != _expected:
            self._raise_exception(f'Unexpected token: {self.current_token}')
        return True

    def _expect_and_move(self, _expected):
        self._expect(_expected)
        self._next_token()
        return True
    
    def _check(self, _expected):
        return self.current_token[0] == _expected
    
    def _check_all(self, _expected_list):
        return self.current_token[0] in _expected_list

    def _pop_token(self):
        token = self.current_token[0]
        self._next_token()
        return token

    def _pop_identifier(self):
        identifier = self.current_token[1]
        self._next_token()
        return identifier

    def _raise_exception(self, message):
        raise AttributeError(f'Parse error: {message}')
    
    def parse(self):
        main_node = MainNode()
        match self.current_token[0]:
            case 'EOF':
                return main_node
            case 'MODULE':
                self._next_token()
                raise NotImplementedError('Нет имплементации для модуля')
            case _:
                main_node = self._parse_prog()
                return main_node
    
    def _parse_prog(self):
        node = NodeProgram()
        if self._check('PROGRAM'):
            self._next_token()
            node.identifier = self._pop_identifier()
            self.current_scope.append(node.identifier)
            self._expect_and_move('SEMICOLON')
        node.global_declaration = self._parse_declaration_part()
        node.statement_part = self._parse_statement_block()
        self._expect_and_move('DOT')
        return node

    def _parse_declaration_part(self):
        declaration_list = list()
        while not self._check('BEGIN'):
            match self.current_token[0]:
                case 'VAR':
                    declaration_list.extend(self._parse_variable_part())
                case 'TYPE':
                    declaration_list.extend(self._parse_type_part())
                case 'CONST':
                    self._next_token()
                    declaration_list.extend(self._parse_const_part())
                case 'PROCEDURE' | 'FUNCTION':
                    declaration_list.append(self._parse_subroutine())
                case _:
                    self._raise_exception('Impossible to parse declaration part. Infinity loop')
        return NodeDeclarationPart(declaration_list)
    
    def _parse_variable_part(self):
        variables = list()
        self._expect_and_move('VAR')
        while self._check('IDENTIFIER'):
            temp = list()
            while not self._check('COLON'):
                self._expect('IDENTIFIER')
                temp.append(self._pop_identifier())
                if self._check('COMMA'):
                    self._next_token()
            self._next_token() # Скип COLON
            _type = self._parse_type()
            self._expect_and_move('SEMICOLON')
            for variable in temp:
                node = NodeVariableDeclaration(variable, _type)
                variables.append(node)
        if len(variables) == 0 : self._raise_exception('VAR block is empty but declared')
        return variables

    def _parse_const_part(self):
        consts = list()
        while self._check('IDENTIFIER'):
            identifier = self._pop_identifier()
            self._expect_and_move('EQUALITY')
            expression = self._parse_expression()
            self._expect_and_move('SEMICOLON')
            consts.append(NodeConst(identifier, expression))
        if len(consts) == 0 : self._raise_exception('CONST block is empty but declired')
        return consts
    
    def _parse_type_part(self):
        types = list()
        self._expect_and_move('TYPE')
        current_scope = '.'.join(self.current_scope)
        while self._check('IDENTIFIER'):
            node = NodeType()
            node.identifier = self._pop_identifier()
            self._expect_and_move('EQUALITY')
            node.type = self._parse_type()
            self._expect_and_move('SEMICOLON')
            types.append(node)
            if current_scope not in self._scope_type_dict: # Создаём scope_dict, если его не было
                self._scope_type_dict[current_scope] = dict()
            self._scope_type_dict[current_scope][node.identifier] = node # Вставляем тип в нужный scope
        if len(types) == 0 : self._raise_exception('Type block is empty but declired')
        return types

    def _parse_subroutine(self):
        node = NodeSubroutine()
        if not self._check('FUNCTION') and not self._check('PROCEDURE'):
            self._expect_and_move('PROCEDURE')
        node.subroutine_type = SubroutineType(self._pop_token())
        self._expect('IDENTIFIER')
        node.identifier = self._pop_identifier()
        self.current_scope.append(node.identifier)
        node.formal_params = self._parse_subroutine_formal_params()
        if node.subroutine_type == SubroutineType.FUNCTION:
            self._expect_and_move('COLON')
            node.retunr_type = self._parse_type()
        self._expect_and_move('SEMICOLON')
        if self._check('FORWARD'):
            self._next_token()
            node.is_forward_declaration = True
        else:
            node.declaration_part = self._parse_declaration_part()
            node.statement_part = self._parse_statement_block()
            self._expect_and_move('SEMICOLON')
        self.current_scope.pop()
        return node

    def _parse_subroutine_formal_params(self):
        node = NodeSubroutineFormalParams()
        self._expect_and_move('LPAREN')
        while not self._check('RPAREN'):
            variables = list()
            while not self._check_all(('RPAREN', 'COLON')):
                self._expect('IDENTIFIER')
                variables.append(self._pop_identifier())
                if self._check('COMMA'):
                    self._next_token()
            self._next_token()
            _type = self._parse_type()
            if self._check('SEMICOLON'):
                self._next_token()
            for variable in variables:
                node.append(NodeVariableDeclaration(variable, _type))
        self._next_token()
        return node

    def _parse_type(self):
        if self._check('ARRAY'):
            return self._parse_array_type()
        elif self._check('RECORD'):
            self._next_token()
            raise NotImplementedError('ИМПЛЕМЕНТИРУЙ RECORD')
        elif PrimitiveType.__contains__(self.current_token[0]):
            return self._pop_token()
        else:
            self._expect('IDENTIFIER')
            custom_type = self._pop_identifier()
            scope_parts = list(self.current_scope)
            while len(scope_parts) > 0:
                scope = '.'.join(scope_parts)
                if scope in self._scope_type_dict:
                    if custom_type in self._scope_type_dict[scope]:
                        return self._scope_type_dict[scope][custom_type]
                scope_parts.pop()
            self._raise_exception(f'Type {custom_type} is not declared')
        
    def _parse_array_type(self):
        node = NodeArrayType()
        self._expect_and_move('ARRAY')
        self._expect_and_move('LSBR')
        node.left_bound = self._parse_factor()
        self._expect_and_move('DOT')
        self._expect_and_move('DOT')
        node.right_bound = self._parse_factor()
        self._expect_and_move('RSBR')
        self._expect_and_move('OF')
        node.type = self._parse_type()
        return node

    def _parse_statement(self):
        node = None
        if self._check('IF'):
            node = self._parse_if_statement()
        elif self._check('WHILE'):
            node = self._parse_while_statement()
        elif self._check('FOR'):
            node = self._parse_for_statement()
        elif self._check('IDENTIFIER'):
            node = self._parse_identifier_statement()
            if self.current_token[0] not in ('END', 'ELSE'):
                self._expect_and_move('SEMICOLON')
        elif self._check('RETURN'):
            self._raise_exception('Illegal expression')
        return node   
    
    def _parse_identifier_statement(self):
        self._expect('IDENTIFIER')
        left = NodeVariable(self._pop_identifier())
        while self._check_all(('ASSIGN', 'LPAREN', 'LSBR', 'DOT')):
            if self._check('ASSIGN'):
                self._next_token()
                right = self._parse_condition()
                left = NodeBinaryOperator(left, right, BinaryOperatorType.ASSIGN)
            elif self._check('LPAREN'):
                right = self._parse_subroutine_call()
                left = NodeBinaryOperator(left, right, BinaryOperatorType.SUBROUTINE_CALL)                
            elif self._check('LSBR'):
                right = self._parse_array_call()
                left = NodeBinaryOperator(left, right, BinaryOperatorType.ARRAY_CALL)
            elif self._check('DOT'):
                raise NotImplementedError('ИМПЛЕМЕНТИРУЙ ОБРАЩЕНИЕ К ОБЪЕКТУ')
        return left

    def _parse_array_call(self):
        self._expect_and_move('LSBR')
        params = list()
        while not self._check('RSBR'):
            params.append(self._parse_expression())
            if self._check('COMMA'):
                self._next_token()
        self._next_token()
        return NodeCallParams(params)

    def _parse_subroutine_call(self):
        self._expect_and_move('LPAREN')
        params = list()
        while not self._check('RPAREN'):
            params.append(self._parse_expression())
            if self._check('COMMA'):
                self._next_token()
        self._next_token()
        return NodeCallParams(params)
    
    def _parse_statement_block(self):
        statements = list()
        self._expect_and_move('BEGIN')
        while not self._check('END'):
            statements.append(self._parse_statement())
            if self._check('SEMICOLON'):
                self._next_token()
        self._next_token()
        return NodeStatementPart(statements)

    def _parse_if_statement(self):
        self._expect_and_move('IF')
        condition = self._parse_condition()
        self._expect_and_move('THEN')
        then_statement_part = NodeStatementPart(list())
        if self._check('BEGIN'):
            then_statement_part = self._parse_statement_block()
        else:
            then_statement_part.append(self._parse_statement())
        else_statement_part = NodeStatementPart(list())
        if self._check('ELSE'):
            self._next_token()
            if self._check('BEGIN'):
                else_statement_part = self._parse_statement_block()
            else:
                else_statement_part.append(self._parse_statement())
        return NodeIfStatement(condition, then_statement_part, else_statement_part)

    def _parse_for_statement(self):
        self._expect_and_move('FOR')
        self._expect('IDENTIFIER')
        variable = NodeVariable(self._pop_identifier())
        self._expect_and_move('ASSIGN')
        initial_expression = self._parse_expression()
        is_increase = False
        if self._check('DOWNTO'):
            is_increase = not self._expect_and_move('DOWNTO')
        else:
            is_increase = self._expect_and_move('TO')
        end_expression = self._parse_expression()
        self._expect_and_move('DO')
        statement_part = NodeStatementPart(list())
        if self._check('BEGIN'):
            statement_part = self._parse_statement_block()
        else:
            statement_part.append(self._parse_statement())
        return NodeForStatement(variable, initial_expression, end_expression, statement_part, is_increase)

    def _parse_while_statement(self):
        self._expect_and_move('WHILE')
        condition = self._parse_condition()
        self._expect_and_move('DO')
        statement_part = NodeStatementPart(list())
        if self._check('BEGIN'):
            statement_part = self._parse_statement_block()
        else:
            statement_part.append(self._parse_statement())
        return NodeWhileStatement(condition, statement_part)

    def _parse_condition(self):
        left = self._parse_expression()
        while self.current_token[0] in ('EQUALITY', 'NONEQUALITY', 'GREATER', 'SMALLER'):
            operator = self._pop_token()
            right = self._parse_expression()
            left = NodeBinaryOperator(left, right, BinaryOperatorType(operator))
        return left

    def _parse_expression(self):
        left = self._parse_term()
        while self.current_token[0] in ('PLUS', 'MINUS', 'OR', 'XOR'):
            operator = self._pop_token()
            right = self._parse_term()
            left = NodeBinaryOperator(left, right, BinaryOperatorType(operator))
        return left
    
    def _parse_term(self):
        left = self._parse_factor()
        while self.current_token[0] in ('MULTIPLY', 'DIVIDE','DIV', 'MOD', 'AND', 'SHL', 'SHR'):
            operator = self._pop_token()
            right = self._parse_factor()
            left = NodeBinaryOperator(left, right, BinaryOperatorType(operator))
        return left

    def _parse_factor(self):
        if self._check('LPAREN'):
            self._next_token()
            expression = self._parse_condition()
            self._expect_and_move('RPAREN')
            return expression
        elif self._check('NOT'):
            self._next_token()
            condition = self._parse_condition()
            return NodeUnaryOperator(condition, UnaryOperatorType.NOT)
        elif self.current_token[0] in ('PLUS', 'MINUS'): # Разбор унарного + и -
            operator = self._pop_token()
            expression = self._parse_expression()
            return NodeUnaryOperator(expression, UnaryOperatorType(operator))
        # Блок разбора переменных, строк и чисел
        elif self._check('QUOTES'):
            self._next_token()
            string = ''
            while not self._check('QUOTES'):
                string += self._pop_identifier()
            self._expect_and_move('QUOTES')
            return string
        elif self._check_all(('NUMBER', 'TRUE', 'FALSE')):
            return NodeValue(self._pop_identifier())
        elif self._check('IDENTIFIER'):
            return self._parse_identifier_statement()
        else: self._expect_and_move('IDENTIFIER')
            
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