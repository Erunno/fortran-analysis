import json
import traceback
from parsing.ast_walk.dispatcher import Params
from parsing.ast_walk.symbol_collection.graph import CallGraph
from parsing.ast_walk.symbol_collection.symbol_collection import SymbolCollection
from parsing.definitions import ExternalSymbol, GenericFunctionDefinition
from parsing.ast_walk.symbol_collection.symbol_collection_dispatcher import collectors_dispatcher
from parsing.typing import FunctionType

class CatchNoException(BaseException):
    pass

class GraphCollector:
    def __init__(self, module_dict):
        self.module_dict = module_dict
        
    def collect_graph(self, module_name, function_name):

        start_function_symbol = self._get_function_symbol(module_name, function_name)
        
        queue = [start_function_symbol]
        all_symbols = SymbolCollection()

        visited_functions = set()
        graph = CallGraph()
        graph.set_root_function(start_function_symbol)
        
        iter_count = 1

        while queue:
            # if iter_count == 0:
            #     break
            # iter_count -= 1

            queue.sort(key=lambda symbol: symbol.key())

            # for debugging purposes
            DEBUG_FUNC_NAME = 'cupeman'
            self._move_function_to_front(queue, DEBUG_FUNC_NAME)

            current_function_symbol = queue.pop(0)
            
            print('Collecting function: ', current_function_symbol)
            
            print(f'full key: {current_function_symbol.full_unique_key()}')

            try:
                collected_symbols = self._collect_symbols(current_function_symbol)

                called_functions = collected_symbols.get_function_symbols()
                called_external_functions = collected_symbols.get_external_functions()
                called_std_functions = collected_symbols.get_std_functions()

                all_symbols = all_symbols.merge(collected_symbols)

                queue = queue + [f for f in called_functions if f not in visited_functions]
                visited_functions.add(current_function_symbol)

                graph.add_many_calls(
                    caller=current_function_symbol, 
                    callees=called_functions.union(called_external_functions).union(called_std_functions))
        
                print(f'Collected {collected_symbols.count()} symbols')
                print(f' --> Called functions: {len(called_functions)}')
                print(f' --> All symbols: {all_symbols.count()}')
                print(f' --> Visited functions / current total: {len(visited_functions)}/{len(queue) + len(visited_functions)}')    
            # except Exception as e:
            except CatchNoException as e:
                print(f'\033[91mError collecting symbols for {current_function_symbol}\033[0m')
                full_err_traceback = traceback.format_stack()
                graph.set_erroneous_node(current_function_symbol, e, full_err_traceback)

            print()

        return graph, all_symbols

    def _get_function_symbol(self, module_name, function_name):
        module = self.module_dict.get_module(module_name)
        function_symbol: GenericFunctionDefinition = module.module_local_context.get_symbol(function_name)
        return function_symbol
        

    def _collect_symbols(self, function_symbol: GenericFunctionDefinition):
        return collectors_dispatcher.dispatch(
            node=function_symbol.fparser_node,
            params=Params(
                context=function_symbol.get_context(),
                module_dictionary=self.module_dict,
                call_stack=[function_symbol]))
    
    def _move_function_to_front(self, queue, function_name):
        for i, f in enumerate(queue):
            if f.key() == function_name:
                queue.insert(0, queue.pop(i))
                return queue
        return queue
        
    def _get_external_functions(self, symbols: SymbolCollection):
        external_functions = [f for f in symbols.get_function_symbols() 
                              if not isinstance(f, ExternalSymbol) and \
                                isinstance(f.get_type(), FunctionType)]
        return external_functions