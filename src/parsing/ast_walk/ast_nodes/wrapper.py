from fparser.two.Fortran2003 import Base, Procedure_Stmt, Assignment_Stmt, Subroutine_Stmt, Subroutine_Subprogram, Function_Subprogram, Call_Stmt, \
                                    Function_Stmt, If_Construct, Write_Stmt, Add_Operand, Mult_Operand, Or_Operand, Parenthesis, Part_Ref, Name, \
                                    Intrinsic_Function_Reference, Int_Literal_Constant, Real_Literal_Constant, Char_Literal_Constant, Boz_Literal_Constant, \
                                    Logical_Literal_Constant, Level_2_Expr, Level_4_Expr, Data_Ref, Procedure_Designator, Subscript_Triplet, \
                                    Forall_Header, Forall_Triplet_Spec, Level_2_Unary_Expr, Nullify_Stmt, Return_Stmt, Pointer_Assignment_Stmt, \
                                    Bounds_Spec_List, Bounds_Spec, Equiv_Operand, Function_Reference, And_Operand, Structure_Constructor, Exit_Stmt, \
                                    Cycle_Stmt, Subroutine_Body, Case_Construct, Continue_Stmt, Array_Section, Level_3_Expr, Component_Spec, \
                                    Deallocate_Stmt, Data_Pointer_Object

from fparser.two.Fortran2008.block_nonlabel_do_construct_r814_2 import Block_Nonlabel_Do_Construct
from fparser.two.Fortran2008.if_stmt_r837 import If_Stmt as Fortran8_If_Stmt
from fparser.two.Fortran2008.loop_control_r818 import Loop_Control
from fparser.two.Fortran2008.allocate_stmt_r626 import Allocate_Stmt
from fparser.two.Fortran2008.alloc_opt_r627 import Alloc_Opt

from parsing.ast_walk.ast_nodes.expression_ast import BoundsSpecListNode, BoundsSpecNode, DataPointerObjectNode, DataRefNode, FunctionReferenceNode, IntrinsicFunctionNode, \
    LiteralNode, NameNode, OperatorNode, ParenthesisNode, PartRefNode, ReferenceNode, SubscriptTripletNode, UnaryOperatorNode, PointerAssignmentNode, \
    StructureConstructorNode, ArraySectionNode, ComponentSpecNode
from parsing.ast_walk.ast_nodes.my_ats_node import AllocOptNode, AssignmentNode, CallNode, ForAllHeaderNode, ForAllTripletNode, ForLoopNode, FunctionDefinitionNode, \
    IfBlockNode, LoopControlNode, MyAstNode, NullifyNode, SubroutineDefinitionNode, WriteStdoutNode, ProcedureDesignatorNode, ReturnStmtNode, \
    ExitStmtNode, CycleStmtNode, CaseConstructNode, ContinueStmtNode, AllocateNode, DeallocateNode

_node_map = [
    (Assignment_Stmt, AssignmentNode),
    (Function_Subprogram, FunctionDefinitionNode),
    (Subroutine_Subprogram, SubroutineDefinitionNode),
    (Subroutine_Body, SubroutineDefinitionNode),
    (Call_Stmt, CallNode),
    (Block_Nonlabel_Do_Construct, ForLoopNode),
    (If_Construct, IfBlockNode),
    (Write_Stmt, WriteStdoutNode),
    (Fortran8_If_Stmt, IfBlockNode),
    (Add_Operand, OperatorNode),
    (Mult_Operand, OperatorNode),
    (Or_Operand, OperatorNode),
    (Equiv_Operand, OperatorNode),
    (Level_2_Expr, OperatorNode),
    (Level_3_Expr, OperatorNode),
    (Level_4_Expr, OperatorNode),
    (Level_2_Unary_Expr, UnaryOperatorNode),
    (And_Operand, UnaryOperatorNode),
    (Parenthesis, ParenthesisNode),
    (Name, NameNode),
    (Intrinsic_Function_Reference, IntrinsicFunctionNode),
    (Int_Literal_Constant, LiteralNode),
    (Real_Literal_Constant, LiteralNode),
    (Char_Literal_Constant, LiteralNode),
    (Boz_Literal_Constant, LiteralNode),
    (Logical_Literal_Constant, LiteralNode),
    (Data_Ref, DataRefNode),
    (Data_Pointer_Object, DataPointerObjectNode),
    (Procedure_Designator, ProcedureDesignatorNode),
    (Part_Ref, PartRefNode),
    (Subscript_Triplet, SubscriptTripletNode),
    (Loop_Control, LoopControlNode),
    (Forall_Header, ForAllHeaderNode),
    (Forall_Triplet_Spec, ForAllTripletNode),
    (Nullify_Stmt, NullifyNode),
    (Return_Stmt, ReturnStmtNode),
    (Pointer_Assignment_Stmt, PointerAssignmentNode),
    (Bounds_Spec_List, BoundsSpecListNode),
    (Bounds_Spec, BoundsSpecNode),
    (Function_Reference, FunctionReferenceNode),
    (Structure_Constructor, StructureConstructorNode),
    (Exit_Stmt, ExitStmtNode),
    (Cycle_Stmt, CycleStmtNode),
    (Continue_Stmt, ContinueStmtNode),
    (Case_Construct, CaseConstructNode),
    (Array_Section, ArraySectionNode),
    (Component_Spec, ComponentSpecNode),
    (Allocate_Stmt, AllocateNode),
    (Alloc_Opt, AllocOptNode),
    (Deallocate_Stmt, DeallocateNode),
]

_node_map_dict = {fnode: my_node for fnode, my_node in _node_map}

def wrap_node(fnode: Base) -> MyAstNode:
    return _node_map_dict[fnode.__class__](fnode)