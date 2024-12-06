from parsing.ast_walk.dispatcher import Dispatcher
from parsing.ast_walk.typing.type_handlers import ArraySectionTyper, ComponentSpecTyper, DataRefTyper, IntrinsicFunctionTyper, LiteralTyper, NameTyper, OperatorTyper, ParenthesisTyper, PartRefTyper, ProcedureDesignatorTyper, \
    ReferenceTyper, UnaryOperatorTyper, FunctionReferenceTyper
from parsing.typing import FortranType
from parsing.ast_walk.ast_nodes.expression_ast import ArraySectionNode, ComponentSpecNode, DataRefNode, FunctionReferenceNode, IntrinsicFunctionNode, LiteralNode, NameNode, OperatorNode, ParenthesisNode, PartRefNode, ReferenceNode, UnaryOperatorNode
from parsing.ast_walk.ast_nodes.my_ats_node import AssignmentNode, CallNode, ForLoopNode, FunctionDefinitionNode, IfBlockNode, ProcedureDesignatorNode, SubroutineDefinitionNode, WriteStdoutNode

type_dispatcher = Dispatcher[FortranType]()

type_dispatcher.register(OperatorTyper).for_node(OperatorNode)
type_dispatcher.register(ParenthesisTyper).for_node(ParenthesisNode)
type_dispatcher.register(ReferenceTyper).for_node(ReferenceNode)
type_dispatcher.register(NameTyper).for_node(NameNode)
type_dispatcher.register(IntrinsicFunctionTyper).for_node(IntrinsicFunctionNode)
type_dispatcher.register(LiteralTyper).for_node(LiteralNode)
type_dispatcher.register(DataRefTyper).for_node(DataRefNode)
type_dispatcher.register(PartRefTyper).for_node(PartRefNode)
type_dispatcher.register(UnaryOperatorTyper).for_node(UnaryOperatorNode)
type_dispatcher.register(FunctionReferenceTyper).for_node(FunctionReferenceNode)
type_dispatcher.register(ProcedureDesignatorTyper).for_node(ProcedureDesignatorNode)
type_dispatcher.register(ArraySectionTyper).for_node(ArraySectionNode)
type_dispatcher.register(ComponentSpecTyper).for_node(ComponentSpecNode)
