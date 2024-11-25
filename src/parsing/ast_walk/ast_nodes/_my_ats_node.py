from typing import Generic, TypeVar
from fparser.two.Fortran2003 import Base, Program, Assignment_Stmt, Subroutine_Stmt, Function_Stmt, Subroutine_Subprogram, Function_Subprogram, \
                                    Execution_Part, StmtBase, Call_Stmt, Name, If_Construct, Else_Stmt, Else_If_Stmt, Write_Stmt, End_If_Stmt
from fparser.two.Fortran2008.block_nonlabel_do_construct_r814_2 import Block_Nonlabel_Do_Construct

from parsing.find_in_tree import find_in_node, find_in_tree

T = TypeVar('T', bound=Base)

class MyAstNode(Generic[T]):
    def __init__(self, fnode: T):
        self.fnode = fnode

class AssignmentNode(MyAstNode[Assignment_Stmt]):
    def __init__(self, fnode: Assignment_Stmt):
        super().__init__(fnode)

FunSub = TypeVar('FunSub', Subroutine_Subprogram, Function_Subprogram)
class FuncSubBaseNode(MyAstNode[FunSub]):
    def __init__(self, fnode: Subroutine_Subprogram | Function_Subprogram):
        super().__init__(fnode)
        self.execution_part: list[StmtBase] = find_in_node(fnode, Execution_Part).children

class SubroutineDefinitionNode(FuncSubBaseNode[Subroutine_Subprogram]):
    def __init__(self, fnode: Subroutine_Subprogram):
        super().__init__(fnode)
    
class FunctionDefinitionNode(MyAstNode[Function_Subprogram]):
    def __init__(self, fnode: Function_Subprogram):
        super().__init__(fnode)
        
class CallNode(MyAstNode[Call_Stmt]):
    def __init__(self, fnode: Call_Stmt):
        super().__init__(fnode)

        self.called_function_name = fnode.children[0].tostr()
   
class ForLoopNode(MyAstNode[Block_Nonlabel_Do_Construct]):
    def __init__(self, fnode: Block_Nonlabel_Do_Construct):
        super().__init__(fnode)

        self.execution_part = fnode.children[1:-1]

class IfExecutionBranch:
    def __init__(self, fnode_condition: If_Construct):
        self.fnode = fnode_condition
        self.is_else_brach = isinstance(fnode_condition, Else_Stmt)
        
        self.execution_part: list[StmtBase] = []

    def add_stmt(self, stmt: StmtBase):
        self.execution_part.append(stmt)

class IfBlockNode(MyAstNode[If_Construct]):

    def __init__(self, fnode: If_Construct):
        super().__init__(fnode)
        
        self.branches: list[IfExecutionBranch] = [
            IfExecutionBranch(fnode.children[0])
        ]

        for stmt in fnode.children[1:]:
            if isinstance(stmt, Else_Stmt) or isinstance(stmt, Else_If_Stmt):
                self.branches.append(IfExecutionBranch(stmt))
                continue

            if isinstance(stmt, End_If_Stmt):
                continue

            self.branches[-1].add_stmt(stmt)
        
class WriteStdoutNode(MyAstNode[Write_Stmt]):
    def __init__(self, fnode: Write_Stmt):
        super().__init__(fnode)
        