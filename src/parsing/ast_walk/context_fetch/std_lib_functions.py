from parsing.definitions import GenericFunctionDefinition, SymbolInitParams
from parsing.typing import FunctionArgumentForType, FunctionType, PrimitiveType

class StdLibHolderModule:
    def __init__(self):
        pass
    
    _instance = None
    @staticmethod
    def instance():
        if not StdLibHolderModule._instance:
            StdLibHolderModule._instance = StdLibHolderModule()
        return StdLibHolderModule._instance
    
    def key(self):
        return 'StdLibHolderModule'
    
    def class_label(self):
        return 'StdLibHolderModule'
    
    def is_module(self):
        return True

class StdLibFunctionsDefinition(GenericFunctionDefinition):
    def __init__(self, name, function_type: FunctionType):
        super().__init__(SymbolInitParams(
            fparser_node = None, definition_location_symbol=StdLibHolderModule.instance()))

        self.name = name
        self._type = function_type

    def key(self):
        return self.name

    def class_label(self):
        return 'StdLibFunction'

    def get_actual_function_symbol(self, arg_types):
        return self
    
    def get_type(self):
        return self._type
    
    def is_std_function(self):
        return True

    @staticmethod
    def get_random_number():
        return StdLibFunctionsDefinition('random_number', FunctionType(
            return_type=PrimitiveType.get_any_number_instance(),
            arg_types=[
                FunctionArgumentForType('seed', PrimitiveType.get_any_number_instance(), is_optional=True)
            ]))
    
class StdLibContext:
    _instance = None

    @staticmethod
    def instance():
        if not StdLibContext._instance:
            StdLibContext._instance = StdLibContext()
        return StdLibContext._instance
    
    _functions = {
        'random_number': StdLibFunctionsDefinition.get_random_number()
    }

    def get_symbol(self, symbol_name: str):
        return self._functions.get(symbol_name, None)
    
    def get_operator_symbols(self, op: str):
        return None