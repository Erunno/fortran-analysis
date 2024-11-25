from fparser.two.Fortran2003 import Base, Procedure_Stmt, Assignment_Stmt, Subroutine_Stmt, Subroutine_Subprogram, Function_Subprogram, Call_Stmt, \
                                    Function_Stmt, If_Construct, Write_Stmt, Add_Operand, Mult_Operand, Parenthesis, Part_Ref, Name, \
                                    Intrinsic_Function_Reference, Int_Literal_Constant, Real_Literal_Constant, Char_Literal_Constant, Boz_Literal_Constant, \
                                    Logical_Literal_Constant, Level_2_Expr, Data_Ref

from fparser.two.Fortran2008.block_nonlabel_do_construct_r814_2 import Block_Nonlabel_Do_Construct
from fparser.two.Fortran2008.if_stmt_r837 import If_Stmt as Fortran8_If_Stmt
from parsing.ast_walk.ast_nodes.expression_ast import DataRefNode, IntrinsicFunctionNode, LiteralNode, NameNode, OperatorNode, ParenthesisNode, ReferenceNode
from parsing.ast_walk.ast_nodes.my_ats_node import AssignmentNode, CallNode, ForLoopNode, FunctionDefinitionNode, IfBlockNode, MyAstNode, \
                                                   SubroutineDefinitionNode, WriteStdoutNode

_node_map = [
    (Assignment_Stmt, AssignmentNode),
    (Function_Subprogram, FunctionDefinitionNode),
    (Subroutine_Subprogram, SubroutineDefinitionNode),
    (Call_Stmt, CallNode),
    (Block_Nonlabel_Do_Construct, ForLoopNode),
    (If_Construct, IfBlockNode),
    (Write_Stmt, WriteStdoutNode),
    (Fortran8_If_Stmt, IfBlockNode),
    (Add_Operand, OperatorNode),
    (Mult_Operand, OperatorNode),
    (Level_2_Expr, OperatorNode),
    (Parenthesis, ParenthesisNode),
    (Part_Ref, ReferenceNode),
    (Name, NameNode),
    (Intrinsic_Function_Reference, IntrinsicFunctionNode),
    (Int_Literal_Constant, LiteralNode),
    (Real_Literal_Constant, LiteralNode),
    (Char_Literal_Constant, LiteralNode),
    (Boz_Literal_Constant, LiteralNode),
    (Logical_Literal_Constant, LiteralNode),
    (Data_Ref, DataRefNode),

]

_node_map_dict = {fnode: my_node for fnode, my_node in _node_map}

def wrap_node(fnode: Base) -> MyAstNode:
    return _node_map_dict[fnode.__class__](fnode)