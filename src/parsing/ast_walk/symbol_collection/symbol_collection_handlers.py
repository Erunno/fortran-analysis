from parsing.ast_walk.ast_nodes.expression_ast import DataRefNode, IntrinsicFunctionNode, LiteralNode, NameNode, OperatorNode, ParenthesisNode, ReferenceNode, SubscriptTripletNode
from parsing.ast_walk.ast_nodes.expression_ast import DataRefNode, IntrinsicFunctionNode, LiteralNode, NameNode, OperatorNode, ParenthesisNode, PartRefNode, ReferenceNode
from parsing.ast_walk.ast_nodes.my_ats_node import AssignmentNode, CallNode, ForAllHeaderNode, ForAllTripletNode, ForLoopNode, FunctionDefinitionNode, IfBlockNode, LoopControlNode, ProcedureDesignatorNode, SubroutineDefinitionNode, WriteStdoutNode
from parsing.ast_walk.dispatcher import Dispatcher, Handler, Params
from parsing.ast_walk.context_fetch.context_fetch_dispatcher import symbol_fetch_dispatcher
from parsing.ast_walk.identifier_name_retriever.identifier_name_retriever_dispatcher import identifier_retrieve_dispatcher
from parsing.ast_walk.typing.typing_dispatcher import type_dispatcher
from parsing.ast_walk.symbol_collection.symbol_collection import SymbolCollection
from parsing.definitions import OperatorRedefinition
from parsing.typing import ArrayType, FortranType, PointerType, StructType


class _Helpers:
    @staticmethod
    def unpack_arr_ptr_type(type: FortranType) -> FortranType:
        return_type = type

        if isinstance(return_type, PointerType):
            return_type = type.element_type

        if isinstance(return_type, ArrayType):
            return_type = type.element_type

        return return_type

class FunctionDefinitionCollector(Handler[SymbolCollection]):
    def handle(self, node: FunctionDefinitionNode | SubroutineDefinitionNode, params: Params) -> SymbolCollection:
        collection = SymbolCollection()
        
        for i, stmt in enumerate(node.execution_part):
            print(f' [{i+1}/{len(node.execution_part)}]\r', end='')
            
            node_collection = self.dispatch(node=stmt, params=params)
            collection = collection.merge(node_collection)

        print('                                      \r', end='')

        return collection
    
class CallSubroutineCollector(Handler[SymbolCollection]):
    def handle(self, node: CallNode, params: Params) -> SymbolCollection:
        function_symbol_collection = self._collect_function_symbol(node=node, params=params)
        arguments_collection = self._collect_arguments(node=node, params=params)
        identifier_chain_collection = self.dispatch(node=node.get_call_identifier_fnode(), params=params)

        return function_symbol_collection.merge(arguments_collection).merge(identifier_chain_collection)
    
    def _collect_function_symbol(self, node: CallNode, params: Params) -> SymbolCollection:
        args_fnodes = node.get_argument_expression_fnodes()
        args_types = [type_dispatcher.dispatch(arg_fnode, params) for arg_fnode in args_fnodes]

        call_identifier_symbol = symbol_fetch_dispatcher.dispatch(
            node=node.get_call_identifier_fnode(), params=params)
        
        function_symbol = call_identifier_symbol.get_actual_function_symbol(args_types)
        
        return SymbolCollection().with_function_symbol(function_symbol)

    def _collect_arguments(self, node: CallNode, params: Params) -> SymbolCollection:
        args_fnodes = node.get_argument_expression_fnodes()
        args_collections = [self.dispatch(node=arg_fnode, params=params) for arg_fnode in args_fnodes]

        return SymbolCollection.merge_many(args_collections)

class ProcedureDesignatorCollector(Handler[SymbolCollection]):
    def handle(self, node: ProcedureDesignatorNode, params: Params) -> SymbolCollection:
        identifier_collection: SymbolCollection = self.dispatch(node=node.left_ref_fnode(), params=params)
        
        left_symbol = symbol_fetch_dispatcher.dispatch(node=node.left_ref_fnode(), params=params)
        left_symbol_type: StructType = _Helpers.unpack_arr_ptr_type(left_symbol.get_type())

        property_name = identifier_retrieve_dispatcher.dispatch(node=node.right_ref_fnode(), params=params)
        property_symbol = left_symbol_type.get_property(property_name, params.module_dictionary)

        return identifier_collection.with_symbol(left_symbol).with_property_symbol(property_symbol)

class IfBlockCollector(Handler[SymbolCollection]):
    def handle(self, node: IfBlockNode, params: Params) -> SymbolCollection:
        collection = SymbolCollection()

        for branch_stmts in node.branches:
            for branch_node in branch_stmts.execution_part:
                node_collection = self.dispatch(node=branch_node, params=params)
                collection = collection.merge(node_collection)

        return collection

class WriteStdoutCollector(Handler[SymbolCollection]):
    def handle(self, node: WriteStdoutNode, params: Params) -> SymbolCollection:
        return SymbolCollection()

class OperatorCollector(Handler[SymbolCollection]):
    def handle(self, node: OperatorNode, params: Params) -> SymbolCollection:
        op_function = self._get_operator_function(node=node, params=params)

        left_collection = self.dispatch(node=node.left_expr, params=params)        
        right_collection = self.dispatch(node=node.right_expr, params=params)

        result_collection = left_collection.merge(right_collection)
        return result_collection.with_function_symbol(op_function) if op_function else result_collection
    
    def _get_operator_function(self, node: OperatorNode, params: Params) -> SymbolCollection:
        l_type: FortranType = self.dispatch(node=node.left_expr, params=params)
        r_type: FortranType = self.dispatch(node=node.right_expr, params=params)

        return self._find_operator_function(node.operator_sign, l_type, r_type, params)
        
    def _find_operator_function(self, op_sign, l_type: FortranType, r_type: FortranType, params: Params) -> SymbolCollection:
        operators: list[OperatorRedefinition] = params.context.get_operator_symbols(op_sign)

        function_candidates = [op.get_function_symbol_for_types(l_type, r_type) \
                               for op in operators if op.defines_operator_for(l_type, r_type)]

        if len(function_candidates) > 1:
            raise ValueError(f"Multiple operator functions found for {op_sign} with types {l_type} and {r_type}")
        
        return function_candidates[0] if function_candidates else None
    
class AssignmentCollector(OperatorCollector):
    def handle(self, node: AssignmentNode , params: Params) -> SymbolCollection:
        assignment_operator_function = self._get_operator_function(node=node, params=params)

        target_collection = self.dispatch(node=node.target_fnode, params=params).as_write()
        source_collection = self.dispatch(node=node.source_fnode, params=params)

        result_collection = target_collection.merge(source_collection)
        return result_collection.with_function_symbol(assignment_operator_function) if assignment_operator_function else result_collection
    
    def _get_operator_function(self, node: AssignmentNode, params: Params) -> SymbolCollection:
        l_type: FortranType = self.dispatch(node=node.target_fnode, params=params)
        r_type: FortranType = self.dispatch(node=node.source_fnode, params=params)

        return self._find_operator_function(node.operator_sign, l_type, r_type, params)

class ParenthesisCollector(Handler[SymbolCollection]):  
    def handle(self, node: ParenthesisNode, params: Params) -> SymbolCollection:
        return self.dispatch(node=node.inner_expr, params=params)

class NameCollector(Handler[SymbolCollection]):
    def handle(self, node: NameNode, params: Params) -> SymbolCollection:
        symbol = symbol_fetch_dispatcher.dispatch(node=node, params=params)
        return SymbolCollection().with_symbol(symbol)

class IntrinsicFunctionCollector(Handler[SymbolCollection]):
    def handle(self, node: IntrinsicFunctionNode, params: Params) -> SymbolCollection:
        args_collections = [self.dispatch(node=call_arg, params=params) for call_arg in node.call_args_exprs]
        return SymbolCollection.merge_many(args_collections).with_intrinsic_function(node.function_name)

class LiteralCollector(Handler[SymbolCollection]):
    def handle(self, node: LiteralNode, params: Params) -> SymbolCollection:
        return SymbolCollection()

class DataRefCollector(Handler[SymbolCollection]):
    def handle(self, node: DataRefNode, params: Params) -> SymbolCollection:
        left_symbol = symbol_fetch_dispatcher.dispatch(node=node.get_left_node(), params=params)
        property_name = identifier_retrieve_dispatcher.dispatch(node=node.last_fnode, params=params)
        left_symbol_type = _Helpers.unpack_arr_ptr_type(left_symbol.get_type())
        property_symbol = left_symbol_type.get_property(property_name, params.module_dictionary)

        left_symbol_collection: SymbolCollection = self.dispatch(node=node.get_left_node(), params=params)

        return left_symbol_collection.with_symbol(left_symbol).with_property_symbol(property_symbol)
      
class PartRefCollector(Handler[SymbolCollection]):
    def handle(self, node: PartRefNode, params: Params) -> SymbolCollection:
        ref_name_collection = self.dispatch(node=node.ref_name_fnode(), params=params)
        args_collections = [self.dispatch(node=arg, params=params) for arg in node.args_fnodes()]

        x = SymbolCollection.merge_many(args_collections + [ref_name_collection])
        return x

class SubscriptTripleCollector(Handler[SymbolCollection]):
    def handle(self, node: SubscriptTripletNode, params: Params) -> SymbolCollection:
        lower_bound_collection = self.dispatch(node=node.lower_bound_fnode(), params=params)
        upper_bound_collection = self.dispatch(node=node.upper_bound_fnode(), params=params)
        stride_collection = self.dispatch(node=node.stride_fnode(), params=params) if node.stride_fnode() else SymbolCollection()

        return SymbolCollection.merge_many([lower_bound_collection, upper_bound_collection, stride_collection])

class ForLoopCollector(Handler[SymbolCollection]):
    def handle(self, node: ForLoopNode, params: Params) -> SymbolCollection:
        loop_control_collection = self._collect_loop_control(node=node, params=params)
        execution_part_collection = self._collect_execution_part(node=node, params=params)

        return loop_control_collection.merge(execution_part_collection)

    def _collect_loop_control(self, node: ForLoopNode, params: Params) -> SymbolCollection:
        return self.dispatch(node=node.do_control_fnode(), params=params)
    
    def _collect_execution_part(self, node: ForLoopNode, params: Params) -> SymbolCollection:
        collection = SymbolCollection()

        for stmt in node.execution_part:
            node_collection = self.dispatch(node=stmt, params=params)
            collection = collection.merge(node_collection)

        return collection


class LoopControlCollector(Handler[SymbolCollection]):
    def handle(self, node: LoopControlNode, params: Params) -> SymbolCollection:
        header = node.forall_header_fnode()
        if header:
            return self.dispatch(node=header, params=params)
        
        control, from_to_step = node.do_siple_do_fnodes()

        control_collection = self.dispatch(node=control, params=params)
        from_to_step_collections = [self.dispatch(node=n, params=params) for n in from_to_step]
        
        return SymbolCollection.merge_many([control_collection] + from_to_step_collections)

class ForAllHeaderCollector(Handler[SymbolCollection]):
    def handle(self, node: ForAllHeaderNode, params: Params) -> SymbolCollection:
        collections = [self.dispatch(node=triplet, params=params) for triplet in node.get_triplet_fnodes()]
        
        return SymbolCollection.merge_many(collections)
        
class ForAllTripletCollector(Handler[SymbolCollection]):
    def handle(self, node: ForAllTripletNode, params: Params) -> SymbolCollection:
        control_variable_collection = self.dispatch(node=node.control_variable_fnode(), params=params)
        lower_bound_collection = self.dispatch(node=node.lower_bound_fnode(), params=params)
        upper_bound_collection = self.dispatch(node=node.upper_fnode(), params=params)
        stride_collection = self.dispatch(node=node.stride_fnode(), params=params) if node.stride_fnode() else SymbolCollection()

        return SymbolCollection.merge_many([control_variable_collection, lower_bound_collection, upper_bound_collection, stride_collection])
        