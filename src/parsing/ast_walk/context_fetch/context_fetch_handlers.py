

from parsing.ast_walk.ast_nodes.expression_ast import DataRefNode, IntrinsicFunctionNode, LiteralNode, NameNode, OperatorNode, ParenthesisNode, ReferenceNode
from parsing.ast_walk.ast_nodes.my_ats_node import ProcedureDesignatorNode
from parsing.ast_walk.context_fetch.intrinsic_func import IntrinsicFunctionsDefinition
from parsing.ast_walk.dispatcher import Handler, Params
from parsing.definitions import Function, GenericFunctionDefinition, SymbolDefinition
from parsing.typing import PointerType, StructType

class ParenthesisContextFetcher(Handler[SymbolDefinition]):  
    def handle(self, node: ParenthesisNode, params: Params) -> SymbolDefinition:
        return self.dispatch(node=node.inner_expr, params=params)
    
class ReferenceContextFetcher(Handler[SymbolDefinition]):
    def handle(self, node: ReferenceNode | DataRefNode, params: Params) -> SymbolDefinition:
        symbol = self._get_node_type(node, params)
        return symbol    

class NameContextFetcher(Handler[SymbolDefinition]):
    def handle(self, node: NameNode, params: Params):
        symbol = params.context.get_symbol(node.ref_name)
        return symbol

class IntrinsicFunctionContextFetcher(Handler[SymbolDefinition]):
    intrinsic_map = {
        'real': IntrinsicFunctionsDefinition.get_real(),
        'exp': IntrinsicFunctionsDefinition.get_exp(),
        'maxval': IntrinsicFunctionsDefinition.get_maxval(),
        'minval': IntrinsicFunctionsDefinition.get_minval(),
    }

    def handle(self, node: IntrinsicFunctionNode, params: Params) -> SymbolDefinition:
        return self.intrinsic_map[node.function_name]

class StructReferenceSymbolFetcher(Handler[SymbolDefinition]):
    def handle(self, node: ProcedureDesignatorNode | DataRefNode, params: Params):
        variable_type: StructType = params.context.get_symbol(node.struct_variable_name).get_type()

        if isinstance(variable_type, PointerType):
            variable_type = variable_type.element_type

        if not isinstance(variable_type, StructType):
            raise ValueError(f"Procedure designator to non-struct type {variable_type}")
        
        return variable_type.get_property(node.property_name, params.module_dictionary)
