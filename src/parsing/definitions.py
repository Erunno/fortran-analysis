from fparser.two.Fortran2003 import Program, Module, Specification_Part, \
    Module_Subprogram_Part, Use_Stmt, Subroutine_Subprogram, Access_Stmt, \
    Name, Entity_Decl_List, Include_Filename, Access_Spec, Interface_Block, \
    Interface_Stmt, Function_Subprogram, Function_Stmt, Derived_Type_Def, \
    Derived_Type_Stmt, Initialization, Internal_Subprogram_Part
    
from fparser.two.Fortran2008.type_declaration_stmt_r501 import Type_Declaration_Stmt

from parsing.context import SubroutineFunctionContext
from parsing.find_in_tree import find_in_tree, findall_in_tree

class FortranDefinitions:
    pass

class SymbolDefinition:
    def __init__(self, fparser_node, definition_location):
        self.fparser_node = fparser_node
        self._is_public = False
        self.access_modifier = None
        self.definition_location = definition_location

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

    def __str__(self):
        return f"{self.class_label()} <{self.key()}> defined in {self.definition_location}"

    def __repr__(self):
        return self.__str__()

    def class_label(self):
        return "Symbol"

    def defined_in(self):
        return self.definition_location

class VariableDeclaration(SymbolDefinition):
    def __init__(self, fparser_node: Type_Declaration_Stmt, name: str, definition_location: str):
        super().__init__(fparser_node, definition_location)
        self.name = name

        self.access_modifier = self._get_access_modifier()
        if self.access_modifier:
            self._is_public = self.access_modifier.tostr().lower() == "public"

    def _get_access_modifier(self):
        return find_in_tree(self.fparser_node, Access_Spec)

    @staticmethod
    def create_from(fparser_node, definition_location):
        if isinstance(fparser_node, Type_Declaration_Stmt):
            decl_list = find_in_tree(fparser_node, Entity_Decl_List)
            names = [name.tostr().lower() for name in findall_in_tree(decl_list, Name, exclude=Initialization)]

            return [VariableDeclaration(fparser_node, name, definition_location) for name in names]
        
    def class_label(self):
        return "Variable"

class UsingStatement(SymbolDefinition):
    def __init__(self, fparser_node, definition_location: str):
        super().__init__(fparser_node, definition_location)

    @staticmethod
    def create_from(fparser_node, definition_location):
        if isinstance(fparser_node, Use_Stmt):
            return UsingStatement(fparser_node, definition_location)
        
    def class_label(self):
        return "Using"

class GenericFunctionDefinition(SymbolDefinition):
    def get_definitions(self) -> FortranDefinitions:
        specification = find_in_tree(self.fparser_node, Specification_Part)
        subprogram = find_in_tree(self.fparser_node, Internal_Subprogram_Part)
        location = f'[{self.class_label()} {self.key()}]'

        return FortranDefinitions(location, specification, subprogram, module_dictionary=None)
    
    def get_local_context(self):
        return SubroutineFunctionContext(self.get_definitions())

class Subroutine(GenericFunctionDefinition):
    def __init__(self, fparser_node: Subroutine_Subprogram, definition_location: str):
        super().__init__(fparser_node, definition_location)
    
    @staticmethod
    def create_from(fparser_node, definition_location):
        if isinstance(fparser_node, Subroutine_Subprogram):
            return Subroutine(fparser_node, definition_location)

    def class_label(self):
        return "Subroutine"

class Function(GenericFunctionDefinition):
    def __init__(self, fparser_node: Function_Subprogram, definition_location: str):
        super().__init__(fparser_node, definition_location)

        func_stmt = find_in_tree(fparser_node, Function_Stmt)
        self.name = func_stmt.items[1].tostr().lower()
    
    def class_label(self):
        return "Function"
    
    @staticmethod
    def create_from(fparser_node, definition_location):
        if isinstance(fparser_node, Function_Subprogram):
            return Function(fparser_node, definition_location)

class Include(SymbolDefinition):
    def __init__(self, fparser_node: Subroutine_Subprogram, fname, definition_location: str):
        self.fname = fname
        super().__init__(fparser_node, definition_location)

    def key(self):
        return self.fname.split(".")[0].lower()

    def class_label(self):
        return "Include"

    @staticmethod
    def create_from(fparser_node, definition_location):
        if isinstance(fparser_node, Subroutine_Subprogram):
            incl_fnames = findall_in_tree(fparser_node, Include_Filename)
            if incl_fnames: 
                return [Include(fparser_node, fname.tostr(), definition_location) for fname in incl_fnames]
            
class Interface(SymbolDefinition):
    def __init__(self, fparser_node: Interface_Block, definition_location: str):
        super().__init__(fparser_node, definition_location)
        
        interface_stmt = find_in_tree(fparser_node, Interface_Stmt)
        self.name = find_in_tree(interface_stmt, Name).tostr().lower()

    @staticmethod
    def create_from(fparser_node, definition_location):
        if isinstance(fparser_node, Interface_Block):
            return Interface(fparser_node, definition_location)
        
    def class_label(self):
        return "Interface"

class ProxySymbolDefinition(SymbolDefinition):
    def __init__(self, name, definition_location, module_dictionary, usings: list[UsingStatement]):
        super().__init__(None, definition_location)

        self.name = name
        self._is_public = True
        
        self.module_dictionary = module_dictionary
        self.usings = usings

    def class_label(self):
        return "ProxyForwardSymbol"

class Type(SymbolDefinition):
    def __init__(self, fparser_node: Derived_Type_Def, definition_location: str):
        super().__init__(fparser_node, definition_location)

        type_stmt = find_in_tree(fparser_node, Derived_Type_Stmt)
        self.name = type_stmt.items[1].tostr().lower()

    @staticmethod
    def create_from(fparser_node, definition_location):
        if isinstance(fparser_node, Derived_Type_Def):
            return Type(fparser_node, definition_location)
        
    def class_label(self):
        return "Type"

class AccessModifier:
    def __init__(self, fparser_node: Access_Stmt, definition_location: str):
        self.fparser_node = fparser_node
        self.definition_location = definition_location

    def defines_public(self):
        modifier, _ = self.fparser_node.items
        modifier = modifier.lower() if modifier else ""

        return modifier == "public"
    
    def is_global(self):
        _, decl_list = self.fparser_node.items
        return not decl_list

    def __str__(self):
        return f"Access modifier <{self.key()}> defined in {self.definition_location}"
    
    def get_modified_symbol_keys(self):
        _, access_spec_list = self.fparser_node.items

        return [name.tostr().lower() for name in access_spec_list.items]

    @staticmethod
    def create_from(fparser_node, definition_location):
        if isinstance(fparser_node, Access_Stmt):
            return AccessModifier(fparser_node, definition_location)


class FortranDefinitions:
    def __init__(self, \
                 definition_location: str,
                 specification: Specification_Part, subprogram: Module_Subprogram_Part, \
                 module_dictionary):
        
        self.module_dictionary = module_dictionary
        self.definition_location = definition_location

        self.variables: list[VariableDeclaration] = []
        self.using_statements: list[UsingStatement] = []
        self.subroutines: list[Subroutine] = []
        self.includes: list[Include] = []
        self.access_modifiers: list[AccessModifier] = []
        self.interfaces: list[Interface] = []
        self.functions: list[Function] = []
        self.types: list[Type] = []

        self.forward_imports: list[ProxySymbolDefinition] = []

        self.builders = [
            (AccessModifier.create_from, self.access_modifiers),
            (VariableDeclaration.create_from, self.variables),
            (UsingStatement.create_from, self.using_statements),
            (Include.create_from, self.includes),
            (Subroutine.create_from, self.subroutines),
            (Interface.create_from, self.interfaces),
            (Function.create_from, self.functions),
            (Type.create_from, self.types),
        ]

        # default is public i guess ?? ¯\_(ツ)_/¯
        self.defining_public = True

        self.load(specification)
        if subprogram:
            self.load(subprogram)

        self._load_forward_imports()

        self._set_public_symbols()

    def load(self, root: Specification_Part | Module_Subprogram_Part):
        if not root:
            return
        
        for child in root.children:
            for builder, container in self.builders:
                symbol = builder(child, self.definition_location)
                if not symbol:
                    continue

                if isinstance(symbol, AccessModifier) and symbol.is_global():
                    self.defining_public = symbol.defines_public()

                symbols = [symbol] if not isinstance(symbol, list) else symbol 
                
                for symbol in symbols:
                    if isinstance(symbol, SymbolDefinition) and not symbol.has_access_modifier():
                        symbol.set_public(value=self.defining_public)
                    
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
                
                forward_import = ProxySymbolDefinition(key, self.definition_location,
                                                       self.module_dictionary, self.using_statements)
                self.forward_imports.append(forward_import)

    def get_local_symbols(self):
        return self.variables + self.subroutines + self.interfaces + self.functions + self.types
    
    def get_all_symbols(self):
        return self.get_local_symbols() + self.forward_imports
    
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

    def find_local_symbol(self, key):
        return next((symbol for symbol in self.get_local_symbols() if symbol.key() == key), None)
    
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

