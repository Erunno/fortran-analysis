from parsing.definitions import GenericFunctionDefinition
from parsing.typing import FortranType, FunctionArgumentForType, FunctionType, PrimitiveType


class IntrinsicFunctionsDefinition(GenericFunctionDefinition):
    def __init__(self, name, function_type: FunctionType):
        super().__init__(
            fparser_node = None,
            definition_location = '[Intrinsic function]', 
            definition_module = '<no module>')

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
    
