import parserV2 as p

class Gen:
    l = "   "

    def __init__(self):
        self.code = ""

    def declaration_part(self, dp):
        return ""
    
    def if_type(self, node):
        c = ""
        if isinstance(node, p.NodeVariable):
            c += f'"{node.value}"'
        else: c += f"{node.value}"
        return c
    
    def condition(self, node):
        c = ""
        if_type = self.if_type(node.right)
        if isinstance(node, p.NodeEqualOperator):
            c += f" == {if_type}"
        elif isinstance(node, p.NodeNotEqualOperator):
            c += f" != {if_type}"
        elif isinstance(node, p.NodeGreaterOperator):
            c += f" > {if_type}"
        elif isinstance(node, p.NodeSmallerOperator):
            c += f" < {if_type}"

        return c

    def if_operation(self, node):
        c = ""
        if isinstance(node, p.NodePlusOperator):
            c += " + "
        elif isinstance(node, p.NodeMinusOperator):
            c += " - "
        elif isinstance(node, p.NodeMultiplyOperator):
            c += " * "
        elif isinstance(node, p.NodeDivideOperator):
            c += " / "
        elif isinstance(node, p.NodeEqualOperator):
            c += " == "
        elif isinstance(node, p.NodeNotEqualOperator):
            c += " != "
        elif isinstance(node, p.NodeGreaterOperator):
            c += " > "
        elif isinstance(node, p.NodeSmallerOperator):
            c += " < "

        if isinstance(node.right, p.NodeNumber) or isinstance(node.right, p.NodeVariable):
            if_type = self.if_type(node.right)
            c += f"{if_type}"
        else:
            if_type = self.if_type(node.right.left)
            c += f"{if_type}"
            if_operation = self.if_operation(node.right)
            c += f"{if_operation}"


        return c

    def assign_operation(self, node):
        c = f"{node.left.value} = "
        cond = not (isinstance(node.right, p.NodeNumber) or isinstance(node.right, p.NodeVariable))
        f = True

        if not cond and f:
            if_type = self.if_type(node.right)
            c += f"{if_type}"
        else:
            f = False

            if_type = self.if_type(node.right.left)
            c += f"{if_type}"

            # node = node.right
            cond = not (isinstance(node.right.right, p.NodeNumber) or isinstance(node.right.right, p.NodeVariable))
            if not cond:
                if_operation = self.if_operation(node.right)
                c += f"{if_operation}"
            else:
                if_operation = self.if_operation(node.right)
                c += f"{if_operation}"

        
        c += ";\n"
        return c
    
    def if_condition(self, node, level):
        condition = self.condition(node.condition)
        c = f"if ({node.condition.left.value}{condition})"+" {\n"
        node = node.block.statement_sequence
        # как вставить statement_part
        statement_part = self.statement_part(node, level+1)
        c += f"{statement_part}"

        for i in range (0, level):
            c += self.l
        c += "}\n"
        return c
    
    def while_repetitive_statement(self, node, level):
        condition = self.condition(node.condition)
        c = f"while ({node.condition.left.value}{condition})"+" {\n"
        node = node.block.statement_sequence
        # как вставить statement_part
        statement_part = self.statement_part(node, level+1)
        c += f"{statement_part}"


        for i in range (0, level):
            c += self.l
        c += "}\n"
        return c
        

    def statement_part(self, sp, level):
        c = ""

        for i in sp:
            for j in range (0, level):
                c += self.l
            if (isinstance(i, p.NodeAssignOperation)):
                assign_operation = self.assign_operation(i)
                c += f"{assign_operation}"
            if (isinstance(i, p.NodeIfCondition)):
                if_condition = self.if_condition(i, level)
                c += f"{if_condition}"
            if (isinstance(i, p.NodeWhileRepetitiveStatement)):
                while_repetitive_statement = self.while_repetitive_statement(i, level)
                c += f"{while_repetitive_statement}"

        return c

    def generate(self, parser : p.NodeProgram):
        self.code = ""

        self.code += "int main(){\n"
        statement_part = self.statement_part(parser.statement_part.statement_sequence, 1)
        self.code += f"{statement_part}"

        self.code += "   return 0;\n}" 
