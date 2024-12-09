from fparser.two.Fortran2003 import Program, Module, Specification_Part, \
    Module_Subprogram_Part, Use_Stmt, Subroutine_Subprogram, Access_Stmt, \
    Name, Entity_Decl_List, Include_Filename, Access_Spec, Interface_Block, \
    Interface_Stmt, Function_Subprogram, Function_Stmt, Derived_Type_Def, \
    Derived_Type_Stmt, Initialization, Internal_Subprogram_Part, \
    Intrinsic_Type_Spec, Kind_Selector, Attr_Spec, Dimension_Attr_Spec, \
    Assumed_Shape_Spec_List, Assumed_Shape_Spec, Dummy_Arg_List, \
    Declaration_Type_Spec, Type_Name, Intent_Attr_Spec, Length_Selector, Type_Param_Value, \
    Suffix, Component_Part, Component_Decl_List, Component_Decl, Dimension_Component_Attr_Spec, \
    Deferred_Shape_Spec_List, Procedure_Stmt, Subroutine_Body,  Generic_Spec, \
    Specific_Binding, Type_Bound_Procedure_Part, Contains_Stmt, Int_Literal_Constant, \
    Prefix, Prefix_Spec, Extended_Intrinsic_Op, Only_List, Rename
    

from fparser.two.Fortran2008 import Procedure_Name_List    
from fparser.two.Fortran2008.type_declaration_stmt_r501 import Type_Declaration_Stmt
from fparser.two.Fortran2008 import Attr_Spec_List, Component_Attr_Spec_List
from fparser.two.Fortran2008.data_component_def_stmt_r436 import Data_Component_Def_Stmt
from fparser.two.Fortran2008.component_attr_spec_r437 import Component_Attr_Spec

from parsing.context import ChainedContext, SubroutineFunctionContext
from parsing.find_in_tree import find_in_node, find_in_tree, findall_in_node, findall_in_tree
from parsing.typing import ArrayType, FortranType, FunctionArgumentForType, FunctionType, InterfaceType, PointerType, PrimitiveType, StructType, TypeParser, VoidType

class SymbolInitParams:
    def __init__(self, fparser_node, definition_location_symbol: 'SymbolDefinition'):
        self.fparser_node = fparser_node
        self.definition_location_symbol = definition_location_symbol

class SymbolDefinition:
    def __init__(self, init_params: SymbolInitParams):
        self.fparser_node = init_params.fparser_node
        self._is_public = False
        self.access_modifier = None
        self._defined_in_symbol = init_params.definition_location_symbol

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
        return f"{self.class_label()} <{self.key()}> defined in [{self.defined_in()}]"

    def __repr__(self):
        return self.__str__()

    def class_label(self):
        return "Symbol"

    def defined_in(self) -> 'SymbolDefinition':
        return self._defined_in_symbol
    
    def defined_in_module_str(self) -> str:
        module = self.defined_in_module()
        return module.key()
    
    def defined_in_module(self):
        if self._defined_in_symbol.is_module():
            return self._defined_in_symbol
        
        return self._defined_in_symbol.defined_in_module()

    def is_module(self):
        return False
    
    def full_unique_key(self):
        return f'{self.class_label()} {self.key()}::{self.defined_in().full_unique_key()}'

class ModuleDefinition(SymbolDefinition):
    def __init__(self, init_params: SymbolInitParams):
        super().__init__(init_params)
        self.name = find_in_tree(init_params.fparser_node, Name).tostr().lower()
        self.module_context = None

    def class_label(self):
        return "Module"

    def set_module_context(self, module_context):
        self.module_context = module_context

class VariableDeclaration(SymbolDefinition):
    def __init__(self, name: str, init_params: SymbolInitParams):
        super().__init__(init_params)
        self.name = name

        self.access_modifier = self._get_access_modifier()
        if self.access_modifier:
            self._is_public = self.access_modifier.tostr().lower() == "public"

        self._type: FortranType = None
        self._denoted_as_optional: bool = None

    def _get_access_modifier(self):
        return find_in_tree(self.fparser_node, Access_Spec)

    @staticmethod
    def create_from(init_params: SymbolInitParams):
        if isinstance(init_params.fparser_node, Type_Declaration_Stmt):
            decl_list = find_in_tree(init_params.fparser_node, Entity_Decl_List)
            names = [name.tostr().lower() for name in findall_in_tree(decl_list, Name, exclude=Initialization)]

            return [VariableDeclaration(name, init_params) for name in names]
    
    def class_label(self):
        return "Variable"
    
    def get_type(self):
        if not self._type:
            self._type, self._denoted_as_optional = self._parse_type(self.fparser_node)

        return self._type
    
    def denoted_as_optional(self) -> bool:
        if not self._denoted_as_optional:
            self._type, self._denoted_as_optional = self._parse_type(self.fparser_node)

        return self._denoted_as_optional
    
    def _parse_type(self, fparser_node: Type_Declaration_Stmt):
        return TypeParser.parse_type(fparser_node, module_of_definition=self.defined_in_module_str())

class ImportRenamedSymbol(SymbolDefinition):
    def __init__(self, new_name, inner_symbol: SymbolDefinition, module_of_renaming):
        self.inner_symbol = inner_symbol
        self.name = new_name
        self.module_of_renaming = module_of_renaming

    def class_label(self):
        return "ImportRenamedSymbol"

    def defined_in(self):
        return self.module_of_renaming

    def __getattr__(self, item):
        return getattr(self.inner_symbol, item)

class FunctionReturnVariableDeclaration(VariableDeclaration):
    def __init__(self,
                 name: str,
                 init_params: SymbolInitParams):
        
        super().__init__(name, init_params)

    def class_label(self):
        return "FunctionReturnVariable"
        
    def _parse_type(self, fparser_node: Function_Stmt):
        # TODO this maybe more complicated - so far i don not see an example in the code
        # TODO it is more complicated for the pure functions
        
        type_spec = find_in_tree(fparser_node, Intrinsic_Type_Spec)
        return_type = TypeParser.parse_intrinsic_type(type_spec)
        
        # is not important for return variable, but needs to be returned
        denoted_as_optional = False

        return return_type, denoted_as_optional

class UsingStatement(SymbolDefinition):
    def __init__(self, init_params: SymbolInitParams):
        super().__init__(init_params)

    @staticmethod
    def create_from(init_params: SymbolInitParams):
        if isinstance(init_params.fparser_node, Use_Stmt):
            return UsingStatement(init_params)
        
    def class_label(self):
        return "Using"
    
    def get_imported_names(self):
        only_list = find_in_node(self.fparser_node, Only_List)

        returned_names = []

        for name in only_list.children:
            if isinstance(name, Name):
                returned_names.append(name.tostr().lower())
            elif isinstance(name, Rename):
                if not (name.children[0] is None and isinstance(name.children[1], Name) and isinstance(name.children[1], Name)):
                    raise NotImplementedError(f"Rename {name} not supported yet")

                new_name_of_the_symbol = name.children[1].tostr().lower()
                returned_names.append(new_name_of_the_symbol)
            else:
                raise NotImplementedError(f"Only list element {name} not supported yet")

        return returned_names
    
    def has_only_clause(self):
        return find_in_node(self.fparser_node, Only_List) is not None
    
    def get_renaming(self):
        only_list = find_in_node(self.fparser_node, Only_List)
        
        if not only_list:
            return {}
        
        renaming = {}

        for name in only_list.children:
            if isinstance(name, Rename):

                new_name_of_the_symbol = name.children[1].tostr().lower()
                actual_name_of_the_symbol = name.children[2].tostr().lower()
                
                renaming[new_name_of_the_symbol] = actual_name_of_the_symbol

        return renaming

class GenericFunctionDefinition(SymbolDefinition):
    def __init__(self, init_params: SymbolInitParams):
        super().__init__(init_params)
        self._type: FortranType = None
        self._local_context = None
        self._definitions = None
        self.module_dictionary = None

    def get_definitions(self) -> 'FortranDefinitions':
        if self._definitions:
            return self._definitions
        
        specification = find_in_tree(self.fparser_node, Specification_Part)
        subprogram = find_in_tree(self.fparser_node, Internal_Subprogram_Part)

        self._definitions = FortranDefinitions(self, specification, subprogram, module_dictionary=None)

        if hasattr(self, '_patch_definitions'):
            self._definitions = self._patch_definitions(self._definitions)

        return self._definitions
    
    def is_std_function(self):
        return False
    
    def _set_module_dictionary(self, module_dictionary):
        self.module_dictionary = module_dictionary

    def get_local_context(self):
        if not self._local_context:
            self._local_context = SubroutineFunctionContext(self.get_definitions(), self.module_dictionary)
        return self._local_context

    def get_context(self):
        parent_context = self.defined_in().get_context()
        local_context = self.get_local_context()

        return ChainedContext([parent_context, local_context])

    def _get_input_args(self) -> list[FunctionArgumentForType]:
        function_stmt = self.fparser_node.children[0]
        arg_list = find_in_tree(function_stmt, Dummy_Arg_List)

        if not arg_list:
            return []
        
        local_context = self.get_local_context()
        arg_types = []

        for arg_name in arg_list.children:
            arg_symbol: VariableDeclaration = local_context.get_symbol(arg_name.tostr().lower())
            if not arg_symbol:
                raise ValueError(f"Argument {arg_name} not found in function definition")
            
            arg_types.append(FunctionArgumentForType(
                name=arg_symbol.key(),
                arg_type=arg_symbol.get_type(),
                is_optional=arg_symbol.denoted_as_optional()))

        return arg_types

    def get_type(self) -> FunctionType:
        raise NotImplementedError("get_type not implemented by children classes")

    def get_actual_function_symbol(self, call_args_types) -> 'GenericFunctionDefinition':
        if not self.get_type().can_be_called_with(call_args_types):
            raise ValueError(f"Function {self} cannot be called with arguments {call_args_types}")

        return self
    
    def _unpack_pointers_to_arrays(self, call_args_types):
        return [arg.element_type if isinstance(arg, PointerType) else arg for arg in call_args_types]
    
class Subroutine(GenericFunctionDefinition):
    def __init__(self, init_params: SymbolInitParams):
        super().__init__(init_params)
    
    @staticmethod
    def create_from(init_params: SymbolInitParams):
        if isinstance(init_params.fparser_node, Subroutine_Subprogram) or isinstance(init_params.fparser_node, Subroutine_Body):
            return Subroutine(init_params)

    def class_label(self):
        return "Subroutine"
    
    def get_type(self) -> FortranType:
        return FunctionType(
            return_type=VoidType.get_instance(),
            arg_types=self._get_input_args())

class Function(GenericFunctionDefinition):
    def __init__(self, init_params: SymbolInitParams):
        super().__init__(init_params)

        func_stmt = find_in_tree(init_params.fparser_node, Function_Stmt)
        self.name = func_stmt.items[1].tostr().lower()
    
    def class_label(self):
        return "Function"
    
    @staticmethod
    def create_from(init_params: SymbolInitParams):
        if isinstance(init_params.fparser_node, Function_Subprogram) and \
           not Function.is_definition_without_result_clause(init_params.fparser_node):
            return Function(init_params)
    
    def _patch_definitions(self, definitions: 'FortranDefinitions') -> 'FortranDefinitions':
        return_variable = FunctionReturnVariableDeclaration(
            name=self._get_return_variable_name(),
            init_params=SymbolInitParams(
                fparser_node=self.fparser_node,
                definition_location_symbol=self))

        definitions.add_variable(return_variable)
        return definitions

    def get_type(self) -> FortranType:
        return FunctionType(
            return_type=self._get_return_type(),
            arg_types=self._get_input_args())

    def _get_return_type(self) -> FortranType:
        function_stmt = find_in_node(self.fparser_node, Function_Stmt)
        suffix = find_in_node(function_stmt, Suffix)
        return_name = find_in_tree(suffix, Name).tostr().lower()

        return self.get_local_context().get_symbol(return_name).get_type()
    
    def _get_return_variable_name(self) -> str:
        function_stmt = find_in_node(self.fparser_node, Function_Stmt)
        suffix = find_in_node(function_stmt, Suffix)
        name = find_in_tree(suffix, Name)

        return name.tostr().lower() if name else None

    @staticmethod
    def is_definition_without_result_clause(fparser_node):
        prefix = find_in_tree(fparser_node, Prefix)
        
        if not prefix:
            return False
        
        return not find_in_tree(prefix, Suffix)
    
    @staticmethod
    def is_definition_of_pure_function(fparser_node):
        prefix = find_in_tree(fparser_node, Prefix)
        
        if not prefix:
            return False
        
        prefix_spec = find_in_tree(prefix, Prefix_Spec)
        spec_str = prefix_spec.tostr().lower() if prefix_spec else None

        return spec_str == "pure"

class FunctionWithoutResultClause(Function):
    def __init__(self, init_params: SymbolInitParams):
        super().__init__(init_params)

    def class_label(self):
        return "FunctionWithoutResultClause"
    
    @staticmethod
    def create_from(init_params):
        if isinstance(init_params.fparser_node, Function_Subprogram) and \
           Function.is_definition_without_result_clause(init_params.fparser_node):
            return FunctionWithoutResultClause(init_params)

    def _get_return_type(self) -> FortranType:
        prefix = find_in_tree(self.fparser_node, Prefix)
        type_def = find_in_tree(prefix, Intrinsic_Type_Spec)

        return TypeParser.parse_intrinsic_type(type_def)

    def _get_return_variable_name(self) -> str:
        name_from_return_clause = super()._get_return_variable_name()

        if name_from_return_clause:
            return name_from_return_clause
        
        return self.key()

class Include(SymbolDefinition):
    def __init__(self, fname, init_params: SymbolInitParams):
        self.fname = fname
        super().__init__(init_params)

    def key(self):
        return self.fname.split(".")[0].lower()

    def class_label(self):
        return "Include"

    @staticmethod
    def create_from(init_params):
        if isinstance(init_params.fparser_node, Subroutine_Subprogram):
            incl_fnames = findall_in_tree(init_params.fparser_node, Include_Filename)
            if incl_fnames: 
                return [Include(fname.tostr(), init_params) for fname in incl_fnames]

class Interface(SymbolDefinition):
    def __init__(self, init_params: SymbolInitParams):
        super().__init__(init_params)
        
        interface_stmt = find_in_tree(init_params.fparser_node, Interface_Stmt)
        self.name = find_in_tree(interface_stmt, Name).tostr().lower()

        self.module_dictionary = None

        self._wrapped_function_names = self._get_wrapped_symbol_names(init_params.fparser_node)
        self._wrapped_function_symbols: list[GenericFunctionDefinition] = None

    @staticmethod
    def create_from(init_params: SymbolInitParams):
        if isinstance(init_params.fparser_node, Interface_Block):
            interface_stmt = find_in_tree(init_params.fparser_node, Interface_Stmt)
            
            if find_in_tree(interface_stmt, Name):
                return Interface(init_params)
            
    def get_type(self) -> InterfaceType:
        return InterfaceType(self.name)
    
    def get_context(self):
        return self.defined_in().get_context()

    def get_actual_function_symbol(self, call_args_types) -> GenericFunctionDefinition:
        wrapped_functions = self._fetch_wrapped_functions()

        possible_functions = []

        for function in wrapped_functions:
            if function.get_type().can_be_called_with(call_args_types):
                possible_functions.append(function)
    
        if len(possible_functions) > 1:
            raise ValueError(f"Interface {self} have more functions that can be called with {call_args_types} namely {possible_functions}")

        if len(possible_functions) == 0:
            raise ValueError(f"Interface {self} does not have a function that can be called with arguments {call_args_types}")

        return possible_functions[0]

    def _set_module_dictionary(self, module_dictionary):
        self.module_dictionary = module_dictionary

    def _get_wrapped_symbol_names(self, fnode: Interface_Block):
        procedures_stmts = findall_in_node(fnode, Procedure_Stmt)
        procedure_definitions = findall_in_node(fnode, Subroutine_Body)

        if len(procedures_stmts) + len(procedure_definitions) != len(fnode.children) - 2:
            raise ValueError(f"Interface {self} does not support non-procedure symbols")

        names = []

        for proc in procedures_stmts:
            name_list = find_in_node(proc, Procedure_Name_List)
            names.extend([name.tostr().lower() for name in name_list.children])
            
        internal_definitions = self._load_internal_subroutine_definitions(procedure_definitions)
        names.extend([definition.key() for definition in internal_definitions])

        # TODO: for functions it may work as well (??)

        return names

    def _fetch_wrapped_functions(self) -> list[GenericFunctionDefinition]:
        if self._wrapped_function_symbols:
            return self._wrapped_function_symbols
        
        self._wrapped_function_symbols = []
        
        interfaces_module = self.module_dictionary.get_module(self.defined_in_module_str())
        internal_definitions = self._load_internal_subroutine_definitions(findall_in_node(self.fparser_node, Subroutine_Body))

        for name in self._wrapped_function_names:
            if name in [d.key() for d in internal_definitions]:
                continue

            symbol = interfaces_module.module_context.get_symbol(name)

            if not symbol:
                raise ValueError(f"Symbol {name} not found in module {interfaces_module}")
            
            self._wrapped_function_symbols.append(symbol)

        self._wrapped_function_symbols.extend(internal_definitions)
        return self._wrapped_function_symbols

    def _load_internal_subroutine_definitions(self, bodies: list[Subroutine_Body]):
        return [ \
            Subroutine.create_from(SymbolInitParams(
                fparser_node=proc_body, 
                definition_location_symbol=self))
            for proc_body in bodies]

    def class_label(self):
        return "Interface"

class OperatorRedefinition(SymbolDefinition):
    def __init__(self, init_params: SymbolInitParams):
        super().__init__(init_params)
        self._operator_sign: str = None
        self.module_dictionary = None
        self._operator_functions = None
        self._operator_function_names = None

        self.name = OperatorRedefinition.make_key(self.operator_sign())

    def class_label(self):
        return "OperatorRedefinition"

    def operator_sign(self):
        return self._fetch_operator_sign()
    
    def defines_operator_for(self, left_type, right_type):
        operator_functions = self._fetch_operator_functions()
        
        return any([f.get_type().can_be_called_with([left_type, right_type]) for f in operator_functions])
    
    def get_function_symbol_for_types(self, left_type, right_type):
        operator_functions = self._fetch_operator_functions()
        
        possible_functions = [f for f in operator_functions if f.get_type().can_be_called_with([left_type, right_type])]
        
        if len(possible_functions) > 1:
            raise ValueError(f"Operator {self} has more than one function that can be called with arguments {left_type}, {right_type}")
        
        if len(possible_functions) == 0:
            raise ValueError(f"Operator {self} has no function that can be called with arguments {left_type}, {right_type}")
        
        return possible_functions[0]

    def is_default():
        return False

    def _set_module_dictionary(self, module_dictionary):
        self.module_dictionary = module_dictionary
    
    def _fetch_operator_sign(self):
        if self._operator_sign:
            return self._operator_sign
        
        operator_stmt = find_in_node(self.fparser_node, Interface_Stmt)
        intrinsic_op = find_in_tree(operator_stmt, Extended_Intrinsic_Op)

        if intrinsic_op:
            self._operator_sign = intrinsic_op.tostr()
        else:
            assignment_op = find_in_tree(operator_stmt, Generic_Spec).items[1]
            self._operator_sign = str(assignment_op)

        return self._operator_sign

    def _fetch_operator_functions(self) -> list[GenericFunctionDefinition]:
        if self._operator_functions:
            return self._operator_functions
        
        self_module = self.module_dictionary.get_module(self.defined_in_module_str())
        self._operator_functions = [self_module.get_context().get_symbol(name) for name in self._fetch_operator_function_names()]

        return self._operator_functions

    def _fetch_operator_function_names(self) -> list[str]:
        if self._operator_function_names:
            return self._operator_function_names
        

        procedure_stmts = findall_in_node(self.fparser_node, Procedure_Stmt)

        if len(self.fparser_node.children) - 2 != len(procedure_stmts):
            raise ValueError(f"Operator {self} does not support non-procedure symbols")
        
        name_lists = [find_in_tree(procedure_stmt, Procedure_Name_List) for procedure_stmt in procedure_stmts]
        names = [[name.tostr().lower() for name in findall_in_tree(name_list, Name)] for name_list in name_lists]
        
        self._operator_function_names = [name for sublist in names for name in sublist]
        return self._operator_function_names

    @staticmethod
    def make_key(op: str):
        # the format is defined in fparser

        if 'operator' in op or 'assignment' in op:
            return op

        return f"operator({op})" if op != '=' else "assignment(=)"

    @staticmethod
    def create_from(init_params: SymbolInitParams):
        if isinstance(init_params.fparser_node, Interface_Block):
            interface_stmt = find_in_tree(init_params.fparser_node, Interface_Stmt)
            
            if not find_in_tree(interface_stmt, Name):
                return OperatorRedefinition(init_params)

class ProxySymbolDefinition(SymbolDefinition):
    def __init__(self, name, module_dictionary, usings: list[UsingStatement], init_params: SymbolInitParams):
        super().__init__(init_params)

        self.name = name
        self._is_public = True
        
        self.module_dictionary = module_dictionary
        self.usings = usings

        self._loaded_modules = [] 
        self._inner_symbol: SymbolDefinition = None

    def class_label(self):
        return "ProxyForwardSymbol"

    def _fetch_inner_symbol(self):
        if self._inner_symbol:
            return self._inner_symbol

        for module in self._fetch_modules():
            symbol = module.public_exports_context.get_symbol(self.name)
            if symbol:
                self._inner_symbol = symbol
                return symbol
            
        raise ValueError(f"Proxy Symbol {self} not found in any of the modules")

    def _fetch_modules(self):
        if self._loaded_modules:
            return self._loaded_modules
        
        self._loaded_modules = [self.module_dictionary.get_module(using.key()) for using in self.usings]
        return self._loaded_modules
    
    def __getattr__(self, item):
        inner_symbol = self._fetch_inner_symbol()
        return getattr(inner_symbol, item)

class StructProperty(VariableDeclaration):
    def __init__(self, name, init_params: SymbolInitParams):
        super().__init__(name, init_params)

    def class_label(self):
        return "Property of Type"
    
    @staticmethod
    def create_from(init_params: SymbolInitParams):
        
        if not isinstance(init_params.fparser_node, Data_Component_Def_Stmt):
            raise ValueError(f"PropertyOfTypeDefinition can only be created from Data_Component_Def_Stmt, got {init_params.fparser_node}")
        
        decl_list = find_in_tree(init_params.fparser_node, Component_Decl_List)
        
        result = []

        for decl in decl_list.children:
            if not isinstance(decl, Component_Decl):
                raise NotImplementedError(f"Component decl {decl} not supported yet")
            
            name = find_in_tree(decl, Name).tostr().lower()
            prop = StructProperty(name, init_params)
            
            result.append(prop)
        
        return result

class StructMethod(SymbolDefinition):
    def __init__(self, module_dictionary, init_params: SymbolInitParams):
        super().__init__(init_params)
        
        self._full_type: FunctionType = None

        self._actual_function_symbol = None
        self.module_dictionary = module_dictionary
        self.name, self.implementation_name = self._load_names(init_params.fparser_node)

    def get_type(self) -> FunctionType:
        return self.get_full_type().as_method_on_struct()

    def get_full_type(self) -> FunctionType:
        if not self._full_type:
            self._full_type = self._fetch_symbol().get_type()

        return self._full_type

    def get_actual_function_symbol(self, call_args_types) -> GenericFunctionDefinition:
        if not self.get_type().can_be_called_with(call_args_types):
            raise ValueError(f"Function {self} cannot be called with arguments {call_args_types}")

        return self._fetch_symbol()
    
    def class_label(self):
        return "MethodOnType"

    def _fetch_symbol(self) -> GenericFunctionDefinition:
        if self._actual_function_symbol:
            return self._actual_function_symbol
        
        module = self.module_dictionary.get_module(self.defined_in_module_str())
        self._actual_function_symbol = module.module_context.get_symbol(self.implementation_name)
        
        return self._actual_function_symbol

    def _load_names(self, fnode: Specific_Binding):
        if not isinstance(fnode, Specific_Binding):
            raise ValueError(f"Specific_Binding expected, got {fnode}")
        
        names = findall_in_tree(fnode, Name)

        if len(names) != 2:
            raise ValueError(f"Specific_Binding {fnode} does not have 2 names")
        
        return names[0].tostr().lower(), names[1].tostr().lower()

class Type(SymbolDefinition):
    def __init__(self, init_params: SymbolInitParams):
        super().__init__(init_params)

        self.module_dictionary = None

        type_stmt = find_in_tree(init_params.fparser_node, Derived_Type_Stmt)
        self.name = type_stmt.items[1].tostr().lower()

        self._properties: list[VariableDeclaration] = None
        self._methods: list[StructMethod] = None

    @staticmethod
    def create_from(init_params: SymbolInitParams):
        if isinstance(init_params.fparser_node, Derived_Type_Def):
            return Type(init_params)

    def _set_module_dictionary(self, module_dictionary):
        self.module_dictionary = module_dictionary
    
    def get_type(self) -> StructType:
        return StructType(self.name, self.defined_in_module_str())
    
    def class_label(self):
        return "Type"
    
    def get_method(self, key) -> StructMethod:
        return next((method for method in self.get_methods() if method.key() == key), None)

    def get_property(self, key) -> StructProperty:
        return next((prop for prop in self.get_properties() if prop.key() == key), None)
    
    def get_methods(self) -> list[StructMethod]:
        if self._methods:
            return self._methods
        
        procedures = find_in_tree(self.fparser_node, Type_Bound_Procedure_Part)

        if not procedures:
            self._methods = []
            return []
        
        if not isinstance(procedures.children[0], Contains_Stmt):
            raise ValueError(f"Contains_Stmt expected, got {procedures.children[0]} at the beginning of Type_Bound_Procedure_Part")
        
        self._methods = [StructMethod( 
                module_dictionary=self.module_dictionary,
                init_params=SymbolInitParams(proc, self)) 
            for proc in procedures.children[1:]]
        
        self._assert_first_arg_is_the_struct_for_each(self._methods)
        
        return self._methods

    def get_properties(self) -> list[VariableDeclaration]:
        if self._properties:
            return self._properties
        
        component_part = find_in_node(self.fparser_node, Component_Part)

        self._properties = []

        for data_component in component_part.children:
            if not isinstance(data_component, Data_Component_Def_Stmt):
                raise NotImplementedError(f"Component definition {data_component} not supported yet")

            properties_defined_on_a_line = StructProperty.create_from(SymbolInitParams(
                fparser_node=data_component, 
                definition_location_symbol=self))
            
            self._properties.extend(properties_defined_on_a_line)
            
        return self._properties

    def _assert_first_arg_is_the_struct_for_each(self, methods: list[StructMethod]):
        struct_type = self.get_type()

        for method in methods:
            first_arg = method.get_full_type().arg_types[0]

            if not struct_type.is_equivalent(first_arg.arg_type):
                raise ValueError(f"Method {method} does not have the struct as the first argument")

class ExternalSymbol(SymbolDefinition):
    def __init__(self, name, type):
        super().__init__(SymbolInitParams(fparser_node=None, definition_location_symbol=None))
        self.name = name
        self._type = type
        self._is_public = True

    def key(self):
        return self.name.lower()

    def class_label(self):
        return "ExternalSymbol"

    def get_type(self):
        return self._type
    
    def _set_module(self, module):
        self._defined_in_symbol = module

    def get_actual_function_symbol(self, call_args_types):
        return self

class AccessModifier:
    def __init__(self, init_params: SymbolInitParams):
        self.fparser_node = init_params.fparser_node
        self.definition_location_symbol = init_params.definition_location_symbol

    def defines_public(self):
        modifier, _ = self.fparser_node.items
        modifier = modifier.lower() if modifier else ""

        return modifier == "public"
    
    def is_global(self):
        _, decl_list = self.fparser_node.items
        return not decl_list

    def __str__(self):
        return f"Access modifier <{self.key()}> defined in [{self.definition_location_symbol}]"
    
    def get_modified_symbol_keys(self):
        _, access_spec_list = self.fparser_node.items

        return [name.tostr().lower() for name in access_spec_list.items]

    @staticmethod
    def create_from(init_params: SymbolInitParams):
        if isinstance(init_params.fparser_node, Access_Stmt):
            return AccessModifier(init_params)

class FortranDefinitions:
    def __init__(self,
                 definition_location_symbol: SymbolDefinition,
                 specification: Specification_Part, subprogram: Module_Subprogram_Part, \
                 module_dictionary):
        
        self.module_dictionary = module_dictionary
        self.definition_location_symbol = definition_location_symbol

        self.variables: list[VariableDeclaration] = []
        self.using_statements: list[UsingStatement] = []
        self.subroutines: list[Subroutine] = []
        self.includes: list[Include] = []
        self.access_modifiers: list[AccessModifier] = []
        self.interfaces: list[Interface] = []
        self.functions: list[Function] = []
        self.types: list[Type] = []
        self.operator_redefinitions: list[OperatorRedefinition] = []

        self.forward_imports: list[ProxySymbolDefinition] = []

        self.builders = [
            (AccessModifier.create_from, self.access_modifiers),
            (VariableDeclaration.create_from, self.variables),
            (UsingStatement.create_from, self.using_statements),
            (Include.create_from, self.includes),
            (Subroutine.create_from, self.subroutines),
            (Interface.create_from, self.interfaces),
            (Function.create_from, self.functions),
            (FunctionWithoutResultClause.create_from, self.functions),
            (Type.create_from, self.types),
            (OperatorRedefinition.create_from, self.operator_redefinitions),
        ]

        # default is public i guess ?? ¯\_(ツ)_/¯
        self.defining_public = True

        self.load(specification)
        if subprogram:
            self.load(subprogram)

        self._load_forward_imports()

        self._set_public_symbols()

    def add_variable(self, variable: VariableDeclaration):
        self.variables.append(variable)

    def load(self, root: Specification_Part | Module_Subprogram_Part):
        if not root:
            return
        
        for child in root.children:
            for builder, container in self.builders:
                symbol = builder(SymbolInitParams(
                    child, self.definition_location_symbol))

                if not symbol:
                    continue

                if isinstance(symbol, AccessModifier) and symbol.is_global():
                    self.defining_public = symbol.defines_public()

                if isinstance(symbol, (Interface, Type, OperatorRedefinition, GenericFunctionDefinition)):
                    symbol._set_module_dictionary(self.module_dictionary)

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
                ops = self.find_all_operators(key)

                if symbol or len(ops) > 0:
                    continue 
                
                forward_import = ProxySymbolDefinition(key, self.module_dictionary, self.using_statements,
                                    SymbolInitParams(fparser_node=None,
                                        definition_location_symbol=self.definition_location_symbol))
                
                self.forward_imports.append(forward_import)

    def get_local_symbols(self) -> list[SymbolDefinition]:
        return self.variables + self.subroutines + self.functions + self.types + self.interfaces
    
    def get_all_symbols(self) -> list[SymbolDefinition]:
        return self.get_local_symbols() + self.forward_imports
    
    def get_interfaces(self) -> list[Interface]:
        return self.interfaces

    def get_variables(self) -> list[VariableDeclaration]:
        return self.variables
    
    def get_subroutines(self) -> list[Subroutine]:
        return self.subroutines

    def get_functions(self) -> list[Function]:
        return self.functions

    def get_types(self) -> list[Type]:
        return self.types

    def get_includes(self) -> list[Include]:
        return self.includes
    
    def get_using_statements(self) -> list[UsingStatement]:
        return self.using_statements
    
    def get_forward_imports(self) -> list[ProxySymbolDefinition]:
        return self.forward_imports

    def get_public_operator_redefinitions(self) -> list[OperatorRedefinition]:
        return [op for op in self.operator_redefinitions if op.is_public()]
    
    def get_all_operator_redefinitions(self) -> list[OperatorRedefinition]:
        return [s for s in self.operator_redefinitions]

    def find_public_operators(self, op_str: str) -> list[OperatorRedefinition]:
        op_key = OperatorRedefinition.make_key(op_str)
        return [op for op in self.get_public_operator_redefinitions() if op.key() == op_key]

    def find_all_operators(self, op_str: str) -> list[OperatorRedefinition]:
        op_key = OperatorRedefinition.make_key(op_str)
        return [op for op in self.get_all_operator_redefinitions() if op.key() == op_key]

    def get_public_symbols(self) -> list[SymbolDefinition]:
        return [symbol for symbol in self.get_all_symbols() if symbol.is_public()]
    
    def get_private_symbols(self) -> list[SymbolDefinition]:
        return [symbol for symbol in self.get_all_symbols() if not symbol.is_public()]

    def find_public_symbol(self, key) -> SymbolDefinition:
        return next((symbol for symbol in self.get_public_symbols() if symbol.key() == key), None)

    def find_local_symbol(self, key) -> SymbolDefinition:
        return next((symbol for symbol in self.get_local_symbols() if symbol.key() == key), None)
    
    def find_symbol(self, key) -> SymbolDefinition:
        return next((symbol for symbol in self.get_all_symbols() if symbol.key() == key), None)
    
    def _set_public_symbols(self):
        for acc_modifier in self.access_modifiers:
            if not acc_modifier.defines_public():
                continue

            if acc_modifier.is_global():
                continue

            for key in acc_modifier.get_modified_symbol_keys():
                symbols = self.find_symbol(key) or self.find_all_operators(key)
                
                symbols = [symbols] if not isinstance(symbols, list) else symbols

                for symbol in symbols:
                    symbol.set_public(value=True)

