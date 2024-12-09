import re
from parsing.ast_walk.symbol_collection.graph import GraphNode

class FileLocationRepository:
    
    def __init__(self):
        self._files = {}
        
    
    def get_line_of_definition(self, node: GraphNode):

        file_location = node.get_path()
        if not file_location:
            return None

        function_name = node.short_name()
        file_content = self._load_file(file_location).split('\n')

        function_def_regex = re.compile(r'\b(subroutine|function)\b.*\s' + re.escape(function_name))
        
        for i, line in enumerate(file_content):
            if function_def_regex.search(line):
                return i + 1
            
            
    def _load_file(self, file_path):
        if file_path not in self._files:
            with open(file_path, 'r', encoding='utf8') as f:
                self._files[file_path] = f.read()

        return self._files[file_path]