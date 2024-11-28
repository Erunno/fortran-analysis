

from parsing.ast_walk.ast_nodes.expression_ast import DataRefNode, IntrinsicFunctionNode, LiteralNode, NameNode, OperatorNode, ParenthesisNode, ReferenceNode
from parsing.ast_walk.dispatcher import Handler, Params
from parsing.typing import ArrayType, FortranType, FunctionType, PointerType, PrimitiveType, StructType
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

        l_type: FortranType = self.dispatch(node=node.left_expr, params=params)
        r_type: FortranType = self.dispatch(node=node.right_expr, params=params)

        return l_type.get_unified_with(r_type)

class ParenthesisTyper(Handler[FortranType]):  
    def handle(self, node: ParenthesisNode, params: Params) -> FortranType:
        return self.dispatch(node=node.inner_expr, params=params)

class ReferenceTyper(Handler[FortranType]):
    def handle(self, node: ReferenceNode | DataRefNode, params: Params) -> FortranType:
        symbol_type = self._get_node_type(node, params)

        if isinstance(symbol_type, FunctionType):
            return symbol_type.return_type
        
        # TODO interfaces

        arr_elem_type = _TypeHelpers.get_array_elem_type(symbol_type)
        if arr_elem_type:
            if node.indexes_to_array_are_slices():
                return symbol_type
            
            return arr_elem_type
        
        raise ValueError(f"Undefined reference for {symbol_type} for fnode {node.fnode}")
    
    def _get_node_type(self, node: ReferenceNode, params: Params) -> FortranType:
        symbol = params.context.get_symbol(node.ref_name)
        return symbol.get_type()
        

class NameTyper(Handler[FortranType]):
    def handle(self, node: NameNode, params: Params):
        symbol = params.context.get_symbol(node.ref_name)
        return symbol.get_type()

class IntrinsicFunctionTyper(Handler[FortranType]):

    def handle(self, node: IntrinsicFunctionNode, params: Params) -> FortranType:
        function_parser = self._get_return_type_parser(node.function_name)

        if not function_parser:
            raise ValueError(f"Undefined intrinsic function {node.function_name}")       
        
        return function_parser(node, params)
    
    def _get_real_ret_type(self, node: IntrinsicFunctionNode, _):
        real = PrimitiveType.get_real_instance()
        
        if len(node.call_args_exprs) > 1:
            kind = node.call_args_exprs[1].tostr().lower()
            real.add_attribute('kind', kind) 
        
        return real

    def _get_exp_ret_type(self, node: IntrinsicFunctionNode, params: Params):
        return self.dispatch(node=node.call_args_exprs[0], params=params)
    
    def _get_minmax_ret_type(self, node: IntrinsicFunctionNode, params: Params):
        inner_type = self.dispatch(node=node.call_args_exprs[0], params=params)
        
        arr_elem_type = _TypeHelpers.get_array_elem_type(inner_type)
        if arr_elem_type:
            return arr_elem_type
        
        raise ValueError(f"Undefined type for min/max function {inner_type}")

    def _get_return_type_parser(self, name):
        return {
            'real': self._get_real_ret_type,
            'exp': self._get_exp_ret_type,
            'maxval': self._get_minmax_ret_type,
            'minval': self._get_minmax_ret_type,
        }.get(name, None)


class LiteralTyper(Handler[FortranType]):
    def handle(self, node: LiteralNode, params: Params) -> FortranType:
        val = node.value.strip()
        return_type = None

        if re.match(r'^-?\d+$', val):
            return_type = PrimitiveType.get_integer_instance()
            return_type.add_attribute('kind', 'defaultLiteralKind')
        elif re.match(r'^-?\d*\.\d+', val):
            return_type = PrimitiveType.get_real_instance()

        elif re.match(r'^"."$', val):
            return_type = PrimitiveType.get_character_instance()

        else:
            raise ValueError(f"Unknown literal type for value {node.value}")

        if node.kind:
            return_type.add_attribute('kind', node.kind)

        return return_type

                

class DataRefTyper(ReferenceTyper):
    def _get_node_type(self, node: DataRefNode, params: Params):
        struct_type: StructType = params.context.get_symbol(node.object_name).get_type()
        
        if not isinstance(struct_type, StructType):
            raise ValueError(f"Data reference to non-struct type {struct_type}")
        
        struct_property_symbol = struct_type.get_property(node.property_name, params.module_dictionary)
        return struct_property_symbol.get_type()
    