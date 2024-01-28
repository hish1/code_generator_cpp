from SupportClasses import PrimitiveType
from Node import Node
from SupportClasses import NodeType
from SupportClasses import NodeVariable, NodeSubroutine, NodeCallParams, NodeArrayType, NodeValue
# Классы для объявления
from SupportClasses import NodeVariableDeclaration, NodeTypeDeclaration, NodeConstantDeclaration 
from SupportClasses import NodeBinaryOperator, NodeUnaryOperator
from SupportClasses import Operator
import SemanticTools as semantic_tools

# Класс для хранения объявленных переменных в семантике
class Variable:
    def __init__(self, 
                 identifier = '', 
                 _type = PrimitiveType.UNDEFINED,
                 is_immutable = False):
        self.identifier = identifier
        self.type = _type
        self.IS_IMMUTABLE = is_immutable
    
    def to_node_variable(self):
        node = NodeVariable()
        node.identifier = self.identifier
        node.type = self.type
        return node

    @staticmethod
    def to_variable(node : NodeVariable):
        variable = Variable()
        variable.identifier = node.identifier
        variable.type = node.type
        return variable

class ArrayVariable(Variable):
    def __init__(self, 
                 identifier = '',
                 _type = PrimitiveType.UNDEFINED,
                 left_bound = None,
                 right_bound = None):
        super().__init__(identifier, _type)
        self.left_bound = left_bound
        self.right_bound = right_bound

    @staticmethod
    def to_variable(node : NodeArrayType):
        variable = Variable()
        variable.identifier = node.identifier
        variable.type = node.type
        variable.left_bound = node.left_bound
        variable.right_bound = node.right_bound
        return variable

class TypeVariable(Variable):
    
    def  to_node_variable(self):
        node = NodeType()
        node.identifier = self.identifier
        node.type = self.type
        return node

    @staticmethod
    def to_variable(node : NodeType):
        variable = TypeVariable()
        variable.identifier = node.identifier
        variable.type = node.type
        return variable 

class SubroutineVariable(Variable):
    def __init__(self, 
                 identifier = '',
                 _type = PrimitiveType.UNDEFINED,
                 formal_params = None):
        super().__init__(identifier, _type)
        self.formal_params = formal_params

class SemanticModule:

    def __init__(self):
        self.__scope_table = dict()

    def __raise_exception(self, message):
        raise AttributeError(f'Semantic Module error: {message}')

    def __add_to_scope(self, full_name, variable : Variable):
        if full_name in self.__scope_table:
            self.__raise_exception(f'Identifier {full_name} is already declared')
        self.__scope_table[full_name] = variable

    def add_variable(self, scope, identifier, _type):
        full_name = f'{".".join(scope)}.{identifier}'
        variable = Variable(identifier, _type)
        self.__add_to_scope(full_name, variable)

    def add_type(self, scope, identifier, original_type : NodeType):
        full_name = f'{".".join(scope)}.{identifier}'
        variable = TypeVariable(identifier, original_type)
        self.__add_to_scope(full_name, variable)

    def add_const(self, scope, identifier, _type):
        full_name = f'{".".join(scope)}.{identifier}'
        variable = Variable(identifier, _type, True)
        self.__add_to_scope(full_name, variable)

    def add_subroutine(self, scope, identifier, _type, formal_params):
        full_name = f'{".".join(scope)}.{identifier}'
        variable = SubroutineVariable(identifier, _type, formal_params)
        self.__add_to_scope(full_name, variable)

    def analyze_type(self, expression):
        return PrimitiveType.INTEGER

    def __get_object(self, scope, identifier, prefered_object = None):
        local_scope = scope.copy()
        scope_len_counter = len(scope)
        while scope_len_counter >= 0:
            full_name = f'{".".join(local_scope)}.{identifier}'
            if prefered_object is None:
                declarations = list(filter(lambda pair: pair[0] == full_name, self.__scope_table.items()))
            else:
                declarations = list(filter(lambda pair: pair[0] == full_name and isinstance(pair[1], prefered_object), self.__scope_table.items()))
            if len(declarations) == 1:
                return declarations[0][1]
            if len(local_scope) > 0:
                local_scope.pop()
            scope_len_counter -= 1
        self.__raise_exception(f'Identifier {identifier} doesn\'t declared')

    def get_type(self, scope, type_name):
        return self.__get_object(scope, type_name, TypeVariable)

    def get_variable(self, scope, variable_name):
        return self.__get_object(scope, variable_name, Variable)
    
    def get_array(self, scope, array_name):
        return self.__get_object(scope, array_name, Variable)

    def get_subroutine(self, scope, subroutine_name):
        return self.__get_object(scope, subroutine_name, SubroutineVariable)

    def return_value_type(self, value):
        return semantic_tools.get_value_type(value)

    def check_subroutine_call(self, scope, subroutine_name, input_params):
        subroutine = self.get_subroutine(scope, subroutine_name)
        if not isinstance(subroutine, SubroutineVariable):
            self.__raise_exception(f'Identifier {subroutine.identifier} is not callable')
        formal_params = subroutine.formal_params.params
        call_params = input_params.params
        if len(call_params) != len(formal_params):
            self.__raise_exception(f'Subroute {subroutine.identifier} expect {len(formal_params)} params, got {len(call_params)}')
        for index in range (0, len(formal_params)):
            formal_param = formal_params[index]
            call_param = call_params[index]
            if isinstance(call_param, NodeVariable):
                call_param = self.get_variable(scope, call_param.identifier)
            formal_type = self.predict_condition_type(formal_param, scope)
            call_type = self.predict_condition_type(call_param, scope)
            # TODO Аналогично с плюсом
            if (formal_type, call_type, Operator.PLUS) not in semantic_tools.base_type_upcast:
                self.__raise_exception(f'TypeAttribute error: Subroutine {subroutine.identifier} expect {formal_type} in {index}, got {call_type.value}')
        return True

    def check_array_access(self, scope, array_name, param):
        array = self.get_array(scope, array_name)
        array_type = array.type
        while not isinstance(array_type, NodeArrayType):
            try:
                array_type = array_type.type
            except:
                self.__raise_exception(f'Identifier {array_name} is not array')
        left_bound = array_type.left_bound
        right_bound = array_type.right_bound
        if len(param.params) != 1:
            self.__raise_exception(f'Array {array.identifier} call expect 1 param, got {len(param)}')
        if isinstance(param.params[0], NodeVariable):
            param_type = self.get_variable(scope, param.params[0].identifier).type
        else:
            param_type = param.params[0].type
        if not PrimitiveType.is_type_integer(param_type):
            self.__raise_exception(f'Хз что тут написать, однако параметр должен быть исчесляемый у массивов')
        if isinstance(param.params[0], NodeValue):
            left_bound = int(left_bound.value)
            right_bound = int(right_bound.value)
            param_value = int(param.params[0].value)
            if not left_bound < param_value < right_bound:
                self.__raise_exception(f'Array {array.identifier} index out of bound')
        return True

    def check_assign(self, scope, variable_name, condition):
        variable = self.get_variable(scope, variable_name)
        variable_type = variable.type
        while not PrimitiveType.__contains__(variable_type):
            variable_type = variable_type.type
        condition_type = self.predict_condition_type(condition, scope)
        # TODO убрать костыль с Operator.PLUS
        if (variable_type, condition_type, Operator.PLUS) not in semantic_tools.base_type_upcast:
            self.__raise_exception(f'Incompatible types: got "{condition_type.value}" expected "{variable_type.value}"')
        return True

    def predict_condition_type(self, condition, scope = None):
        order_result = self.post_order_condition(condition, scope)
        predict_type = self.convolute_type_operator_vector(order_result)
        return predict_type

    def post_order_condition(self, top, scope = None):
        stack = [top]
        visited = []
        result = []
        while len(stack) > 0:
            top = stack.pop()
            if isinstance(top, NodeBinaryOperator):
                if top.left not in visited and top.right not in visited:
                    stack.append(top)
                    stack.append(top.right)
                    stack.append(top.left)
                else:
                    visited.append(top)
                    if top.operation_type in Operator.get_value_operators():
                        result.append(top.operation_type)
            elif isinstance(top, NodeUnaryOperator):
                if top.left not in visited:
                    stack.append(top)
                    stack.append(top.left)
                else:
                    visited.append(top)
                    result.append(top.operation_type)
            else:
                visited.append(top)
                if isinstance(top, NodeVariable):
                    variable = self.__get_object(scope, top.identifier)
                    result.append(variable.type)
                else:
                    if 'type' in top.__dict__:
                        result.append(top.type)
        return result

    def convolute_type_operator_vector(self, post_order_result):
        while len(post_order_result) != 1:
            temp = []
            index = 0
            while len(post_order_result) > index:
                if len(post_order_result) <= index + 1:
                    while len(post_order_result) > index:
                        temp.append(post_order_result[index])
                        index += 1
                elif isinstance(post_order_result[index], Operator):
                    temp.append(post_order_result[index])
                    index += 1  
                else:
                    first = post_order_result[index]
                    if post_order_result[index + 1] == Operator.UNARY_MINUS or post_order_result[index + 1] == Operator.UNARY_PLUS:
                        operator = post_order_result[index + 1]
                        temp.append(cast_types_by_operator(first, None, operator))
                        index += 2
                    else:
                        second = post_order_result[index + 1]
                        operator = post_order_result[index + 2]
                        if first.support_operation(operator) and second.support_operation(operator):
                            temp.append(semantic_tools.cast_types_by_operator(first, second, operator))
                        index += 3
            post_order_result = temp
        return post_order_result[0]
 