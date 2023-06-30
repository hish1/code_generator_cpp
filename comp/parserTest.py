import pytest
from lexer import Lexer
import parserV2 as p
 
def read_from_file(filepath) -> str:
    f = open(filepath, 'r')
    code = f.read()
    return code

def test_hello_world():
    code = read_from_file('C:/Users/User/Desktop/second/Simple Project/python_module/parser/test_files/hello world.pas')
    lexer = Lexer(code)
    parser = p.Parser(lexer)
    res = parser.parse_prog()
    declaration = p.NodeDeclarationPart()
    param_list = p.NodeSubroutineParamsList([p.NodeString('hello world')])
    writeln_call = p.NodeSubroutineCall(p.NodeIdentifier('writeln'),param_list)
    statement_part = p.NodeStatementPart()
    statement_part.append(writeln_call)
    main_node = p.NodeProgram('V1', declaration, statement_part)
    assert str(res).strip() == str(main_node).strip()

def test_declaration_parse():
    code1 = read_from_file('python_module/parser/test_files/var declaration.pas')
    lexer1 = Lexer(code1)
    parser1 = p.Parser(lexer1)
    res = parser1.parse_prog()
    const_definition_part = p.NodeConstDefinitionPart()
    const_definition_part.append(p.NodeConstDeclaration('N', p.NodeNumber(10)))
    var_declaration_part = p.NodeVariableDeclarationPart()
    var_declaration_part.append(p.NodeVariableDeclaration('i', p.NodeType('INTEGER')))
    var_declaration_part.append(p.NodeVariableDeclaration('j', p.NodeType('INTEGER')))
    declaration = p.NodeDeclarationPart(variable_declaration_part=var_declaration_part, const_definition_part=const_definition_part)
    statement_part1 = p.NodeStatementPart([])
    print(statement_part1)
    main_node = p.NodeProgram('V1', declaration, statement_part1)
    assert str(res) == str(main_node)

def test_if_statement():
    code = read_from_file('python_module/parser/test_files/if statement.pas')
    lexer = Lexer(code)
    parser = p.Parser(lexer)
    res = parser.parse_prog()
    declaration = p.NodeDeclarationPart(None, None, None, None)
    statement_part = p.NodeStatementPart([])
    if_condition = p.NodeGreaterOperator(p.NodeVariable('i'), p.NodeNumber(3))
    if_then_block = p.NodeStatementPart([])
    if_then_block.append(p.NodeAssignOperation(p.NodeVariable('i'), p.NodeUnaryMinusOperator(p.NodeNumber(3))))
    if_else_block = p.NodeStatementPart([])
    if_else_block.append(p.NodeAssignOperation(p.NodeVariable('i'), p.NodeNumber(12)))
    if_st = p.NodeIfCondition(condition=if_condition, block=if_then_block, else_block=if_else_block)
    statement_part.append(if_st)
    main_node = p.NodeProgram('V1', declaration, statement_part)
    assert str(res) == str(main_node)

def test_for_statement():
    code = read_from_file('python_module/parser/test_files/for statement.pas')
    lexer = Lexer(code)
    parser = p.Parser(lexer)
    res = parser.parse_prog()
    declaration = p.NodeDeclarationPart(None, None, None, None)
    for_var = p.NodeVariable('i')
    for_initial = p.NodeNumber(1)
    for_end_initial = p.NodePlusOperator(p.NodeNumber(5), p.NodeNumber(7))
    for_st_part = p.NodeStatementPart([])
    for_st_part.append(p.NodeAssignOperation(p.NodeVariable('c'), p.NodePlusOperator(p.NodeVariable('c'), p.NodeVariable('i'))))
    for_st_part.append(p.NodeAssignOperation(p.NodeVariable('d'), p.NodeMultiplyOperator(p.NodeVariable('c'), p.NodeNumber(2))))
    for_st = p.NodeForRepetitiveStatement(for_var, for_initial, for_end_initial, for_st_part)
    statement_part = p.NodeStatementPart([])
    statement_part.append(for_st)
    main_node = p.NodeProgram('V1', declaration, statement_part)
    assert str(res) == str(main_node)

def test_procedure_definition():
    code = read_from_file('python_module/parser/test_files/prcodeure definition.pas')
    lexer = Lexer(code)
    parser = p.Parser(lexer)
    res = parser.parse_prog()
    subroutine_formal_list = p.NodeSubroutineFormalParamList([])
    subroutine_formal_list.append(p.NodeVariableDeclaration('i', p.NodeType('INTEGER')))
    proc_var_decl = p.NodeVariableDeclarationPart([])
    proc_var_decl.append(p.NodeVariableDeclaration('j', p.NodeType('INTEGER')))
    sub_declaration = p.NodeDeclarationPart(None, None, proc_var_decl, None)
    sub_statement_part = p.NodeStatementPart([])
    sub_statement_part.append(p.NodeAssignOperation(p.NodeVariable('i'), p.NodeVariable('j')))
    proc_decl = p.NodeProcedure('test', subroutine_formal_list, sub_declaration, sub_statement_part)
    subroutine_formal_params = p.NodeSubroutineParamsList([p.NodeNumber(5)])
    node_subroutine_del_part = p.NodeSubroutineDeclarationPart([])
    node_subroutine_del_part.append(proc_decl)
    declaration = p.NodeDeclarationPart(None, None, None, node_subroutine_del_part)
    statement_part = p.NodeStatementPart([])
    statement_part.append(p.NodeSubroutineCall(p.NodeIdentifier('test'), subroutine_formal_params))
    main_node = p.NodeProgram('V1', declaration, statement_part)
    # print(main_node)
    # print(res)
    assert str(res) == str(main_node)

