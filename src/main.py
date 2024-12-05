from parsing.ast_walk.run_translation import run_translation
from parsing.ast_walk.symbol_collection.call_graph import GraphCollector
from parsing.functions_analyzer import FunctionAnalyzer
from parsing.module_dictionary import ModuleDictionary

reg_cm = 'C:\\Users\\matya\\source\\repos\\RegCM' 

d = ModuleDictionary(base_dir=reg_cm, skip_dirs=['Tools'])

modules = [
'mod_moloch',
'mod_intkinds',
'mod_realkinds',
'mod_dynparam',
'mod_constants',
'mod_runparams',
'mod_mppparam',
'mod_mpmessage',
'mod_stdio',
'mod_service',
'mod_memutil',
'mod_atm_interface',
'mod_che_interface',
'mod_cu_interface',
'mod_lm_interface',
'mod_rad_interface',
'mod_pbl_interface',
'mod_micro_interface',
'mod_bdycod',
'mod_slice',
'mod_sun',
'mod_slabocean',
'mod_massck',
'mod_stdatm',
'mod_zita'
]

# for module in modules:
#     print (module)
#     module = d.get_module(module)
#     print(module)


# for module in modules:
#     module = d.get_module(module)
#     definitions = module.definitions
    
#     out = f"""            '{module.name}': {'{'}
#                 'public': [{', '.join([f"'{s.key()}'" for s in definitions.get_public_symbols()])}],
#                 'private': [{', '.join([f"'{s.key()}'" for s in definitions.get_private_symbols()])}],
#                 'usings': [{', '.join([f"'{s.key()}'" for s in definitions.get_using_statements()])}],
#                 'subroutines': [{', '.join([f"'{s.key()}'" for s in definitions.get_subroutines()])}],
#                 'variables': [{', '.join([f"'{s.key()}'" for s in definitions.get_variables()])}],
#                 'includes': [{', '.join([f"'{s.key()}'" for s in definitions.get_includes()])}],
#                 'interfaces': [{', '.join([f"'{s.key()}'" for s in definitions.get_interfaces()])}],
#                 'functions': [{', '.join([f"'{s.key()}'" for s in definitions.get_functions()])}],
#                 'types': [{', '.join([f"'{s.key()}'" for s in definitions.get_types()])}],
#                 'forward_imports': [{', '.join([f"'{s.key()}'" for s in definitions.get_forward_imports()])}],
#     {'}'},"""
    
#     for line in out.split('\n'):
#         print(line)


# module = d.get_module('mod_moloch')

# analyzer = FunctionAnalyzer(module)

# analyzer.analyze('moloch', d)

# run_translation(
#     module_dict=d,
#     module_name='mod_moloch',
#     function_name='moloch'
# )

# run_translation(
#     module_dict=d,
#     module_name='mod_timer',
#     function_name='step_timer'
# )

collector = GraphCollector(module_dict=d)

all_symbols = collector.collect_all_symbols('mod_moloch', 'moloch')

print('refereed symbols:')

for symbol in all_symbols.symbols:
    print(symbol)
