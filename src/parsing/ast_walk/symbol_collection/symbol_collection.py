from parsing.definitions import GenericFunctionDefinition


class SymbolCollection:
    def __init__(self):
        self.symbols = set()
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
        return {symbol for symbol in self.symbols if isinstance(symbol, GenericFunctionDefinition)}

    def count(self) -> int:
        return len(self.symbols)

    @staticmethod
    def merge_many(args_collections: list['SymbolCollection']) -> 'SymbolCollection':
        new_col = SymbolCollection()
        new_col.symbols = set(symbol for arg_col in args_collections for symbol in arg_col.symbols)
        return new_col
