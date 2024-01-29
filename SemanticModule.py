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

    def __str__(self):
        return self.identifier

class TypeVariable(Variable):
    pass

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

    # Convert scope and identifier to key
    def __convert_to_name(self, scope, identifier):
        return f'{".".join(scope)}.{identifier}' if len(scope) != 0 else identifier

    # Add variable or Type to scope
    def __add_to_scope(self, scope, identifier, variable : Variable):
        full_name = self.__convert_to_name(scope, identifier)
        if full_name in self.__scope_table:
            self.__raise_exception(f'Try to redefine identifier {name} is same scope .{".".join(scope)}')
        self.__scope_table[full_name] = variable

    def add_variable(self, scope, identifier, _type, constant = False):
        variable = Variable(identifier, _type, constant)
        self.__add_to_scope(scope, identifier, variable)

    def add_type(self, scope, identifier, original_type : NodeType):
        variable = TypeVariable(identifier, original_type)
        self.__add_to_scope(scope, identifier, variable)

    def add_subroutine(self, scope, identifier, _type, formal_params):
        variable = SubroutineVariable(identifier, _type, formal_params)
        self.__add_to_scope(scope, identifier, variable)

    def __get_object(self, scope, identifier, prefered_object = None):
        local_scope = scope.copy()
        scope_len_counter = len(scope)
        while scope_len_counter >= 0:
            full_name = self.__convert_to_name(local_scope, identifier)
            if full_name in self.__scope_table:
                object = self.__scope_table[full_name]
                if (prefered_object is None) or (isinstance(object, prefered_object)):
                    return object
            if len(local_scope) > 0:
                local_scope.pop()
            scope_len_counter -= 1
        self.__raise_exception(f'Identifier {identifier} doesn\'t declared')

    def get_type(self, scope, type_name):
        return self.__get_object(scope, type_name, TypeVariable)

    def get_variable(self, scope, variable_name):
        return self.__get_object(scope, variable_name, Variable)

    def return_value_type(self, value):
        return semantic_tools.get_value_type(value)

    def check_subroutine_call(self, scope, subroutine_name, input_params):
        subroutine = self.get_variable(scope, subroutine_name)
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
            if (formal_type, call_type) not in semantic_tools.assign_support:
                self.__raise_exception(f'TypeAttribute error: Subroutine {subroutine.identifier} expect {formal_type} in {index}, got {call_type.value}')
        return True

    def check_array_access(self, scope, variable_name, params):
        params = params.params
        variable = self.get_variable(scope, variable_name)
        variable_type = variable.type
        while isinstance(variable_type, Variable):
            variable_type = variable_type.type
        if not isinstance(variable_type, NodeArrayType):
            self.__raise_exception(f'Identifier {variable_name} is not callable')
        ranges = variable_type.array_ranges
        if len(ranges) != len(params):
            self.__raise_exception(f'{variable.identifier} call expect {len(ranges)} params, got {len(params)}')
        for index in range(0, len(ranges)):
            param = params[index]
            if isinstance(param, NodeVariable):
                param = self.get_variable(scope, param.identifier)
            if not PrimitiveType.is_type_integer(param.type):
                self.__raise_exception(f'Хз что тут написать, однако параметр должен быть исчесляемый у массивов')
            if isinstance(param, NodeValue):
                left_bound = ranges[index].left_bound.value
                right_bound = ranges[index].right_bound.value
                if not int(left_bound) <= int(param.value) <= int(right_bound):
                    self.__raise_exception(f'Array {variable.identifier} index out of bound [{left_bound}..{right_bound}]')
        return True

    def check_assign(self, scope, variable_name, condition):
        variable = self.get_variable(scope, variable_name)
        variable_type = variable.type
        while not PrimitiveType.__contains__(variable_type):
            variable_type = variable_type.type
        condition_type = self.predict_condition_type(condition, scope)
        if (variable_type, condition_type) not in semantic_tools.assign_support:
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
 