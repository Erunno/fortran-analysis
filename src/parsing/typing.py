class FortranType:
    pass

class FortranType: 
    def is_equivalent(self, other: FortranType) -> bool:
        raise NotImplementedError("is_equivalent to be implemented by children classes")
    
    def get_unified_with(self, other: FortranType) -> FortranType:
        if not self.is_equivalent(other):
            raise ValueError(f"Cannot unify {self} with {other}")

        return self.clone()

    def clone(self) -> FortranType:
        raise NotImplementedError("clone to be implemented by children classes")

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

    def is_equivalent(self, other: FortranType) -> bool:
        if not isinstance(other, PrimitiveType):
            return False
        
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

    def get_unified_with(self, other_type) -> FortranType:
        if not isinstance(other_type, PrimitiveType):
            raise ValueError("Cannot unify primitive type with non-primitive type")
        
        if not self.is_equivalent(other_type):
            raise ValueError(f"Cannot unify {self} with {other_type}")

        clone = self.clone()

        if 'kind' in clone.attributes:
            unified_kind = PrimitiveType.unify_kinds(clone.attributes['kind'], other_type.attributes.get('kind'))
            clone.attributes['kind'] = unified_kind

        return clone
    
    @staticmethod
    def default_int_kind():
        return 'defaultIntLiteralKind'
     
    castable_kinds = [
        # from, to
        ('rk8', 'rkx'),
        (default_int_kind(), 'ik4'),
    ]

    @staticmethod
    def unify_kinds(k1, k2):
        if k1 == k2:
            return k1

        if (k1, k2) in PrimitiveType.castable_kinds:
            return k2
        
        if (k2, k1) in PrimitiveType.castable_kinds:
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
    def get_type_from_string(type_str):
        type_map = {
            "integer": PrimitiveType.get_integer_instance,
            "real": PrimitiveType.get_real_instance,
            "logical": PrimitiveType.get_logical_instance,
            "character": PrimitiveType.get_character_instance,
        }

        return type_map[type_str.lower()]()

class ArrayType(FortranType):
    def __init__(self, element_type: FortranType, dimensions: list[int]):
        self.element_type = element_type
        self.dimensions = dimensions

    def is_equivalent(self, other: FortranType) -> bool:
        if not isinstance(other, ArrayType):
            return False
        
        if not self.element_type.is_equivalent(other.element_type):
            return False
        
        if len(self.dimensions) != len(other.dimensions):
            return False
        
        for self_dim, other_dim in zip(self.dimensions, other.dimensions):
            if self_dim != other_dim:
                return False

    def __str__(self):
        var_len = ArrayType.variable_length()
        array_spec = ",".join([(str(dim) if dim != var_len else ':') for dim in self.dimensions])

        return f"({self.element_type})[{array_spec}]"
    
    def get_unified_with(self, other: FortranType) -> FortranType:
        if not isinstance(other, ArrayType):
            raise ValueError("Cannot unify array type with non-array type")
        
        if len(self.dimensions) != len(other.dimensions):
            raise ValueError("Cannot unify arrays with different number of dimensions")
        
        if self.dimensions != other.dimensions:
            raise ValueError("Cannot unify arrays with different dimensions")

    @staticmethod
    def variable_length():
        return -1

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

    
class FunctionType(FortranType):
    def __init__(self, return_type: FortranType, arg_types: list[FunctionArgumentForType]):
        self.return_type = return_type
        self.arg_types = arg_types

        self._first_optional_index = next((i for i, arg in enumerate(arg_types) if arg.is_optional), len(arg_types))
        if any(not arg.is_optional for arg in arg_types[self._first_optional_index:]):
            raise ValueError("Optional arguments must be at the end of the argument list")


    def is_equivalent(self, other: FortranType) -> bool:
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
        
        for self_arg, other_arg in zip(self.arg_types, arg_types):
            if not self_arg.arg_type.is_equivalent(other_arg):
                return False

        return True

    def clone(self) -> FortranType:
        return FunctionType(self.return_type.clone(), [arg.clone() for arg in self.arg_types])

class StructType(FortranType):
    def __init__(self, type_name, variable_defined_in_module):
        self.type_name = type_name
        self.original_variable_defined_in_module = variable_defined_in_module

    def is_equivalent(self, other: FortranType) -> bool:
        return self.type_name == other.name

    def get_property(self, property_name, module_dictionary):
        module_of_original_variable = module_dictionary.get_module(self.original_variable_defined_in_module)
        struct_definition = module_of_original_variable.module_context.get_symbol(self.type_name)
        return struct_definition.find_property(property_name)

    def __str__(self):
        return f"<struct {self.type_name}>"

    def clone(self) -> FortranType:
        return StructType(self.type_name, self.struct_definition)

    
class PointerType(FortranType):
    def __init__(self, element_type: FortranType):
        self.element_type = element_type

    def is_equivalent(self, other: FortranType) -> bool:
        if not isinstance(other, PointerType):
            return False
        return self.element_type.is_equivalent(other.element_type)

    def __str__(self):
        return f"({self.element_type})*"

    def clone(self) -> FortranType:
        return PointerType(self.element_type.clone())
