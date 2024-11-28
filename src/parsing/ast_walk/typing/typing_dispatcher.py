from parsing.ast_walk.dispatcher import Dispatcher
from parsing.ast_walk.typing.type_handlers import DataRefTyper, IntrinsicFunctionTyper, LiteralTyper, NameTyper, OperatorTyper, ParenthesisTyper, ReferenceTyper
from parsing.typing import FortranType
from parsing.ast_walk.ast_nodes.expression_ast import DataRefNode, IntrinsicFunctionNode, LiteralNode, NameNode, OperatorNode, ParenthesisNode, ReferenceNode
from parsing.ast_walk.ast_nodes.my_ats_node import AssignmentNode, CallNode, ForLoopNode, FunctionDefinitionNode, IfBlockNode, SubroutineDefinitionNode, WriteStdoutNode

type_dispatcher = Dispatcher[FortranType]()

type_dispatcher.register(OperatorTyper).for_node(OperatorNode)
type_dispatcher.register(ParenthesisTyper).for_node(ParenthesisNode)
type_dispatcher.register(ReferenceTyper).for_node(ReferenceNode)
type_dispatcher.register(NameTyper).for_node(NameNode)
type_dispatcher.register(IntrinsicFunctionTyper).for_node(IntrinsicFunctionNode)
type_dispatcher.register(LiteralTyper).for_node(LiteralNode)
type_dispatcher.register(DataRefTyper).for_node(DataRefNode)