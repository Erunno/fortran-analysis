import os
import sys
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from parsing.module_dictionary import ModuleDictionary
from parsing.definitions import FortranDefinitions
import _evn_specific_params as params

class TestFortranDefinitions(unittest.TestCase):
    def setUp(self):
        self.reg_cm = params.root_reg_cm 
        self.d = ModuleDictionary(base_dir=self.reg_cm)

    def test_fortran_definitions_not_NONEs(self):
        module_name = 'mod_moloch'
        module = self.d.get_module(module_name)
        self.assertIsNotNone(module)
        self.assertIsNotNone(module.ast)

        definitions = module.definitions
        self.assertIsNotNone(definitions)

        public_symbols = definitions.get_public_symbols()
        self.assertGreater(len(public_symbols), 0)

    @parameterized.expand([
        ('mod_moloch',),
        ('mod_intkinds',),
        ('mod_realkinds',),
        ('mod_dynparam',),
        ('mod_constants',),
        ('mod_runparams',),
        ('mod_mppparam',),
        ('mod_mpmessage',),
        ('mod_stdio',),
        ('mod_service',),
        ('mod_memutil',),
        ('mod_atm_interface',),
        ('mod_che_interface',),
        ('mod_cu_interface',),
        ('mod_lm_interface',),
        ('mod_rad_interface',),
        ('mod_pbl_interface',),
        ('mod_micro_interface',),
        ('mod_bdycod',),
        ('mod_slice',),
        ('mod_sun',),
        ('mod_slabocean',),
        ('mod_massck',),
        ('mod_stdatm',),
        ('mod_zita',)
    ])
    def test_public_symbols(self, module_name):
        module = self.d.get_module(module_name)
        definitions = module.definitions
        public_symbols = definitions.get_public_symbols()


    def get_expected_per_module(self, module_name):
        return {
            '': {
                'public': [],
                'private': [],
                'usings': [],
                'subroutines': [],
                'variables': [],
            }
        }
        

        

if __name__ == '__main__':
    unittest.main()
