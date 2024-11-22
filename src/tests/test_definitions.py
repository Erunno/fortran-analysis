import os
import sys
import unittest
from parameterized import parameterized

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from parsing.module_dictionary import ModuleDictionary
from parsing.definitions import FortranDefinitions
import _evn_specific_params as params

class TestFortranDefinitions(unittest.TestCase):
    def setUp(self):
        self.reg_cm = params.root_reg_cm 
        self.d = ModuleDictionary(base_dir=self.reg_cm, skip_dirs=['Tools'])

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
    def test_symbol_names(self, module_name):
        module = self.d.get_module(module_name)
        definitions = module.definitions

        actual = {
            'public': [s.key() for s in definitions.get_public_symbols()],
            'private': [s.key() for s in definitions.get_private_symbols()],
            'usings': [s.key() for s in definitions.get_using_statements()],
            'subroutines': [s.key() for s in definitions.get_subroutines()],
            'variables': [s.key() for s in definitions.get_variables()],
            'includes': [s.key() for s in definitions.get_includes()],
            'interfaces': [s.key() for s in definitions.get_interfaces()],
            'functions': [s.key() for s in definitions.get_functions()],
            'types': [s.key() for s in definitions.get_types()],
            'forward_imports': [s.key() for s in definitions.get_forward_imports()],
        }       

        expected = self.get_expected_per_module(module_name)[module_name]

        self.assertEqual(actual, expected)


    def load_definitions_object(self, module_name):
        module = self.d.get_module(module_name)
        definitions = module.definitions
        return definitions


    def get_expected_per_module(self, module_name):
        return {
            'mod_moloch': {
                'public': ['allocate_moloch', 'init_moloch', 'moloch'],
                'private': ['s', 'wx', 'deltaw', 'tkex', 'wz', 'mx2', 'rmu', 'rmv', 'p0', 'zdiv2', 'ten0', 'qen0', 'chiten0', 'gzitak', 'gzitakh', 'xknu', 'p2d', 'xlat', 'xlon', 'coru', 'corv', 'mu', 'hx', 'mx', 'mv', 'hy', 'ps', 'ts', 'ht', 'fmz', 'fmzf', 'pai', 'pf', 'tetav', 'tf', 'tvirt', 'zeta', 'zetau', 'zetav', 'u', 'v', 'w', 'ux', 'vx', 'ud', 'vd', 'p', 't', 'rho', 'qv', 'qc', 'qi', 'qr', 'qs', 'qsat', 'qwltot', 'qwitot', 'tke', 'qx', 'trac', 'minden', 'xdamp', 'do_fulleq', 'do_bdy', 'do_divdamp', 'do_vadvtwice', 'do_filterpai', 'do_filtertheta', 'do_phys', 'do_convection', 'do_microphysics', 'do_radiation', 'do_surface', 'do_pbl', 'moloch_realcase', 'lrotllr', 'nupaitq', 'dzita', 'jmin', 'jmax', 'imin', 'imax', 'wstagtox', 'xtowstag', 'xtoustag', 'xtovstag', 'xtouvstag', 'uvstagtox', 'pfesat', 'pfesat_water', 'pfesat_ice', 'pfwsat'],
                'usings': ['mod_intkinds', 'mod_realkinds', 'mod_dynparam', 'mod_constants', 'mod_runparams', 'mod_mppparam', 'mod_mpmessage', 'mod_stdio', 'mod_service', 'mod_memutil', 'mod_atm_interface', 'mod_che_interface', 'mod_cu_interface', 'mod_lm_interface', 'mod_rad_interface', 'mod_pbl_interface', 'mod_micro_interface', 'mod_bdycod', 'mod_slice', 'mod_sun', 'mod_slabocean', 'mod_massck', 'mod_stdatm', 'mod_zita'],
                'subroutines': ['allocate_moloch', 'init_moloch', 'moloch', 'wstagtox', 'xtowstag', 'xtoustag', 'xtovstag', 'xtouvstag', 'uvstagtox'],
                'variables': ['s', 'wx', 'deltaw', 'tkex', 'wz', 'mx2', 'rmu', 'rmv', 'p0', 'zdiv2', 'ten0', 'qen0', 'chiten0', 'gzitak', 'gzitakh', 'xknu', 'p2d', 'xlat', 'xlon', 'coru', 'corv', 'mu', 'hx', 'mx', 'mv', 'hy', 'ps', 'ts', 'ht', 'fmz', 'fmzf', 'pai', 'pf', 'tetav', 'tf', 'tvirt', 'zeta', 'zetau', 'zetav', 'u', 'v', 'w', 'ux', 'vx', 'ud', 'vd', 'p', 't', 'rho', 'qv', 'qc', 'qi', 'qr', 'qs', 'qsat', 'qwltot', 'qwitot', 'tke', 'qx', 'trac', 'minden', 'xdamp', 'do_fulleq', 'do_bdy', 'do_divdamp', 'do_vadvtwice', 'do_filterpai', 'do_filtertheta', 'do_phys', 'do_convection', 'do_microphysics', 'do_radiation', 'do_surface', 'do_pbl', 'moloch_realcase', 'lrotllr', 'nupaitq', 'dzita', 'jmin', 'jmax', 'imin', 'imax'],
                'includes': [],
                'interfaces': [],
                'functions': ['pfesat', 'pfesat_water', 'pfesat_ice', 'pfwsat'],
                'types': [],
                'forward_imports': [],
    },
            'mod_intkinds': {
                'public': ['ik8', 'ik4', 'ik2', 'ik1', 'bigint'],
                'private': [],
                'usings': ['iso_fortran_env'],
                'subroutines': [],
                'variables': ['ik8', 'ik4', 'ik2', 'ik1', 'bigint'],
                'includes': [],
                'interfaces': [],
                'functions': [],
                'types': [],
                'forward_imports': [],
    },
            'mod_realkinds': {
                'public': ['rk4', 'rk8', 'rk16', 'rkx', 'nan', 'inf', 'is_nan', 'is_inf', 'is_nan_double', 'is_inf_double', 'is_nan_single', 'is_inf_single'],
                'private': [],
                'usings': ['iso_fortran_env', 'ieee_arithmetic'],
                'subroutines': [],
                'variables': ['rk4', 'rk8', 'rk16', 'rkx', 'nan', 'inf'],
                'includes': [],
                'interfaces': ['is_nan', 'is_inf'],
                'functions': ['is_nan_double', 'is_inf_double', 'is_nan_single', 'is_inf_single'],
                'types': [],
                'forward_imports': [],
    },
            'mod_dynparam': {
                'public': ['iy', 'jx', 'kz', 'dsmax', 'dsmin', 'nsg', 'idynamic', 'iproj', 'i_band', 'i_crm', 'lakedpth', 'lsmoist', 'ds', 'ptop', 'clat', 'cntri', 'clon', 'cntrj', 'plat', 'plon', 'xcone', 'truelatl', 'truelath', 'ismthlev', 'debug_level', 'dbgfrq', 'nspgx', 'nspgd', 'bdy_nm', 'bdy_dm', 'high_nudge', 'medium_nudge', 'low_nudge', 'dattyp', 'cmip6_inp', 'cmip6_model', 'cmip6_variant', 'cmip6_experiment', 'cmip6_grid', 'pmip4_inp', 'pmip4_model', 'pmip4_variant', 'pmip4_experiment', 'pmip4_grid', 'chemtyp', 'ssttyp', 'nveg', 'ntr', 'base_state_pressure', 'logp_lrate', 'mo_ztop', 'mo_h', 'mo_a0', 'iym1', 'iym2', 'iym3', 'jxm1', 'jxm2', 'jxm3', 'kzm1', 'kzm2', 'kzp1', 'kzp2', 'kzp3', 'kzp4', 'iysg', 'jxsg', 'iym1sg', 'jxm1sg', 'iym2sg', 'jxm2sg', 'iym3sg', 'jxm3sg', 'nnsg', 'njcross', 'njdot', 'njout', 'njoutsg', 'nicross', 'nidot', 'niout', 'nioutsg', 'jcross1', 'icross1', 'jcross2', 'icross2', 'jdot1', 'idot1', 'jdot2', 'idot2', 'jout1', 'iout1', 'jout2', 'iout2', 'joutsg1', 'ioutsg1', 'joutsg2', 'ioutsg2', 'ide1', 'ide2', 'jde1', 'jde2', 'ide1sg', 'ide2sg', 'jde1sg', 'jde2sg', 'idi1', 'idi2', 'jdi1', 'jdi2', 'idii1', 'idii2', 'jdii1', 'jdii2', 'ice1', 'ice2', 'jce1', 'jce2', 'ici1', 'ici2', 'jci1', 'jci2', 'icii1', 'icii2', 'jcii1', 'jcii2', 'ici1ga', 'ici2ga', 'jci1ga', 'jci2ga', 'ice1ga', 'ice2ga', 'jce1ga', 'jce2ga', 'ide1ga', 'ide2ga', 'jde1ga', 'jde2ga', 'idi1ga', 'idi2ga', 'jdi1ga', 'jdi2ga', 'ici1gb', 'ici2gb', 'jci1gb', 'jci2gb', 'ice1gb', 'ice2gb', 'jce1gb', 'jce2gb', 'ide1gb', 'ide2gb', 'jde1gb', 'jde2gb', 'idi1gb', 'idi2gb', 'jdi1gb', 'jdi2gb', 'ici1gc', 'ici2gc', 'jci1gc', 'jci2gc', 'ice1gc', 'ice2gc', 'jce1gc', 'jce2gc', 'ide1gc', 'ide2gc', 'jde1gc', 'jde2gc', 'idi1gc', 'idi2gc', 'jdi1gc', 'jdi2gc', 'ici1sl', 'ici2sl', 'jci1sl', 'jci2sl', 'ice1sl', 'ice2sl', 'jce1sl', 'jce2sl', 'ide1sl', 'ide2sl', 'jde1sl', 'jde2sl', 'idi1sl', 'idi2sl', 'jdi1sl', 'jdi2sl', 'mycomm', 'nproc', 'nprocshm', 'myid', 'myidshm', 'njxcpus', 'niycpus', 'iyp', 'jxp', 'iypsg', 'jxpsg', 'h2opct', 'h2ohgt', 'lresamp', 'roidem', 'smthbdy', 'fudge_lnd', 'fudge_lnd_s', 'fudge_tex', 'fudge_tex_s', 'fudge_lak', 'fudge_lak_s', 'domname', 'prestr', 'globidate1', 'globidate2', 'calendar', 'ical', 'dayspy', 'vernal_equinox', 'half_dayspy', 'sixteenth_dayspy', 'dpd', 'mpy', 'ntex', 'nats', 'ndpmax', 'nspi', 'npgwlev', 'num_soil_layers', 'pthsep', 'dirter', 'inpter', 'dirglob', 'inpglob', 'dirout', 'moist_filename', 'tersrc', 'smsrc', 'iomode', 'ncfilter', 'ncfilter_nparams', 'max_filter_params', 'ncfilter_params', 'ifsave', 'ifatm', 'ifshf', 'ifrad', 'ifsrf', 'ifsub', 'ifsts', 'iflak', 'ifopt', 'ifchem', 'ifcordex', 'outnwf', 'savfrq', 'atmfrq', 'radfrq', 'lakfrq', 'subfrq', 'srffrq', 'chemfrq', 'optfrq', 'ibdyfrq', 'ensemble_run', 'lperturb_topo', 'lperturb_ts', 'lperturb_ps', 'lperturb_t', 'lperturb_q', 'lperturb_u', 'lperturb_v', 'perturb_frac_topo', 'perturb_frac_ts', 'perturb_frac_ps', 'perturb_frac_t', 'perturb_frac_q', 'perturb_frac_u', 'perturb_frac_v', 'lclm45lake', 'initparam', 'init_fnestparam', 'init_globwindow'],
                'private': ['h5gzipcode'],
                'usings': ['mod_stdio', 'mod_intkinds', 'mod_realkinds', 'mod_constants', 'mod_date', 'netcdf'],
                'subroutines': ['initparam', 'init_fnestparam', 'init_globwindow'],
                'variables': ['iy', 'jx', 'kz', 'dsmax', 'dsmin', 'nsg', 'idynamic', 'iproj', 'i_band', 'i_crm', 'lakedpth', 'lsmoist', 'ds', 'ptop', 'clat', 'cntri', 'clon', 'cntrj', 'plat', 'plon', 'xcone', 'truelatl', 'truelath', 'ismthlev', 'debug_level', 'dbgfrq', 'nspgx', 'nspgd', 'bdy_nm', 'bdy_dm', 'high_nudge', 'medium_nudge', 'low_nudge', 'dattyp', 'cmip6_inp', 'cmip6_model', 'cmip6_variant', 'cmip6_experiment', 'cmip6_grid', 'pmip4_inp', 'pmip4_model', 'pmip4_variant', 'pmip4_experiment', 'pmip4_grid', 'chemtyp', 'ssttyp', 'nveg', 'ntr', 'base_state_pressure', 'logp_lrate', 'mo_ztop', 'mo_h', 'mo_a0', 'iym1', 'iym2', 'iym3', 'jxm1', 'jxm2', 'jxm3', 'kzm1', 'kzm2', 'kzp1', 'kzp2', 'kzp3', 'kzp4', 'iysg', 'jxsg', 'iym1sg', 'jxm1sg', 'iym2sg', 'jxm2sg', 'iym3sg', 'jxm3sg', 'nnsg', 'njcross', 'njdot', 'njout', 'njoutsg', 'nicross', 'nidot', 'niout', 'nioutsg', 'jcross1', 'icross1', 'jcross2', 'icross2', 'jdot1', 'idot1', 'jdot2', 'idot2', 'jout1', 'iout1', 'jout2', 'iout2', 'joutsg1', 'ioutsg1', 'joutsg2', 'ioutsg2', 'ide1', 'ide2', 'jde1', 'jde2', 'ide1sg', 'ide2sg', 'jde1sg', 'jde2sg', 'idi1', 'idi2', 'jdi1', 'jdi2', 'idii1', 'idii2', 'jdii1', 'jdii2', 'ice1', 'ice2', 'jce1', 'jce2', 'ici1', 'ici2', 'jci1', 'jci2', 'icii1', 'icii2', 'jcii1', 'jcii2', 'ici1ga', 'ici2ga', 'jci1ga', 'jci2ga', 'ice1ga', 'ice2ga', 'jce1ga', 'jce2ga', 'ide1ga', 'ide2ga', 'jde1ga', 'jde2ga', 'idi1ga', 'idi2ga', 'jdi1ga', 'jdi2ga', 'ici1gb', 'ici2gb', 'jci1gb', 'jci2gb', 'ice1gb', 'ice2gb', 'jce1gb', 'jce2gb', 'ide1gb', 'ide2gb', 'jde1gb', 'jde2gb', 'idi1gb', 'idi2gb', 'jdi1gb', 'jdi2gb', 'ici1gc', 'ici2gc', 'jci1gc', 'jci2gc', 'ice1gc', 'ice2gc', 'jce1gc', 'jce2gc', 'ide1gc', 'ide2gc', 'jde1gc', 'jde2gc', 'idi1gc', 'idi2gc', 'jdi1gc', 'jdi2gc', 'ici1sl', 'ici2sl', 'jci1sl', 'jci2sl', 'ice1sl', 'ice2sl', 'jce1sl', 'jce2sl', 'ide1sl', 'ide2sl', 'jde1sl', 'jde2sl', 'idi1sl', 'idi2sl', 'jdi1sl', 'jdi2sl', 'mycomm', 'nproc', 'nprocshm', 'myid', 'myidshm', 'njxcpus', 'niycpus', 'iyp', 'jxp', 'iypsg', 'jxpsg', 'h2opct', 'h2ohgt', 'lresamp', 'roidem', 'smthbdy', 'fudge_lnd', 'fudge_lnd_s', 'fudge_tex', 'fudge_tex_s', 'fudge_lak', 'fudge_lak_s', 'domname', 'prestr', 'globidate1', 'globidate2', 'calendar', 'ical', 'dayspy', 'vernal_equinox', 'half_dayspy', 'sixteenth_dayspy', 'dpd', 'mpy', 'ntex', 'nats', 'ndpmax', 'nspi', 'npgwlev', 'num_soil_layers', 'pthsep', 'dirter', 'inpter', 'dirglob', 'inpglob', 'dirout', 'moist_filename', 'tersrc', 'smsrc', 'iomode', 'h5gzipcode', 'ncfilter', 'ncfilter_nparams', 'max_filter_params', 'ncfilter_params', 'ifsave', 'ifatm', 'ifshf', 'ifrad', 'ifsrf', 'ifsub', 'ifsts', 'iflak', 'ifopt', 'ifchem', 'ifcordex', 'outnwf', 'savfrq', 'atmfrq', 'radfrq', 'lakfrq', 'subfrq', 'srffrq', 'chemfrq', 'optfrq', 'ibdyfrq', 'ensemble_run', 'lperturb_topo', 'lperturb_ts', 'lperturb_ps', 'lperturb_t', 'lperturb_q', 'lperturb_u', 'lperturb_v', 'perturb_frac_topo', 'perturb_frac_ts', 'perturb_frac_ps', 'perturb_frac_t', 'perturb_frac_q', 'perturb_frac_u', 'perturb_frac_v', 'lclm45lake'],
                'includes': [],
                'interfaces': [],
                'functions': [],
                'types': [],
                'forward_imports': [],
    },
            'mod_constants': {
                'public': ['d_zero', 'd_one', 'd_two', 'd_three', 'd_four', 'd_five', 'd_six', 'd_nine', 'd_half', 'd_rfour', 'd_twelve', 'd_60', 'd_10', 'd_r10', 'd_100', 'd_r100', 'd_1000', 'd_r1000', 'onet', 'twot', 'fourt', 'deg00', 'deg45', 'deg90', 'deg180', 'deg360', 'minqq', 'minqc', 'minqv', 'mintr', 'minqx', 'dlowval', 'dhival', 'slowval', 'shival', 'dmissval', 'smissval', 'secpm', 'secph', 'secpd', 'rsecpd', 'minph', 'minpd', 'houpd', 'egrav', 'speedoflight', 'plankconstant', 'sigm', 'boltzk', 'navgdr', 'amd', 'amw', 'amo2', 'amo3', 'amco2', 'amn2o', 'amch4', 'amcfc11', 'amcfc12', 'pdbratio', 'rgasmol', 'c287', 'rgas', 'rwat', 'rdry', 'rgow', 'rgowi', 'cpd', 'cpv', 'cvd', 'cpw', 'cpi', 'cpw0', 'cp_h2o', 'ch2o', 'shice', 'cwi', 'csnw', 'cws', 'spcpfw', 'spcpsw', 'spcpice', 'wlhv', 'wlhf', 'wlhs', 'rwlhv', 'rwlhf', 'rwlhs', 'regrav', 'rcpd', 'rovcp', 'rdrcv', 'cpovr', 'rovg', 'govr', 'gdry', 'hcratio', 'hcrm1', 'rhoh2o', 'rhosea', 'rhosnow', 'rhosnowp', 'rhoice', 'tzero', 'tiso', 'rtzero', 'wattp', 'tboil', 'c1es', 'c2es', 'c3les', 'c3ies', 'c4les', 'c4ies', 'c5les', 'c5ies', 'c5alvcp', 'c5alscp', 'wlhvocp', 'wlhsocp', 'wlhfocp', 'cpowlhv', 'cpowlhs', 'cpowlhf', 'rtber', 'rtice', 'rtwat', 'mpcrt', 'rtwat_rtice_r', 'pq0', 'eliwv', 'p00', 'stdp', 'stdpmb', 'stdpcb', 'stdt', 'stdrho', 'lrate', 'atmos', 'rtcon', 'rumolec', 'dropdif', 'difgas', 'm_euler', 'mathpi', 'invpi', 'halfpi', 'quartpi', 'twopi', 'pisqr', 'degrad', 'raddeg', 'rmax0', 'dewmax', 'dewmaxi', 'trsmx0', 'drain', 'minwrat', 'earthrad', 'erkm', 'rearthrad', 'eomeg', 'eomeg2', 'zlnd', 'zoce', 'zsno', 'vonkar', 'csoilc', 'wtur', 'ep1', 'ep2', 'rep2', 'xlv0', 'xlv1', 'xls0', 'xls1', 'avt', 'bvt', 'g4pb', 'g3pb', 'g5pb', 'vtc', 'alpha_hyd', 'beta_hyd', 'emsw', 'lnd_sfcemiss', 'ocn_sfcemiss', 'ice_sfcemiss', 'aliq', 'bliq', 'cliq', 'dliq', 'aice', 'bice', 'cice', 'dice', 't00pg', 'p00pg', 'alam', 'pgfaa1', 'hdmw', 'iceminh', 'lowcld', 'hicld'],
                'private': [],
                'usings': ['mod_realkinds'],
                'subroutines': [],
                'variables': ['d_zero', 'd_one', 'd_two', 'd_three', 'd_four', 'd_five', 'd_six', 'd_nine', 'd_half', 'd_rfour', 'd_twelve', 'd_60', 'd_10', 'd_r10', 'd_100', 'd_r100', 'd_1000', 'd_r1000', 'onet', 'twot', 'fourt', 'deg00', 'deg45', 'deg90', 'deg180', 'deg360', 'minqq', 'minqc', 'minqv', 'mintr', 'minqx', 'dlowval', 'dhival', 'slowval', 'shival', 'dmissval', 'smissval', 'secpm', 'secph', 'secpd', 'rsecpd', 'minph', 'minpd', 'houpd', 'egrav', 'speedoflight', 'plankconstant', 'sigm', 'boltzk', 'navgdr', 'amd', 'amw', 'amo2', 'amo3', 'amco2', 'amn2o', 'amch4', 'amcfc11', 'amcfc12', 'pdbratio', 'rgasmol', 'c287', 'rgas', 'rwat', 'rdry', 'rgow', 'rgowi', 'cpd', 'cpv', 'cvd', 'cpw', 'cpi', 'cpw0', 'cp_h2o', 'ch2o', 'shice', 'cwi', 'csnw', 'cws', 'spcpfw', 'spcpsw', 'spcpice', 'wlhv', 'wlhf', 'wlhs', 'rwlhv', 'rwlhf', 'rwlhs', 'regrav', 'rcpd', 'rovcp', 'rdrcv', 'cpovr', 'rovg', 'govr', 'gdry', 'hcratio', 'hcrm1', 'rhoh2o', 'rhosea', 'rhosnow', 'rhosnowp', 'rhoice', 'tzero', 'tiso', 'rtzero', 'wattp', 'tboil', 'c1es', 'c2es', 'c3les', 'c3ies', 'c4les', 'c4ies', 'c5les', 'c5ies', 'c5alvcp', 'c5alscp', 'wlhvocp', 'wlhsocp', 'wlhfocp', 'cpowlhv', 'cpowlhs', 'cpowlhf', 'rtber', 'rtice', 'rtwat', 'mpcrt', 'rtwat_rtice_r', 'pq0', 'eliwv', 'p00', 'stdp', 'stdpmb', 'stdpcb', 'stdt', 'stdrho', 'lrate', 'atmos', 'rtcon', 'rumolec', 'dropdif', 'difgas', 'm_euler', 'mathpi', 'invpi', 'halfpi', 'quartpi', 'twopi', 'pisqr', 'degrad', 'raddeg', 'rmax0', 'dewmax', 'dewmaxi', 'trsmx0', 'drain', 'minwrat', 'earthrad', 'erkm', 'rearthrad', 'eomeg', 'eomeg2', 'zlnd', 'zoce', 'zsno', 'vonkar', 'csoilc', 'wtur', 'ep1', 'ep2', 'rep2', 'xlv0', 'xlv1', 'xls0', 'xls1', 'avt', 'bvt', 'g4pb', 'g3pb', 'g5pb', 'vtc', 'alpha_hyd', 'beta_hyd', 'emsw', 'lnd_sfcemiss', 'ocn_sfcemiss', 'ice_sfcemiss', 'aliq', 'bliq', 'cliq', 'dliq', 'aice', 'bice', 'cice', 'dice', 't00pg', 'p00pg', 'alam', 'pgfaa1', 'hdmw', 'iceminh', 'lowcld', 'hicld'],
                'includes': [],
                'interfaces': [],
                'functions': [],
                'types': [],
                'forward_imports': [],
    },
            'mod_runparams': {
                'public': ['namelistfile', 'prgname', 'carb_aging_control', 'nqx', 'iqfrst', 'iqlst', 'iqv', 'iqc', 'iqi', 'iqr', 'iqs', 'iqg', 'iqh', 'cqn', 'cqc', 'cqr', 'number_of_prognostic_components', 'pc_total', 'pc_dynamic', 'pc_physic', 'idate0', 'idate1', 'idate2', 'rcmtimer', 'alarm_hour', 'alarm_day', 'alarm_out_nwf', 'alarm_out_sav', 'alarm_out_atm', 'alarm_out_rad', 'alarm_out_srf', 'alarm_out_shf', 'alarm_out_sts', 'alarm_out_che', 'alarm_out_lak', 'alarm_out_opt', 'alarm_out_sub', 'alarm_in_bdy', 'syncro_dbg', 'syncro_rep', 'syncro_srf', 'syncro_rad', 'syncro_radfor', 'syncro_emi', 'syncro_cum', 'syncro_che', 'syncro_cpl', 'year_offset', 'eccen', 'obliq', 'mvelp', 'obliqr', 'lambm0', 'mvelpp', 'eccf', 'bdydate1', 'bdydate2', 'somdate1', 'somdate2', 'intbdy', 'intsom', 'declin', 'xbctime', 'calday', 'twodt', 'xslabtime', 'solcon', 'scon', 'uvrotate', 'rnsrf_for_day', 'rnsrf_for_srffrq', 'rnsrf_for_lakfrq', 'rnsrf_for_subfrq', 'rnrad_for_optfrq', 'rnrad_for_radfrq', 'dtsec', 'irceideal', 'lrcemip_perturb', 'lrcemip_noise_level', 'icup_lnd', 'icup_ocn', 'icup', 'igcc', 'icumcloud', 'ibltyp', 'idiffu', 'idif', 'lakemod', 'idcsst', 'iwhitecap', 'iseaice', 'icetriggert', 'iocnrough', 'iocnflx', 'iocncpl', 'iocnzoq', 'iwavcpl', 'icopcpl', 'ioasiscpl', 'idirect', 'iindirect', 'iemiss', 'isolconst', 'ifixsolar', 'isnowdark', 'ichecold', 'fixedsolarval', 'isladvec', 'iqmsl', 'iconvlwp', 'icldfrac', 'icldmstrat', 'vqrang', 'rcrit', 'coef_ccn', 'abulk', 'scenario', 'ghg_year_const', 'moloch_do_test_1', 'moloch_do_test_2', 'mo_dzita', 'mo_anu2', 'mo_divfilter', 'mo_nzfilt', 'mo_nadv', 'mo_nsound', 'dt', 'dt2', 'dtsq', 'dtcb', 'dtbdys', 'rdt', 'dx', 'dx2', 'dx4', 'dx8', 'dx16', 'dxsq', 'rdx', 'rdxsq', 'dtsrf', 'dtabem', 'dtrad', 'dtcum', 'dtche', 'cpldt', 'zomax', 'ustarmax', 'ckh', 'diffu_hgtf', 'adyndif', 'iboudy', 'ichem', 'ipgf', 'ipptls', 'iaerosol', 'igaschem', 'ioxclim', 'iisoropia', 'chtrname', 'nbin', 'nmine', 'do_parallel_netcdf_in', 'do_parallel_netcdf_out', 'do_parallel_save', 'ifrest', 'doing_restart', 'lsync', 'chechgact', 'dtau', 'dtsplit', 'hsigma', 'dsigma', 'qcon', 'sigma', 'zita', 'zitah', 'ffilt', 'ak', 'bk', 'twt', 'clfrcv', 'replacemoist', 'replacetemp', 'nsplit', 'lstand', 'gnu1', 'gnu2', 'upstream_mode', 'uoffc', 'stability_enhance', 't_extrema', 'q_rel_extrema', 'base_state_ts0', 'ifupr', 'nhbet', 'nhxkd', 'ifrayd', 'itopnudge', 'rayndamp', 'rayalpha0', 'rayzd', 'rayhd', 'mincld', 'skbmax', 'shrmax_ocn', 'shrmin_ocn', 'edtmax_ocn', 'edtmin_ocn', 'edtmaxo_ocn', 'edtmino_ocn', 'edtmaxx_ocn', 'edtminx_ocn', 'shrmax', 'shrmin', 'edtmax', 'edtmin', 'edtmaxo', 'edtmino', 'edtmaxx', 'edtminx', 'dtauc', 'pbcmax', 'htmax', 'htmin', 'alphae', 'betae', 'coeffr', 'coeffs', 'cu', 'damp', 'dtmax', 'elcrit_ocn', 'elcrit_lnd', 'entp', 'omtrain', 'omtsnow', 'sigd', 'sigs', 'tlcrit', 'epmax_ocn', 'epmax_lnd', 'minorig', 'istochastic', 'sigs_min', 'sigs_max', 'sigd_min', 'sigd_max', 'elcrit_lnd_min', 'elcrit_lnd_max', 'epmax_lnd_min', 'epmax_lnd_max', 'lmfpen', 'lmfmid', 'lmfdd', 'lepcld', 'lmfdudv', 'lmfscv', 'lmfuvdis', 'lmftrac', 'lmfsmooth', 'lmfwstar', 'iconv', 'entrdd', 'entrpen_lnd', 'entrpen_ocn', 'entrscv', 'entrmid', 'cprcon', 'entrmax', 'cmtcape', 'rcuc_lnd', 'rcuc_ocn', 'rcpec_lnd', 'rcpec_ocn', 'rhebc_lnd', 'rhebc_ocn', 'rprc_lnd', 'rprc_ocn', 'revap_lnd', 'revap_ocn', 'detrpen_lnd', 'detrpen_ocn', 'entshalp', 'kf_entrate', 'kf_convrate', 'kf_min_pef', 'kf_max_pef', 'kf_dpp', 'kf_min_dtcape', 'kf_max_dtcape', 'kf_tkemax', 'kf_wthreshold', 'itweak', 'itweak_sst', 'itweak_temperature', 'itweak_solar_irradiance', 'itweak_greenhouse_gases', 'sst_tweak', 'temperature_tweak', 'solar_tweak', 'gas_tweak_factors', 'rrtm_extend', 'irrtm', 'irrtm_cldov', 'irrtm_sw_opcliq', 'irrtm_sw_opcice', 'inflgsw', 'iceflgsw', 'liqflgsw', 'icld', 'irng', 'imcica', 'inflglw', 'iceflglw', 'liqflglw', 'nradfo', 'iclimao3', 'iclimaaer', 'radclimpath', 'iuwvadv', 'rstbl', 'atwo', 'czero', 'nuk', 'ricr_ocn', 'ricr_lnd', 'zhnew_fac', 'ifaholtth10', 'ifaholt', 'holtth10iter', 'chemsimtype', 'ichcumtra', 'ichdrdepo', 'ichremcvc', 'ichremlsc', 'ichsursrc', 'ichsolver', 'ismoke', 'ichdustemd', 'ichdustparam', 'ichdiag', 'ichebdy', 'ichjphcld', 'ichbion', 'ichlinox', 'rdstemfac', 'rocemfac', 'nchlmax', 'nochl', 'nbchl', 'iochl', 'ibchl', 'ibchb', 'iochb', 'ianh4', 'iano3', 'iisop', 'ich4', 'ism1', 'ism2', 'ino', 'io3', 'ncld', 'lsrfhack', 'larcticcorr', 'rhmin', 'rhmax', 'rh0land', 'rh0oce', 'tc0', 'cllwcv', 'clfrcvmax', 'cftotmax', 'kfac_shal', 'kfac_deep', 'k2_const', 'qck1land', 'qck1oce', 'gulland', 'guloce', 'caccrlnd', 'cevaplnd', 'caccroce', 'cevapoce', 'conf', 'islab_ocean', 'ifslaboc', 'do_qflux_adj', 'do_restore_sst', 'sst_restore_timescale', 'mixed_layer_depth', 'stepcount', 'stats', 'budget_compute', 'nssopt', 'iautoconv', 'vfqr', 'vfqi', 'vfqs', 'auto_rate_khair', 'auto_rate_kessl', 'auto_rate_klepi', 'rkconv', 'skconv', 'rcldiff', 'rcovpmin', 'rpecons', 'temp_tend_maxval', 'wind_tend_maxval', 'idiag', 'icosp', 'allocate_mod_runparams', 'exponential_nudging', 'iswater', 'isocean', 'islake'],
                'private': [],
                'usings': ['mod_intkinds', 'mod_realkinds', 'mod_constants', 'mod_date', 'mod_dynparam', 'mod_mpmessage', 'mod_memutil', 'mod_timer', 'mod_spline'],
                'subroutines': ['allocate_mod_runparams', 'exponential_nudging'],
                'variables': ['namelistfile', 'prgname', 'carb_aging_control', 'nqx', 'iqfrst', 'iqlst', 'iqv', 'iqc', 'iqi', 'iqr', 'iqs', 'iqg', 'iqh', 'cqn', 'cqc', 'cqr', 'number_of_prognostic_components', 'pc_total', 'pc_dynamic', 'pc_physic', 'idate0', 'idate1', 'idate2', 'rcmtimer', 'alarm_hour', 'alarm_day', 'alarm_out_nwf', 'alarm_out_sav', 'alarm_out_atm', 'alarm_out_rad', 'alarm_out_srf', 'alarm_out_shf', 'alarm_out_sts', 'alarm_out_che', 'alarm_out_lak', 'alarm_out_opt', 'alarm_out_sub', 'alarm_in_bdy', 'syncro_dbg', 'syncro_rep', 'syncro_srf', 'syncro_rad', 'syncro_radfor', 'syncro_emi', 'syncro_cum', 'syncro_che', 'syncro_cpl', 'year_offset', 'eccen', 'obliq', 'mvelp', 'obliqr', 'lambm0', 'mvelpp', 'eccf', 'bdydate1', 'bdydate2', 'somdate1', 'somdate2', 'intbdy', 'intsom', 'declin', 'xbctime', 'calday', 'twodt', 'xslabtime', 'solcon', 'scon', 'uvrotate', 'rnsrf_for_day', 'rnsrf_for_srffrq', 'rnsrf_for_lakfrq', 'rnsrf_for_subfrq', 'rnrad_for_optfrq', 'rnrad_for_radfrq', 'dtsec', 'irceideal', 'lrcemip_perturb', 'lrcemip_noise_level', 'icup_lnd', 'icup_ocn', 'icup', 'igcc', 'icumcloud', 'ibltyp', 'idiffu', 'idif', 'lakemod', 'idcsst', 'iwhitecap', 'iseaice', 'icetriggert', 'iocnrough', 'iocnflx', 'iocncpl', 'iocnzoq', 'iwavcpl', 'icopcpl', 'ioasiscpl', 'idirect', 'iindirect', 'iemiss', 'isolconst', 'ifixsolar', 'isnowdark', 'ichecold', 'fixedsolarval', 'isladvec', 'iqmsl', 'iconvlwp', 'icldfrac', 'icldmstrat', 'vqrang', 'rcrit', 'coef_ccn', 'abulk', 'scenario', 'ghg_year_const', 'moloch_do_test_1', 'moloch_do_test_2', 'mo_dzita', 'mo_anu2', 'mo_divfilter', 'mo_nzfilt', 'mo_nadv', 'mo_nsound', 'dt', 'dt2', 'dtsq', 'dtcb', 'dtbdys', 'rdt', 'dx', 'dx2', 'dx4', 'dx8', 'dx16', 'dxsq', 'rdx', 'rdxsq', 'dtsrf', 'dtabem', 'dtrad', 'dtcum', 'dtche', 'cpldt', 'zomax', 'ustarmax', 'ckh', 'diffu_hgtf', 'adyndif', 'iboudy', 'ichem', 'ipgf', 'ipptls', 'iaerosol', 'igaschem', 'ioxclim', 'iisoropia', 'chtrname', 'nbin', 'nmine', 'do_parallel_netcdf_in', 'do_parallel_netcdf_out', 'do_parallel_save', 'ifrest', 'doing_restart', 'lsync', 'chechgact', 'dtau', 'dtsplit', 'hsigma', 'dsigma', 'qcon', 'sigma', 'zita', 'zitah', 'ffilt', 'ak', 'bk', 'twt', 'clfrcv', 'replacemoist', 'replacetemp', 'nsplit', 'lstand', 'gnu1', 'gnu2', 'upstream_mode', 'uoffc', 'stability_enhance', 't_extrema', 'q_rel_extrema', 'base_state_ts0', 'ifupr', 'nhbet', 'nhxkd', 'ifrayd', 'itopnudge', 'rayndamp', 'rayalpha0', 'rayzd', 'rayhd', 'mincld', 'skbmax', 'shrmax_ocn', 'shrmin_ocn', 'edtmax_ocn', 'edtmin_ocn', 'edtmaxo_ocn', 'edtmino_ocn', 'edtmaxx_ocn', 'edtminx_ocn', 'shrmax', 'shrmin', 'edtmax', 'edtmin', 'edtmaxo', 'edtmino', 'edtmaxx', 'edtminx', 'dtauc', 'pbcmax', 'htmax', 'htmin', 'alphae', 'betae', 'coeffr', 'coeffs', 'cu', 'damp', 'dtmax', 'elcrit_ocn', 'elcrit_lnd', 'entp', 'omtrain', 'omtsnow', 'sigd', 'sigs', 'tlcrit', 'epmax_ocn', 'epmax_lnd', 'minorig', 'istochastic', 'sigs_min', 'sigs_max', 'sigd_min', 'sigd_max', 'elcrit_lnd_min', 'elcrit_lnd_max', 'epmax_lnd_min', 'epmax_lnd_max', 'lmfpen', 'lmfmid', 'lmfdd', 'lepcld', 'lmfdudv', 'lmfscv', 'lmfuvdis', 'lmftrac', 'lmfsmooth', 'lmfwstar', 'iconv', 'entrdd', 'entrpen_lnd', 'entrpen_ocn', 'entrscv', 'entrmid', 'cprcon', 'entrmax', 'cmtcape', 'rcuc_lnd', 'rcuc_ocn', 'rcpec_lnd', 'rcpec_ocn', 'rhebc_lnd', 'rhebc_ocn', 'rprc_lnd', 'rprc_ocn', 'revap_lnd', 'revap_ocn', 'detrpen_lnd', 'detrpen_ocn', 'entshalp', 'kf_entrate', 'kf_convrate', 'kf_min_pef', 'kf_max_pef', 'kf_dpp', 'kf_min_dtcape', 'kf_max_dtcape', 'kf_tkemax', 'kf_wthreshold', 'itweak', 'itweak_sst', 'itweak_temperature', 'itweak_solar_irradiance', 'itweak_greenhouse_gases', 'sst_tweak', 'temperature_tweak', 'solar_tweak', 'gas_tweak_factors', 'rrtm_extend', 'irrtm', 'irrtm_cldov', 'irrtm_sw_opcliq', 'irrtm_sw_opcice', 'inflgsw', 'iceflgsw', 'liqflgsw', 'icld', 'irng', 'imcica', 'inflglw', 'iceflglw', 'liqflglw', 'nradfo', 'iclimao3', 'iclimaaer', 'radclimpath', 'iuwvadv', 'rstbl', 'atwo', 'czero', 'nuk', 'ricr_ocn', 'ricr_lnd', 'zhnew_fac', 'ifaholtth10', 'ifaholt', 'holtth10iter', 'chemsimtype', 'ichcumtra', 'ichdrdepo', 'ichremcvc', 'ichremlsc', 'ichsursrc', 'ichsolver', 'ismoke', 'ichdustemd', 'ichdustparam', 'ichdiag', 'ichebdy', 'ichjphcld', 'ichbion', 'ichlinox', 'rdstemfac', 'rocemfac', 'nchlmax', 'nochl', 'nbchl', 'iochl', 'ibchl', 'ibchb', 'iochb', 'ianh4', 'iano3', 'iisop', 'ich4', 'ism1', 'ism2', 'ino', 'io3', 'ncld', 'lsrfhack', 'larcticcorr', 'rhmin', 'rhmax', 'rh0land', 'rh0oce', 'tc0', 'cllwcv', 'clfrcvmax', 'cftotmax', 'kfac_shal', 'kfac_deep', 'k2_const', 'qck1land', 'qck1oce', 'gulland', 'guloce', 'caccrlnd', 'cevaplnd', 'caccroce', 'cevapoce', 'conf', 'islab_ocean', 'ifslaboc', 'do_qflux_adj', 'do_restore_sst', 'sst_restore_timescale', 'mixed_layer_depth', 'stepcount', 'stats', 'budget_compute', 'nssopt', 'iautoconv', 'vfqr', 'vfqi', 'vfqs', 'auto_rate_khair', 'auto_rate_kessl', 'auto_rate_klepi', 'rkconv', 'skconv', 'rcldiff', 'rcovpmin', 'rpecons', 'temp_tend_maxval', 'wind_tend_maxval', 'idiag', 'icosp'],
                'includes': [],
                'interfaces': [],
                'functions': ['iswater', 'isocean', 'islake'],
                'types': [],
                'forward_imports': [],
    },
            'mod_mppparam': {
                'public': ['global_cross_istart', 'global_cross_iend', 'global_cross_jstart', 'global_cross_jend', 'global_dot_istart', 'global_dot_iend', 'global_dot_jstart', 'global_dot_jend', 'lndcomm', 'ocncomm', 'iocpu', 'italk', 'ncout_mpi_info', 'ma', 'on_device', 'trueforall', 'set_nproc', 'broadcast_params', 'uvtentotenx', 'tenxtouvten', 'uvcross2dot', 'uvdot2cross', 'psc2psd', 'gather_r', 'gather_i', 'allgather_r', 'allgather_i', 'allsync', 'cl_dispose', 'grid_nc_create', 'grid_nc_write', 'grid_nc_destroy', 'grid_distribute', 'subgrid_distribute', 'grid_collect', 'subgrid_collect', 'exchange', 'exchange_lrbt', 'exchange_lr', 'exchange_bt', 'exchange_lb', 'exchange_rt', 'exchange_bdy_lr', 'exchange_bdy_bt', 'grid_fill', 'bcast', 'sumall', 'c2l_ss', 'c2l_gs', 'l2c_ss', 'glb_c2l_ss', 'glb_c2l_gs', 'glb_l2c_ss', 'reorder_glb_subgrid', 'reorder_subgrid', 'reorder_add_subgrid', 'input_reorder', 'cl_setup', 'maxall', 'minall', 'meanall', 'cross2dot', 'get_cartcomm', 'grid_nc_var2d', 'grid_nc_var3d', 'grid_nc_var4d'],
                'private': ['lreorder', 'cartesian_communicator', 'ccid', 'ccio', 'r8vector1', 'r8vector2', 'r4vector1', 'r4vector2', 'i4vector1', 'i4vector2', 'lvector1', 'lvector2', 'window', 'windows', 'ifake', 'wincount', 'windispl', 'mpierr', 'r8subgrid', 'r4subgrid', 'i4subgrid', 'lsubgrid', 'global_r8subgrid', 'global_r4subgrid', 'global_i4subgrid', 'global_lsubgrid', 'global_r8grid', 'global_r4grid', 'global_i4grid', 'global_lgrid', 'tag_bt', 'tag_tb', 'tag_lr', 'tag_rl', 'tag_brtl', 'tag_tlbr', 'tag_bltr', 'tag_trbl', 'bcast_logical', 'bcast_int4', 'bcast_int8', 'bcast_real4', 'bcast_real8', 'bcast_arr_logical', 'bcast_arr_character', 'bcast_arr_text_list', 'bcast_arr_int4', 'bcast_arr_int8', 'bcast_arr_real4', 'bcast_arr_real8', 'bcast_matr_real8', 'bcast_matr_real4', 'bcast_arr_rcm_time_and_date', 'bcast_rcm_time_and_date', 'sumall_real8', 'sumall_real4', 'maxall_real8', 'maxall_real4', 'maxall_integer4', 'meanall_real8', 'meanall_real4', 'minall_real8', 'minall_real4', 'minall_integer4', 'sumall_int4', 'sumall_int4_array', 'send_array_logical', 'send_array_int4', 'send_array_real4', 'send_array_real8', 'recv_array_logical', 'recv_array_int4', 'recv_array_real4', 'recv_array_real8', 'exchange_array_r8', 'exchange_array_r4', 'cyclic_exchange_array_r8', 'cyclic_exchange_array_r4', 'real8_2d_do_distribute', 'real4_2d_do_distribute', 'integer4_2d_do_distribute', 'logical_2d_do_distribute', 'real8_2d_distribute', 'real8_3d_distribute', 'real8_4d_distribute', 'real4_2d_distribute', 'real4_3d_distribute', 'real4_4d_distribute', 'integer_2d_distribute', 'integer_3d_distribute', 'integer_4d_distribute', 'logical_2d_distribute', 'logical_3d_distribute', 'logical_4d_distribute', 'real8_2d_do_sub_distribute', 'real4_2d_do_sub_distribute', 'integer4_2d_do_sub_distribute', 'logical_2d_do_sub_distribute', 'real8_2d_sub_distribute', 'real4_2d_sub_distribute', 'real8_3d_sub_distribute', 'real4_3d_sub_distribute', 'logical_2d_sub_distribute', 'integer_2d_sub_distribute', 'integer_3d_sub_distribute', 'real8_2d_do_collect', 'real4_2d_do_collect', 'integer4_2d_do_collect', 'logical_2d_do_collect', 'real8_2d_collect', 'real8_2d_3d_collect', 'real8_3d_collect', 'real8_3d_2d_collect', 'real8_4d_collect', 'real8_4d_2d_collect', 'real4_2d_collect', 'real4_2d_3d_collect', 'real4_3d_collect', 'real4_3d_2d_collect', 'real4_4d_collect', 'real4_4d_2d_collect', 'logical_2d_collect', 'integer_2d_collect', 'integer_3d_collect', 'integer_4d_collect', 'real8_2d_do_sub_collect', 'real4_2d_do_sub_collect', 'integer4_2d_do_sub_collect', 'logical_2d_do_sub_collect', 'real8_2d_sub_collect', 'real8_3d_sub_collect', 'real4_2d_sub_collect', 'real4_3d_sub_collect', 'integer_2d_sub_collect', 'integer_3d_sub_collect', 'logical_2d_sub_collect', 'logical_3d_sub_collect', 'real8_2d_exchange', 'real8_3d_exchange', 'real8_4d_exchange', 'real4_2d_exchange', 'real4_3d_exchange', 'real4_4d_exchange', 'real8_2d_exchange_left_right_bottom_top', 'real8_3d_exchange_left_right_bottom_top', 'real8_4d_exchange_left_right_bottom_top', 'real4_2d_exchange_left_right_bottom_top', 'real4_3d_exchange_left_right_bottom_top', 'real4_4d_exchange_left_right_bottom_top', 'real8_2d_exchange_left_right', 'real8_3d_exchange_left_right', 'real8_4d_exchange_left_right', 'real4_2d_exchange_left_right', 'real4_3d_exchange_left_right', 'real4_4d_exchange_left_right', 'real8_2d_exchange_bottom_top', 'real8_3d_exchange_bottom_top', 'real8_4d_exchange_bottom_top', 'real4_2d_exchange_bottom_top', 'real4_3d_exchange_bottom_top', 'real4_4d_exchange_bottom_top', 'real8_2d_exchange_left_bottom', 'real8_3d_exchange_left_bottom', 'real8_4d_exchange_left_bottom', 'real4_2d_exchange_left_bottom', 'real4_3d_exchange_left_bottom', 'real4_4d_exchange_left_bottom', 'real8_2d_exchange_right_top', 'real8_3d_exchange_right_top', 'real8_4d_exchange_right_top', 'real4_2d_exchange_right_top', 'real4_3d_exchange_right_top', 'real4_4d_exchange_right_top', 'real8_bdy_exchange_left_right', 'real4_bdy_exchange_left_right', 'real8_bdy_exchange_bottom_top', 'real4_bdy_exchange_bottom_top', 'real8_2d_grid_fill_extend1', 'real4_2d_grid_fill_extend1', 'real8_2d_grid_fill_extend2', 'real4_2d_grid_fill_extend2', 'cross2dot2d', 'cross2dot3d', 'grid_nc_create_var2d', 'grid_nc_write_var2d', 'grid_nc_destroy_var2d', 'grid_nc_create_var3d', 'grid_nc_write_var3d', 'grid_nc_destroy_var3d', 'grid_nc_create_var4d', 'grid_nc_write_var4d', 'grid_nc_destroy_var4d', 'reorder_add_subgrid_2d_real8', 'reorder_add_subgrid_2d_real4', 'reorder_subgrid_2d_real8', 'reorder_subgrid_2d_real4', 'reorder_logical_global_subgrid_2d', 'reorder_subgrid_2d_logical', 'reorder_add_subgrid_2d3d_real8', 'reorder_add_subgrid_2d3d_real4', 'reorder_subgrid_2d3d_real8', 'reorder_subgrid_2d3d_real4', 'reorder_add_subgrid_3d_real8', 'reorder_add_subgrid_3d_real4', 'reorder_subgrid_3d_real8', 'reorder_subgrid_3d_real4', 'reorder_subgrid_4d_real8', 'reorder_subgrid_4d_real4', 'input_reorder_real8', 'input_reorder_real4', 'clset', 'cl_setup_real8', 'cl_setup_real4', 'cartesian_to_linear_logical_subgrid_subgrid', 'linear_to_cartesian_logical_subgrid_subgrid', 'cartesian_to_linear_integer_subgrid_subgrid', 'linear_to_cartesian_integer_subgrid_subgrid', 'cartesian_to_linear_real8_subgrid_subgrid_4d', 'cartesian_to_linear_real4_subgrid_subgrid_4d', 'linear_to_cartesian_real8_subgrid_subgrid_4d', 'linear_to_cartesian_real4_subgrid_subgrid_4d', 'cartesian_to_linear_real8_subgrid_subgrid', 'cartesian_to_linear_real4_subgrid_subgrid', 'linear_to_cartesian_real8_subgrid_subgrid', 'linear_to_cartesian_real4_subgrid_subgrid', 'cartesian_to_linear_logical_grid_subgrid', 'cartesian_to_linear_integer_grid_subgrid', 'cartesian_to_linear_real8_grid_subgrid', 'cartesian_to_linear_real4_grid_subgrid', 'global_to_linear_logical_subgrid_subgrid', 'linear_to_global_logical_subgrid_subgrid', 'global_to_linear_integer_subgrid_subgrid', 'linear_to_global_integer_subgrid_subgrid', 'global_to_linear_real8_subgrid_subgrid', 'global_to_linear_real4_subgrid_subgrid', 'global_to_linear_real4_real8_subgrid_subgrid', 'linear_to_global_real8_subgrid_subgrid', 'linear_to_global_real4_subgrid_subgrid', 'linear_to_global_real8_real4_subgrid_subgrid', 'global_to_linear_real8_subgrid_subgrid_4d', 'global_to_linear_real4_subgrid_subgrid_4d', 'global_to_linear_real4_real8_subgrid_subgrid_4d', 'linear_to_global_real8_subgrid_subgrid_4d', 'linear_to_global_real4_subgrid_subgrid_4d', 'linear_to_global_real8_real4_subgrid_subgrid_4d', 'global_to_linear_logical_grid_subgrid', 'global_to_linear_integer_grid_subgrid', 'global_to_linear_real8_grid_subgrid', 'global_to_linear_real4_grid_subgrid', 'global_to_linear_real4_real8_grid_subgrid', 'mypack_logical_grid', 'mypack_logical_subgrid', 'mypack_integer_grid', 'mypack_integer_subgrid', 'mypack_real8_grid', 'mypack_real4_grid', 'mypack_real8_subgrid', 'mypack_real4_subgrid', 'mypack_real8_subgrid_4d', 'mypack_real4_subgrid_4d', 'mypack_real8_subgrid_slice', 'mypack_real4_subgrid_slice', 'myunpack_logical_grid', 'myunpack_logical_subgrid', 'myunpack_integer_grid', 'myunpack_integer_subgrid', 'myunpack_real8_grid', 'myunpack_real4_grid', 'myunpack_real8_real4_grid', 'myunpack_real8_subgrid', 'myunpack_real4_subgrid', 'myunpack_real8_real4_subgrid', 'myunpack_real8_subgrid_4d', 'myunpack_real4_subgrid_4d', 'myunpack_real8_real4_subgrid_4d', 'myunpack_real8_subgrid_slice', 'myunpack_real4_subgrid_slice', 'myunpack_real8_real4_subgrid_slice', 'mypack_global_logical_grid', 'mypack_global_logical_subgrid', 'mypack_global_integer_grid', 'mypack_global_integer_subgrid', 'mypack_global_real8_grid', 'mypack_global_real4_grid', 'mypack_global_real4_real8_grid', 'mypack_global_real8_subgrid', 'mypack_global_real4_subgrid', 'mypack_global_real4_real8_subgrid', 'mypack_global_real8_subgrid_4d', 'mypack_global_real4_subgrid_4d', 'mypack_global_real4_real8_subgrid_4d', 'mypack_global_real8_subgrid_slice', 'mypack_global_real4_subgrid_slice', 'mypack_global_real4_real8_subgrid_slice', 'myunpack_global_logical_grid', 'myunpack_global_logical_subgrid', 'myunpack_global_integer_grid', 'myunpack_global_integer_subgrid', 'myunpack_global_real8_grid', 'myunpack_global_real4_grid', 'myunpack_global_real8_real4_grid', 'myunpack_global_real8_subgrid', 'myunpack_global_real4_subgrid', 'myunpack_global_real8_real4_subgrid', 'myunpack_global_real8_subgrid_4d', 'myunpack_global_real4_subgrid_4d', 'myunpack_global_real8_real4_subgrid_4d', 'myunpack_global_real8_subgrid_slice', 'myunpack_global_real4_subgrid_slice', 'myunpack_global_real8_real4_subgrid_slice', 'exchange_array', 'cyclic_exchange_array', 'send_array', 'recv_array', 'mypack', 'myunpack', 'mypack_global', 'myunpack_global', 'glosplitw'],
                'usings': ['mod_intkinds', 'mod_realkinds', 'mod_dynparam', 'mod_constants', 'mod_runparams', 'mod_mpmessage', 'mod_memutil', 'mod_date', 'mod_stdio', 'netcdf', 'mod_regcm_types', 'mpi'],
                'subroutines': ['bcast_logical', 'bcast_int4', 'bcast_int8', 'bcast_real4', 'bcast_real8', 'bcast_arr_logical', 'bcast_arr_character', 'bcast_arr_text_list', 'bcast_arr_int4', 'bcast_arr_int8', 'bcast_arr_real4', 'bcast_arr_real8', 'bcast_matr_real8', 'bcast_matr_real4', 'bcast_arr_rcm_time_and_date', 'bcast_rcm_time_and_date', 'trueforall', 'sumall_real8', 'sumall_real4', 'maxall_real8', 'maxall_real4', 'maxall_integer4', 'meanall_real8', 'meanall_real4', 'minall_real8', 'minall_real4', 'minall_integer4', 'sumall_int4', 'sumall_int4_array', 'send_array_logical', 'send_array_int4', 'send_array_real4', 'send_array_real8', 'recv_array_logical', 'recv_array_int4', 'recv_array_real4', 'recv_array_real8', 'exchange_array_r8', 'exchange_array_r4', 'cyclic_exchange_array_r8', 'cyclic_exchange_array_r4', 'set_nproc', 'broadcast_params', 'real8_2d_do_distribute', 'real4_2d_do_distribute', 'integer4_2d_do_distribute', 'logical_2d_do_distribute', 'real8_2d_distribute', 'real8_3d_distribute', 'real8_4d_distribute', 'real4_2d_distribute', 'real4_3d_distribute', 'real4_4d_distribute', 'integer_2d_distribute', 'integer_3d_distribute', 'integer_4d_distribute', 'logical_2d_distribute', 'logical_3d_distribute', 'logical_4d_distribute', 'real8_2d_do_sub_distribute', 'real4_2d_do_sub_distribute', 'integer4_2d_do_sub_distribute', 'logical_2d_do_sub_distribute', 'real8_2d_sub_distribute', 'real4_2d_sub_distribute', 'real8_3d_sub_distribute', 'real4_3d_sub_distribute', 'logical_2d_sub_distribute', 'integer_2d_sub_distribute', 'integer_3d_sub_distribute', 'real8_2d_do_collect', 'real4_2d_do_collect', 'integer4_2d_do_collect', 'logical_2d_do_collect', 'real8_2d_collect', 'real8_2d_3d_collect', 'real8_3d_collect', 'real8_3d_2d_collect', 'real8_4d_collect', 'real8_4d_2d_collect', 'real4_2d_collect', 'real4_2d_3d_collect', 'real4_3d_collect', 'real4_3d_2d_collect', 'real4_4d_collect', 'real4_4d_2d_collect', 'logical_2d_collect', 'integer_2d_collect', 'integer_3d_collect', 'integer_4d_collect', 'real8_2d_do_sub_collect', 'real4_2d_do_sub_collect', 'integer4_2d_do_sub_collect', 'logical_2d_do_sub_collect', 'real8_2d_sub_collect', 'real8_3d_sub_collect', 'real4_2d_sub_collect', 'real4_3d_sub_collect', 'integer_2d_sub_collect', 'integer_3d_sub_collect', 'logical_2d_sub_collect', 'logical_3d_sub_collect', 'real8_2d_exchange', 'real8_3d_exchange', 'real8_4d_exchange', 'real4_2d_exchange', 'real4_3d_exchange', 'real4_4d_exchange', 'real8_2d_exchange_left_right_bottom_top', 'real8_3d_exchange_left_right_bottom_top', 'real8_4d_exchange_left_right_bottom_top', 'real4_2d_exchange_left_right_bottom_top', 'real4_3d_exchange_left_right_bottom_top', 'real4_4d_exchange_left_right_bottom_top', 'real8_2d_exchange_left_right', 'real8_3d_exchange_left_right', 'real8_4d_exchange_left_right', 'real4_2d_exchange_left_right', 'real4_3d_exchange_left_right', 'real4_4d_exchange_left_right', 'real8_2d_exchange_bottom_top', 'real8_3d_exchange_bottom_top', 'real8_4d_exchange_bottom_top', 'real4_2d_exchange_bottom_top', 'real4_3d_exchange_bottom_top', 'real4_4d_exchange_bottom_top', 'real8_2d_exchange_left_bottom', 'real8_3d_exchange_left_bottom', 'real8_4d_exchange_left_bottom', 'real4_2d_exchange_left_bottom', 'real4_3d_exchange_left_bottom', 'real4_4d_exchange_left_bottom', 'real8_2d_exchange_right_top', 'real8_3d_exchange_right_top', 'real8_4d_exchange_right_top', 'real4_2d_exchange_right_top', 'real4_3d_exchange_right_top', 'real4_4d_exchange_right_top', 'real8_bdy_exchange_left_right', 'real4_bdy_exchange_left_right', 'real8_bdy_exchange_bottom_top', 'real4_bdy_exchange_bottom_top', 'real8_2d_grid_fill_extend1', 'real4_2d_grid_fill_extend1', 'real8_2d_grid_fill_extend2', 'real4_2d_grid_fill_extend2', 'uvtentotenx', 'tenxtouvten', 'uvcross2dot', 'uvdot2cross', 'cross2dot2d', 'cross2dot3d', 'psc2psd', 'grid_nc_create_var2d', 'grid_nc_write_var2d', 'grid_nc_destroy_var2d', 'grid_nc_create_var3d', 'grid_nc_write_var3d', 'grid_nc_destroy_var3d', 'grid_nc_create_var4d', 'grid_nc_write_var4d', 'grid_nc_destroy_var4d', 'gather_r', 'gather_i', 'allgather_r', 'allgather_i', 'reorder_add_subgrid_2d_real8', 'reorder_add_subgrid_2d_real4', 'reorder_subgrid_2d_real8', 'reorder_subgrid_2d_real4', 'reorder_logical_global_subgrid_2d', 'reorder_subgrid_2d_logical', 'reorder_add_subgrid_2d3d_real8', 'reorder_add_subgrid_2d3d_real4', 'reorder_subgrid_2d3d_real8', 'reorder_subgrid_2d3d_real4', 'reorder_add_subgrid_3d_real8', 'reorder_add_subgrid_3d_real4', 'reorder_subgrid_3d_real8', 'reorder_subgrid_3d_real4', 'reorder_subgrid_4d_real8', 'reorder_subgrid_4d_real4', 'input_reorder_real8', 'input_reorder_real4', 'allsync', 'clset', 'cl_setup_real8', 'cl_setup_real4', 'cartesian_to_linear_logical_subgrid_subgrid', 'linear_to_cartesian_logical_subgrid_subgrid', 'cartesian_to_linear_integer_subgrid_subgrid', 'linear_to_cartesian_integer_subgrid_subgrid', 'cartesian_to_linear_real8_subgrid_subgrid_4d', 'cartesian_to_linear_real4_subgrid_subgrid_4d', 'linear_to_cartesian_real8_subgrid_subgrid_4d', 'linear_to_cartesian_real4_subgrid_subgrid_4d', 'cartesian_to_linear_real8_subgrid_subgrid', 'cartesian_to_linear_real4_subgrid_subgrid', 'linear_to_cartesian_real8_subgrid_subgrid', 'linear_to_cartesian_real4_subgrid_subgrid', 'cartesian_to_linear_logical_grid_subgrid', 'cartesian_to_linear_integer_grid_subgrid', 'cartesian_to_linear_real8_grid_subgrid', 'cartesian_to_linear_real4_grid_subgrid', 'global_to_linear_logical_subgrid_subgrid', 'linear_to_global_logical_subgrid_subgrid', 'global_to_linear_integer_subgrid_subgrid', 'linear_to_global_integer_subgrid_subgrid', 'global_to_linear_real8_subgrid_subgrid', 'global_to_linear_real4_subgrid_subgrid', 'global_to_linear_real4_real8_subgrid_subgrid', 'linear_to_global_real8_subgrid_subgrid', 'linear_to_global_real4_subgrid_subgrid', 'linear_to_global_real8_real4_subgrid_subgrid', 'global_to_linear_real8_subgrid_subgrid_4d', 'global_to_linear_real4_subgrid_subgrid_4d', 'global_to_linear_real4_real8_subgrid_subgrid_4d', 'linear_to_global_real8_subgrid_subgrid_4d', 'linear_to_global_real4_subgrid_subgrid_4d', 'linear_to_global_real8_real4_subgrid_subgrid_4d', 'global_to_linear_logical_grid_subgrid', 'global_to_linear_integer_grid_subgrid', 'global_to_linear_real8_grid_subgrid', 'global_to_linear_real4_grid_subgrid', 'global_to_linear_real4_real8_grid_subgrid', 'cl_dispose', 'mypack_logical_grid', 'mypack_logical_subgrid', 'mypack_integer_grid', 'mypack_integer_subgrid', 'mypack_real8_grid', 'mypack_real4_grid', 'mypack_real8_subgrid', 'mypack_real4_subgrid', 'mypack_real8_subgrid_4d', 'mypack_real4_subgrid_4d', 'mypack_real8_subgrid_slice', 'mypack_real4_subgrid_slice', 'myunpack_logical_grid', 'myunpack_logical_subgrid', 'myunpack_integer_grid', 'myunpack_integer_subgrid', 'myunpack_real8_grid', 'myunpack_real4_grid', 'myunpack_real8_real4_grid', 'myunpack_real8_subgrid', 'myunpack_real4_subgrid', 'myunpack_real8_real4_subgrid', 'myunpack_real8_subgrid_4d', 'myunpack_real4_subgrid_4d', 'myunpack_real8_real4_subgrid_4d', 'myunpack_real8_subgrid_slice', 'myunpack_real4_subgrid_slice', 'myunpack_real8_real4_subgrid_slice', 'mypack_global_logical_grid', 'mypack_global_logical_subgrid', 'mypack_global_integer_grid', 'mypack_global_integer_subgrid', 'mypack_global_real8_grid', 'mypack_global_real4_grid', 'mypack_global_real4_real8_grid', 'mypack_global_real8_subgrid', 'mypack_global_real4_subgrid', 'mypack_global_real4_real8_subgrid', 'mypack_global_real8_subgrid_4d', 'mypack_global_real4_subgrid_4d', 'mypack_global_real4_real8_subgrid_4d', 'mypack_global_real8_subgrid_slice', 'mypack_global_real4_subgrid_slice', 'mypack_global_real4_real8_subgrid_slice', 'myunpack_global_logical_grid', 'myunpack_global_logical_subgrid', 'myunpack_global_integer_grid', 'myunpack_global_integer_subgrid', 'myunpack_global_real8_grid', 'myunpack_global_real4_grid', 'myunpack_global_real8_real4_grid', 'myunpack_global_real8_subgrid', 'myunpack_global_real4_subgrid', 'myunpack_global_real8_real4_subgrid', 'myunpack_global_real8_subgrid_4d', 'myunpack_global_real4_subgrid_4d', 'myunpack_global_real8_real4_subgrid_4d', 'myunpack_global_real8_subgrid_slice', 'myunpack_global_real4_subgrid_slice', 'myunpack_global_real8_real4_subgrid_slice'],
                'variables': ['global_cross_istart', 'global_cross_iend', 'global_cross_jstart', 'global_cross_jend', 'global_dot_istart', 'global_dot_iend', 'global_dot_jstart', 'global_dot_jend', 'lreorder', 'lndcomm', 'ocncomm', 'iocpu', 'italk', 'cartesian_communicator', 'ccid', 'ccio', 'ncout_mpi_info', 'ma', 'r8vector1', 'r8vector2', 'r4vector1', 'r4vector2', 'i4vector1', 'i4vector2', 'lvector1', 'lvector2', 'window', 'windows', 'ifake', 'wincount', 'windispl', 'mpierr', 'r8subgrid', 'r4subgrid', 'i4subgrid', 'lsubgrid', 'global_r8subgrid', 'global_r4subgrid', 'global_i4subgrid', 'global_lsubgrid', 'global_r8grid', 'global_r4grid', 'global_i4grid', 'global_lgrid', 'tag_bt', 'tag_tb', 'tag_lr', 'tag_rl', 'tag_brtl', 'tag_tlbr', 'tag_bltr', 'tag_trbl', 'on_device'],
                'includes': [],
                'interfaces': ['exchange_array', 'cyclic_exchange_array', 'grid_nc_create', 'grid_nc_write', 'grid_nc_destroy', 'grid_distribute', 'subgrid_distribute', 'grid_collect', 'subgrid_collect', 'exchange', 'exchange_lrbt', 'exchange_lr', 'exchange_bt', 'exchange_lb', 'exchange_rt', 'exchange_bdy_lr', 'exchange_bdy_bt', 'grid_fill', 'bcast', 'sumall', 'send_array', 'recv_array', 'c2l_ss', 'c2l_gs', 'l2c_ss', 'glb_c2l_ss', 'glb_c2l_gs', 'glb_l2c_ss', 'reorder_glb_subgrid', 'reorder_subgrid', 'reorder_add_subgrid', 'input_reorder', 'mypack', 'myunpack', 'mypack_global', 'myunpack_global', 'cl_setup', 'maxall', 'minall', 'meanall', 'cross2dot'],
                'functions': ['glosplitw', 'get_cartcomm'],
                'types': ['grid_nc_var2d', 'grid_nc_var3d', 'grid_nc_var4d'],
                'forward_imports': [],
    },
            'mod_mpmessage': {
                'public': ['iprntv', 'vprntm', 'vprntv', 'setup_mesg', 'die', 'aline', 'say', 'note', 'cry', 'fatal', 'checkalloc'],
                'private': ['vprntv_r8', 'vprntv_r4', 'vprntm_r8', 'vprntm_r4'],
                'usings': ['mod_intkinds', 'mod_realkinds', 'mod_stdio', 'mod_message'],
                'subroutines': ['vprntv_r8', 'vprntv_r4', 'iprntv', 'vprntm_r8', 'vprntm_r4'],
                'variables': [],
                'includes': [],
                'interfaces': ['vprntm', 'vprntv'],
                'functions': [],
                'types': [],
                'forward_imports': ['setup_mesg', 'die', 'aline', 'say', 'note', 'cry', 'fatal', 'checkalloc'],
    },
            'mod_stdio': {
                'public': ['stdin', 'stdout', 'stderr', 'file_freeunit', 'file_getunit'],
                'private': ['file_maxunit', 'file_minunit', 'unit_tag'],
                'usings': ['mod_intkinds', 'iso_fortran_env'],
                'subroutines': ['file_freeunit'],
                'variables': ['stdin', 'stdout', 'stderr', 'file_maxunit', 'file_minunit', 'unit_tag'],
                'includes': [],
                'interfaces': [],
                'functions': ['file_getunit'],
                'types': [],
                'forward_imports': [],
    },
            'mod_service': {
                'public': ['unised_module'],
                'private': [],
                'usings': [],
                'subroutines': [],
                'variables': ['unised_module'],
                'includes': [],
                'interfaces': [],
                'functions': [],
                'types': [],
                'forward_imports': [],
    },
            'mod_memutil': {
                'public': ['memory_init', 'memory_destroy', 'remappnt4', 'assignpnt', 'getmem1d', 'relmem1d', 'getmem2d', 'relmem2d', 'getmem3d', 'relmem3d', 'getmem4d', 'relmem4d', 'getmem5d', 'relmem5d'],
                'private': ['r1di', 'l1di', 'c1di', 'n1di', 'p1di', 'r1ds', 'l1ds', 'c1ds', 'n1ds', 'p1ds', 'r1dl', 'l1dl', 'c1dl', 'n1dl', 'p1dl', 'r1dr', 'l1dr', 'c1dr', 'n1dr', 'p1dr', 'r1dd', 'l1dd', 'c1dd', 'n1dd', 'p1dd', 'r1dt', 'l1dt', 'c1dt', 'n1dt', 'p1dt', 'r2di', 'l2di', 'c2di', 'n2di', 'p2di', 'r2ds', 'l2ds', 'c2ds', 'n2ds', 'p2ds', 'r2dl', 'l2dl', 'c2dl', 'n2dl', 'p2dl', 'r2dr', 'l2dr', 'c2dr', 'n2dr', 'p2dr', 'r2dd', 'l2dd', 'c2dd', 'n2dd', 'p2dd', 'r3di', 'l3di', 'c3di', 'n3di', 'p3di', 'r3ds', 'l3ds', 'c3ds', 'n3ds', 'p3ds', 'r3dl', 'l3dl', 'c3dl', 'n3dl', 'p3dl', 'r3dr', 'l3dr', 'c3dr', 'n3dr', 'p3dr', 'r3dd', 'l3dd', 'c3dd', 'n3dd', 'p3dd', 'r4di', 'l4di', 'c4di', 'n4di', 'p4di', 'r4ds', 'l4ds', 'c4ds', 'n4ds', 'p4ds', 'r4dl', 'l4dl', 'c4dl', 'n4dl', 'p4dl', 'r4dr', 'l4dr', 'c4dr', 'n4dr', 'p4dr', 'r4dd', 'l4dd', 'c4dd', 'n4dd', 'p4dd', 'r5di', 'l5di', 'c5di', 'n5di', 'p5di', 'r5ds', 'l5ds', 'c5ds', 'n5ds', 'p5ds', 'r5dl', 'l5dl', 'c5dl', 'n5dl', 'p5dl', 'r5dr', 'l5dr', 'c5dr', 'n5dr', 'p5dr', 'r5dd', 'l5dd', 'c5dd', 'n5dd', 'p5dd', 'ista', 'getmem1d_l', 'relmem1d_l', 'getmem1d_t', 'relmem1d_t', 'getmem1d_s', 'relmem1d_s', 'getmem1d_i', 'relmem1d_i', 'getmem1d_r', 'relmem1d_r', 'getmem1d_d', 'relmem1d_d', 'finalize_pool1d_i', 'finalize_pool1d_s', 'finalize_pool1d_l', 'finalize_pool1d_r', 'finalize_pool1d_d', 'finalize_pool1d_t', 'getmem2d_l', 'relmem2d_l', 'getmem2d_s', 'relmem2d_s', 'getmem2d_i', 'relmem2d_i', 'getmem2d_r', 'relmem2d_r', 'getmem2d_d', 'relmem2d_d', 'finalize_pool2d_i', 'finalize_pool2d_s', 'finalize_pool2d_l', 'finalize_pool2d_r', 'finalize_pool2d_d', 'getmem3d_l', 'relmem3d_l', 'getmem3d_s', 'relmem3d_s', 'getmem3d_i', 'relmem3d_i', 'getmem3d_r', 'relmem3d_r', 'getmem3d_d', 'relmem3d_d', 'finalize_pool3d_s', 'finalize_pool3d_i', 'finalize_pool3d_l', 'finalize_pool3d_r', 'finalize_pool3d_d', 'getmem4d_l', 'relmem4d_l', 'getmem4d_s', 'relmem4d_s', 'getmem4d_i', 'relmem4d_i', 'getmem4d_r', 'relmem4d_r', 'getmem4d_d', 'relmem4d_d', 'finalize_pool4d_s', 'finalize_pool4d_i', 'finalize_pool4d_l', 'finalize_pool4d_r', 'finalize_pool4d_d', 'getmem5d_l', 'relmem5d_l', 'getmem5d_s', 'relmem5d_s', 'getmem5d_i', 'relmem5d_i', 'getmem5d_r', 'relmem5d_r', 'getmem5d_d', 'relmem5d_d', 'finalize_pool5d_s', 'finalize_pool5d_i', 'finalize_pool5d_l', 'finalize_pool5d_r', 'finalize_pool5d_d', 'assignp1d_l', 'assignp1d_s', 'assignp1d_i', 'assignp1d_r', 'assignp1d_d', 'assignp1d2_d', 'assignp1d2_r', 'assignp1d_t', 'assignp2d_l', 'assignp2d_s', 'assignp2d_i', 'assignp2d_r', 'assignp2d_d', 'assignp2d3_l', 'assignp2d3_s', 'assignp2d3_i', 'assignp2d3_r', 'assignp2d3_d', 'assignp3d_l', 'assignp3d_s', 'assignp3d_i', 'assignp3d_r', 'assignp3d_d', 'assignp3d4_l', 'assignp3d4_s', 'assignp3d4_i', 'assignp3d4_r', 'assignp3d4_d', 'assignp2d4_l', 'assignp2d4_s', 'assignp2d4_i', 'assignp2d4_r', 'assignp2d4_d', 'assignp4d_l', 'assignp4d_s', 'assignp4d_i', 'assignp4d_r', 'assignp4d_d', 'assignp4d5_l', 'assignp4d5_s', 'assignp4d5_i', 'assignp4d5_r', 'assignp4d5_d', 'assignp5d_l', 'assignp5d_s', 'assignp5d_i', 'assignp5d_r', 'assignp5d_d', 'remappnt4_r8', 'remappnt4_r4', 'pool1d_i', 'pool1d_s', 'pool1d_l', 'pool1d_r', 'pool1d_d', 'pool1d_t', 'pool2d_i', 'pool2d_s', 'pool2d_l', 'pool2d_r', 'pool2d_d', 'pool3d_s', 'pool3d_i', 'pool3d_l', 'pool3d_r', 'pool3d_d', 'pool4d_s', 'pool4d_i', 'pool4d_l', 'pool4d_r', 'pool4d_d', 'pool5d_s', 'pool5d_i', 'pool5d_l', 'pool5d_r', 'pool5d_d'],
                'usings': ['mod_intkinds', 'mod_realkinds', 'mod_space', 'mod_message', 'mod_constants', 'mod_date'],
                'subroutines': ['memory_init', 'getmem1d_l', 'relmem1d_l', 'getmem1d_t', 'relmem1d_t', 'getmem1d_s', 'relmem1d_s', 'getmem1d_i', 'relmem1d_i', 'getmem1d_r', 'relmem1d_r', 'getmem1d_d', 'relmem1d_d', 'finalize_pool1d_i', 'finalize_pool1d_s', 'finalize_pool1d_l', 'finalize_pool1d_r', 'finalize_pool1d_d', 'finalize_pool1d_t', 'getmem2d_l', 'relmem2d_l', 'getmem2d_s', 'relmem2d_s', 'getmem2d_i', 'relmem2d_i', 'getmem2d_r', 'relmem2d_r', 'getmem2d_d', 'relmem2d_d', 'finalize_pool2d_i', 'finalize_pool2d_s', 'finalize_pool2d_l', 'finalize_pool2d_r', 'finalize_pool2d_d', 'getmem3d_l', 'relmem3d_l', 'getmem3d_s', 'relmem3d_s', 'getmem3d_i', 'relmem3d_i', 'getmem3d_r', 'relmem3d_r', 'getmem3d_d', 'relmem3d_d', 'finalize_pool3d_s', 'finalize_pool3d_i', 'finalize_pool3d_l', 'finalize_pool3d_r', 'finalize_pool3d_d', 'getmem4d_l', 'relmem4d_l', 'getmem4d_s', 'relmem4d_s', 'getmem4d_i', 'relmem4d_i', 'getmem4d_r', 'relmem4d_r', 'getmem4d_d', 'relmem4d_d', 'finalize_pool4d_s', 'finalize_pool4d_i', 'finalize_pool4d_l', 'finalize_pool4d_r', 'finalize_pool4d_d', 'getmem5d_l', 'relmem5d_l', 'getmem5d_s', 'relmem5d_s', 'getmem5d_i', 'relmem5d_i', 'getmem5d_r', 'relmem5d_r', 'getmem5d_d', 'relmem5d_d', 'finalize_pool5d_s', 'finalize_pool5d_i', 'finalize_pool5d_l', 'finalize_pool5d_r', 'finalize_pool5d_d', 'memory_destroy', 'assignp1d_l', 'assignp1d_s', 'assignp1d_i', 'assignp1d_r', 'assignp1d_d', 'assignp1d2_d', 'assignp1d2_r', 'assignp1d_t', 'assignp2d_l', 'assignp2d_s', 'assignp2d_i', 'assignp2d_r', 'assignp2d_d', 'assignp2d3_l', 'assignp2d3_s', 'assignp2d3_i', 'assignp2d3_r', 'assignp2d3_d', 'assignp3d_l', 'assignp3d_s', 'assignp3d_i', 'assignp3d_r', 'assignp3d_d', 'assignp3d4_l', 'assignp3d4_s', 'assignp3d4_i', 'assignp3d4_r', 'assignp3d4_d', 'assignp2d4_l', 'assignp2d4_s', 'assignp2d4_i', 'assignp2d4_r', 'assignp2d4_d', 'assignp4d_l', 'assignp4d_s', 'assignp4d_i', 'assignp4d_r', 'assignp4d_d', 'assignp4d5_l', 'assignp4d5_s', 'assignp4d5_i', 'assignp4d5_r', 'assignp4d5_d', 'assignp5d_l', 'assignp5d_s', 'assignp5d_i', 'assignp5d_r', 'assignp5d_d', 'remappnt4_r8', 'remappnt4_r4'],
                'variables': ['r1di', 'l1di', 'c1di', 'n1di', 'p1di', 'r1ds', 'l1ds', 'c1ds', 'n1ds', 'p1ds', 'r1dl', 'l1dl', 'c1dl', 'n1dl', 'p1dl', 'r1dr', 'l1dr', 'c1dr', 'n1dr', 'p1dr', 'r1dd', 'l1dd', 'c1dd', 'n1dd', 'p1dd', 'r1dt', 'l1dt', 'c1dt', 'n1dt', 'p1dt', 'r2di', 'l2di', 'c2di', 'n2di', 'p2di', 'r2ds', 'l2ds', 'c2ds', 'n2ds', 'p2ds', 'r2dl', 'l2dl', 'c2dl', 'n2dl', 'p2dl', 'r2dr', 'l2dr', 'c2dr', 'n2dr', 'p2dr', 'r2dd', 'l2dd', 'c2dd', 'n2dd', 'p2dd', 'r3di', 'l3di', 'c3di', 'n3di', 'p3di', 'r3ds', 'l3ds', 'c3ds', 'n3ds', 'p3ds', 'r3dl', 'l3dl', 'c3dl', 'n3dl', 'p3dl', 'r3dr', 'l3dr', 'c3dr', 'n3dr', 'p3dr', 'r3dd', 'l3dd', 'c3dd', 'n3dd', 'p3dd', 'r4di', 'l4di', 'c4di', 'n4di', 'p4di', 'r4ds', 'l4ds', 'c4ds', 'n4ds', 'p4ds', 'r4dl', 'l4dl', 'c4dl', 'n4dl', 'p4dl', 'r4dr', 'l4dr', 'c4dr', 'n4dr', 'p4dr', 'r4dd', 'l4dd', 'c4dd', 'n4dd', 'p4dd', 'r5di', 'l5di', 'c5di', 'n5di', 'p5di', 'r5ds', 'l5ds', 'c5ds', 'n5ds', 'p5ds', 'r5dl', 'l5dl', 'c5dl', 'n5dl', 'p5dl', 'r5dr', 'l5dr', 'c5dr', 'n5dr', 'p5dr', 'r5dd', 'l5dd', 'c5dd', 'n5dd', 'p5dd', 'ista'],
                'includes': [],
                'interfaces': ['remappnt4', 'assignpnt', 'getmem1d', 'relmem1d', 'getmem2d', 'relmem2d', 'getmem3d', 'relmem3d', 'getmem4d', 'relmem4d', 'getmem5d', 'relmem5d'],
                'functions': [],
                'types': ['pool1d_i', 'pool1d_s', 'pool1d_l', 'pool1d_r', 'pool1d_d', 'pool1d_t', 'pool2d_i', 'pool2d_s', 'pool2d_l', 'pool2d_r', 'pool2d_d', 'pool3d_s', 'pool3d_i', 'pool3d_l', 'pool3d_r', 'pool3d_d', 'pool4d_s', 'pool4d_i', 'pool4d_l', 'pool4d_r', 'pool4d_d', 'pool5d_s', 'pool5d_i', 'pool5d_l', 'pool5d_r', 'pool5d_d'],
                'forward_imports': [],
    },
            'mod_atm_interface': {
                'public': ['cross', 'dot', 'mddom', 'mdsub', 'atm1', 'atm2', 'atmc', 'aten', 'atmx', 'tdiag', 'qdiag', 'sfs', 'atms', 'xtb', 'xqb', 'xub', 'xvb', 'xppb', 'xwwb', 'xpaib', 'xlb', 'xib', 'xpsb', 'xtsb', 'ba_cr', 'ba_dt', 'ba_ut', 'ba_vt', 'atm0', 'mdv', 'nhbh0', 'nhbh1', 'mo_atm', 'dstor', 'hstor', 'qdot', 'omega', 'coszrs', 'icumbot', 'icumtop', 'ktrop', 'convpr', 'pptc', 'sptc', 'prca', 'ptrop', 'sabveg', 'dsol', 'solis', 'solvs', 'solvsd', 'solvl', 'solvld', 'totcf', 'flw', 'fsw', 'flwd', 'cldfra', 'cldlwc', 'heatrt', 'dpsdxm', 'dpsdym', 'tmask', 'albvl', 'albvs', 'aldirs', 'aldifs', 'aldirl', 'aldifl', 'emiss', 'sinc', 'pptnc', 'prnca', 'crrate', 'ncrrate', 'fcc', 'remrat', 'rembc', 'ccn', 'rain_ls', 'kpbl', 'zpbl', 'q_detr', 'rain_cc', 'sdelq', 'sdelt', 'ssw2da', 'sfracv2d', 'sfracb2d', 'sfracs2d', 'svegfrac2d', 'sxlai2d', 'wetdepflx', 'drydepflx', 'cplmsk', 'setup_model_indexes', 'setup_boundaries', 'allocate_v3dbound', 'allocate_v2dbound', 'allocate_mod_atm_interface', 'export_data_from_atm'],
                'private': ['ix1', 'ix2', 'jx1', 'jx2', 'id1', 'id2', 'jd1', 'jd2', 'allocate_atmosphere', 'allocate_atmstate_a', 'allocate_atmstate_b', 'allocate_atmstate_c', 'allocate_atmstate_decoupled', 'allocate_atmstate_tendency', 'allocate_reference_atmosphere', 'allocate_mass_divergence', 'allocate_tendiag', 'allocate_qendiag', 'allocate_domain', 'allocate_domain_subgrid', 'allocate_surfstate', 'allocate_slice', 'allocate_nhbh'],
                'usings': ['mod_dynparam', 'mod_stdio', 'mod_constants', 'mod_runparams', 'mod_mppparam', 'mod_mpmessage', 'mod_service', 'mod_memutil', 'mod_regcm_types'],
                'subroutines': ['setup_model_indexes', 'setup_boundaries', 'allocate_v3dbound', 'allocate_v2dbound', 'allocate_atmosphere', 'allocate_atmstate_a', 'allocate_atmstate_b', 'allocate_atmstate_c', 'allocate_atmstate_decoupled', 'allocate_atmstate_tendency', 'allocate_reference_atmosphere', 'allocate_mass_divergence', 'allocate_tendiag', 'allocate_qendiag', 'allocate_domain', 'allocate_domain_subgrid', 'allocate_surfstate', 'allocate_slice', 'allocate_nhbh', 'allocate_mod_atm_interface', 'export_data_from_atm'],
                'variables': ['cross', 'dot', 'mddom', 'mdsub', 'atm1', 'atm2', 'atmc', 'aten', 'atmx', 'tdiag', 'qdiag', 'sfs', 'atms', 'xtb', 'xqb', 'xub', 'xvb', 'xppb', 'xwwb', 'xpaib', 'xlb', 'xib', 'xpsb', 'xtsb', 'ba_cr', 'ba_dt', 'ba_ut', 'ba_vt', 'atm0', 'mdv', 'nhbh0', 'nhbh1', 'mo_atm', 'dstor', 'hstor', 'qdot', 'omega', 'coszrs', 'icumbot', 'icumtop', 'ktrop', 'convpr', 'pptc', 'sptc', 'prca', 'ptrop', 'sabveg', 'dsol', 'solis', 'solvs', 'solvsd', 'solvl', 'solvld', 'totcf', 'flw', 'fsw', 'flwd', 'cldfra', 'cldlwc', 'heatrt', 'dpsdxm', 'dpsdym', 'tmask', 'albvl', 'albvs', 'aldirs', 'aldifs', 'aldirl', 'aldifl', 'emiss', 'sinc', 'pptnc', 'prnca', 'crrate', 'ncrrate', 'fcc', 'remrat', 'rembc', 'ccn', 'rain_ls', 'kpbl', 'zpbl', 'q_detr', 'rain_cc', 'sdelq', 'sdelt', 'ssw2da', 'sfracv2d', 'sfracb2d', 'sfracs2d', 'svegfrac2d', 'sxlai2d', 'wetdepflx', 'drydepflx', 'cplmsk', 'ix1', 'ix2', 'jx1', 'jx2', 'id1', 'id2', 'jd1', 'jd2'],
                'includes': [],
                'interfaces': [],
                'functions': [],
                'types': [],
                'forward_imports': [],
    },
            'mod_che_interface': {
                'public': ['init_chem', 'start_chem', 'cumtran', 'tractend2', 'nudge_chi', 'chem_config', 'setup_che_bdycon', 'close_chbc', 'allocate_mod_che_common', 'allocate_mod_che_mppio', 'allocate_mod_che_dust', 'allocate_mod_che_bdyco', 'allocate_mod_che_bionit', 'idust', 'totsp', 'trac_io', 'chia_io', 'chib_io', 'convcldfra', 'cadvhdiag', 'cadvvdiag', 'cbdydiag', 'cconvdiag', 'cdifhdiag', 'ctbldiag', 'chem_bdyin', 'chem_bdyval', 'chemall', 'chemall_io', 'washout', 'washout_io', 'remdrd', 'remdrd_io', 'rainout', 'rainout_io', 'convpr_io', 'sdelq_io', 'sdelt_io', 'sfracb2d_io', 'sfracs2d_io', 'ssw2da_io', 'duflux_io', 'voflux_io', 'sfracv2d_io', 'svegfrac2d_io', 'taucldsp_io'],
                'private': [],
                'usings': ['mod_realkinds', 'mod_regcm_types', 'mod_runparams', 'mod_che_common', 'mod_che_cumtran', 'mod_che_dust', 'mod_che_indices', 'mod_che_mppio', 'mod_che_ncio', 'mod_che_param', 'mod_che_drydep', 'mod_che_bdyco', 'mod_che_emission', 'mod_che_carbonaer', 'mod_che_species', 'mod_che_tend', 'mod_che_start', 'mod_che_bionit', 'mod_che_linox'],
                'subroutines': ['init_chem'],
                'variables': [],
                'includes': [],
                'interfaces': [],
                'functions': [],
                'types': [],
                'forward_imports': ['start_chem', 'cumtran', 'tractend2', 'nudge_chi', 'chem_config', 'setup_che_bdycon', 'close_chbc', 'allocate_mod_che_common', 'allocate_mod_che_mppio', 'allocate_mod_che_dust', 'allocate_mod_che_bdyco', 'allocate_mod_che_bionit', 'idust', 'totsp', 'trac_io', 'chia_io', 'chib_io', 'convcldfra', 'cadvhdiag', 'cadvvdiag', 'cbdydiag', 'cconvdiag', 'cdifhdiag', 'ctbldiag', 'chem_bdyin', 'chem_bdyval', 'chemall', 'chemall_io', 'washout', 'washout_io', 'remdrd', 'remdrd_io', 'rainout', 'rainout_io', 'convpr_io', 'sdelq_io', 'sdelt_io', 'sfracb2d_io', 'sfracs2d_io', 'ssw2da_io', 'duflux_io', 'voflux_io', 'sfracv2d_io', 'svegfrac2d_io', 'taucldsp_io'],
    },
            'mod_cu_interface': {
                'public': ['allocate_cumulus', 'init_cumulus', 'cucloud', 'cumulus', 'shallow_convection', 'cuscheme', 'cbmf2d', 'avg_ww', 'cldefi', 'twght', 'vqflx', 'shrmax2d', 'shrmin2d', 'edtmax2d', 'edtmin2d', 'edtmaxo2d', 'edtmino2d', 'edtmaxx2d', 'edtminx2d', 'pbcmax2d', 'mincld2d', 'kbmax2d', 'htmax2d', 'htmin2d', 'dtauc2d', 'k700', 'total_precip_points', 'cu_cldfrc'],
                'private': ['m2c', 'c2m', 'utenx', 'vtenx', 'utend', 'vtend', 'cmcptop'],
                'usings': ['mod_intkinds', 'mod_realkinds', 'mod_constants', 'mod_stdio', 'mod_dynparam', 'mod_runparams', 'mod_memutil', 'mod_regcm_types', 'mod_mppparam', 'mod_mppparam', 'mod_mppparam', 'mod_cu_common', 'mod_cu_common', 'mod_cu_tiedtke', 'mod_cu_tables', 'mod_cu_bm', 'mod_cu_em', 'mod_cu_kuo', 'mod_cu_grell', 'mod_cu_kf', 'mod_cu_shallow'],
                'subroutines': ['allocate_cumulus', 'init_cumulus', 'cucloud', 'cumulus', 'shallow_convection'],
                'variables': ['m2c', 'c2m', 'utenx', 'vtenx', 'utend', 'vtend', 'cmcptop'],
                'includes': [],
                'interfaces': [],
                'functions': [],
                'types': [],
                'forward_imports': ['cuscheme', 'cbmf2d', 'avg_ww', 'cldefi', 'twght', 'vqflx', 'shrmax2d', 'shrmin2d', 'edtmax2d', 'edtmin2d', 'edtmaxo2d', 'edtmino2d', 'edtmaxx2d', 'edtminx2d', 'pbcmax2d', 'mincld2d', 'kbmax2d', 'htmax2d', 'htmin2d', 'dtauc2d', 'k700', 'total_precip_points', 'cu_cldfrc'],      
    },
            'mod_lm_interface': {
                'public': ['lms', 'allocate_surface_model', 'init_surface_model', 'initialize_surface_model', 'surface_model', 'surface_albedo', 'export_data_from_surface', 'import_data_into_surface', 'dtbat', 'ocncomm', 'lndcomm'],
                'private': ['runoffcount', 'slp', 'sfp', 'slp1', 'lm', 'collect_output', 'mslp', 'compute_maxgust', 'pfesat', 'pfesat_water', 'pfesat_ice', 'pfwsat', 'pfesdt', 'pfesdt_water', 'pfesdt_ice', 'pfqsdt', 'evpt', 'evpt_fao', 'wlh'],
                'usings': ['mod_dynparam', 'mod_runparams', 'mod_memutil', 'mod_regcm_types', 'mod_outvars', 'mod_constants', 'mod_mppparam', 'mod_mpmessage', 'mod_service', 'mod_bats_common', 'mod_ocn_common', 'mod_stdio', 'mod_slabocean', 'mod_heatindex'],
                'subroutines': ['allocate_surface_model', 'init_surface_model', 'initialize_surface_model', 'surface_model', 'surface_albedo', 'export_data_from_surface', 'import_data_into_surface', 'collect_output', 'mslp', 'compute_maxgust'],
                'variables': ['runoffcount', 'slp', 'sfp', 'slp1', 'lm', 'lms'],
                'includes': [],
                'interfaces': [],
                'functions': ['pfesat', 'pfesat_water', 'pfesat_ice', 'pfwsat', 'pfesdt', 'pfesdt_water', 'pfesdt_ice', 'pfqsdt', 'evpt', 'evpt_fao', 'wlh'],
                'types': [],
                'forward_imports': ['dtbat', 'ocncomm', 'lndcomm'],
    },
            'mod_rad_interface': {
                'public': ['allocate_radiation', 'init_radiation', 'radiation', 'inito3', 'updateaerosol', 'closeaerosol', 'updateo3', 'updateaeropp', 'updateaeropp_cmip6', 'closeo3', 'export_data_from_rad', 'aerclima_ntr', 'aerclima_nbin', 'set_scenario', 'o3prof', 'gasabsnxt', 'gasabstot', 'gasemstot', 'taucldsp'],
                'private': ['m2r', 'r2m'],
                'usings': ['mod_intkinds', 'mod_realkinds', 'mod_dynparam', 'mod_constants', 'mod_stdio', 'mod_mppparam', 'mod_date', 'mod_memutil', 'mod_runparams', 'mod_regcm_types', 'mod_ipcc_scenario', 'mod_stdatm', 'mod_rad_common', 'mod_rad_colmod3', 'mod_rrtmg_driver', 'mod_rad_o3blk', 'mod_rad_o3blk', 'mod_rad_aerosol', 'mod_rad_aerosol', 'mod_rad_aerosol', 'mod_rad_aerosol', 'mod_rad_aerosol', 'mod_rad_outrad'],
                'subroutines': ['allocate_radiation', 'init_radiation', 'radiation', 'inito3', 'updateaerosol', 'closeaerosol', 'updateo3', 'updateaeropp', 'updateaeropp_cmip6', 'closeo3', 'export_data_from_rad'],
                'variables': ['m2r', 'r2m'],
                'includes': [],
                'interfaces': [],
                'functions': [],
                'types': [],
                'forward_imports': ['aerclima_ntr', 'aerclima_nbin', 'set_scenario', 'o3prof', 'gasabsnxt', 'gasabstot', 'gasemstot', 'taucldsp'],
    },
            'mod_pbl_interface': {
                'public': ['tkemin', 'allocate_pblscheme', 'init_pblscheme', 'pblscheme', 'uwstate', 'ricr', 'kmxpbl'],
                'private': ['m2p', 'p2m', 'utenx', 'vtenx', 'utend', 'vtend'],
                'usings': ['mod_realkinds', 'mod_service', 'mod_constants', 'mod_dynparam', 'mod_memutil', 'mod_mppparam', 'mod_regcm_types', 'mod_pbl_common', 'mod_pbl_holtbl', 'mod_pbl_uwtcm', 'mod_pbl_uwtcm', 'mod_pbl_gfs', 'mod_pbl_myj', 'mod_pbl_shinhong', 'mod_runparams', 'mod_runparams'],
                'subroutines': ['allocate_pblscheme', 'init_pblscheme', 'pblscheme'],
                'variables': ['m2p', 'p2m', 'tkemin', 'utenx', 'vtenx', 'utend', 'vtend'],
                'includes': [],
                'interfaces': [],
                'functions': [],
                'types': [],
                'forward_imports': ['uwstate', 'ricr', 'kmxpbl'],
    },
            'mod_micro_interface': {
                'public': ['ngs', 'rh0', 'allocate_micro', 'init_micro', 'microscheme', 'cldfrac', 'condtq', 'qck1', 'cgul', 'cevap', 'xcevap', 'caccr'],
                'private': ['mo2mc', 'mc2mo', 'qtcrit', 'totc', 'rh0adj', 'alphaice', 'nchi', 'chis', 'do_cfscaling', 'qccrit_lnd', 'qccrit_oce'],
                'usings': ['mod_realkinds', 'mod_service', 'mod_stdio', 'mod_constants', 'mod_dynparam', 'mod_memutil', 'mod_mppparam', 'mod_regcm_types', 'mod_runparams', 'mod_micro_nogtom', 'mod_micro_subex', 'mod_micro_wsm5', 'mod_micro_wsm7', 'mod_micro_wdm7', 'mod_cloud_subex', 'mod_cloud_xuran', 'mod_cloud_thomp', 'mod_cloud_guli2007', 'mod_cloud_texeira', 'mod_cloud_tompkins', 'mod_cloud_echam5'],
                'subroutines': ['allocate_micro', 'init_micro', 'microscheme', 'cldfrac', 'condtq'],
                'variables': ['ngs', 'mo2mc', 'mc2mo', 'rh0', 'qtcrit', 'totc', 'rh0adj', 'alphaice', 'nchi', 'chis', 'do_cfscaling', 'qccrit_lnd', 'qccrit_oce'],
                'includes': [],
                'interfaces': [],
                'functions': [],
                'types': [],
                'forward_imports': ['qck1', 'cgul', 'cevap', 'xcevap', 'caccr'],
    },
            'mod_bdycod': {
                'public': ['sue', 'sui', 'nue', 'nui', 'sve', 'svi', 'nve', 'nvi', 'wue', 'wui', 'eue', 'eui', 'wve', 'wvi', 'eve', 'evi', 'fnudge', 'gnudge', 'initideal', 'allocate_mod_bdycon', 'setup_bdycon', 'init_bdy', 'bdyin', 'bdyval', 'nudge', 'sponge', 'raydamp', 'is_present_qc', 'is_present_qi'],        
                'private': ['psdot', 'fcx', 'gcx', 'fcd', 'gcd', 'hefc', 'hegc', 'hefd', 'hegd', 'wgtd', 'wgtx', 'fg1', 'fg2', 'rdtbdy', 'jday', 'som_month', 'qxbval', 'bdyflow', 'present_qc', 'present_qi', 'bdyuv', 'sponge4d', 'mosponge4d', 'spongeuv', 'mospongeuv', 'sponge3d', 'mosponge3d', 'sponge2d', 'mosponge2d', 'nudge4d3d', 'monudge4d3d', 'nudgeuv', 'monudgeuv', 'monudge4d', 'nudge4d', 'nudge3d', 'monudge3d', 'nudge2d', 'monudge2d', 'couple', 'raydampuv', 'raydampuv_c', 'raydamp3f', 'raydamp3', 'moraydamp', 'raydampqv', 'timeint2', 'timeint3', 'paicompute', 'moloch_static_test1', 'moloch_static_test2', 'relax', 'invert_top_bottom', 'timeint', 'tau'],
                'usings': ['mod_intkinds', 'mod_realkinds', 'mod_date', 'mod_stdio', 'mod_constants', 'mod_dynparam', 'mod_runparams', 'mod_regcm_types', 'mod_mppparam', 'mod_memutil', 'mod_atm_interface', 'mod_pbl_interface', 'mod_che_interface', 'mod_lm_interface', 'mod_mpmessage', 'mod_ncio', 'mod_service', 'mod_zita', 'mod_stdatm', 'mod_slabocean', 'mod_vertint', 'mod_humid'],
                'subroutines': ['initideal', 'allocate_mod_bdycon', 'setup_bdycon', 'init_bdy', 'bdyin', 'bdyuv', 'bdyval', 'sponge4d', 'mosponge4d', 'spongeuv', 'mospongeuv', 'sponge3d', 'mosponge3d', 'sponge2d', 'mosponge2d', 'nudge4d3d', 'monudge4d3d', 'nudgeuv', 'monudgeuv', 'monudge4d', 'nudge4d', 'nudge3d', 'monudge3d', 'nudge2d', 'monudge2d', 'couple', 'raydampuv', 'raydampuv_c', 'raydamp3f', 'raydamp3', 'moraydamp', 'raydampqv', 'timeint2', 'timeint3', 'paicompute', 'moloch_static_test1', 'moloch_static_test2', 'relax', 'invert_top_bottom'],
                'variables': ['sue', 'sui', 'nue', 'nui', 'sve', 'svi', 'nve', 'nvi', 'wue', 'wui', 'eue', 'eui', 'wve', 'wvi', 'eve', 'evi', 'psdot', 'fcx', 'gcx', 'fcd', 'gcd', 'hefc', 'hegc', 'hefd', 'hegd', 'wgtd', 'wgtx', 'fg1', 'fg2', 'fnudge', 'gnudge', 'rdtbdy', 'jday', 'som_month', 'qxbval', 'bdyflow', 'present_qc', 'present_qi'],
                'includes': [],
                'interfaces': ['timeint', 'nudge', 'sponge', 'raydamp'],
                'functions': ['is_present_qc', 'is_present_qi', 'tau'],
                'types': [],
                'forward_imports': [],
    },
            'mod_slice': {
                'public': ['init_slice', 'mkslice'],
                'private': ['ix1', 'ix2', 'jx1', 'jx2', 'id1', 'id2', 'jd1', 'jd2', 'rpsb', 'rpsdotb'],
                'usings': ['mod_intkinds', 'mod_realkinds', 'mod_dynparam', 'mod_constants', 'mod_runparams', 'mod_memutil', 'mod_atm_interface', 'mod_che_interface', 'mod_pbl_interface', 'mod_rad_interface'],
                'subroutines': ['init_slice', 'mkslice'],
                'variables': ['ix1', 'ix2', 'jx1', 'jx2', 'id1', 'id2', 'jd1', 'jd2', 'rpsb', 'rpsdotb'],
                'includes': [],
                'interfaces': [],
                'functions': [],
                'types': [],
                'forward_imports': [],
    },
            'mod_sun': {
                'public': ['zenitm'],
                'private': ['heppatsi', 'tsi', 'tsifac', 'ii', 'jj', 'solar1', 'read_solarforcing', 'solar_irradiance'],
                'usings': ['mod_intkinds', 'mod_realkinds', 'mod_stdio', 'mod_memutil', 'mod_constants', 'mod_dynparam', 'mod_runparams', 'mod_mpmessage', 'mod_mppparam', 'mod_service', 'mod_date', 'mod_sunorbit', 'netcdf'],
                'subroutines': ['solar1', 'zenitm', 'read_solarforcing'],
                'variables': ['heppatsi', 'tsi', 'tsifac', 'ii', 'jj'],
                'includes': [],
                'interfaces': [],
                'functions': ['solar_irradiance'],
                'types': [],
                'forward_imports': [],
    },
            'mod_slabocean': {
                'public': ['qflux_restore_sst', 'qflb0', 'qflb1', 'qflbt', 'allocate_mod_slabocean', 'init_slabocean', 'update_slabocean', 'fill_slaboc_outvars'],
                'private': ['dtocean', 'sstemp', 'ohfx', 'oqfx', 'ofsw', 'oflw', 'slabmld', 'qflux_sst', 'qflux_adj', 'net_hflx', 'hflx', 'ocmask'],
                'usings': ['mod_intkinds', 'mod_realkinds', 'mod_dynparam', 'mod_runparams', 'mod_memutil', 'mod_regcm_types', 'mod_atm_interface', 'mod_mppparam', 'mod_constants', 'mod_stdio', 'mod_outvars', 'mod_mpmessage', 'netcdf', 'mod_kdinterp'],
                'subroutines': ['allocate_mod_slabocean', 'init_slabocean', 'update_slabocean', 'fill_slaboc_outvars'],
                'variables': ['dtocean', 'sstemp', 'ohfx', 'oqfx', 'ofsw', 'oflw', 'slabmld', 'qflux_restore_sst', 'qflux_sst', 'qflux_adj', 'net_hflx', 'hflx', 'qflb0', 'qflb1', 'qflbt', 'ocmask'],
                'includes': [],
                'interfaces': [],
                'functions': [],
                'types': [],
                'forward_imports': [],
    },
            'mod_massck': {
                'public': ['dryini', 'watini', 'dryerror', 'waterror', 'massck'],
                'private': ['wrkp', 'q_zero', 'mcrai', 'mncrai', 'mevap', 'mdryadv', 'mqadv'],
                'usings': ['mod_intkinds', 'mod_realkinds', 'mod_stdio', 'mod_dynparam', 'mod_constants', 'mod_runparams', 'mod_mppparam', 'mod_atm_interface'],
                'subroutines': ['massck'],
                'variables': ['wrkp', 'q_zero', 'dryini', 'watini', 'dryerror', 'waterror', 'mcrai', 'mncrai', 'mevap', 'mdryadv', 'mqadv'],
                'includes': [],
                'interfaces': [],
                'functions': [],
                'types': [],
                'forward_imports': [],
    },
            'mod_stdatm': {
                'public': ['itropical', 'imidlatsummer', 'imidlatwinter', 'ipolarsummer', 'ipolarwinter', 'istdatm_hgtkm', 'istdatm_prsmb', 'istdatm_tempk', 'istdatm_airdn', 'istdatm_qdens', 'istdatm_ozone', 'n_atmzones', 'n_atmparms', 'n_atmlevls', 'n_preflev', 'n_prehlev', 'n_hreflev', 'n_hrehlev', 'stdhlevh', 'stdhlevf', 'stdplevh', 'stdplevf', 'stdatm_val', 'stdlrate'],
                'private': ['stdatm', 'stdatm_val_noseason', 'stdatm_val_seasonal', 'winter_wgt', 'find_klev', 'find_zlev', 'plev_wgt'],
                'usings': ['mod_intkinds', 'mod_realkinds', 'mod_constants'],
                'subroutines': [],
                'variables': ['itropical', 'imidlatsummer', 'imidlatwinter', 'ipolarsummer', 'ipolarwinter', 'istdatm_hgtkm', 'istdatm_prsmb', 'istdatm_tempk', 'istdatm_airdn', 'istdatm_qdens', 'istdatm_ozone', 'n_atmzones', 'n_atmparms', 'n_atmlevls', 'n_preflev', 'n_prehlev', 'n_hreflev', 'n_hrehlev', 'stdhlevh', 'stdhlevf', 'stdplevh', 'stdplevf', 'stdatm'],
                'includes': [],
                'interfaces': ['stdatm_val'],
                'functions': ['stdatm_val_noseason', 'stdatm_val_seasonal', 'winter_wgt', 'find_klev', 'find_zlev', 'plev_wgt', 'stdlrate'],
                'types': [],
                'forward_imports': [],
    },
            'mod_zita': {
                'public': ['model_zitaf', 'model_zitah', 'zita_interp', 'sigmazita', 'zitasigma', 'gzita', 'md_fmz_h', 'md_zeta_h', 'md_ak', 'md_bk', 'md_fmz', 'md_zeta'],
                'private': ['zh3d', 'zh4d', 'zfz', 'bzita', 'bzitap', 'gzitap'],
                'usings': ['mod_realkinds', 'mod_intkinds', 'mod_constants', 'mod_dynparam'],
                'subroutines': ['model_zitaf', 'model_zitah', 'zh3d', 'zh4d'],
                'variables': [],
                'includes': [],
                'interfaces': ['zita_interp'],
                'functions': ['sigmazita', 'zitasigma', 'zfz', 'bzita', 'bzitap', 'gzita', 'gzitap', 'md_fmz_h', 'md_zeta_h', 'md_ak', 'md_bk', 'md_fmz', 'md_zeta'],
                'types': [],
                'forward_imports': [],
    },
        }

if __name__ == '__main__':
    unittest.main()
