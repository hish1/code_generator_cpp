from SupportClasses import NodeBinaryOperator, NodeValue, NodeVariable, NodeUnaryOperator
from SupportClasses import Operator as OP
from SupportClasses import PrimitiveType as PT
from typing import Final
import re
import math

base_type_upcast = {}

# https://pascalabc.net/downloads/pabcnethelp/index.htm?page=LangGuide/Types/real.html 
# Opeartions upcast on + - and * (not /)
for type1 in PT.get_all_integer_integer_types():
    for type2 in PT.get_all_integer_integer_types():
        increase_weight = 2**math.ceil(math.log2(type1.byte_weight + type2.byte_weight))
        max_divide_weight = type1.byte_weight if type1.byte_weight > type2.byte_weight else type2.byte_weight
        if PT.is_type_signed_integer(type1) or PT.is_type_signed_integer(type2):
            next_type = PT.get_signed_int_by_weight(increase_weight)
            current_level_type = PT.get_signed_int_by_weight(max_divide_weight)
        else:
            next_type = PT.get_unsigned_int_by_weight(increase_weight)
            current_level_type = PT.get_unsigned_int_by_weight(max_divide_weight)
        base_type_upcast[(type1, type2, OP.PLUS)] = next_type
        base_type_upcast[(type1, type2, OP.MINUS)] = next_type
        base_type_upcast[(type1, type2, OP.MULTIPLY)] = next_type
        base_type_upcast[(type1, type2, OP.DIVIDE)] = current_level_type
        base_type_upcast[(type1, type2, OP.DIV)] = current_level_type
        base_type_upcast[(type1, type2, OP.MOD)] = current_level_type

for type in PT.get_all_integer_integer_types():
    if PT.is_type_unsigned_integer(type):
        base_type_upcast[(type, OP.UNARY_MINUS)] = PT.get_signed_int_by_weight(type.byte_weight)
    else:
        base_type_upcast[(type, OP.UNARY_MINUS)] = type
    base_type_upcast[(type, OP.PLUS)] = type

base_type_upcast[(PT.STRING, PT.STRING, OP.PLUS)] = PT.STRING
base_type_upcast[(PT.STRING, PT.CHAR, OP.PLUS)] = PT.STRING
base_type_upcast[(PT.CHAR, PT.CHAR, OP.PLUS)] = PT.STRING
         


MAX_BYTE_VALUE : Final = 2**8
MAX_WORD_VALUE : Final = 2**16
MAX_LONGWORD_VALUE : Final = 2**32
MAX_UINT64_VALUE : Final = 2**64
MAX_SHORTINT_VALUE : Final = MAX_BYTE_VALUE // 2
MAX_SMALLINT_VALUE : Final = MAX_WORD_VALUE // 2
MAX_INTEGER_VALUE : Final = MAX_LONGWORD_VALUE // 2
MAX_INT64_VALUE : Final = MAX_UINT64_VALUE // 2

INTEGER_REGEX : Final = r'^[-+]?[0-9]+$'
FLOAT_REGEX : Final = r'^[-+]?\d*\.?\d+|\d+$'
BOOLEAN_REGEX : Final = r'^(true)|(false)$'

BYTE_RANGE_CHECK = lambda num: 0 <= num <= MAX_BYTE_VALUE - 1
WORD_RANGE_CHECK = lambda num: 0 <= num <= MAX_WORD_VALUE - 1
LONGWORD_RANGE_CHECK = lambda num: 0 <= num <= MAX_LONGWORD_VALUE - 1
UINT64_RANGE_CHECK = lambda num: 0 <= num <= MAX_UINT64_VALUE - 1
SHORTINT_RANGE_CHECK = lambda num: -MAX_SHORTINT_VALUE <= num <= MAX_SHORTINT_VALUE
SMALLINT_RANGE_CHECK = lambda num: -MAX_SMALLINT_VALUE <= num <= MAX_SMALLINT_VALUE
INTEGER_RANGE_CHECK = lambda num: -MAX_INTEGER_VALUE <= num <= MAX_INTEGER_VALUE
INT64_RANGE_CHECK = lambda num: -MAX_INT64_VALUE <= num <= MAX_INT64_VALUE 

reverse_upcast = {}
for type_pair, return_type in base_type_upcast.items():
    if type_pair[0] != type_pair[1]:
        reverse_upcast[(type_pair[1], type_pair[0])] = return_type
base_type_upcast.update(reverse_upcast)
del reverse_upcast

def is_value_number(value):
    return re.match(INTEGER_REGEX, value) != None or re.match(FLOAT_REGEX, value)

def is_value_integer(value):
    return re.match(INTEGER_REGEX, value) != None

def is_value_float(value):
    return re.match(FLOAT_REGEX, value) != None

def is_value_boolean(value):
    return re.match(BOOLEAN_REGEX, value.lowercase())

def is_value_char(value):
    return len(value) == 1

def get_integer_value_type(value):
    match int(value):
        case num if BYTE_RANGE_CHECK(num):
            result = PT.BYTE
        case num if WORD_RANGE_CHECK(num):
            result = PT.WORD
        case num if LONGWORD_RANGE_CHECK(num):
            result = PT.LONGWORD
        case num if UINT64_RANGE_CHECK(num):
            result = PT.UINT64
        case num if SHORTINT_RANGE_CHECK(num):
            result = PT.SHORTINT
        case num if SMALLINT_RANGE_CHECK(num):
            result = PT.SMALLINT
        case num if INTEGER_RANGE_CHECK(num):
            result = PT.INTEGER
        case num if INT64_RANGE_CHECK(num):
            result = PT.INT64
        case _:
            raise Error(f'OUT OF RANGE: {-MAX_INT64_VALUE} AND {MAX_UINT64_VALUE}')
    return result

def get_value_type(value):
    if is_value_integer(value):
        _type = get_integer_value_type(value)
    elif is_value_float(value):
        _type = PT.FLOAT
    elif is_value_boolean(value):
        _type = PT.BOOLEAN
    elif is_value_char(value):
        _type = PT.CHAR
    else:
        _type = PT.STRING
    return _type

def cast_types_by_operator(type_1, type_2, oper):
    if oper in [OP.GREATER, OP.SMALLER, OP.EQUALITY, OP.NONEQUALITY]:
        return PT.BOOLEAN
    if type_2 is not None:
        return base_type_upcast[type_1, type_2, oper]
    else:
        return base_type_upcast[type1, oper]

def main():
    t1 = PT.INTEGER
    t2 = PT.INTEGER
    res = base_type_upcast[t1, t2, OP.PLUS]
    i = 43

if __name__ == '__main__':
    main()