from typing import Generic, TypeVar, Callable
from fparser.two.Fortran2003 import Base, Function_Stmt, Procedure_Stmt
from parsing.ast_walk.ast_nodes.wrapper import wrap_node
from parsing.ast_walk.my_ast_nodes import MyAstNode

class Params:
    def __init__(self):
        pass

class Handler:
    def __init__(self):
        self.dispatch: Callable[[MyAstNode | Base, Params], None] = None

    def set_dispatch(self, dispatch: Callable[[MyAstNode | Base, Params], None]):
        self.dispatch = dispatch

    def handle(self, node: MyAstNode, params: Params):
        raise NotImplementedError(f"handle to be implemented by children classes")
    
class Dispatcher:
    def __init__(self):
        self.handlers: list[Callable[[], Handler]] = {}

    def dispatch(self, node: MyAstNode | Base, params: Params):
        if not isinstance(node, MyAstNode):
            node = wrap_node(node)

        handler_builder = self.handlers.get(node.__class__, None)

        if handler_builder is None:
            return self.handler_not_found(node, params)
        
        handler = handler_builder()
        handler.set_dispatch(self.dispatch)
        
        return handler.handle(node, params)

    def register(self, handler_builder: Callable[[], Handler]):
        class For:
            def __init__(self, handlers):
                self.handlers = handlers

            def for_node(self, node_class):
                self.handlers[node_class] = handler_builder
                return self
            
        return For(self.handlers)

    def handler_not_found(self, node, params):
        msg = f"handler for node {node} not implemented"

        print(msg)

        # raise NotImplementedError(msg)
