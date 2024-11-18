import os
import sys
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from parsing.preprocessor import Preprocessor

class TestPreprocessor(unittest.TestCase):
    def setUp(self):
        self.preprocessor = Preprocessor(file_path="test_file.f90")

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


if __name__ == '__main__':
    unittest.main()
