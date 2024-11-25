from fparser.two.Fortran2003 import Base, Procedure_Stmt, Assignment_Stmt, Subroutine_Stmt, Subroutine_Subprogram, Function_Subprogram, Call_Stmt, \
                                    Function_Stmt, If_Construct, Write_Stmt

from fparser.two.Fortran2008.block_nonlabel_do_construct_r814_2 import Block_Nonlabel_Do_Construct
from fparser.two.Fortran2008.if_stmt_r837 import If_Stmt as Fortran8_If_Stmt
from parsing.ast_walk.ast_nodes._my_ats_node import AssignmentNode, CallNode, ForLoopNode, FunctionDefinitionNode, IfBlockNode, SubroutineDefinitionNode, WriteStdoutNode
from parsing.ast_walk.my_ast_nodes import MyAstNode

_node_map = [
    (Assignment_Stmt, AssignmentNode),
    (Function_Subprogram, FunctionDefinitionNode),
    (Subroutine_Subprogram, SubroutineDefinitionNode),
    (Call_Stmt, CallNode),
    (Block_Nonlabel_Do_Construct, ForLoopNode),
    (If_Construct, IfBlockNode),
    (Write_Stmt, WriteStdoutNode),
    (Fortran8_If_Stmt, IfBlockNode),
]

_node_map_dict = {fnode: my_node for fnode, my_node in _node_map}

def wrap_node(fnode: Base) -> MyAstNode:
    return _node_map_dict[fnode.__class__](fnode)