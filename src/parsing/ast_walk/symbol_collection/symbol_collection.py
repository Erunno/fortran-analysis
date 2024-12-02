class SymbolCollection:
    pass

class SymbolCollection:
    def merge(self, other: SymbolCollection) -> SymbolCollection:
        return self

    def with_function_symbol(self, function_symbol) -> SymbolCollection:
        return self

    def with_symbol(self, symbol) -> SymbolCollection:
        return self
    
    def with_property_symbol(self, symbol) -> SymbolCollection:
        return self

    def as_write(self) -> SymbolCollection:
        return self
    
    def with_intrinsic_function(self, function_name) -> SymbolCollection:
        return self

    @staticmethod
    def merge_many(args_collections: list[SymbolCollection]) -> SymbolCollection:
        return SymbolCollection()

    

