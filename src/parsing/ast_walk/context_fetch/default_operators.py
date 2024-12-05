from parsing.definitions import OperatorRedefinition, SymbolDefinition
from parsing.typing import ArrayType, FunctionArgumentForType, FunctionType, PointerType, PrimitiveType

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

_unification_cases = [
    # (left_type, right_type, condition, return_type)
    (PrimitiveType, PrimitiveType,  _no_condition,              _unify_types),
    (ArrayType, ArrayType,          _no_condition,              _unify_types),
    (PointerType, PointerType,      _no_condition,              _unify_types),
    (ArrayType, PrimitiveType,      _types_are_number_based,    lambda l, r: l),
    (PointerType, PrimitiveType,    _types_are_number_based,    lambda l, r: l),
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

class DefaultOperatorContext:
    @staticmethod
    def instance():
        return DefaultOperatorContext()
    
    _ops = {
        '+': DefaultOperator.plus(),
        '/': DefaultOperator.div(),
        '*': DefaultOperator.mul(),
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
