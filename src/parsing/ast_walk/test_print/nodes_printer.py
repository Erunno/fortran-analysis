from parsing.ast_walk.ast_nodes.expression_ast import DataRefNode, IntrinsicFunctionNode, LiteralNode, NameNode, OperatorNode, ParenthesisNode, ReferenceNode
from parsing.ast_walk.ast_nodes.my_ats_node import AssignmentNode, CallNode, ForLoopNode, FunctionDefinitionNode, IfBlockNode, SubroutineDefinitionNode, WriteStdoutNode
from parsing.ast_walk.dispatcher import Handler, Params
from parsing.ast_walk.typing.typing_dispatcher import type_dispatcher
from parsing.context import SubroutineFunctionContext

class AssignmentPrinter(Handler):
    def handle(self, node: AssignmentNode , params: Params):
        print(f"Assignment Node: <{node.fnode}>")
        target_t = type_dispatcher.dispatch(node.target_fnode, params=params)
        source_t = type_dispatcher.dispatch(node.source_fnode, params=params)

        if not target_t or not target_t.is_equivalent(source_t):
            print(f"\033[91mType mismatch in assignment: {target_t} != {source_t}\033[0m")

        print(f"Target of a type: {target_t}")
        self.dispatch(node=node.target_fnode, params=params)

        print(f"Source of a type: {source_t}")
        self.dispatch(node=node.source_fnode, params=params)
        pass

class FunctionDefinitionPrinter(Handler):
    def handle(self, node: FunctionDefinitionNode | SubroutineDefinitionNode, params: Params):
        print(f"Function Definition Node: <{params.get_current_function()}>")

        for stmt in node.execution_part:
            self.dispatch(node=stmt, params=params)

class CallSubroutinePrinter(Handler):
    def handle(self, node: CallNode, params: Params):
        print(f"Called: <{node.called_function_name}>")
        
class ForLoopPrinter(Handler):
    def handle(self, node: ForLoopNode, params: Params):
        print ("For Loop started")
        
        for stmt in node.execution_part:
            self.dispatch(node=stmt, params=params)

        print(f"For Loop ended")

class IfBlockPrinter(Handler):
    def handle(self, node: IfBlockNode, params: Params):
        print ("If Block started")
        
        for branch in node.branches:
            print (' -- Branch started, is else branch:', branch.is_else_brach)
            
            branch_stmts = branch.execution_part
            
            for stmt in branch_stmts:
                self.dispatch(node=stmt, params=params)
        
        print(f"If Block ended")

class WriteStdoutPrinter(Handler):
    def handle(self, node: WriteStdoutNode, params: Params):
        print(f"Write to stdout Node")

class OperatorPrinter(Handler):
    def handle(self, node: OperatorNode, params: Params):

        print("Operator Node started")
        self.dispatch(node=node.left_expr, params=params)
        
        print(f"Op Sign: <{node.operator_sign}>")

        self.dispatch(node=node.right_expr, params=params)
        print("Operator Node ended")

class ParenthesisPrinter(Handler):  
    def handle(self, node: ParenthesisNode, params: Params):
        print("Parenthesis Node started")
        self.dispatch(node=node.inner_expr, params=params)
        print("Parenthesis Node ended")

class ReferencePrinter(Handler):
    def handle(self, node: ReferenceNode, params: Params):
        symbol = params.context.get_symbol(node.ref_name)
        print(f"Reference Node: referencing <{symbol}> of type {symbol.get_type()}")

class NamePrinter(Handler):
    def handle(self, node: NameNode, params: Params):
        print(f"Name Node: referencing <{node.ref_name}>")


class IntrinsicFunctionPrinter(Handler):
    def handle(self, node: IntrinsicFunctionNode, params: Params):
        print(f"Intrinsic Function Node: <{node.function_name}>")

        for call_arg in node.call_args_exprs:
            self.dispatch(node=call_arg, params=params)

class LiteralPrinter(Handler):
    def handle(self, node: LiteralNode, params: Params):
        print(f"Literal Node: <{node.value}>")

class DataRefPrinter(Handler):
    def handle(self, node: DataRefNode, params: Params):
        print(f"Data Ref Node: <{node.object_name}>%<{node.property_name}>")
