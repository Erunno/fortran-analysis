from typing import Generic, TypeVar
from fparser.two.Fortran2003 import Base, Function_Stmt, Procedure_Stmt

T = TypeVar('T', bound=Base)

class MyAstNode(Generic[T]):
    def __init__(self, fnode: T):
        self.fnode = fnode

    def key(self):
        return self.__class__.__name__

class FunctionCallNode(MyAstNode[Function_Stmt]):
    def __init__(self, fnode: Function_Stmt):
        super().__init__(fnode)

class ProcedureCallNode(MyAstNode[Procedure_Stmt]):
    def __init__(self, fnode: Procedure_Stmt):
        super().__init__(fnode)

