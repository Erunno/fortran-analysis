from parsing.ast_walk.ast_nodes.my_ats_node import CallNode, MyAstNode
from fparser.two.Fortran2003 import Add_Operand, Mult_Operand, Parenthesis, Part_Ref, Name, Intrinsic_Function_Reference, \
    Int_Literal_Constant, Real_Literal_Constant, Char_Literal_Constant, Boz_Literal_Constant, Logical_Literal_Constant, Data_Ref, \
    Base, Section_Subscript_List, Subscript_Triplet, Level_2_Unary_Expr, Procedure_Designator

from parsing.find_in_tree import find_in_node, find_in_tree, findall_in_node, findall_in_tree

class _Helpers:
    @staticmethod
    def indexes_to_array_in_reference_are_slices(fnode):
        subscript_list = find_in_node(fnode, Section_Subscript_List)
        triplets = findall_in_node(subscript_list, Subscript_Triplet)

        if len(triplets) == 0:
            return False

        if len(triplets) != len(subscript_list.children):
            pass

        return True
    
    @staticmethod
    def get_slices_dimensions(fnode):
        subscript_list = find_in_node(fnode, Section_Subscript_List)

        sliced_dims = []

        for dim, child in enumerate(subscript_list.children):
            if isinstance(child, Subscript_Triplet):
                sliced_dims.append(dim)

        return sliced_dims

    @staticmethod
    def is_reference_without_indexing(fnode):
        subscript_list = find_in_tree(fnode, Section_Subscript_List)
        return subscript_list is None

class OperatorNode(MyAstNode[Add_Operand | Mult_Operand]):
    def __init__(self, fnode: Add_Operand | Mult_Operand):
        super().__init__(fnode)
    
    def left_fnode(self):
        return self.fnode.children[0]
    
    def operator_sign(self):
        return self.fnode.children[1]
    
    def right_fnode(self):
        return self.fnode.children[2]

class UnaryOperatorNode(MyAstNode[Level_2_Unary_Expr]):
    def __init__(self, fnode: Level_2_Unary_Expr):
        super().__init__(fnode)

    def operator_sign(self):
        return self.fnode.children[0]

    def expr_fnode(self):
        return self.fnode.children[1]

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
    # !!! warning `fnode` can be a list of nodes not a single node 

    def __init__(self, fnode: Data_Ref | list[Base]):
        super().__init__(fnode)
        self.last_fnode = fnode[-1] if isinstance(fnode, (list, tuple)) else fnode.children[-1]

    def indexes_to_array_are_slices(self):
        return _Helpers.indexes_to_array_in_reference_are_slices(self.last_fnode)
    
    def is_reference_without_indexing(self):
        return _Helpers.is_reference_without_indexing(self.fnode)

    def get_left_node(self):
        fnodes = self.fnode[:-1] if isinstance(self.fnode, (list, tuple)) else self.fnode.children[:-1]
        
        if len(fnodes) == 1:
            return fnodes[0]
        
        return DataRefNode(fnodes)

    def get_sliced_dimensions(self):
        return _Helpers.get_slices_dimensions(self.last_fnode)

class PartRefNode(MyAstNode[Part_Ref]):
    def __init__(self, fnode: Part_Ref):
        super().__init__(fnode)
        self.ref_name = fnode.children[0].tostr().lower()
    
    def indexes_to_array_are_slices(self):
        return _Helpers.indexes_to_array_in_reference_are_slices(self.fnode)
    
    def is_reference_without_indexing(self):
        return _Helpers.is_reference_without_indexing(self.fnode)
    
    def get_sliced_dimensions(self):
        return _Helpers.get_slices_dimensions(self.fnode)

    def ref_name_fnode(self):
        return self.fnode.children[0]

    def args_fnodes(self):
        subscription_list = find_in_node(self.fnode, Section_Subscript_List)
        return subscription_list.children
    
class SubscriptTripletNode(MyAstNode[Subscript_Triplet]):
    def __init__(self, fnode: Subscript_Triplet):
        super().__init__(fnode)
   
    def lower_bound_fnode(self):
        return self.fnode.children[0]
    
    def upper_bound_fnode(self):
        return self.fnode.children[1]

    def stride_fnode(self):
        return self.fnode.children[2] 

class PointerAssignmentNode(MyAstNode[Base]):
    def __init__(self, fnode: Base):
        super().__init__(fnode)

    def target_fnode(self):
        return self.fnode.children[0]
    
    def target_bounds_fnode(self):
        return self.fnode.children[1]
    
    def source_fnode(self):
        return self.fnode.children[2]

class BoundsSpecListNode(MyAstNode[Base]):
    def __init__(self, fnode: Base):
        super().__init__(fnode)

    def bounds_fnodes(self):
        return self.fnode.children

class BoundsSpecNode(MyAstNode[Base]):
    def __init__(self, fnode: Base):
        super().__init__(fnode)

    def lower_bound_fnode(self):
        return self.fnode.children[0]
    
    def upper_bound_fnode(self):
        return self.fnode.children[1]
    
class FunctionReferenceNode(MyAstNode[Base]):
    def __init__(self, fnode: Base):
        super().__init__(fnode)

        if not self._children_are_procedure_designator_and_NONE(fnode):
            raise NotImplementedError("New case that is not handled")

    def function_expr_fnode(self):
        return self.fnode.children[0]
    
    def _children_are_procedure_designator_and_NONE(self, fnode):
        return len(fnode.children) == 2 and isinstance(fnode.children[0], Procedure_Designator) and fnode.children[1] is None
    
class StructureConstructorNode(CallNode):
    ## !!! 
    ##      Warning: fparser seams to wrap (some) function calls in a StructureConstructor node
    ##               therefore I will mask this class as a CallNode
    ##               ... unless I find a case where a actual structure constructor is used
    ## !!!

    def __init__(self, fnode: Base):
        super().__init__(fnode)

    # reimplement the CallNode methods

    def get_call_identifier_fnode(self):
        return NameNode(self.fnode.children[0])

    def get_argument_expression_fnodes(self):
        return self.fnode.children[1].children if self.fnode.children[1] is not None else []
  