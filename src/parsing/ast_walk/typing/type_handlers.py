

from parsing.ast_walk.ast_nodes.expression_ast import ArraySectionNode, ComponentSpecNode, DataRefNode, FunctionReferenceNode, IntrinsicFunctionNode, LiteralNode, NameNode, OperatorNode, ParenthesisNode, PartRefNode, ReferenceNode, UnaryOperatorNode
from parsing.ast_walk.ast_nodes.my_ats_node import ProcedureDesignatorNode
from parsing.ast_walk.dispatcher import Handler, Params
from parsing.definitions import Interface, OperatorRedefinition
from parsing.typing import ArrayType, FortranType, FunctionType, InterfaceType, PointerType, PrimitiveType, StructType
from parsing.ast_walk.context_fetch.context_fetch_dispatcher import symbol_fetch_dispatcher  

import re

class _TypeHelpers:
    @staticmethod
    def get_array_elem_type(arr_type: FortranType) -> FortranType:
        if isinstance(arr_type, PointerType):
            arr_type = arr_type.element_type

        if isinstance(arr_type, ArrayType):
            return arr_type.element_type
        
    @staticmethod
    def get_sliced_array(arr_type: FortranType, sliced_dims: list[int]) -> FortranType:
        if isinstance(arr_type, PointerType):
            return PointerType(_TypeHelpers.get_sliced_array(arr_type.element_type, sliced_dims))

        if isinstance(arr_type, ArrayType):
            new_dims = []
            for dim, dim_size in enumerate(arr_type.dimensions):
                if dim in sliced_dims:
                    new_dims.append(dim_size)


            return ArrayType(
                arr_type.element_type,
                new_dims)
        
        if PrimitiveType.is_string(arr_type):
            # TODO: make the length sliced
            return arr_type

class OperatorTyper(Handler[FortranType]):
    def handle(self, node: OperatorNode, params: Params) -> FortranType:
        operators: list[OperatorRedefinition] = params.context.get_operator_symbols(node.operator_sign())

        l_type: FortranType = self.dispatch(node=node.left_fnode(), params=params)
        r_type: FortranType = self.dispatch(node=node.right_fnode(), params=params)

        for op in operators:
            if op.defines_operator_for(l_type, r_type):
                function_symbol = op.get_function_symbol_for_types(l_type, r_type)
                return function_symbol.get_type().return_type

        # TODO: implement default operators (like + on ints etc) ... this unification may fail ??
        # NOTE: some operators have been implemented in the `default_operators.py` file
        return l_type.get_unified_with(r_type)
    
class UnaryOperatorTyper(Handler[FortranType]):
    def handle(self, node: UnaryOperatorNode, params: Params) -> FortranType:
        # TODO: maybe unary ops can be overloaded too?
        return self.dispatch(node=node.expr_fnode(), params=params)

class ParenthesisTyper(Handler[FortranType]):  
    def handle(self, node: ParenthesisNode, params: Params) -> FortranType:
        return self.dispatch(node=node.inner_expr, params=params)

class ReferenceTyper(Handler[FortranType]):
    def handle(self, node: ReferenceNode | DataRefNode | PartRefNode, params: Params) -> FortranType:
        symbol_type = self._get_node_type(node, params)

        if isinstance(symbol_type, FunctionType):
            return symbol_type.return_type
        
        if isinstance(symbol_type, InterfaceType):
            return self._handle_interface_type(node, params)

        arr_elem_type = _TypeHelpers.get_array_elem_type(symbol_type)
        if arr_elem_type:
            if node.is_reference_without_indexing():
                return symbol_type
            
            if node.indexes_to_array_are_slices():
                sliced_dims = node.get_sliced_dimensions()
                return _TypeHelpers.get_sliced_array(symbol_type, sliced_dims) 
            
            return arr_elem_type
        
        return symbol_type
    
    def _get_node_type(self, node: ReferenceNode, params: Params) -> FortranType:
        symbol = symbol_fetch_dispatcher.dispatch(node=node, params=params)
        return symbol.get_type()
    
    def _handle_interface_type(self, node: ReferenceNode | DataRefNode | PartRefNode, params: Params) -> FortranType:
        call_arg_types = [self.dispatch(node=arg, params=params) for arg in node.args_fnodes()]

        interface_symbol: Interface = symbol_fetch_dispatcher.dispatch(node=node, params=params)
        function_symbol = interface_symbol.get_actual_function_symbol(call_arg_types)

        return function_symbol.get_type().return_type

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

        elif val.lower() == '.true.' or val.lower() == '.false.':
            return_type = PrimitiveType.get_logical_instance()

        elif re.match(r"^'.'$", val):
            return_type = PrimitiveType.get_character_instance()
            
        elif re.match(r"^'.*'$", val):
            return_type = PrimitiveType.get_string_instance()

        elif re.match(r'^-?\d*\.\d*', val):
            return_type = PrimitiveType.get_real_instance().with_any_kind()

        elif re.match(r'^-?\d*\.[eE]\d+$', val):
            return_type = PrimitiveType.get_real_instance().with_any_kind()

        elif re.match(r'^-?\d*[eE]-?\d+$', val):
            return_type = PrimitiveType.get_real_instance().with_any_kind()

        else:
            raise ValueError(f"Unknown literal type for value {node.value}")

        if node.kind:
            return_type.add_attribute('kind', node.kind)

        return return_type

class DataRefTyper(ReferenceTyper):
    pass

class PartRefTyper(ReferenceTyper):
    pass

class FunctionReferenceTyper(Handler[FortranType]):
    def handle(self, node: FunctionReferenceNode, params: Params) -> FortranType:
        return self.dispatch(node=node.function_expr_fnode(), params=params)

class ProcedureDesignatorTyper(Handler[FortranType]):
    def handle(self, node: ProcedureDesignatorNode, params: Params) -> FortranType:
        function_symbol = symbol_fetch_dispatcher.dispatch(node=node, params=params)
        return function_symbol.get_type().return_type
    
class ArraySectionTyper(Handler[FortranType]):
    def handle(self, node: ArraySectionNode, params: Params) -> FortranType:
        arr_type = self.dispatch(node=node.array_fnode(), params=params)
        return _TypeHelpers.get_sliced_array(arr_type, node.get_sliced_dimensions())
    
class ComponentSpecTyper(Handler[FortranType]):
    def handle(self, node: ComponentSpecNode, params: Params) -> FortranType:
        return self.dispatch(node=node.component_expr_fnode(), params=params)