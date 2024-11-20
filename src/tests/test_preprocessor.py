import os
import sys
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from parsing.preprocessor import Preprocessor
import _evn_specific_params as params

class TestPreprocessor(unittest.TestCase):
    def setUp(self):
        self.preprocessor = Preprocessor(file_path="test_file.f90")
        if not os.path.exists(params.tmp_dir):
            os.makedirs(params.tmp_dir)

    def test_add_define(self):
        self.preprocessor.add_define('TEST_DEFINE', '1')
        self.assertIn('TEST_DEFINE', self.preprocessor.defines)
        self.assertEqual(self.preprocessor.defines['TEST_DEFINE'], '1')

    def test_remove_define(self):
        self.preprocessor.add_define('TEST_DEFINE', '1')
        self.preprocessor.remove_define('TEST_DEFINE')
        self.assertNotIn('TEST_DEFINE', self.preprocessor.defines)

    def test_preprocess_code(self):
        code = """
        #define TEST_DEFINE 1
        #ifdef TEST_DEFINE
        integer :: i = 1
        #else
        integer :: i = 0
        #endif
        """
        expected_output = """
        integer :: i = 1
        """
        output = self.preprocessor.preprocess_code(code)
        self.assertEqual(output.strip(), expected_output.strip())

    def test_preprocess_code_with_undef(self):
        code = """
        #define TEST_DEFINE 1
        #undef TEST_DEFINE
        #ifdef TEST_DEFINE
        integer :: i = 1
        #else
        integer :: i = 0
        #endif
        """
        expected_output = """
        integer :: i = 0
        """
        output = self.preprocessor.preprocess_code(code)
        self.assertEqual(output.strip(), expected_output.strip())

    def test_preprocess_code_nested_ifdef(self):
        code = """
        #define OUTER_DEFINE 1
        #ifdef OUTER_DEFINE
        #define INNER_DEFINE 1
        #ifdef INNER_DEFINE
        integer :: i = 1
        #else
        integer :: i = 0
        #endif
        #else
        integer :: i = 0
        #endif
        """
        expected_output = """
        integer :: i = 1
        """
        output = self.preprocessor.preprocess_code(code)
        self.assertEqual(output.strip(), expected_output.strip())

    def test_preprocess_code_nested_ifndef(self):
        code = """
        #define OUTER_DEFINE 1
        #ifndef OUTER_DEFINE
        integer :: i = 0
        #else
        #define INNER_DEFINE 1
        #ifndef INNER_DEFINE
        integer :: i = 0
        #else
        integer :: i = 1
        #endif
        #endif
        """
        expected_output = """
        integer :: i = 1
        """
        output = self.preprocessor.preprocess_code(code)
        self.assertEqual(output.strip(), expected_output.strip())

    def test_preprocess_code_nested_ifdef_not_expanded(self):
        code = """
        #define OUTER_DEFINE 1
        #ifdef OUTER_DEFINE
        integer :: i = 1
        #else
        #define INNER_DEFINE 1
        #ifdef INNER_DEFINE
        integer :: j = 1
        #else
        integer :: j = 0
        #endif
        #endif
        """
        expected_output = """
        integer :: i = 1
        """
        output = self.preprocessor.preprocess_code(code)
        self.assertEqual(output.strip(), expected_output.strip())

    def test_preprocess_code_with_include(self):
        code = """
        #include <included_file.f90>
        """
        included_file_path = os.path.join(params.tmp_dir, 'included_file.f90')
        with open(included_file_path, 'w') as f:
            f.write("""
            integer :: i = 1
            """)
        
        expected_output = """
        integer :: i = 1
        """
        
        output = self.preprocessor.preprocess_code(code, MockModuleDictionary())

        self.assertEqual(output.strip(), expected_output.strip())
        os.remove(included_file_path)

    def test_preprocess_code_with_nested_include(self):
        code = """
        #include <outer_file.f90>
        """
        outer_file_path = os.path.join(params.tmp_dir, 'outer_file.f90')
        inner_file_path = os.path.join(params.tmp_dir, 'inner_file.f90')
        with open(outer_file_path, 'w') as f:
            f.write("""
            #include <inner_file.f90>
            """)
        with open(inner_file_path, 'w') as f:
            f.write("""
            integer :: i = 1
            """)
        
        expected_output = """
        integer :: i = 1
        """
        output = self.preprocessor.preprocess_code(code, MockModuleDictionary())
        self.assertEqual(output.strip(), expected_output.strip())
        os.remove(outer_file_path)
        os.remove(inner_file_path)

class MockModuleDictionary:
    def get_file_for(self, module_name, extension='.f90'):
        return os.path.join(params.tmp_dir, module_name)


if __name__ == '__main__':
    unittest.main()
