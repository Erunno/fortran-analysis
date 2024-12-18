import os
import sys
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from parsing.module_dictionary import ModuleDictionary
import _evn_specific_params as params
from parameterized import parameterized

class TestModuleDictionary(unittest.TestCase):
    def setUp(self):
        self.reg_cm = params.root_reg_cm 
        self.d = ModuleDictionary(base_dir=self.reg_cm, skip_dirs=['Tools'])

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
    def test_get_module(self, module_name):
        module = self.d.get_module(module_name)
        self.assertIsNotNone(module)
        self.assertIsNotNone(module.ast)