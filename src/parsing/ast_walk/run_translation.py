from parsing.ast_walk.ast_nodes.expression_ast import DataRefNode, IntrinsicFunctionNode, LiteralNode, NameNode, OperatorNode, ParenthesisNode, ReferenceNode
from parsing.ast_walk.ast_nodes.my_ats_node import AssignmentNode, CallNode, ForLoopNode, FunctionDefinitionNode, IfBlockNode, SubroutineDefinitionNode, WriteStdoutNode
from parsing.ast_walk.dispatcher import Dispatcher, Params
from parsing.ast_walk.test_print.nodes_printer import AssignmentPrinter, CallSubroutinePrinter, ForLoopPrinter, FunctionDefinitionPrinter, IfBlockPrinter, \
    IntrinsicFunctionPrinter, NamePrinter, OperatorPrinter, ParenthesisPrinter, ReferencePrinter, WriteStdoutPrinter, LiteralPrinter, DataRefPrinter
from parsing.context import SubroutineFunctionContext
from parsing.definitions import GenericFunctionDefinition
from parsing.module_dictionary import ModuleDictionary

ast_printer_dispatcher = Dispatcher[None]()
ast_printer_dispatcher.register(AssignmentPrinter).for_node(AssignmentNode)
ast_printer_dispatcher.register(FunctionDefinitionPrinter).for_node(FunctionDefinitionNode).for_node(SubroutineDefinitionNode)
ast_printer_dispatcher.register(ForLoopPrinter).for_node(ForLoopNode)
ast_printer_dispatcher.register(CallSubroutinePrinter).for_node(CallNode)
ast_printer_dispatcher.register(IfBlockPrinter).for_node(IfBlockNode)
ast_printer_dispatcher.register(WriteStdoutPrinter).for_node(WriteStdoutNode)
ast_printer_dispatcher.register(OperatorPrinter).for_node(OperatorNode)
ast_printer_dispatcher.register(ParenthesisPrinter).for_node(ParenthesisNode)
ast_printer_dispatcher.register(ReferencePrinter).for_node(ReferenceNode)
ast_printer_dispatcher.register(NamePrinter).for_node(NameNode)
ast_printer_dispatcher.register(IntrinsicFunctionPrinter).for_node(IntrinsicFunctionNode)
ast_printer_dispatcher.register(LiteralPrinter).for_node(LiteralNode)
ast_printer_dispatcher.register(DataRefPrinter).for_node(DataRefNode)

def run_translation(
        module_dict: ModuleDictionary,
        module_name, function_name
):

    module = module_dict.get_module(module_name)
    module_context = module.module_context

    function_symbol: GenericFunctionDefinition = module.module_local_context.get_symbol(function_name)
    function_fnode = function_symbol.fparser_node
    
    function_local_context = function_symbol.get_local_context()
    full_context_within_function = module_context.get_expanded(function_local_context)

    # variable = function_local_context.get_symbol('dtsound')
    # print(variable)

    # moloch_type = function_symbol.get_type()
    # print('moloch type: ', moloch_type)

    # psf = module_context.get_symbol('pfwsat')
    # print(psf)
    # print('pfwsat type: ', psf.get_type())

    # subroutine = module_context.get_symbol('getmem1d_t')
    # print(subroutine)
    # print('getmem1d_t type: ', subroutine.get_type())
    # exit()
    
    base_params = Params(context=full_context_within_function, 
                         module_dictionary=module_dict,
                         call_stack=[function_symbol])

    ast_printer_dispatcher.dispatch(node=function_fnode, params=base_params)

    print(f"Function: {function_symbol.key()}")

    print('run_translation')


