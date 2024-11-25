from parsing.ast_walk.ast_nodes.my_ats_node import MyAstNode
from fparser.two.Fortran2003 import Add_Operand, Mult_Operand, Parenthesis, Part_Ref, Name, Intrinsic_Function_Reference, \
    Int_Literal_Constant, Real_Literal_Constant, Char_Literal_Constant, Boz_Literal_Constant, Logical_Literal_Constant, Data_Ref, \
    Base

from parsing.find_in_tree import find_in_tree

class OperatorNode(MyAstNode[Add_Operand | Mult_Operand]):
    def __init__(self, fnode: Add_Operand | Mult_Operand):
        super().__init__(fnode)
        
        self.left_expr = fnode.children[0]
        self.operator_sign = fnode.children[1]
        self.right_expr = fnode.children[2]

class ParenthesisNode(MyAstNode[Parenthesis]):
    def __init__(self, fnode: Parenthesis):
        super().__init__(fnode)

        self.inner_expr = fnode.children[1]

class ReferenceNode(MyAstNode[Part_Ref]):
    def __init__(self, fnode: Part_Ref):
        super().__init__(fnode)

        self.ref_name = fnode.children[0].tostr().lower()

class NameNode(MyAstNode[Name]):
    def __init__(self, fnode: Name):
        super().__init__(fnode)

        self.ref_name = fnode.tostr().lower()

class IntrinsicFunctionNode(MyAstNode[Intrinsic_Function_Reference]):
    def __init__(self, fnode: Intrinsic_Function_Reference):
        self.function_name = fnode.children[0].tostr().lower()
        self.call_args_exprs: list[Base] = fnode.children[1].children

class LiteralNode(MyAstNode[Int_Literal_Constant | Real_Literal_Constant | Char_Literal_Constant | Boz_Literal_Constant | Logical_Literal_Constant]):
    def __init__(self, fnode: Int_Literal_Constant | Real_Literal_Constant | Char_Literal_Constant | Boz_Literal_Constant | Logical_Literal_Constant):
        super().__init__(fnode)
        self.value = fnode.children[0]

class DataRefNode(MyAstNode[Data_Ref]):
    def __init__(self, fnode: Data_Ref):
        super().__init__(fnode)

        self.object_name = fnode.children[0].tostr().lower()
        self.property_fnode = fnode.children[1]

        # this might not work as expected ¯\_(ツ)_/¯
        self.property_name = find_in_tree(fnode.children[1], Name).tostr().lower()
