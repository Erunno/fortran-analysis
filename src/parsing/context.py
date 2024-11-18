from fparser.two.Fortran2003 import Program, Module, Specification_Part, Module_Subprogram_Part, Module_Stmt

from parsing.definitions import FortranDefinitions

class FortranContext:
    def get_symbol(symbol_name: str):
        raise NotImplementedError("This method should be implemented by subclasses")

class ModulePublicExportsContext(FortranContext):
    def __init__(self, definitions: FortranDefinitions):
        self.definitions = definitions
        pass

class ModulePrivatesContext(FortranContext):
    def __init__(self, definitions: FortranDefinitions):
        self.definitions = definitions
    
class ModuleImportedContext():
    def __init__(self, definitions: FortranDefinitions, moduleDictionary):
        self.definitions = definitions

class SubroutineContext(FortranContext):
    def __init__(self, subroutine: Module_Subprogram_Part):
        self.subroutine = subroutine
        self.variables = self._get_variables()

class ChainedContext(FortranContext):
    def __init__(self, contexts: list[FortranContext]):
        self.contexts = contexts

    def push_context(self, context: FortranContext):
        self.contexts.append(context)

    def pop_context(self):      
        self.contexts.pop()

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

    

    