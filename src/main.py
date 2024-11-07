import module_dictionary

reg_cm = 'C:\\Users\\matya\\source\\repos\\RegCM' 

d = module_dictionary.ModuleDictionary(base_dir=reg_cm)

modules = [
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

for module in modules:
    d.get_module(module).print_info()