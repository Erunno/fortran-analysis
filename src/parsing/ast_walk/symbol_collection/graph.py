from parsing.ast_walk.symbol_collection.symbol_collection import SymbolCollection
from parsing.definitions import ExternalSymbol, GenericFunctionDefinition

_reg_cm_base_path = 'https://github.com/ICTP/RegCM/blob/master/'

class GraphNode:

    def __init__(self, function_symbol: GenericFunctionDefinition, file_repo):
        self._key = function_symbol.full_unique_key()
        self._function_symbol = function_symbol
        self._called_functions: list['GraphNode'] = []

        self._error : Exception = None
        self._traceback = None
        self._parent = None

        from parsing.ast_walk.symbol_collection.functions_location_definitions import FileLocationRepository
        self._file_repo : FileLocationRepository = file_repo
        self._touched_symbols: SymbolCollection = None

    def add_call(self, callee: 'GraphNode'):
        if not isinstance(callee, GraphNode):
            raise ValueError("callee must be a GraphNode")
        
        self._called_functions.append(callee)

    def key(self):
        return self._key
    
    def short_name(self):
        return self._function_symbol.key()
    
    def set_error(self, error, traceback=None):
        self._error = error
        self._traceback = traceback

    def all_called_functions(self):
        return self._called_functions

    def try_set_parent(self, parent: 'GraphNode'):
        if self._parent is None:
            self._parent = parent
    
    def get_children(self):
        return [func for func in self.all_called_functions() 
                if self.key() == func.parent().key()]
    
    def parent(self):
        return self._parent

    def get_other_callees(self):
        return [func for func in self.all_called_functions() 
                if self.key() != func.parent().key()] 

    def json_dict_metadata(self):

        metadata = {
            'error': str(self._error) if self._error else None,
            'traceback': str(self._error) if self._traceback else None,
            'is_external_function': isinstance(self._function_symbol, ExternalSymbol),
            'is_std_function': self._function_symbol.is_std_function(),
            'line_count': self.get_line_count(),
            'touched_global_vars': self.get_touched_global_variables_pretty_str()
        }

        url = self.get_url()
        if url:
            line_num = self._file_repo.get_line_of_definition(self)
            suffix = f'#L{line_num}' if line_num else ''
            metadata['url'] = url + suffix

        return metadata
    
    def get_path(self):
        module = self._function_symbol.defined_in_module()

        if not hasattr(module, 'file_path'):
            return None
        
        return module.file_path()

    def get_url(self):
        path = self.get_path()

        if path is None:
            return None
        
        path = path.replace('\\', '/')
        tail = path.split('RegCM/')[-1]

        return _reg_cm_base_path + tail
    
    def get_line_count(self):
        if not isinstance(self._function_symbol, GenericFunctionDefinition):
            return None
        
        if self._function_symbol.is_std_function():
            return None
        
        str_code = str(self._function_symbol.fparser_node).lower().split('contains')[0]
        return len(str_code.split('\n'))
    
    def set_touched_symbols(self, symbols: SymbolCollection):
        self._touched_symbols = symbols

    def get_touched_global_variables(self):
        return self._touched_symbols.get_global_variables() if self._touched_symbols else []
    
    def get_touched_global_variables_pretty_str(self):
        global_vars = self.get_touched_global_variables()
        return [f'{v.key()}::{v.defined_in().key()}: ({v.get_type()})' for v in global_vars]

class CallGraph:
    def __init__(self):
        self._nodes = {}
        self._root_function = None

        from parsing.ast_walk.symbol_collection.functions_location_definitions import FileLocationRepository
        self._file_repo = FileLocationRepository()

    def add_call(self, caller: GenericFunctionDefinition, callee: GenericFunctionDefinition):
        caller_node = self._get_or_create_node(caller)
        callee_node = self._get_or_create_node(callee)

        caller_node.add_call(callee_node)
        callee_node.try_set_parent(caller_node)

    def add_many_calls(self, caller, callees):
        for callee in callees:
            self.add_call(caller, callee)

    def set_touched_symbols(self, function: GenericFunctionDefinition, symbols: SymbolCollection):
        node = self._get_or_create_node(function)
        node.set_touched_symbols(symbols)

    def set_erroneous_node(self, node, error, traceback=None):
        node = self._get_or_create_node(node)
        node.set_error(error, traceback)

    def _get_or_create_node(self, symbol: GenericFunctionDefinition) -> GraphNode:
        key = symbol.full_unique_key()

        if key not in self._nodes:
            self._nodes[key] = GraphNode(symbol, self._file_repo)

        return self._nodes[key]
    
    def set_root_function(self, function: GenericFunctionDefinition):
        self._root_function = function

    def get_json_dict_graph(self, root_node: GenericFunctionDefinition = None):

        if root_node is None:
            root_node = self._root_function

        def node_to_json_dict(node: GraphNode):
            json_node = {}
            json_node['name'] = node.short_name()
            json_node['full_name'] = node.key()
            json_node['metadata'] = node.json_dict_metadata()
            json_node['children'] = [node_to_json_dict(c) for c in node.get_children()]
            json_node['other_calls'] = [f.key() for f in node.get_other_callees()]

            return json_node

        root = self._nodes[root_node.full_unique_key()]
        return node_to_json_dict(node=root)
        