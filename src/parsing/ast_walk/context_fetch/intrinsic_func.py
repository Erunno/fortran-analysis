from parsing.definitions import GenericFunctionDefinition, SymbolInitParams
from parsing.module import FortranModule
from parsing.typing import ArrayType, FortranType, FunctionArgumentForType, FunctionType, PrimitiveType


class IntrinsicsHolderModule(FortranModule):
    def __init__(self):
        pass
    
    _instance = None
    @staticmethod
    def instance():
        if not IntrinsicsHolderModule._instance:
            IntrinsicsHolderModule._instance = IntrinsicsHolderModule()
        return IntrinsicsHolderModule._instance
    
    def key(self):
        return 'IntrinsicsHolderModule'
    
    def class_label(self):
        return 'IntrinsicsHolderModule'

class IntrinsicFunctionsDefinition(GenericFunctionDefinition):
    def __init__(self, name, function_type: FunctionType):
        super().__init__(SymbolInitParams(
            fparser_node = None, definition_location_symbol=IntrinsicsHolderModule.instance()))

        self.name = name
        self._type = function_type

    def key(self):
        return self.name

    def class_label(self):
        return 'IntrinsicFunction'

    def get_actual_function_symbol(self):
        return self
    
    def get_type(self):
        return self._type

    @staticmethod
    def get_real():
        type = FunctionType(
            return_type=PrimitiveType.get_real_instance().with_any_kind(),
            arg_types=[
                FunctionArgumentForType('a', PrimitiveType.get_any_number_instance(), is_optional=False),
                FunctionArgumentForType('kind', PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False)
            ]
        )

        return IntrinsicFunctionsDefinition('real', type)

    @staticmethod
    def get_int():
        type = FunctionType(
            return_type=PrimitiveType.get_integer_instance().with_any_kind(),
            arg_types=[
                FunctionArgumentForType('a', PrimitiveType.get_any_number_instance(), is_optional=False),
                FunctionArgumentForType('kind', PrimitiveType.get_integer_instance().with_any_kind(), is_optional=False)
            ]
        )

        return IntrinsicFunctionsDefinition('int', type)

    @staticmethod
    def get_exp():
        type = FunctionType(
            return_type=PrimitiveType.get_real_instance().with_any_kind(),
            arg_types=[
                FunctionArgumentForType('x', PrimitiveType.get_any_number_instance(), is_optional=False)
            ]
        )

        return IntrinsicFunctionsDefinition('exp', type)
    
    @staticmethod
    def get_maxval():
        type = FunctionType(
            return_type=PrimitiveType.get_any_number_instance(),
            arg_types=[
                FunctionArgumentForType('array', PrimitiveType.get_any_number_instance(), is_optional=False)
            ]
        )

        return IntrinsicFunctionsDefinition('maxval', type)
    
    @staticmethod
    def get_minval():
        type = FunctionType(
            return_type=PrimitiveType.get_any_number_instance(),
            arg_types=[
                FunctionArgumentForType('array', PrimitiveType.get_any_number_instance(), is_optional=False)
            ]
        )

        return IntrinsicFunctionsDefinition('minval', type)

    @staticmethod
    def get_mod():
        type = FunctionType(
            return_type=PrimitiveType.get_any_number_instance(),
            arg_types=[
                FunctionArgumentForType('a', PrimitiveType.get_any_number_instance(), is_optional=False),
                FunctionArgumentForType('p', PrimitiveType.get_any_number_instance(), is_optional=False)
            ]
        )

        return IntrinsicFunctionsDefinition('mod', type)
    
    @staticmethod
    def get_trim():
        type = FunctionType(
            return_type=PrimitiveType.get_string_instance().with_attribute('len', '*'),
            arg_types=[
                FunctionArgumentForType('input_string', PrimitiveType.get_string_instance().any_kind(), is_optional=False)
            ]
        )

        return IntrinsicFunctionsDefinition('trim', type)

    @staticmethod
    def get_log():
        type = FunctionType(
            return_type=PrimitiveType.get_real_instance().with_any_kind(),
            arg_types=[
                FunctionArgumentForType('x', PrimitiveType.get_any_number_instance(), is_optional=False)
            ]
        )

        return IntrinsicFunctionsDefinition('log', type)

    @staticmethod
    def get_max():
        type = FunctionType(
            return_type=PrimitiveType.get_any_number_instance(),
            arg_types=[
                FunctionArgumentForType('a', PrimitiveType.get_any_number_instance(), is_optional=False),
                FunctionArgumentForType('b', PrimitiveType.get_any_number_instance(), is_optional=False),
                FunctionArgumentForType('c', PrimitiveType.get_any_number_instance(), is_optional=True),
                FunctionArgumentForType('d', PrimitiveType.get_any_number_instance(), is_optional=True),
                FunctionArgumentForType('e', PrimitiveType.get_any_number_instance(), is_optional=True),
                FunctionArgumentForType('f', PrimitiveType.get_any_number_instance(), is_optional=True),
                FunctionArgumentForType('g', PrimitiveType.get_any_number_instance(), is_optional=True),
                FunctionArgumentForType('h', PrimitiveType.get_any_number_instance(), is_optional=True),
                FunctionArgumentForType('i', PrimitiveType.get_any_number_instance(), is_optional=True),
                FunctionArgumentForType('j', PrimitiveType.get_any_number_instance(), is_optional=True),
            ]
        )

        return IntrinsicFunctionsDefinition('max', type)
    
    @staticmethod
    def get_min():
        type = FunctionType(
            return_type=PrimitiveType.get_any_number_instance(),
            arg_types=[
                FunctionArgumentForType('a', PrimitiveType.get_any_number_instance(), is_optional=False),
                FunctionArgumentForType('b', PrimitiveType.get_any_number_instance(), is_optional=False),
                FunctionArgumentForType('c', PrimitiveType.get_any_number_instance(), is_optional=True),
                FunctionArgumentForType('d', PrimitiveType.get_any_number_instance(), is_optional=True),
                FunctionArgumentForType('e', PrimitiveType.get_any_number_instance(), is_optional=True),
                FunctionArgumentForType('f', PrimitiveType.get_any_number_instance(), is_optional=True),
                FunctionArgumentForType('g', PrimitiveType.get_any_number_instance(), is_optional=True),
                FunctionArgumentForType('h', PrimitiveType.get_any_number_instance(), is_optional=True),
                FunctionArgumentForType('i', PrimitiveType.get_any_number_instance(), is_optional=True),
                FunctionArgumentForType('j', PrimitiveType.get_any_number_instance(), is_optional=True),
            ]
        )

        return IntrinsicFunctionsDefinition('min', type)

    @staticmethod
    def get_sqrt():
        type = FunctionType(
            return_type=PrimitiveType.get_real_instance().with_any_kind(),
            arg_types=[
                FunctionArgumentForType('x', PrimitiveType.get_any_number_instance(), is_optional=False)
            ]
        )

        return IntrinsicFunctionsDefinition('sqrt', type)

    @staticmethod
    def get_abs():
        type = FunctionType(
            return_type=PrimitiveType.get_any_number_instance(),
            arg_types=[
                FunctionArgumentForType('x', PrimitiveType.get_any_number_instance(), is_optional=False)
            ]
        )

        return IntrinsicFunctionsDefinition('abs', type)
    
    @staticmethod
    def get_any():
        type = FunctionType(
            return_type=PrimitiveType.get_logical_instance(),
            arg_types=[
                FunctionArgumentForType('a', PrimitiveType.get_any_number_instance(), is_optional=False),
                FunctionArgumentForType('b', PrimitiveType.get_any_number_instance(), is_optional=True),
                FunctionArgumentForType('c', PrimitiveType.get_any_number_instance(), is_optional=True),
                FunctionArgumentForType('d', PrimitiveType.get_any_number_instance(), is_optional=True),
                FunctionArgumentForType('e', PrimitiveType.get_any_number_instance(), is_optional=True),
            ]
        )

        return IntrinsicFunctionsDefinition('any', type)
    
    @staticmethod
    def get_all():
        type = FunctionType(
            return_type=PrimitiveType.get_logical_instance(),
            arg_types=[
                FunctionArgumentForType('a', PrimitiveType.get_any_number_instance(), is_optional=False),
                FunctionArgumentForType('b', PrimitiveType.get_any_number_instance(), is_optional=True),
                FunctionArgumentForType('c', PrimitiveType.get_any_number_instance(), is_optional=True),
                FunctionArgumentForType('d', PrimitiveType.get_any_number_instance(), is_optional=True),
                FunctionArgumentForType('e', PrimitiveType.get_any_number_instance(), is_optional=True),
            ]
        )

        return IntrinsicFunctionsDefinition('all', type)
    
    @staticmethod
    def get_sum():
        type = FunctionType(
            return_type=PrimitiveType.get_any_number_instance(),
            arg_types=[
                FunctionArgumentForType('array', ArrayType.any_array(PrimitiveType.get_any_number_instance()), is_optional=False),
                FunctionArgumentForType('dim', PrimitiveType.get_integer_instance().with_any_kind(), is_optional=True),
                FunctionArgumentForType('mask', PrimitiveType.get_logical_instance().with_any_kind(), is_optional=True),
            ]
        )

        return IntrinsicFunctionsDefinition('sum', type)

    @staticmethod
    def get_size():
        type = FunctionType(
            return_type=PrimitiveType.get_integer_instance().with_any_kind(),
            arg_types=[
                FunctionArgumentForType('array', ArrayType.any_array(PrimitiveType.get_any_number_instance()), is_optional=False),
                FunctionArgumentForType('dim', PrimitiveType.get_integer_instance().with_any_kind(), is_optional=True),
                FunctionArgumentForType('kind', PrimitiveType.get_integer_instance().with_any_kind(), is_optional=True),
            ]
        )

        return IntrinsicFunctionsDefinition('size', type)