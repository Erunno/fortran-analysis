from parsing.definitions import OperatorRedefinition, SymbolDefinition
from parsing.typing import ArrayType, FortranType, FunctionArgumentForType, FunctionType, PointerType, PrimitiveType

class DefaultOperatorFunctionSymbol:
    def __init__(self, l_type, r_type, return_type):
        self._l_type = l_type
        self._r_type = r_type
        self._return_type = return_type

    def get_type(self):
        return FunctionType(
            return_type=self._return_type,
            arg_types=[
                FunctionArgumentForType('l_operand', self._l_type, is_optional=False), 
                FunctionArgumentForType('r_operand', self._r_type, is_optional=False)]
        )
    
    def is_default(self):
        return True

def _types_are_number_based(l_type, r_type):
    def _is_number_based(t):
        if isinstance(t, PointerType):
            return _is_number_based(t.element_type)
        if isinstance(t, ArrayType):
            return _is_number_based(t.element_type)
        
        return PrimitiveType.is_number(t)
    
    return _is_number_based(l_type) and _is_number_based(r_type)

def _no_condition(l, r):
    return True

def _unify_types(l, r):
    return l.get_unified_with(r)

def _return_bool(l, r):
    return PrimitiveType.get_logical_instance().with_any_kind()

def _are_equivalent(l, r):
    return l.is_equivalent(r)

def _return_left(l, r):
    return l

def _return_right(l, r):
    return r

def _return_bool_array_of_same_size(l: ArrayType | PointerType, r):
    if not isinstance(l, PointerType):
        return PointerType(_return_bool_array_of_same_size(l.element_type, r))
    
    return ArrayType(PrimitiveType.get_logical_instance().with_any_kind(), l.dimensions)


_unification_cases = [
    # (left_type, right_type, condition, return_type)
    (PrimitiveType, PrimitiveType,  _no_condition,              _unify_types),
    (ArrayType, ArrayType,          _no_condition,              _unify_types),
    (PointerType, PointerType,      _no_condition,              _unify_types),

    (ArrayType, PrimitiveType,      _types_are_number_based,    _return_left),
    (PointerType, PrimitiveType,    _types_are_number_based,    _return_left),
    
    (PrimitiveType, ArrayType,      _types_are_number_based,    _return_right),
    (PrimitiveType, PointerType,    _types_are_number_based,    _return_right),
]

_logical_unification_cases = [
    # (left_type, right_type, condition, return_type)
    (PrimitiveType, PrimitiveType,  _no_condition,              _return_bool),
    (ArrayType, ArrayType,          _are_equivalent,            _return_left),
    (PointerType, PointerType,      _are_equivalent,            _return_left),
    (ArrayType, PrimitiveType,      _types_are_number_based,    _return_bool_array_of_same_size),
    (PointerType, PrimitiveType,    _types_are_number_based,    _return_bool_array_of_same_size),
]

class DefaultOperator(OperatorRedefinition):
    def __init__(self, op_sign: str, input_cases):
        self._operator_sign = op_sign
        self._input_cases = input_cases

    def class_label(self):
        return "DefaultOperator"

    def operator_sign(self):
        return self._operator_sign
    
    def defines_operator_for(self, left_type, right_type):
        f_symbol = self.get_function_symbol_for_types(left_type, right_type)
        return f_symbol is not None
    
    def get_function_symbol_for_types(self, left_type, right_type):
        for l_type, r_type, condition, return_type in _unification_cases:
            if isinstance(left_type, l_type) and isinstance(right_type, r_type) and condition(left_type, right_type):
                return DefaultOperatorFunctionSymbol(left_type, right_type, return_type(left_type, right_type))

    def is_default(self):
        return True

    @staticmethod
    def plus():
        return DefaultOperator("+", _unification_cases)

    @staticmethod
    def div():
        return DefaultOperator("/", _unification_cases)

    @staticmethod
    def mul():
        return DefaultOperator("*", _unification_cases)
    
    @staticmethod
    def eq():
        return DefaultOperator("==", _logical_unification_cases)
    
    @staticmethod
    def or_():
        return DefaultOperator(".or.", _logical_unification_cases)
    
    @staticmethod
    def and_():
        return DefaultOperator(".and.", _logical_unification_cases)
    

class DefaultOperatorContext:
    
    _instance = None

    @staticmethod
    def instance():
        if not DefaultOperatorContext._instance:
            DefaultOperatorContext._instance = DefaultOperatorContext()
        return DefaultOperatorContext._instance
    
    _ops = {
        '+':     DefaultOperator.plus(),
        '/':     DefaultOperator.div(),
        '*':     DefaultOperator.mul(),
        '==':    DefaultOperator.eq(),
        '.or.':  DefaultOperator.or_(),
        '.and.': DefaultOperator.and_(),
    }

    def get_symbol(self, _):
        return None
    
    def get_operator(self, operator: str):
        return self._ops.get(operator)
    
    def get_operator_symbols(self, op: str):
        ops = [self.get_operator(op)] if op in self._ops else []
        
        if len(ops) != 0:
            pass

        return ops
