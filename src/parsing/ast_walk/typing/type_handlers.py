

from parsing.ast_walk.ast_nodes.expression_ast import DataRefNode, IntrinsicFunctionNode, LiteralNode, NameNode, OperatorNode, ParenthesisNode, ReferenceNode
from parsing.ast_walk.dispatcher import Handler, Params
from parsing.typing import FortranType


class OperatorTyper(Handler[FortranType]):
    def handle(self, node: OperatorNode, params: Params) -> FortranType:

        print("Operator Node started")
        self.dispatch(node=node.left_expr, params=params)
        
        print(f"Op Sign: <{node.operator_sign}>")

        self.dispatch(node=node.right_expr, params=params)
        print("Operator Node ended")

class ParenthesisTyper(Handler[FortranType]):  
    def handle(self, node: ParenthesisNode, params: Params) -> FortranType:
        print("Parenthesis Node started")
        self.dispatch(node=node.inner_expr, params=params)
        print("Parenthesis Node ended")

class ReferenceTyper(Handler[FortranType]):
    def handle(self, node: ReferenceNode, params: Params) -> FortranType:
        print(f"Reference Node: referencing <{node.ref_name}>")

class NameTyper(Handler[FortranType]):
    def handle(self, node: NameNode, params: Params):
        print(f"Name Node: referencing <{node.ref_name}>")

class IntrinsicFunctionTyper(Handler[FortranType]):
    def handle(self, node: IntrinsicFunctionNode, params: Params) -> FortranType:
        print(f"Intrinsic Function Node: <{node.function_name}>")

        for call_arg in node.call_args_exprs:
            self.dispatch(node=call_arg, params=params)

class LiteralTyper(Handler[FortranType]):
    def handle(self, node: LiteralNode, params: Params) -> FortranType:
        print(f"Literal Node: <{node.value}>")

class DataRefTyper(Handler[FortranType]):
    def handle(self, node: DataRefNode, params: Params) -> FortranType:
        print(f"Data Ref Node: <{node.object_name}>%<{node.property_name}>")
