import fparser
from parsing.ast_walk.context_fetch.default_operators import DefaultOperatorContext
from parsing.ast_walk.context_fetch.std_lib_functions import StdLibContext
from parsing.find_in_tree import find_in_tree
from parsing.context import ChainedContext, ExternalLibraryContext, FortranContext, ModuleImportedContext, ModuleLocalContext, ModulePublicExportsContext
from parsing.definitions import ExternalSymbol, FortranDefinitions
from parsing.preprocessor import Preprocessor
from fparser.two.parser import ParserFactory
from fparser.common.readfortran import FortranStringReader
from fparser.two.Fortran2003 import Program, Module, Specification_Part, Module_Subprogram_Part, Module_Stmt

class FortranModule:
    def __init__(self, name, file_path, base_dir, module_dictionary):
        self.name = name
        self.path = file_path
        self.base_dir = base_dir
        self.module_dictionary = module_dictionary
        
        self.preprocessor = Preprocessor(file_path=file_path)
        self.preprocessor.add_define('F2008')
        self.preprocessor.add_define('STDPAR')
        
        self.ast = self._load_fortran_file(file_path)
        
        self.program: Module = self.ast.content[0]
        self.module, self.specif, self.sub_program = self._load_parts_of_module(self.program)
        
        assert self.module.get_name().tostr().lower() == self.name

        self.definitions = FortranDefinitions(
            definition_location_symbol=self,
            module_dictionary=module_dictionary,
            specification=self.specif,
            subprogram=self.sub_program)

        self.public_exports_context = ModulePublicExportsContext(self.definitions)
        self.module_local_context = ModuleLocalContext(self.definitions)
        self.imported_context = ModuleImportedContext(self.definitions, self.module_dictionary)

        self.module_context = ChainedContext([
            DefaultOperatorContext.instance(), StdLibContext.instance(), 
            self.imported_context, self.module_local_context])

    def __str__(self):
        return f"Module {self.name} - located at {self.path}"
    
    def __repr__(self):
        return self.__str__()

    def _load_fortran_file(self, file_path: str) -> Program:

        with open(file_path, 'r', encoding="utf8") as f:
            code = f.read()

        code = self.preprocessor.preprocess_code(code, self.module_dictionary)

        reader = FortranStringReader(code, ignore_comments=True, include_dirs=[self.base_dir])
        f2008_parser = ParserFactory().create(std="f2008")
        ast = f2008_parser(reader)
        
        return ast

    def _load_parts_of_module(self, program) -> tuple[Module_Stmt, Specification_Part, Module_Subprogram_Part]:
        module = find_in_tree(program, Module_Stmt)
        specif_part = find_in_tree(program, Specification_Part)
        sub_program = find_in_tree(program, Module_Subprogram_Part)

        return module, specif_part, sub_program
    
    def key(self):
        return self.name
    
    def is_module(self):
        return True
    
    def get_context(self):
        return self.module_context
    
    def full_unique_key(self):
        return self.key()
    
    def file_path(self):
        return self.path

class ExternalLibraryModule(FortranModule):
    def __init__(self, name, defined_symbols: list[ExternalSymbol]):
        self.name = name

        for symbol in defined_symbols:
            symbol._set_module(self)

        self.public_exports_context = ExternalLibraryContext(defined_symbols)
        self.module_context = ExternalLibraryContext(defined_symbols)

        self.path = '<external/lib/path>'

    def get_context(self):
        return self.module_context

        
    
    