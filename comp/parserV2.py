from lexer import Lexer
from lexer import regex_patterns as Token
from enum import Enum

class Node:
    def __get_class_name(self):
        c = str(self.__class__)
        pos_1 = c.find('.')+1
        pos_2 = c.find("'", pos_1)
        return f"{c[pos_1:pos_2]}"

    def __repr__(self, level=0):
        attrs = self.__dict__
        if len(attrs) == 1 and isinstance(list(attrs.values())[0], list):
            is_sequence = True
        else:
            is_sequence = False
        res = f"{self.__get_class_name()}\n"
        if is_sequence:
            elements = list(attrs.values())[0]
            for el in elements:
                res += '|   ' * level
                res += "|+-"
                res += el.__repr__(level+1)
        else:
            for attr_name in attrs:
                res += '|   ' * level
                res += "|+-"
                if isinstance(attrs[attr_name], Node):
                    res += f"{attr_name}: {attrs[attr_name].__repr__(level+1)}"
                else:
                    res += f"{attr_name}: {attrs[attr_name]}\n"
                    
        return res
    
class NodeProgram(Node):
    def __init__(self, identifier, declaration_part, statement_part):
        self.identifier = identifier
        self.declaration_part = declaration_part
        self.statement_part = statement_part

class NodeIdentifier(Node):
    def __init__(self, code):
        self.code = code

class NodeDeclarationPart(Node):
    def __init__(self, const_definition_part = None, 
                type_definition_part = None, 
                variable_declaration_part = None, 
                proc_func_declaration_part = None):
        self.const_definition_part = const_definition_part
        self.type_definition_part = type_definition_part
        self.variable_declaration_part = variable_declaration_part
        self.proc_func_declaration_part = proc_func_declaration_part

class NodeConstDefinitionPart(Node):
    def __init__(self, const_declaration_list = []):
        self.const_declaration_list = const_declaration_list
    def append(self, const_declaration):
        self.const_declaration_list.append(const_declaration)

class NodeConstDeclaration(Node):
    def __init__(self, identifier, value):
        self.idntifier = identifier
        self.value = value

# Класс блок объявления переменных
class NodeVariableDeclarationPart(Node):
    def __init__(self, variable_declaration_list = []):
        self.variable_declaration_list = variable_declaration_list
    def append(self, variable_declarattion):
        self.variable_declaration_list.append(variable_declarattion)

# Класс для переменной и её типа
class NodeVariableDeclaration(Node):
    def __init__(self, identifier, type):
        self.identifier = identifier
        self.type = type

class NodeType(Node):
    def __init__(self, _type):
        self._type = _type
class NodeArrayType(Node):
    def __init__(self, left_bound, right_bound, type):
        self.left_bound = left_bound
        self.right_bound = right_bound
        self.type = type

class NodeStatementPart(Node): 
    def __init__(self, statement_sequence =[]):
        self.statement_sequence = statement_sequence
    def append(self, statement):
        self.statement_sequence.append(statement)
class NodeReturnStatement(Node):
    def __init__(self, return_expression):
        self.return_rexpression = return_expression

class NodeIfCondition(Node):
    def __init__(self, condition, block, else_block):
        self.condition = condition
        self.block = block
        self.elseBlock = else_block

class NodeWhileRepetitiveStatement(Node):
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block
class NodeForRepetitiveStatement(Node):
    def __init__(self, variable_identifier, initial_expression, final_expression, statement_part):
        self.variable_identifier = variable_identifier
        self.initial_expression = initial_expression
        self.final_expression = final_expression
        self.statement_part = statement_part

class NodeContainer(Node):
    def __init__(self, value):
        self.value = value
class NodeVariable(NodeContainer):pass
class NodeNumber(NodeContainer):pass
class NodeString(NodeContainer):pass
class NodeArrayBracketCall(Node):
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

# Всё относится к подпрограммам
class NodeSubroutineDeclarationPart(Node):
    def __init__(self, subroutine_list = []):
        self.subroutine_list = subroutine_list
    def append(self, subroutine):
        self.subroutine_list.append(subroutine)
class NodeSubroutine(Node):
    def __init__(self, identifier, formal_param_list, declaration_part, statement_part):
        self.identifier = identifier
        self.formal_param_list = formal_param_list
        self.declaration_part = declaration_part
        self.statement = statement_part
class NodeSubroutineFormalParamList(Node):
    def __init__(self, formal_params_list = []):
        self.formal_params_list = formal_params_list
    def append(self, formal_pararm):
        self.formal_params_list.append(formal_pararm)
class NodeSubroutineForwardDeclaration(Node):
    def __init__(self, identifier, formal_param_list):
        self.identifier = identifier
        self.formal_param_list = formal_param_list
class NodeProcedureForwardDeclaration(NodeSubroutineForwardDeclaration):pass
class NodeFunctionForwardDeclaration(NodeSubroutineForwardDeclaration):
    def __init__(self, identifier, formal_param_list, return_type):
        super().__init__(identifier, formal_param_list)
        self.return_type = return_type
class NodeProcedure(NodeSubroutine):pass
class NodeFunction(NodeSubroutine):
    def __init__(self, identifier, formal_param_list, return_type, declaration_part, statement_part):
        super().__init__(identifier, formal_param_list, declaration_part, statement_part)
        self.return_type = return_type

# Тело вызова подпрограммы
class NodeSubroutineCall(Node):
    def __init__(self, identifier, subroutine_param_list):
        self.identifier = identifier
        self.subroutine_param_list = subroutine_param_list
class NodeSubroutineParamsList(Node):
    def __init__(self, formal_params = []):
        self.formal_params = formal_params


class NodeUnaryOperator(Node):
    def __init__(self, left):
        self.left = left
class NodeUnaryMinusOperator(NodeUnaryOperator):pass
class NodeUnaryPlusOperator(NodeUnaryOperator):pass
class NodeBinaryOperation(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right
class NodeAssignOperation(NodeBinaryOperation):pass
class NodePlusOperator(NodeBinaryOperation):pass
class NodeMinusOperator(NodeBinaryOperation):pass
class NodeMultiplyOperator(NodeBinaryOperation):pass
class NodeDivideOperator(NodeBinaryOperation):pass
class NodeEqualOperator(NodeBinaryOperation):pass
class NodeNotEqualOperator(NodeBinaryOperation):pass
class NodeGreaterOperator(NodeBinaryOperation):pass
class NodeSmallerOperator(NodeBinaryOperation):pass

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = lexer.next_token()
    
    def _next_token(self):
        self.current_token = self.lexer.next_token()

    def _expect(self, _expected):
        if self.current_token[0] != _expected:
            self._error(f'Un_expected token: {self.current_token}')

    def _expect_and_move(self, _expected):
        if not self._check(_expected):
            self._error(f'Unexpected token: {self.current_token}')
        self._next_token()

    # Проверка на текущий токен без выброса ошибки
    def _check(self, _expected):
        return self.current_token[0] == _expected
    
    def _check_and_move_if_successfully(self, _expected):
        if self._check(_expected):
            self._next_token()
            return True
        return False
    
    # Проверка текущего токена и сдвиг
    def _check_and_move(self, _expected):
        current = self.current_token
        self._next_token()
        return current[0] == _expected
    
    def _error(self, message):
        raise Exception(f'Prase _error: {message}')
    
    # Вход в программу
    def parse_prog(self) -> NodeProgram:
        if self._check('EOF'):
            self._error('Файл пуст')
        self._expect_and_move('PROGRAM')
        identifier = self._parse_identifier()
        self._expect_and_move('SEMICOLON')
        declaration_part = self._parse_declaration_part()
        self._expect_and_move('BEGIN')
        statement_part = self.__parse_statement_part()
        self._expect_and_move('END')
        self._expect('DOT')
        return NodeProgram(identifier, declaration_part, statement_part)
    
    def _parse_identifier(self):
        self._expect('IDENTIFIER')
        token = self.current_token
        self._next_token()
        return token[1]

    def _parse_declaration_part(self):
        const_def = None
        type_def = None
        var_decl = None
        subroutines = None
        if self._check_and_move_if_successfully('CONST'): 
            const_def = self._parse_const_definition_part()
        if self._check('TYPE'): pass
        if self._check_and_move_if_successfully('VAR'): 
            var_decl = self._parse_var_declaration_part()
        if self._check('PROCEDURE') or self._check('FUNCTION'):
            subroutines = self._parse_subroutine_declaration_part()
        return NodeDeclarationPart(const_def, type_def, var_decl, subroutines)
    
    def _parse_const_definition_part(self):
        body = []
        self._expect('IDENTIFIER')
        while not self._check('TYPE') and not self._check('VAR') and not self._check('PROCEDURE') and not self._check('FUNCTION') and not self._check('BEGIN'):
            identifier = self.current_token[1]
            self._next_token()
            self._expect_and_move('EQUALITY')
            value = self._parse_expression()
            self._expect_and_move('SEMICOLON')
            body.append(NodeConstDeclaration(identifier, value))
        if len(body) == 0:
            self._error(f'_expect const declaration got {self.current_token[1]}')
        return NodeConstDefinitionPart(body)

    def _parse_var_declaration_part(self):
        body = []
        self._expect('IDENTIFIER')
        while not self._check('PROCEDURE') and not self._check('FUNCTION') and not self._check('BEGIN'):
            variables = []
            identifier = self._parse_identifier()
            variables.append(identifier)
            while self._check_and_move_if_successfully('COMMA'):
                identifier = self._parse_identifier()
                variables.append(identifier)
            self._expect_and_move('COLON') # Проверка на : после объявления переменных
            _type = self._parse_type()
            self._expect_and_move('SEMICOLON')
            for variable in variables:
                body.append(NodeVariableDeclaration(variable, _type))
        return NodeVariableDeclarationPart(body)
    
    def _parse_subroutine_declaration_part(self):
        subroutine_declaration_part = NodeSubroutineDeclarationPart()
        while not self._check('BEGIN'):
            if self._check('PROCEDURE') or self._check('FUNCTION'):
                subroutine_declaration_part.append(self._parse_subroutine_part())
            else:
                self._error('Un_expected _error while parsing subrouting declaration')
        return subroutine_declaration_part
    
    def _parse_subroutine_part(self):
        is_function = self._check_and_move('FUNCTION')
        self._expect('IDENTIFIER')
        identifier = self._parse_identifier()
        self._expect_and_move('LPAREN')
        variables_declaration = self._parse_subroutine_formal_param_list()
        self._expect_and_move('RPAREN')
        return_type = None
        if is_function: 
            self._expect_and_move('COLON')
            return_type = self._parse_type()
        self._expect_and_move('SEMICOLON')
        if self._check_and_move_if_successfully('FORWARD'):
            self._expect_and_move('SEMICOLON')
            if is_function:
                return NodeFunctionForwardDeclaration(identifier, variables_declaration, return_type)
            else:
                return NodeProcedureForwardDeclaration(identifier, variables_declaration, return_type)
        declaration_part = self._parse_declaration_part()
        self._expect_and_move('BEGIN')
        statemet_part = self.__parse_statement_part()
        self._expect_and_move('END')
        self._expect_and_move('SEMICOLON')
        if is_function:
            return NodeFunction(identifier, variables_declaration, return_type, declaration_part, statemet_part)
        else:
            return NodeProcedure(identifier, variables_declaration, declaration_part, statemet_part)

    def _parse_subroutine_formal_param_list(self):
        body = NodeSubroutineFormalParamList()
        while not self._check('RPAREN'):
            self._expect('IDENTIFIER')
            variables = []
            identifier = self._parse_identifier()
            variables.append(identifier)
            while self._check_and_move_if_successfully('COMMA'):
                self._expect('IDENTIFIER')
                variables.append(self._parse_identifier())
            self._expect_and_move('COLON')
            _type = self._parse_type()
            if not self._check('RPAREN'):
                self._expect_and_move('SEMICOLON')
            for variable in variables:
                body.append(NodeVariableDeclaration(variable, _type))
        return body

    def _parse_type(self):
        if self._check_and_move_if_successfully('ARRAY'):
            return self._parse_array_type()
        if self._check_and_move_if_successfully('INTEGER'):
            return NodeType('INTEGER')
        elif self._check_and_move_if_successfully('REAL'):
            return NodeType('REAL')
        elif self._check_and_move_if_successfully('STRING'):
            return NodeType('STRING')
        elif self._check_and_move_if_successfully('BOOLEAN'):
            return NodeType('BOOLEAN')
    
    def _parse_array_type(self):
        self._expect_and_move('LSBR')
        left_bound = self._parse_factor()
        self._expect_and_move('DOT')
        self._expect_and_move('DOT')
        right_bound = self._parse_factor()
        self._expect_and_move('RSBR')
        self._expect_and_move('OF')
        _type = self._parse_type()
        return NodeArrayType(left_bound, right_bound, _type)
    
    def __parse_statement_part(self, depth = -1):
        body = []
        current_depth = 0
        while not self._check('END') and not self._check('ELSE') and not self._check('END'):
            if depth != -1 and current_depth >= depth:
                return NodeStatementPart(body)
            childNode = None
            if self._check_and_move_if_successfully('RETURN'):
                body.append(NodeReturnStatement(self._parse_expression()))
                self._expect_and_move('SEMICOLON')
            elif self._check_and_move_if_successfully('IF'): 
                body.append(self._parse_if_statement())
            elif self._check_and_move_if_successfully('WHILE'): 
                body.append(self._parse_while_statement())
            elif self._check_and_move_if_successfully('FOR'):
                body.append(self._parse_for_statement())
            else:
                childNode = self._parse_statement()
                body.append(childNode)
            self._expect_and_move('SEMICOLON')
            current_depth += 1
        return NodeStatementPart(body)
    
    def _parse_statement(self):
        if self._check('IDENTIFIER'):
            left = self._parse_factor()
            if self._check_and_move_if_successfully('ASSIGN'):
                return NodeAssignOperation(left, self._parse_expression())
            return left
                  
    def _parse_subroutine_params(self):
        params = []
        while not self._check_and_move_if_successfully('RPAREN'):
            term = self._parse_expression()
            params.append(term)
            if self._check('COMMA'):
                self._next_token()
        return params

    def _parse_if_statement(self):
        self._expect_and_move('LPAREN')
        condition = self._parse_expression()
        self._expect_and_move('RPAREN')
        self._expect_and_move('THEN')
        block = None
        if self._check_and_move_if_successfully('BEGIN'):
            block = self.__parse_statement_part()
            self._expect_and_move('END')
        else:
            block = self.__parse_statement_part(depth=1)
        else_block = None
        if self._check_and_move_if_successfully('ELSE'):
            else_block = None
            if self._check_and_move_if_successfully('BEGIN'):
                else_block = self.__parse_statement_part()
                self._expect_and_move('END')
            else:
                else_block = self.__parse_statement_part(depth=1)
        return NodeIfCondition(condition, block, else_block)
    
    def _parse_while_statement(self):
        self._expect_and_move('LPAREN')
        condition = self._parse_expression()
        self._expect_and_move('RPAREN')
        self._expect_and_move('DO')
        block = None
        if self._check_and_move_if_successfully('BEGIN'):
            block = self.__parse_statement_part()
            self._expect_and_move('END')
        else:
            block = self.__parse_statement_part(depth=1)
        return NodeWhileRepetitiveStatement(condition, block)
    
    def _parse_for_statement(self):
        variable = self._parse_factor()
        if not isinstance(variable,NodeVariable) :
            self._error('_expect variable')
        self._expect_and_move('ASSIGN')
        initial_expression = self._parse_expression()
        if not self._check('TO') and not self._check('DOWNTO'):
            self._error('_expect TO or DOWNTO')
        self._next_token()
        final_expression = self._parse_expression()
        self._expect_and_move('DO')
        statement_part = None
        if self._check_and_move_if_successfully('BEGIN'):
            statement_part = self.__parse_statement_part()
            self._expect_and_move('END')
        else:
            statement_part = self.__parse_statement_part(depth=1)
        return NodeForRepetitiveStatement(variable, initial_expression, final_expression, statement_part)
    
    def _parse_expression(self):
        term = None
        if self._check_and_move_if_successfully('LPAREN'):
            term = self._parse_expression()
            self._expect_and_move('RPAREN')
        else:
            term = self._parse_term()
        if self._check_and_move_if_successfully('MINUS'):
            return NodeMinusOperator(term, self._parse_expression())
        if self._check_and_move_if_successfully('PLUS'):
            return NodePlusOperator(term, self._parse_expression())
        if self._check_and_move_if_successfully('EQUALITY'):
            return NodeEqualOperator(term, self._parse_expression())
        if self._check_and_move_if_successfully('NONEQUALITY'):
            pass
        if self._check_and_move_if_successfully('GREATER'):
            return NodeGreaterOperator(term, self._parse_expression())
        if self._check_and_move_if_successfully('SMALLER'):
            return NodeSmallerOperator(term, self._parse_expression())
        return term
        
    def _parse_term(self):
        factor = self._parse_factor()
        if self._check_and_move_if_successfully('MULTIPLY'):
            return NodeMultiplyOperator(factor, self._parse_term())
        if self._check_and_move_if_successfully('DIVIDE'):
            return NodeDivideOperator(factor, self._parse_term())
        return factor
    
    def _parse_factor(self):
        token_value = self.current_token[1]
        if self._check_and_move_if_successfully('MINUS'):
            return NodeUnaryMinusOperator(self._parse_factor())
        if self._check_and_move_if_successfully('PLUS'):
            return NodeUnaryPlusOperator(self._parse_factor())
        if self._check_and_move_if_successfully('NUMBER'):
            return NodeNumber(token_value)
        if self._check_and_move_if_successfully('QUOTES'):
            token_value = ''
            while not self._check_and_move_if_successfully('QUOTES'):
                token_value += self.current_token[1] +' '
                self._next_token()
            return NodeString(token_value[0:len(token_value)])
        self._next_token()
        if self._check_and_move_if_successfully('LSBR'):
            node = NodeArrayBracketCall(NodeIdentifier(token_value), self._parse_expression())
            self._expect_and_move('RSBR')
            return node
        if self._check_and_move_if_successfully('LPAREN'):
            return NodeSubroutineCall(NodeIdentifier(token_value), NodeSubroutineParamsList(self._parse_subroutine_params()))
        else:
            return NodeVariable(token_value)
        