from parsing.external_module_libs import ExternalLibs
from parsing.module import ExternalLibraryModule, FortranModule
import os
from Levenshtein import distance as lev

class ModuleDictionary:
    def __init__(self, base_dir, skip_dirs):
        self.modules = {}
        self.base_dir = base_dir
        self.skip_dirs = skip_dirs or []

        self.file_system = self._load_files(base_dir)

    def get_module(self, module_name) -> FortranModule:
        if ExternalLibs.is_external(module_name):
            return ExternalLibs.get_module(module_name)

        if module_name not in self.modules:
            self.modules[module_name] = self._load_module(module_name)

        return self.modules[module_name]
    
    def get_file_for(self, module_name, extension='.F90'):
        return self._module_name_to_path(module_name, extension)

    def _load_module(self, module_name) -> FortranModule:
        module_file = self._module_name_to_path(module_name)
        return FortranModule(module_name, file_path=module_file, base_dir=self.base_dir, module_dictionary=self)
        
    def _load_files(self, base_dir):
        file_dict = {}
        for root, _, files in os.walk(base_dir):
            if self._should_skip_dir(root):
                continue

            for file in files:
                full_path = os.path.join(root, file)

                file_dict[file] = full_path
        return file_dict
    
    def _should_skip_dir(self, dir_name):
        for skip_dir in self.skip_dirs:
            skip_path = os.path.join(self.base_dir, skip_dir)

            if dir_name.startswith(skip_path):
                return True
            
        return False

    _manual_module_name_fixes = {
        'mo_simple_plumes': 'mo_simple_plumes_v1'
    }

    def _module_name_to_path(self, module_name, extensions=['.F90', '.f90']):

        if module_name in ModuleDictionary._manual_module_name_fixes:
            module_name = ModuleDictionary._manual_module_name_fixes[module_name]

        best_match = None
        lowest_distance = float('inf')

        for f_name in self.file_system:
            f_file_no_f90_suffix = self._remove_suffixes(f_name, extensions)

            dist = lev(module_name, f_file_no_f90_suffix)
            if dist < lowest_distance:
                lowest_distance = dist
                best_match = f_name

        return self.file_system[best_match]
    

    def _remove_suffixes(self, module_name, suffixes):
        if len(suffixes) == 0:
            return module_name
        
        suffix, *other_suffixes = suffixes

        if module_name.endswith(suffix):
            return module_name[:-len(suffix)]

        return self._remove_suffixes(module_name, other_suffixes)