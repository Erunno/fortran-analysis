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
    Prefix, Prefix_Spec, Explicit_Shape_Spec_List

from fparser.two.Fortran2008 import Procedure_Name_List    
from fparser.two.Fortran2008.type_declaration_stmt_r501 import Type_Declaration_Stmt
from fparser.two.Fortran2008 import Attr_Spec_List, Component_Attr_Spec_List
from fparser.two.Fortran2008.data_component_def_stmt_r436 import Data_Component_Def_Stmt
from fparser.two.Fortran2008.component_attr_spec_r437 import Component_Attr_Spec

from parsing.find_in_tree import find_in_node, find_in_tree, findall_in_node, findall_in_tree

class FortranType: 
    def is_equivalent(self, other: 'FortranType') -> bool:
        raise NotImplementedError("is_equivalent to be implemented by children classes")
    
    def get_unified_with(self, other: 'FortranType') -> 'FortranType':
        if not self.is_equivalent(other):
            raise ValueError(f"Cannot unify {self} with {other}")

        return self.clone()

    def clone(self) -> 'FortranType':
        raise NotImplementedError("clone to be implemented by children classes")
    
    def __repr__(self):
        return self.__str__()

class AnyType(FortranType):
    
    def is_equivalent(self, other: FortranType) -> bool:
        return True

    def get_unified_with(self, other: FortranType) -> FortranType:
        return other.clone()
    
    _instance = None
    @staticmethod
    def instance():
        if not hasattr(AnyType, "_instance"):
            AnyType._instance = AnyType()
        return AnyType._instance

    def __str__(self):
        return "<any>"


class VoidType(FortranType):
    def is_equivalent(self, other: FortranType) -> bool:
        return isinstance(other, VoidType)

    @staticmethod
    def get_instance():
        if not hasattr(VoidType, "_instance"):
            VoidType._instance = VoidType()
        return VoidType._instance

    def __str__(self):
        return "void"
    
    def get_unified_with(self, other: FortranType) -> FortranType:
        if not isinstance(other, VoidType):
            raise ValueError("Cannot unify void with non-void type")
        
        return VoidType.get_instance()

    def clone(self) -> FortranType:
        return VoidType.get_instance()

class PrimitiveType(FortranType):
    def __init__(self, name):
        self.name = name
        self.attributes = {}

    def is_equivalent(self, other: FortranType, with_number_cast=False) -> bool:
        if isinstance(other, AnyType):
            return True
        
        if not isinstance(other, PrimitiveType):
            return False
        
        if PrimitiveType.is_number(self) and PrimitiveType.is_number(other):
            if 'anyNumber' in (self.name, other.name):
                return True
            
            if with_number_cast:
                if (self.name, other.name) in PrimitiveType._castable_number_types or \
                    (other.name, self.name) in PrimitiveType._castable_number_types:
                    return True

        for attr in self.attributes:
            if attr == 'kind':
                unified_kind = PrimitiveType.unify_kinds(self.attributes[attr], other.attributes.get(attr))

                if unified_kind is None:
                    return False
                
            elif self.attributes[attr] != other.attributes.get(attr):
                return False
        
        return self.name == other.name

    def add_attribute(self, name, value):
        self.attributes[name] = value

    def with_attribute(self, name, value):
        clone = self.clone()
        clone.add_attribute(name, value)
        return clone
    
    def with_any_kind(self):
        return self.with_attribute('kind', PrimitiveType.any_kind())

    def with_infinite_length(self):
        return self.with_length('*')

    def with_length(self, length):
        if length == float('inf'):
            length = '*'

        return self.with_attribute('length', str(length))

    def has_infinite_length(self):
        return self.attributes.get('length') == '*'

    def get_length(self):
        return self.attributes.get('length', None)
    
    def get_added_length(self: 'PrimitiveType', other: 'PrimitiveType') -> str:
        len1 = self.get_length()
        len2 = other.get_length()
        
        if len1 == '*' or len2 == '*':
            return '*'
        
        return str(int(len1) + int(len2))

    def get_unified_with(self, other_type) -> FortranType:
        if isinstance(other_type, AnyType):
            return self.clone()
        
        if not isinstance(other_type, PrimitiveType):
            raise ValueError("Cannot unify primitive type with non-primitive type")
        
        if not self.is_equivalent(other_type, with_number_cast=True):
            raise ValueError(f"Cannot unify {self} with {other_type}")
        
        if self.name == PrimitiveType.any_number_name():
            return other_type.clone()
        
        if other_type.name == PrimitiveType.any_number_name():
            return self.clone()

        for _from, _to in PrimitiveType._castable_number_types:
            if self.name == _from and other_type.name == _to:
                return other_type.clone()
            
            if self.name == _to and other_type.name == _from:
                return self.clone()

        clone = self.clone()

        if 'kind' in clone.attributes:
            unified_kind = PrimitiveType.unify_kinds(clone.attributes['kind'], other_type.attributes.get('kind'))
            clone.attributes['kind'] = unified_kind

        return clone
    

    @staticmethod
    def default_int_kind():
        return 'defaultIntLiteralKind'
     
    @staticmethod
    def any_number_name():
        return 'anyNumber'

    @staticmethod
    def any_kind():
        return 'anyKind'

    _castable_kinds = [
        # from, to
        ('rk8', 'rkx'),
        ('rk8', 'wrkp'),
        ('wrkp', 'rkx'),
        (default_int_kind(), 'ik4'),
        (default_int_kind(), 'ik8'),
    ]

    _castable_number_types = [
        ('integer', 'real'),
    ]

    _number_types = ['integer', 'real', any_number_name()]

    @staticmethod
    def is_number(type):
        return isinstance(type, PrimitiveType) and type.name in PrimitiveType._number_types 

    @staticmethod
    def unify_kinds(k1, k2):
        if k1 == k2:
            return k1

        if (k1, k2) in PrimitiveType._castable_kinds:
            return k2
        
        if (k2, k1) in PrimitiveType._castable_kinds:
            return k1

        if k1 == PrimitiveType.any_kind():
            return k2
        
        if k2 == PrimitiveType.any_kind():
            return k1

        return None
    
    def __str__(self):
        items = ', '.join(f"{k}={v}" for k, v in self.attributes.items())
        if items:
            items = f" ({items})"
        
        return f"<{self.name}{items}>"

    def clone(self):     
        new_instance = PrimitiveType(self.name)
        new_instance.attributes = self.attributes.copy()
        return new_instance
    
    @staticmethod
    def get_any_number_instance():
        return PrimitiveType(PrimitiveType.any_number_name())

    @staticmethod
    def get_integer_instance():
        return PrimitiveType("integer")

    @staticmethod
    def get_real_instance():
        return PrimitiveType("real")

    @staticmethod
    def get_logical_instance():
        return PrimitiveType("logical")

    @staticmethod
    def get_character_instance():
        return PrimitiveType("character")
    
    @staticmethod
    def is_string(type):
        return isinstance(type, PrimitiveType) and type.name == "character" and 'length' in type.attributes

    @staticmethod
    def get_string_instance():
        return PrimitiveType \
            .get_character_instance() \
            .with_infinite_length()

    @staticmethod
    def get_type_from_string(type_str):
        type_map = {
            "integer": PrimitiveType.get_integer_instance,
            "real": PrimitiveType.get_real_instance,
            "logical": PrimitiveType.get_logical_instance,
            "character": PrimitiveType.get_character_instance,
        }

        return type_map[type_str.lower()]()

class ArrayType(FortranType):
    class AnyArray:
        def __init__(self, element_type: FortranType):
            self.element_type = element_type

        def is_equivalent(self, other: FortranType) -> bool:
            if isinstance(other, AnyType):
                return True

            return isinstance(other, ArrayType.AnyArray) and other.element_type.is_equivalent(self.element_type)

        def get_unified_with(self, other: FortranType) -> FortranType:
            if isinstance(other, AnyType):
                return self.clone()
            
            if not isinstance(other, ArrayType) or not other.element_type.is_equivalent(self.element_type):
                raise ValueError("Cannot unify anyArray with non-array type")
            
            return other

        def __str__(self):
            return "<anyArray>"

        def clone(self) -> FortranType:
            return self

    def __init__(self, element_type: FortranType, dimensions: list[int]):
        self.element_type = element_type
        self.dimensions = dimensions

    def is_equivalent(self, other: FortranType, for_function_call=False) -> bool:
        if isinstance(other, AnyType):
            return True
        
        if isinstance(other, ArrayType.AnyArray) and other.element_type.is_equivalent(self.element_type):
            return True

        if not isinstance(other, ArrayType):
            return False
        
        if not self.element_type.is_equivalent(other.element_type):
            return False
        
        if len(self.dimensions) != len(other.dimensions):
            return False
        
        if not for_function_call:
            for self_dim, other_dim in zip(self.dimensions, other.dimensions):
                if self_dim != other_dim:
                    return False
            
        return True

    def __str__(self):
        var_len = ArrayType.variable_length()
        array_spec = ",".join([(str(dim) if dim != var_len else ':') for dim in self.dimensions])

        return f"({self.element_type})[{array_spec}]"
    
    def get_unified_with(self, other: FortranType) -> FortranType:
        if isinstance(other, ArrayType.AnyArray) and other.element_type.is_equivalent(self.element_type):
            return self.clone()

        if not isinstance(other, ArrayType):
            raise ValueError("Cannot unify array type with non-array type")
        
        if len(self.dimensions) != len(other.dimensions):
            raise ValueError("Cannot unify arrays with different number of dimensions")
        
        if self.dimensions != other.dimensions:
            raise ValueError("Cannot unify arrays with different dimensions")

    @staticmethod
    def variable_length():
        return -1
    
    @staticmethod
    def any_array(element_type: FortranType):
        return ArrayType.AnyArray(element_type)
    
    def clone(self) -> FortranType:
        return ArrayType(self.element_type.clone(), self.dimensions.copy())

class FunctionArgumentForType:
    def __init__(self, name: str, arg_type: FortranType, is_optional: bool):
        self.name = name
        self.arg_type = arg_type
        self.is_optional = is_optional

    def clone(self):
        return FunctionArgumentForType(self.name, self.arg_type.clone(), self.is_optional)

    def __str__(self):
        return f"{self.name}{'?' if self.is_optional else ''}: {self.arg_type}"

    

class StructType(FortranType):
    def __init__(self, type_name, variable_defined_in_module):
        self.type_name = type_name
        self.original_variable_defined_in_module = variable_defined_in_module

    def is_equivalent(self, other: FortranType) -> bool:
        if isinstance(other, AnyType):
                return True

        return isinstance(other, StructType) and \
            self.type_name == other.type_name

    def get_property(self, property_name, module_dictionary):
        module_of_original_variable = module_dictionary.get_module(self.original_variable_defined_in_module)
        struct_definition = module_of_original_variable.get_context().get_symbol(self.type_name)
        
        struct_property = struct_definition.get_property(property_name)
        
        if struct_property:
            return struct_property
        
        struct_method = struct_definition.get_method(property_name)

        if struct_method:
            return struct_method
        
        raise ValueError(f"Property {property_name} not found in struct {self.type_name}")

    def __str__(self):
        return f"<struct {self.type_name}>"

    def clone(self) -> FortranType:
        return StructType(self.type_name, self.struct_definition)

class FunctionType(FortranType):
    def __init__(self, return_type: FortranType, arg_types: list[FunctionArgumentForType]):
        self.return_type = return_type
        self.arg_types = arg_types

        self._first_optional_index = next((i for i, arg in enumerate(arg_types) if arg.is_optional), len(arg_types))
        if any(not arg.is_optional for arg in arg_types[self._first_optional_index:]):
            raise ValueError("Optional arguments must be at the end of the argument list")


    def is_equivalent(self, other: FortranType) -> bool:
        if isinstance(other, AnyType):
            return True

        if not isinstance(other, FunctionType):
            return False
        if not self.return_type.is_equivalent(other.return_type):
            return False
        if len(self.arg_types) != len(other.arg_types):
            return False
        for self_arg, other_arg in zip(self.arg_types, other.arg_types):
            if not self_arg.arg_type(other_arg.arg_type) or self_arg.is_optional != other_arg.is_optional:
                return False
        return True

    def __str__(self):
        arg_types_str = ", ".join(str(arg) for arg in self.arg_types)
        return f"({arg_types_str}) -> ({self.return_type})"
    
    def can_be_called_with(self, arg_types: list[FortranType]) -> bool:
        if len(arg_types) < self._first_optional_index:
            return False
        
        if len(arg_types) > len(self.arg_types):
            return False

        for self_arg, call_arg in zip(self.arg_types, arg_types):
            self_arg_type = self_arg.arg_type

            if isinstance(self_arg_type, ArrayType):

                # fortran function can apparently accept pointers even if the function signature does not specify it
                # e.g. file ~\RegCM\Main\cumlib\mod_cu_em.F90 call to tlift(n,p,t,q,qs,gz,icb,nk,tvp,tp,clw,nd,nl,1)
                if isinstance(call_arg, PointerType):
                    if self_arg_type.is_equivalent(call_arg.element_type, for_function_call=True):
                        # this argument is OK .. carry on
                        continue

                if not self_arg_type.is_equivalent(call_arg, for_function_call=True):
                    return False

            # in fortran i can pass any string to a function that accepts a string of any length
            elif PrimitiveType.is_string(self_arg_type) and self_arg_type.has_infinite_length():
                if PrimitiveType.is_string(call_arg):
                    continue


            elif not self_arg_type.is_equivalent(call_arg):
                return False

        return True

    def clone(self) -> FortranType:
        return FunctionType(self.return_type.clone(), [arg.clone() for arg in self.arg_types])

    def as_method_on_struct(self) -> 'FunctionType':
        return FunctionType(
            return_type=self.return_type,
            # remove the first argument (self)
            arg_types=self.arg_types[1:]
        )

class PointerType(FortranType):
    def __init__(self, element_type: FortranType):
        self.element_type = element_type

    def is_equivalent(self, other: FortranType) -> bool:
        if isinstance(other, AnyType):
            return True
        
        if not isinstance(other, PointerType):
            return False
        return self.element_type.is_equivalent(other.element_type)

    def __str__(self):
        return f"({self.element_type})*"

    def clone(self) -> FortranType:
        return PointerType(self.element_type.clone())

class InterfaceType(FortranType):
    def __init__(self, name: str):
        self.name = name

    def is_equivalent(self, other: FortranType) -> bool:
        raise ValueError("InterfaceType is not directly comparable")
        
    def __str__(self):
        return f"interface {self.function_type}"

    def clone(self) -> FortranType:
        return InterfaceType(self.function_type.clone())

class TypeParser:
    @staticmethod
    def parse_type(fnode: Type_Declaration_Stmt | Intrinsic_Type_Spec, module_of_definition: str) -> tuple[FortranType, bool]:
        return_type: FortranType = None

        type_spec = fnode.children[0]

        if isinstance(type_spec, Intrinsic_Type_Spec):
            return_type = TypeParser.parse_intrinsic_type(type_spec)
        elif isinstance(type_spec, Declaration_Type_Spec):
            typename = find_in_tree(type_spec, Type_Name)
            return_type = StructType(typename.tostr().lower(), module_of_definition)
        else:
            raise NotImplementedError(f"Type spec {type_spec} not supported yet")

        attributes = TypeParser._load_attribute_spec_list(fnode)

        is_pointer, array_dims, denoted_as_optional = TypeParser._parse_attributes(attributes)
        return_type = TypeParser._wrap_base_type(return_type, is_pointer, array_dims)
        
        return return_type, denoted_as_optional
    
    @staticmethod
    def parse_intrinsic_type(type_spec: Intrinsic_Type_Spec):
        intrinsic_type = PrimitiveType.get_type_from_string(type_spec.children[0])
            
        kind = find_in_tree(type_spec, Kind_Selector)
        if kind:
            kind_name = find_in_tree(kind, Name)
            if not kind_name:
                kind_name = find_in_tree(kind, Int_Literal_Constant)
                
            intrinsic_type.add_attribute("kind", kind_name.tostr().lower())

        length = find_in_tree(type_spec, Length_Selector)
        if length:
            length_value = find_in_tree(length, Type_Param_Value)
            if not length_value:
                length_value = find_in_tree(length, Int_Literal_Constant)
            
            intrinsic_type.add_attribute("length", length_value.tostr().lower())
        
        return intrinsic_type

    @staticmethod
    def _load_attribute_spec_list(fnode):
        return find_in_node(fnode, Attr_Spec_List) or find_in_node(fnode, Component_Attr_Spec_List)

    @staticmethod
    def _parse_attributes(attributes):
        is_pointer = False
        array_dims = None
        denoted_as_optional = False

        if not attributes:
            return is_pointer, array_dims, denoted_as_optional
        
        # TODO maybe use something better than shit tun of IFs
        for attr in attributes.children:
            if (isinstance(attr, Attr_Spec) or isinstance(attr, Component_Attr_Spec)) and attr.tostr().lower() == "pointer":
                is_pointer = True
            elif isinstance(attr, Attr_Spec) and attr.tostr().lower() == "optional":
                denoted_as_optional = True
            elif isinstance(attr, Attr_Spec) and attr.tostr().lower() == "parameter":
                pass # parameter means constant (does not affect type)
            elif isinstance(attr, Attr_Spec) and attr.tostr().lower() == "save":
                pass # save does not affect the type
            elif isinstance(attr, Dimension_Attr_Spec) or isinstance(attr, Dimension_Component_Attr_Spec):
                shape_list = find_in_tree(attr, Assumed_Shape_Spec_List) \
                    or find_in_tree(attr, Deferred_Shape_Spec_List) \
                    or find_in_tree(attr, Explicit_Shape_Spec_List)
                array_dims = []

                for shape in shape_list.children:
                    dim_shape = shape.tostr().lower()
                    if dim_shape == ":":
                        array_dims.append(ArrayType.variable_length())
                    else:
                        array_dims.append(dim_shape)

            elif isinstance(attr, Intent_Attr_Spec):
                pass # intent does not affect type
            elif isinstance(attr, Access_Spec):
                pass # access does not affect type
            else:
                raise NotImplementedError(f"Attribute {attr} not supported yet")
    
        return is_pointer, array_dims, denoted_as_optional
    
    @staticmethod
    def _wrap_base_type(base_type: FortranType, is_pointer, array_dims):
        # the order of these checks is important (fortran does not allow pointer arrays ... luckily)   
        if array_dims:
            base_type = ArrayType(base_type, array_dims)

        if is_pointer:
            base_type = PointerType(base_type)

        return base_type