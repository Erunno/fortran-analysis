from parsing.ast_walk.ast_nodes._my_ats_node import AssignmentNode, CallNode, ForLoopNode, FunctionDefinitionNode, IfBlockNode, SubroutineDefinitionNode, WriteStdoutNode
from parsing.ast_walk.dispatcher import Dispatcher, Params
from parsing.ast_walk.test_print.nodes_printer import AssignmentPrinter, CallSubroutinePrinter, ForLoopPrinter, FunctionDefinitionPrinter, IfBlockPrinter, WriteStdoutPrinter
from parsing.module_dictionary import ModuleDictionary

ast_printer_dispatcher = Dispatcher()
ast_printer_dispatcher.register(AssignmentPrinter).for_node(AssignmentNode)
ast_printer_dispatcher.register(FunctionDefinitionPrinter).for_node(FunctionDefinitionNode).for_node(SubroutineDefinitionNode)
ast_printer_dispatcher.register(ForLoopPrinter).for_node(ForLoopNode)
ast_printer_dispatcher.register(CallSubroutinePrinter).for_node(CallNode)
ast_printer_dispatcher.register(IfBlockPrinter).for_node(IfBlockNode)
ast_printer_dispatcher.register(WriteStdoutPrinter).for_node(WriteStdoutNode)

def run_translation(
        module_dict: ModuleDictionary,
        module_name, function_name
):

    module = module_dict.get_module(module_name)
    function_symbol = module.module_local_context.get_symbol(function_name)

    function_fnode = function_symbol.fparser_node

    ast_printer_dispatcher.dispatch(node=function_fnode, params=Params())

    print(f"Function: {function_symbol.key()}")

    print('run_translation')


