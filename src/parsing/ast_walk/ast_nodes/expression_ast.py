from parsing.ast_walk.ast_nodes.my_ats_node import MyAstNode
from fparser.two.Fortran2003 import Add_Operand, Mult_Operand, Parenthesis, Part_Ref, Name, Intrinsic_Function_Reference, \
    Int_Literal_Constant, Real_Literal_Constant, Char_Literal_Constant, Boz_Literal_Constant, Logical_Literal_Constant, Data_Ref, \
    Base, Section_Subscript_List, Subscript_Triplet

from parsing.find_in_tree import find_in_node, find_in_tree, findall_in_node, findall_in_tree

class _Helpers:
    @staticmethod
    def indexes_to_array_in_reference_are_slices(fnode):
        subscript_list = find_in_node(fnode, Section_Subscript_List)
        triplets = findall_in_node(subscript_list, Subscript_Triplet)

        if len(triplets) == 0:
            return False

        if len(triplets) != len(subscript_list.children):
            raise ValueError("Subscript list has non-triplet elements")

        return True


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

    def indexes_to_array_are_slices(self):
        return _Helpers.indexes_to_array_in_reference_are_slices(self.fnode)
        

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
        self.value: str = fnode.children[0]

        self.kind: str | None = fnode.children[1] if len(fnode.children) > 1 else None
        self.kind = self.kind.lower() if self.kind is not None else None

class DataRefNode(MyAstNode[Data_Ref]):
    def __init__(self, fnode: Data_Ref):
        super().__init__(fnode)

        self.object_name = fnode.children[0].tostr().lower()
        self.property_fnode = fnode.children[1]

        # this might not work as expected ¯\_(ツ)_/¯
        self.property_name = find_in_tree(fnode.children[1], Name).tostr().lower()

    def indexes_to_array_are_slices(self):
        return _Helpers.indexes_to_array_in_reference_are_slices(self.fnode)
