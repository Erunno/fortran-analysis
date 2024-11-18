from parsing.module_dictionary import ModuleDictionary

reg_cm = 'C:\\Users\\matya\\source\\repos\\RegCM' 

d = ModuleDictionary(base_dir=reg_cm)

modules = [
'mod_moloch',
'mod_intkinds',
'mod_realkinds',
# 'mod_dynparam',
# 'mod_constants',
# 'mod_runparams',
# 'mod_mppparam',
# 'mod_mpmessage',
# 'mod_stdio',
# 'mod_service',
# 'mod_memutil',
# 'mod_atm_interface',
# 'mod_che_interface',
# 'mod_cu_interface',
# 'mod_lm_interface',
# 'mod_rad_interface',
# 'mod_pbl_interface',
# 'mod_micro_interface',
# 'mod_bdycod',
# 'mod_slice',
# 'mod_sun',
# 'mod_slabocean',
# 'mod_massck',
# 'mod_stdatm',
# 'mod_zita'
]

# for module in modules:
#     print (module)
#     module = d.get_module(module)
#     print(module)


for module in modules:
    module = d.get_module(module)
    definitions = module.definitions
    public_symbols = definitions.get_public_symbols()
    private_symbols = definitions.get_private_symbols()
    usings = definitions.get_using_statements()
    subroutines = definitions.get_subroutines()
    variables = definitions.get_variables()
    includes  = definitions.get_includes()
    
    print(f"""
'{module.name}': {'{'}
    'public': [{', '.join([f"'{s.key()}'" for s in public_symbols])}],
    'private': [{', '.join([f"'{s.key()}'" for s in private_symbols])}],
    'usings': [{', '.join([f"'{s.key()}'" for s in usings])}],
    'subroutines': [{', '.join([f"'{s.key()}'" for s in subroutines])}],
    'variables': [{', '.join([f"'{s.key()}'" for s in variables])}],
    'includes': [{', '.join([f"'{s.key()}'" for s in includes])}],
{'}'},
""")


