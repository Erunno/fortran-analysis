from utils.preprocessor import Preprocessor
from fparser.two.parser import ParserFactory
from fparser.common.readfortran import FortranStringReader
from fparser.two.Fortran2003 import Program


class FortranModule:
    def __init__(self, name, file_path, base_dir):
        self.name = name
        self.path = file_path
        self.base_dir = base_dir
        
        self.preprocessor = Preprocessor(file_path=file_path)
        self.preprocessor.add_define('F2008')
        
        self.ast = self._load_fortran_file(file_path)

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
