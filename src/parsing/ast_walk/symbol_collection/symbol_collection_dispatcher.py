
from parsing.ast_walk.ast_nodes.expression_ast import ArraySectionNode, BoundsSpecListNode, BoundsSpecNode, ComponentSpecNode, DataPointerObjectNode, DataRefNode, FunctionReferenceNode, IntrinsicFunctionNode, LiteralNode, NameNode, OperatorNode, ParenthesisNode, PartRefNode, PointerAssignmentNode, StructureConstructorNode, SubscriptTripletNode, UnaryOperatorNode
from parsing.ast_walk.ast_nodes.my_ats_node import AllocOptNode, AllocateNode, AssignmentNode, CallNode, CaseConstructNode, ContinueStmtNode, CycleStmtNode, DeallocateNode, ExitStmtNode, ForAllHeaderNode, ForAllTripletNode, ForLoopNode, FunctionDefinitionNode, IfBlockNode, LoopControlNode, NullifyNode, ProcedureDesignatorNode, ReturnStmtNode, SubroutineDefinitionNode, WriteStdoutNode
from parsing.ast_walk.dispatcher import Dispatcher
from parsing.ast_walk.symbol_collection.symbol_collection import SymbolCollection
from parsing.ast_walk.symbol_collection.symbol_collection_handlers import AllocOptCollector, AllocateNodeCollector, ArraySectionCollector, AssignmentCollector, BoundsSpecCollector, BoundsSpecListCollector, CallSubroutineCollector, CaseConstructCollector, ComponentSpecCollector, \
    DataRefCollector, DeallocateNodeCollector, DoNothingCollector, ForAllHeaderCollector, ForAllTripletCollector, ForLoopCollector, FunctionDefinitionCollector, IfBlockCollector, \
    IntrinsicFunctionCollector, LoopControlCollector, NameCollector, NullifyCollector, OperatorCollector, ParenthesisCollector, PartRefCollector, \
    PointerAssignmentCollector, ProcedureDesignatorCollector, SubscriptTripleCollector, UnaryOperatorCollector, WriteStdoutCollector, \
    FunctionReferenceCollector

collectors_dispatcher = Dispatcher[SymbolCollection]()

collectors_dispatcher.register(DoNothingCollector).for_node(LiteralNode)
collectors_dispatcher.register(DoNothingCollector).for_node(ReturnStmtNode)
collectors_dispatcher.register(DoNothingCollector).for_node(ExitStmtNode)
collectors_dispatcher.register(DoNothingCollector).for_node(CycleStmtNode)
collectors_dispatcher.register(DoNothingCollector).for_node(ContinueStmtNode)

collectors_dispatcher.register(AssignmentCollector).for_node(AssignmentNode)
collectors_dispatcher.register(FunctionDefinitionCollector).for_node(FunctionDefinitionNode)
collectors_dispatcher.register(FunctionDefinitionCollector).for_node(SubroutineDefinitionNode)
collectors_dispatcher.register(CallSubroutineCollector).for_node(CallNode)
collectors_dispatcher.register(CallSubroutineCollector).for_node(StructureConstructorNode) # NOTE: This may need reimplementing
collectors_dispatcher.register(ForLoopCollector).for_node(ForLoopNode)
collectors_dispatcher.register(IfBlockCollector).for_node(IfBlockNode)
collectors_dispatcher.register(WriteStdoutCollector).for_node(WriteStdoutNode)
collectors_dispatcher.register(OperatorCollector).for_node(OperatorNode)
collectors_dispatcher.register(ParenthesisCollector).for_node(ParenthesisNode)
collectors_dispatcher.register(NameCollector).for_node(NameNode)
collectors_dispatcher.register(IntrinsicFunctionCollector).for_node(IntrinsicFunctionNode)
collectors_dispatcher.register(DataRefCollector).for_node(DataRefNode)
collectors_dispatcher.register(DataRefCollector).for_node(DataPointerObjectNode)
collectors_dispatcher.register(PartRefCollector).for_node(PartRefNode)
collectors_dispatcher.register(ProcedureDesignatorCollector).for_node(ProcedureDesignatorNode)
collectors_dispatcher.register(SubscriptTripleCollector).for_node(SubscriptTripletNode)
collectors_dispatcher.register(LoopControlCollector).for_node(LoopControlNode)
collectors_dispatcher.register(ForAllHeaderCollector).for_node(ForAllHeaderNode)
collectors_dispatcher.register(ForAllTripletCollector).for_node(ForAllTripletNode)
collectors_dispatcher.register(UnaryOperatorCollector).for_node(UnaryOperatorNode)
collectors_dispatcher.register(NullifyCollector).for_node(NullifyNode)
collectors_dispatcher.register(PointerAssignmentCollector).for_node(PointerAssignmentNode)
collectors_dispatcher.register(BoundsSpecListCollector).for_node(BoundsSpecListNode)
collectors_dispatcher.register(BoundsSpecCollector).for_node(BoundsSpecNode)
collectors_dispatcher.register(FunctionReferenceCollector).for_node(FunctionReferenceNode)
collectors_dispatcher.register(CaseConstructCollector).for_node(CaseConstructNode)
collectors_dispatcher.register(ArraySectionCollector).for_node(ArraySectionNode)
collectors_dispatcher.register(ComponentSpecCollector).for_node(ComponentSpecNode)
collectors_dispatcher.register(AllocateNodeCollector).for_node(AllocateNode)
collectors_dispatcher.register(DeallocateNodeCollector).for_node(DeallocateNode)
collectors_dispatcher.register(AllocOptCollector).for_node(AllocOptNode)
