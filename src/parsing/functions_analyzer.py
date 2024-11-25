from parsing.context import SubroutineFunctionContext
from parsing.definitions import GenericFunctionDefinition, Interface, VariableDeclaration
from parsing.find_in_tree import find_in_tree, findall_in_tree
from parsing.module import FortranModule

from fparser.two.Fortran2003 import Program, Module, Specification_Part, \
    Module_Subprogram_Part, Use_Stmt, Subroutine_Subprogram, Access_Stmt, \
    Name, Entity_Decl_List, Include_Filename, Access_Spec, Interface_Block, \
    Interface_Stmt, Function_Subprogram, Function_Stmt, Derived_Type_Def, \
    Derived_Type_Stmt, Execution_Part, Procedure_Designator, Part_Ref, \
    Data_Ref
    

class FunctionAnalyzer:
    def __init__(self, module: FortranModule):
        self.module = module

    def analyze(self, function_name):
        function_symbol: GenericFunctionDefinition = self.module.module_local_context.get_symbol(function_name)
        function_local_context = SubroutineFunctionContext(function_symbol.get_definitions())
        context = self.module.module_context.get_expanded(function_local_context)

        used_symbols_names = self.get_used_symbols(function_symbol)
        
        for s in used_symbols_names:
            print('looking for:', s, end=' ')

            symbol = context.get_symbol(s)
            if symbol:
                print(f"found: {symbol}")
            else:
                print(f"\033[91mSymbol: {s} not found\033[0m")
        
        used_symbols = [context.get_symbol(s) for s in used_symbols_names]

        subroutines_and_functions = [s for s in used_symbols if isinstance(s, GenericFunctionDefinition)]
        interfaces = [s for s in used_symbols if isinstance(s, Interface)]
        variables = [s for s in used_symbols if isinstance(s, VariableDeclaration)]

        symbols_defined_in_function = [s for s in used_symbols_names if function_local_context.get_symbol(s)]
        outside_symbols = [s for s in used_symbols_names if s not in symbols_defined_in_function]

        print (f"\033[94mSubroutines and functions: {subroutines_and_functions}\033[0m")
        print (f"\033[94mInterfaces: {interfaces}\033[0m")
        print (f"\033[94mVariables: {[v.key() for v in variables]}\033[0m")
        print (f"\033[94mSymbols from outside: {outside_symbols}\033[0m")

    def get_used_symbols(self, function_symbol: GenericFunctionDefinition):
        execution_part = find_in_tree(function_symbol.fparser_node, Execution_Part)
        
        name_nodes = findall_in_tree(execution_part, Name)
        name_nodes = self.filter_out_members_on_types(name_nodes)

        names = list(set([n.tostr().lower() for n in name_nodes]))
        names.sort()

        return names
    
    def filter_out_members_on_types(self, names: list[Name]):
        def is_member_of_type(name: Name):
            if isinstance(name.parent, Procedure_Designator):
                # type_instance % procedure_call 
                # 0             1 2
                return name.parent.items[2] == name
            if isinstance(name.parent, Part_Ref) and isinstance(name.parent.parent, Data_Ref):
                # for cases like: tdiag%adh(j, i, k)
                return True

        excluded = [n for n in names if is_member_of_type(n)]

        for e in excluded:
            to_print = e.parent.parent if e.parent and e.parent.parent else e.parent if e.parent else e
            print(f"\033[94mExcluding identifier \033[93m{e.tostr().lower()}\033[94m in expression \033[93m{to_print}\033[0m")

        return [n for n in names if not is_member_of_type(n)]

    