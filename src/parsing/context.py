import sys
from fparser.two.Fortran2003 import Program, Module, Specification_Part, Module_Subprogram_Part, Module_Stmt

# from parsing.definitions import FortranDefinitions
# from parsing.module import FortranModule

class FortranDefinitions:
    pass

class FortranContext:
    def get_symbol(self, symbol_name: str):
        raise NotImplementedError("This method should be implemented by subclasses")

    def get_operator_symbols(self, op: str):
        raise NotImplementedError("This method should be implemented by subclasses")
    
class ModulePublicExportsContext(FortranContext):
    def __init__(self, definitions: FortranDefinitions):
        self.definitions: FortranDefinitions = definitions

    def get_symbol(self, symbol_name: str):
        return self.definitions.find_public_symbol(symbol_name)

    def get_operator_symbols(self, op: str):
        return self.definitions.find_public_operators(op)

class ExternalLibraryContext(FortranContext):
    def __init__(self, defined_external_symbols):
        self._defined_external_symbols = { s.key(): s for s in defined_external_symbols }

    def get_symbol(self, symbol_name: str):
        return self._defined_external_symbols.get(symbol_name, None)

    def get_operator_symbols(self, op: str):
        return None

class ModuleLocalContext(FortranContext):
    def __init__(self, definitions: FortranDefinitions):
        self.definitions: FortranDefinitions = definitions
    
    def get_symbol(self, symbol_name: str):
        return self.definitions.find_local_symbol(symbol_name)
    
    def get_operator_symbols(self, op: str):
        return self.definitions.find_all_operators(op)
    
class ModuleImportedContext():
    def __init__(self, definitions: FortranDefinitions, module_dictionary):
        self.definitions = definitions
        self.modules = None
        
        self.module_dictionary = module_dictionary

    def get_symbol(self, symbol_name: str):
        self._fetch_modules()
        returned_symbols = []

        for module in reversed(self.modules):
            symbol = module.public_exports_context.get_symbol(symbol_name)
            
            if not symbol:
                continue
                
            returned_symbols.append(symbol)
            # TODO: solve only imports ... e.g. file: mod_memutil.f90
            
        if len(returned_symbols) > 1:
            print(f"\033[93mWarning: Symbol {symbol_name} is defined in multiple modules <{[s.defined_in() for s in returned_symbols]}>\033[0m", file=sys.stderr, end=' ')
        
        return returned_symbols[0] if returned_symbols else None

    def get_operator_symbols(self, op: str):
        self._fetch_modules()
        returned_symbols = []

        for module in reversed(self.modules):
            symbols = module.public_exports_context.get_operator_symbols(op)
            returned_symbols.extend(symbols)
        
        return returned_symbols

    def _fetch_modules(self):
        if self.modules is not None:
            return

        module_names = [using.key() for using in self.definitions.get_using_statements()]
        self.modules = [self.module_dictionary.get_module(module_name) for module_name in module_names]


class SubroutineFunctionContext(FortranContext):
    def __init__(self, subroutine_definitions: FortranDefinitions, module_dictionary):
        self.subroutine_definitions = subroutine_definitions 
        self._imported_context = ModuleImportedContext(subroutine_definitions, module_dictionary)

    def get_symbol(self, symbol_name: str):
        return self.subroutine_definitions.find_local_symbol(symbol_name) or \
            self._imported_context.get_symbol(symbol_name)
    
    def get_operator_symbols(self, op: str):
        return []

class ChainedContext:
    def __init__(self, contexts: list[FortranContext]):
        self.contexts = contexts

    def get_expanded(self, context: FortranContext):
        return ChainedContext(self.contexts + [context])

    def __getattr__(self, name):

        def method(*args, **kwargs):
            for context in reversed(self.contexts):
                func = getattr(context, name, None)
                if func:
                    result = func(*args, **kwargs)
                    if result is not None:
                        return result
            return None
        return method

    def get_operator_symbols(self, op: str):
        symbols = []
        
        for context in reversed(self.contexts):
            context_ops = context.get_operator_symbols(op) or []
            symbols.extend(context_ops)
            
        return symbols    
