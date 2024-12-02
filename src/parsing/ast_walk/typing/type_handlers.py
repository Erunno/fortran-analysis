

from parsing.ast_walk.ast_nodes.expression_ast import DataRefNode, IntrinsicFunctionNode, LiteralNode, NameNode, OperatorNode, ParenthesisNode, PartRefNode, ReferenceNode
from parsing.ast_walk.dispatcher import Handler, Params
from parsing.definitions import OperatorRedefinition
from parsing.typing import ArrayType, FortranType, FunctionType, PointerType, PrimitiveType, StructType
from parsing.ast_walk.context_fetch.context_fetch_dispatcher import symbol_fetch_dispatcher  

import re

class _TypeHelpers:
    @staticmethod
    def get_array_elem_type(arr_type: FortranType) -> FortranType:
        if isinstance(arr_type, PointerType):
            arr_type = arr_type.element_type

        if isinstance(arr_type, ArrayType):
            return arr_type.element_type

class OperatorTyper(Handler[FortranType]):
    def handle(self, node: OperatorNode, params: Params) -> FortranType:

        operators: list[OperatorRedefinition] = params.context.get_operator_symbols(node.operator_sign)

        l_type: FortranType = self.dispatch(node=node.left_expr, params=params)
        r_type: FortranType = self.dispatch(node=node.right_expr, params=params)

        for op in  operators:
            if op.defines_operator_for(l_type, r_type):
                function_symbol = op.get_function_symbol_for_types(l_type, r_type)

                print(f"\033[94mOperator {node.operator_sign} with types {l_type} and {r_type} is {function_symbol}\033[0m")
                
                return function_symbol.get_type().return_type

        # TODO: implement default operators (like + on ints etc) ... this unification may fail ??
        return l_type.get_unified_with(r_type)

class ParenthesisTyper(Handler[FortranType]):  
    def handle(self, node: ParenthesisNode, params: Params) -> FortranType:
        return self.dispatch(node=node.inner_expr, params=params)

class ReferenceTyper(Handler[FortranType]):
    def handle(self, node: ReferenceNode | DataRefNode | PartRefNode, params: Params) -> FortranType:
        symbol_type = self._get_node_type(node, params)

        if isinstance(symbol_type, FunctionType):
            return symbol_type.return_type
        
        # TODO interfaces

        arr_elem_type = _TypeHelpers.get_array_elem_type(symbol_type)
        if arr_elem_type:
            if node.indexes_to_array_are_slices():
                return symbol_type
            
            return arr_elem_type
        
        return symbol_type
    
    def _get_node_type(self, node: ReferenceNode, params: Params) -> FortranType:
        symbol = params.context.get_symbol(node.ref_name)
        return symbol.get_type()
        

class NameTyper(Handler[FortranType]):
    def handle(self, node: NameNode, params: Params):
        symbol = params.context.get_symbol(node.ref_name)
        return symbol.get_type()

class IntrinsicFunctionTyper(Handler[FortranType]):
    def handle(self, node: IntrinsicFunctionNode, params: Params) -> FortranType:
        function_symbol = symbol_fetch_dispatcher.dispatch(node=node, params=params)
        return function_symbol.get_type().return_type


class LiteralTyper(Handler[FortranType]):
    def handle(self, node: LiteralNode, params: Params) -> FortranType:
        val = node.value.strip()
        return_type = None

        if re.match(r'^-?\d+$', val):
            return_type = PrimitiveType.get_integer_instance()
            return_type.add_attribute('kind', PrimitiveType.default_int_kind())

        elif re.match(r'^-?\d*\.\d+', val):
            return_type = PrimitiveType.get_real_instance()

        elif re.match(r"^'.'$", val):
            return_type = PrimitiveType.get_character_instance()
            
        elif re.match(r"^'.*'$", val):
            return_type = PrimitiveType.get_string_instance()

        elif val.lower() == '.true.' or val.lower() == '.false.':
            return_type = PrimitiveType.get_logical_instance()

        else:
            raise ValueError(f"Unknown literal type for value {node.value}")

        if node.kind:
            return_type.add_attribute('kind', node.kind)

        return return_type


class DataRefTyper(ReferenceTyper):
    def _get_node_type(self, node: DataRefNode, params: Params):
        symbol = symbol_fetch_dispatcher.dispatch(node=node, params=params)
        return symbol.get_type()
    
class PartRefTyper(ReferenceTyper):
    def _get_node_type(self, node: PartRefNode, params: Params):
        symbol = symbol_fetch_dispatcher.dispatch(node=node, params=params)
        return symbol.get_type()