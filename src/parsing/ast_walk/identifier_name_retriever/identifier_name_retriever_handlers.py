

from parsing.ast_walk.ast_nodes.expression_ast import DataRefNode, IntrinsicFunctionNode, LiteralNode, NameNode, OperatorNode, ParenthesisNode, PartRefNode, ReferenceNode
from parsing.ast_walk.ast_nodes.my_ats_node import ProcedureDesignatorNode
from parsing.ast_walk.context_fetch.intrinsic_func import IntrinsicFunctionsDefinition
from parsing.ast_walk.dispatcher import Handler, Params
from parsing.definitions import Function, GenericFunctionDefinition, SymbolDefinition
from parsing.typing import PointerType, StructType

class ParenthesisIdentifierRetriever(Handler[str]):  
    def handle(self, node: ParenthesisNode, params: Params) -> SymbolDefinition:
        return self.dispatch(node=node.inner_expr, params=params)
    
class ReferenceIdentifierRetriever(Handler[str]):
    def handle(self, node: ReferenceNode, params: Params) -> SymbolDefinition:
        return node.ref_name

class NameIdentifierRetriever(Handler[str]):
    def handle(self, node: NameNode, params: Params):
        return node.ref_name

class PartRefIdentifierRetriever(Handler[str]):
    def handle(self, node: PartRefNode, params: Params):
        return node.ref_name