from typing import Generic, TypeVar, Callable
from fparser.two.Fortran2003 import Base, Function_Stmt, Procedure_Stmt
from parsing.ast_walk.ast_nodes.my_ats_node import MyAstNode
from parsing.ast_walk.ast_nodes.wrapper import wrap_node
from parsing.definitions import GenericFunctionDefinition

class Params:
    def __init__(self, context, module_dictionary, call_stack: list[GenericFunctionDefinition]):
        self.context = context
        self.module_dictionary = module_dictionary
        self.call_stack = call_stack

    def extend(self, context, stack_frame: GenericFunctionDefinition):
        return Params(context, self.module_dictionary, self.call_stack + [stack_frame])
    
    def get_current_function(self):
        return self.call_stack[-1]

THandlerReturn = TypeVar('THandlerReturn')
class Handler[THandlerReturn]:
    def __init__(self):
        self.dispatch: Callable[[MyAstNode | Base, Params], THandlerReturn] = None

    def set_dispatch(self, dispatch: Callable[[MyAstNode | Base, Params], None]):
        self.dispatch = dispatch

    def handle(self, node: MyAstNode, params: Params) -> THandlerReturn:
        raise NotImplementedError(f"handle to be implemented by children classes")

TDispReturn = TypeVar('TDispReturn')
class Dispatcher[TDispReturn]:
    def __init__(self):
        self.handlers: list[Callable[[], Handler]] = {}

    def dispatch(self, node: MyAstNode | Base, params: Params) -> TDispReturn:
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

        print(f"\033[91m{msg}\033[0m")

        raise NotImplementedError(msg)
