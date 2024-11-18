import fparser
from parsing.find_in_tree import find_in_tree
from parsing.context import ChainedContext, FortranContext, ModuleImportedContext, ModulePrivatesContext, ModulePublicExportsContext
from parsing.definitions import FortranDefinitions
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
        
        self.ast = self._load_fortran_file(file_path)
        
        self.program: Module = self.ast.content[0]
        self.module, self.specif, self.sub_program = self.load_parts_of_module(self.program)
        
        assert self.module.get_name().tostr() == self.name

        self.definitions = FortranDefinitions(self.specif, self.sub_program)

        self.public_exports_context = ModulePublicExportsContext(self.definitions)
        self.private_context = ModulePrivatesContext(self.definitions)
        self.imported_context = ModuleImportedContext(self.definitions, self.module_dictionary)

        self.module_context = ChainedContext([self.imported_context, self.public_exports_context, self.private_context])

    def __str__(self):
        return f"Module {self.name} is located at {self.path}"

    def _load_fortran_file(self, file_path: str) -> Program:

        with open(file_path, 'r') as f:
            code = f.read()

        code = self.preprocessor.preprocess_code(code)
        
        reader = FortranStringReader(code, ignore_comments=True, include_dirs=[self.base_dir])
        f2008_parser = ParserFactory().create(std="f2008")
        ast = f2008_parser(reader)
        
        return ast

    def load_parts_of_module(self, program) -> tuple[Module_Stmt, Specification_Part, Module_Subprogram_Part]:
        module = find_in_tree(program, Module_Stmt)
        specif_part = find_in_tree(program, Specification_Part)
        sub_program = find_in_tree(program, Module_Subprogram_Part)

        return module, specif_part, sub_program
        
    def get_published_symbols(self):
        module = self.ast.content[0]
        
        for i, symbol in enumerate(self.ast.content):
            print(i, symbol)