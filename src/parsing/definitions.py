from fparser.two.Fortran2003 import Program, Module, Specification_Part, \
    Module_Subprogram_Part, Use_Stmt, Subroutine_Subprogram, Access_Stmt, \
    Name, Entity_Decl_List, Include_Filename, Access_Spec, Interface_Block, \
    Interface_Stmt, Function_Subprogram, Function_Stmt, Derived_Type_Def, \
    Derived_Type_Stmt
    
from fparser.two.Fortran2008.type_declaration_stmt_r501 import Type_Declaration_Stmt

from parsing.find_in_tree import find_in_tree, findall_in_tree

class SymbolDefinition:
    def __init__(self, fparser_node):
        self.fparser_node = fparser_node
        self._is_public = False
        self.access_modifier = None

    def set_public(self, value=True):
        self._is_public = value

    def is_public(self):
        return self._is_public
        
    def key(self):
        if hasattr(self, 'name'):
            return self.name.lower()

        return find_in_tree(self.fparser_node, Name).tostr().lower()
    
    def has_access_modifier(self):
        return not not self.access_modifier

class VariableDeclaration(SymbolDefinition):
    def __init__(self, fparser_node: Type_Declaration_Stmt, name: str):
        super().__init__(fparser_node)
        self.name = name

        self.access_modifier = self._get_access_modifier()
        if self.access_modifier:
            self._is_public = self.access_modifier.tostr().lower() == "public"

    def _get_access_modifier(self):
        return find_in_tree(self.fparser_node, Access_Spec)

    @staticmethod
    def create_from(fparser_node):
        if isinstance(fparser_node, Type_Declaration_Stmt):
            decl_list = find_in_tree(fparser_node, Entity_Decl_List)
            names = [name.tostr().lower() for name in findall_in_tree(decl_list, Name)]

            return [VariableDeclaration(fparser_node, name) for name in names]
        
    def __str__(self):
        return f"Variable <{self.key()}>"

class UsingStatement(SymbolDefinition):
    def __init__(self, fparser_node):
        super().__init__(fparser_node)

    @staticmethod
    def create_from(fparser_node):
        if isinstance(fparser_node, Use_Stmt):
            return UsingStatement(fparser_node)
        
    def __str__(self):
        return f"Using <{self.key()}>"

class Subroutine(SymbolDefinition):
    def __init__(self, fparser_node: Module_Subprogram_Part):
        super().__init__(fparser_node)
        self._is_public = False
    
    @staticmethod
    def create_from(fparser_node):
        if isinstance(fparser_node, Subroutine_Subprogram):
            return Subroutine(fparser_node)

    def __str__(self):
        return f"Subroutine <{self.key()}>"

class Function(SymbolDefinition):
    def __init__(self, fparser_node: Module_Subprogram_Part):
        super().__init__(fparser_node)
        self._is_public = False

        func_stmt = find_in_tree(fparser_node, Function_Stmt)
        self.name = func_stmt.items[1].tostr().lower()
    
    @staticmethod
    def create_from(fparser_node):
        if isinstance(fparser_node, Function_Subprogram):
            return Function(fparser_node)

    def __str__(self):
        return f"Function <{self.key()}>"

class Include(SymbolDefinition):
    def __init__(self, fparser_node: Subroutine_Subprogram, fname):
        self.fname = fname
        super().__init__(fparser_node)

    def key(self):
        return self.fname.split(".")[0].lower()

    def __str__(self):
        return f"Include #<{self.key()}>"

    @staticmethod
    def create_from(fparser_node):
        if isinstance(fparser_node, Subroutine_Subprogram):
            incl_fnames = findall_in_tree(fparser_node, Include_Filename)
            if incl_fnames: 
                return [Include(fparser_node, fname.tostr()) for fname in incl_fnames]
            
class Interface(SymbolDefinition):
    def __init__(self, fparser_node: Interface_Block):
        super().__init__(fparser_node)
        
        interface_stmt = find_in_tree(fparser_node, Interface_Stmt)
        self.name = find_in_tree(interface_stmt, Name).tostr().lower()

    @staticmethod
    def create_from(fparser_node):
        if isinstance(fparser_node, Interface_Block):
            return Interface(fparser_node)
        
    def __str__(self):
        return f"Interface <{self.key()}>"

class ProxySymbolDefinition(SymbolDefinition):
    def __init__(self, name, module_dictionary, usings: list[UsingStatement]):
        super().__init__(None)

        self.name = name
        self._is_public = True
        
        self.module_dictionary = module_dictionary
        self.usings = usings

class Type(SymbolDefinition):
    def __init__(self, fparser_node: Derived_Type_Def):
        super().__init__(fparser_node)

        type_stmt = find_in_tree(fparser_node, Derived_Type_Stmt)
        self.name = type_stmt.items[1].tostr().lower()

    @staticmethod
    def create_from(fparser_node):
        if isinstance(fparser_node, Derived_Type_Def):
            return Type(fparser_node)
        
    def __str__(self):
        return f"Type <{self.key()}>"

class AccessModifier:
    def __init__(self, fparser_node: Access_Stmt):
        self.fparser_node = fparser_node

    def defines_public(self):
        modifier, _ = self.fparser_node.items
        modifier = modifier.lower() if modifier else ""

        return modifier == "public"
    
    def is_global(self):
        _, decl_list = self.fparser_node.items
        return not decl_list

    def __str__(self):
        return f"Access modifier <{self.key()}>"
    
    def get_modified_symbol_keys(self):
        _, access_spec_list = self.fparser_node.items

        return [name.tostr().lower() for name in access_spec_list.items]

    @staticmethod
    def create_from(fparser_node):
        if isinstance(fparser_node, Access_Stmt):
            return AccessModifier(fparser_node)


class FortranDefinitions:
    def __init__(self, \
                 specification: Specification_Part, subprogram: Module_Subprogram_Part, \
                 module_dictionary):
        
        self.module_dictionary = module_dictionary

        self.variables: list[VariableDeclaration] = []
        self.using_statements: list[UsingStatement] = []
        self.subroutines: list[Subroutine] = []
        self.includes: list[Include] = []
        self.access_modifiers: list[AccessModifier] = []
        self.interfaces: list[Interface] = []
        self.functions: list[Function] = []
        self.types: list[Type] = []

        self.forward_imports: list[ProxySymbolDefinition] = []

        self.handlers = [
            (AccessModifier.create_from, self.access_modifiers),
            (VariableDeclaration.create_from, self.variables),
            (UsingStatement.create_from, self.using_statements),
            (Include.create_from, self.includes),
            (Subroutine.create_from, self.subroutines),
            (Interface.create_from, self.interfaces),
            (Function.create_from, self.functions),
            (Type.create_from, self.types),
        ]

        self.load(specification)
        self.load(subprogram)

        self._load_forward_imports()

        self._set_public_symbols()

    def load(self, root: Specification_Part | Module_Subprogram_Part):
        if not root:
            return
        
        defining_public = False

        for child in root.children:
            for handler, container in self.handlers:
                symbol = handler(child)
                if not symbol:
                    continue

                if isinstance(symbol, AccessModifier) and symbol.is_global():
                    defining_public = symbol.defines_public()

                symbols = [symbol] if not isinstance(symbol, list) else symbol 
                
                for symbol in symbols:
                    if isinstance(symbol, SymbolDefinition) and not symbol.has_access_modifier():
                        symbol.set_public(value=defining_public)
                    
                    container.append(symbol)

    def _load_forward_imports(self):
        # symbols that are public but not defined in this module

        for access_modif in self.access_modifiers:
            if access_modif.is_global() or not access_modif.defines_public():
                continue

            for key in access_modif.get_modified_symbol_keys():
                symbol = self.find_symbol(key)
                if symbol:
                    continue 
                
                forward_import = ProxySymbolDefinition(key, self.module_dictionary, self.using_statements)
                self.forward_imports.append(forward_import)

    def get_all_symbols(self):
        return self.variables + self.subroutines + self.interfaces + self.functions + self.types + self.forward_imports
    
    def get_interfaces(self):
        return self.interfaces

    def get_variables(self):
        return self.variables
    
    def get_subroutines(self):
        return self.subroutines

    def get_functions(self):
        return self.functions

    def get_types(self):
        return self.types

    def get_includes(self):
        return self.includes
    
    def get_using_statements(self):
        return self.using_statements
    
    def get_forward_imports(self):
        return self.forward_imports

    def get_public_symbols(self):
        return [symbol for symbol in self.get_all_symbols() if symbol.is_public()]
    
    def get_private_symbols(self):
        return [symbol for symbol in self.get_all_symbols() if not symbol.is_public()]

    def find_public_symbol(self, key):
        return next((symbol for symbol in self.get_public_symbols() if symbol.key() == key), None)

    def find_symbol(self, key):
        return next((symbol for symbol in self.get_all_symbols() if symbol.key() == key), None)
    
    def _set_public_symbols(self):
        for acc_modifier in self.access_modifiers:
            if not acc_modifier.defines_public():
                continue

            if acc_modifier.is_global():
                continue

            for key in acc_modifier.get_modified_symbol_keys():
                symbol = self.find_symbol(key)
                symbol.set_public()

