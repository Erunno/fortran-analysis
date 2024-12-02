from parsing.ast_walk.ast_nodes.expression_ast import DataRefNode, IntrinsicFunctionNode, LiteralNode, NameNode, OperatorNode, ParenthesisNode, ReferenceNode
from parsing.ast_walk.ast_nodes.expression_ast import DataRefNode, IntrinsicFunctionNode, LiteralNode, NameNode, OperatorNode, ParenthesisNode, PartRefNode, ReferenceNode
from parsing.ast_walk.ast_nodes.my_ats_node import AssignmentNode, CallNode, ForLoopNode, FunctionDefinitionNode, IfBlockNode, SubroutineDefinitionNode, WriteStdoutNode
from parsing.ast_walk.dispatcher import Dispatcher, Handler, Params
from parsing.ast_walk.context_fetch.context_fetch_dispatcher import symbol_fetch_dispatcher
from parsing.ast_walk.identifier_name_retriever.identifier_name_retriever_dispatcher import identifier_retrieve_dispatcher
from parsing.ast_walk.typing.typing_dispatcher import type_dispatcher
from parsing.ast_walk.symbol_collection.symbol_collection import SymbolCollection
from parsing.definitions import OperatorRedefinition
from parsing.typing import FortranType



class FunctionDefinitionCollector(Handler[SymbolCollection]):
    def handle(self, node: FunctionDefinitionNode | SubroutineDefinitionNode, params: Params) -> SymbolCollection:
        collection = SymbolCollection()
        
        for stmt in node.execution_part:
            node_collection = self.dispatch(node=stmt, params=params)
            collection = collection.merge(node_collection)

        return collection
    
class CallSubroutineCollector(Handler[SymbolCollection]):
    def handle(self, node: CallNode, params: Params) -> SymbolCollection:
        function_symbol_collection = self._collect_function_symbol(node=node, params=params)
        arguments_collection = self._collect_arguments(node=node, params=params)

        return function_symbol_collection.merge(arguments_collection)
    
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

class ForLoopCollector(Handler[SymbolCollection]):
    def handle(self, node: ForLoopNode, params: Params) -> SymbolCollection:
        collection = SymbolCollection()

        for stmt in node.execution_part:
            node_collection = self.dispatch(node=stmt, params=params)
            collection = collection.merge(node_collection)

        return collection

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
        # TODO: Some data may be accessed from here ... maybe
        return SymbolCollection()

class OperatorCollector(Handler[SymbolCollection]):
    def handle(self, node: OperatorNode, params: Params) -> SymbolCollection:
        op_function = self._get_operator_function(node=node, params=params)

        left_collection = self.dispatch(node=node.left_expr, params=params)        
        right_collection = self.dispatch(node=node.right_expr, params=params)

        return left_collection.merge(right_collection).with_function_symbol(op_function)

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

        return target_collection.merge(source_collection).with_function_symbol(assignment_operator_function)

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

        left_symbol_collection = self.dispatch(node=node.get_left_node(), params=params)
        property_symbol = left_symbol.get_type().get_property(property_name, params.module_dictionary)

        return left_symbol_collection.with_property_symbol(property_symbol)
      
class PartRefCollector(Handler[SymbolCollection]):
    def handle(self, node: PartRefNode, params: Params) -> SymbolCollection:
        raise NotImplementedError("PartRefCollector not implemented")

 