

from parsing.ast_walk.ast_nodes.expression_ast import _Helpers, DataRefNode, IntrinsicFunctionNode, LiteralNode, NameNode, OperatorNode, ParenthesisNode, PartRefNode, ReferenceNode
from parsing.ast_walk.ast_nodes.my_ats_node import ProcedureDesignatorNode
from parsing.ast_walk.context_fetch.intrinsic_func import IntrinsicFunctionsDefinition
from parsing.ast_walk.dispatcher import Handler, Params
from parsing.definitions import Function, GenericFunctionDefinition, SymbolDefinition
from parsing.typing import ArrayType, PointerType, StructType
from parsing.ast_walk.identifier_name_retriever.identifier_name_retriever_dispatcher import identifier_retrieve_dispatcher

class ParenthesisContextFetcher(Handler[SymbolDefinition]):  
    def handle(self, node: ParenthesisNode, params: Params) -> SymbolDefinition:
        return self.dispatch(node=node.inner_expr, params=params)
    
class ReferenceContextFetcher(Handler[SymbolDefinition]):
    def handle(self, node: ReferenceNode, params: Params) -> SymbolDefinition:
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
        'int': IntrinsicFunctionsDefinition.get_int(),
        'mod': IntrinsicFunctionsDefinition.get_mod(),
        'trim': IntrinsicFunctionsDefinition.get_trim(),
        'log': IntrinsicFunctionsDefinition.get_log(),
        'max': IntrinsicFunctionsDefinition.get_max(),
        'sqrt': IntrinsicFunctionsDefinition.get_sqrt(),
        'abs': IntrinsicFunctionsDefinition.get_abs(),
        'any': IntrinsicFunctionsDefinition.get_any(),
        'all': IntrinsicFunctionsDefinition.get_all(),
        'sum': IntrinsicFunctionsDefinition.get_sum(),
    }

    def handle(self, node: IntrinsicFunctionNode, params: Params) -> SymbolDefinition:
        return self.intrinsic_map[node.function_name]

class StructReferenceSymbolFetcher(Handler[SymbolDefinition]):
    def handle(self, node: DataRefNode, params: Params):
        left_symbol = self.dispatch(node=node.get_left_node(), params=params)
        left_symbol_type: StructType = left_symbol.get_type()

        if isinstance(left_symbol_type, PointerType):
            left_symbol_type = left_symbol_type.element_type

        if isinstance(left_symbol_type, ArrayType) and not node.indexes_to_array_are_slices():
            left_symbol_type = left_symbol_type.element_type
        
        if not isinstance(left_symbol_type, StructType):
            raise ValueError(f"Procedure designator to non-struct type {left_symbol_type}")
        
        property_name = identifier_retrieve_dispatcher.dispatch(node=node.last_fnode, params=params)

        return left_symbol_type.get_property(property_name, params.module_dictionary)

class StructMethodCallContextFetcher(Handler[SymbolDefinition]):
    def handle(self, node: ProcedureDesignatorNode, params: Params):
        left_symbol = self.dispatch(node=node.left_ref_fnode(), params=params)
        left_symbol_type: StructType = left_symbol.get_type()

        if isinstance(left_symbol_type, PointerType):
            left_symbol_type = left_symbol_type.element_type

        if not isinstance(left_symbol_type, StructType):
            raise ValueError(f"Procedure designator to non-struct type {left_symbol_type}")
        
        return left_symbol_type.get_property(node.property_name, params.module_dictionary)
    
class PartRefContextFetcher(Handler[SymbolDefinition]):
    def handle(self, node: PartRefNode, params: Params):
        return params.context.get_symbol(node.ref_name)