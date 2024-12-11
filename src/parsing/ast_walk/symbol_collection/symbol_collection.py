from parsing.definitions import ExternalSymbol, GenericFunctionDefinition, SymbolDefinition, VariableDeclaration
from parsing.typing import FunctionType


class SymbolCollection:
    def __init__(self):
        self.symbols: set[SymbolDefinition] = set()
        self.called_intrinsic_functions_names = set()

    def merge(self, other: 'SymbolCollection') -> 'SymbolCollection':
        new_col = SymbolCollection()
        new_col.symbols = self.symbols.union(other.symbols)
        return new_col

    def with_symbol(self, symbol) -> 'SymbolCollection':
        if not symbol:
            raise ValueError("Function symbol cannot be None")
        
        new_col = SymbolCollection()
        new_col.symbols = self.symbols.union({symbol})
        return new_col
    
    def with_function_symbol(self, function_symbol) -> 'SymbolCollection':
        return self.with_symbol(function_symbol)
    
    def with_property_symbol(self, symbol) -> 'SymbolCollection':
        return self.with_symbol(symbol)

    def as_write(self) -> 'SymbolCollection':
        return self
    
    def with_intrinsic_function(self, function_name) -> 'SymbolCollection':
        if not function_name:
            raise ValueError("Function name cannot be None")

        new_col = SymbolCollection()
        new_col.called_intrinsic_functions_names = self.called_intrinsic_functions_names.union({function_name})
        return new_col

    def get_function_symbols(self) -> set[GenericFunctionDefinition]:
        return {symbol for symbol in self.symbols \
                if isinstance(symbol, GenericFunctionDefinition) and \
                    not symbol.is_std_function()}

    def get_external_functions(self) -> set[ExternalSymbol]:
        return {symbol for symbol in self.symbols
                if isinstance(symbol, ExternalSymbol) and \
                    isinstance(symbol.get_type(), FunctionType)}
    
    def get_std_functions(self) -> set[GenericFunctionDefinition]:
        return {symbol for symbol in self.symbols
                if isinstance(symbol, GenericFunctionDefinition) and \
                    symbol.is_std_function()}

    def count(self) -> int:
        return len(self.symbols)

    def get_global_variables(self):
        actual_symbols = [s.get_underling_symbol() for s in self.symbols]
        variables = [s for s in actual_symbols if isinstance(s, VariableDeclaration)]
        global_variables = [v for v in variables if v.defined_in().is_module()]

        return set(global_variables)

    @staticmethod
    def merge_many(args_collections: list['SymbolCollection']) -> 'SymbolCollection':
        new_col = SymbolCollection()
        new_col.symbols = set(symbol for arg_col in args_collections for symbol in arg_col.symbols)
        return new_col
