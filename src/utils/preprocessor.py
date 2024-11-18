import re


class Preprocessor:
    def __init__(self, file_path):
        self.defines = {
            '__FILE__': f'"{file_path}"'
        }

    def add_define(self, key, value='default'):
        self.defines[key] = value

    def remove_define(self, key):
        if key in self.defines:
            del self.defines[key]

    def preprocess_code(self, code):
        lines = code.split('\n')
        output_lines = []
        skip_next_line_stack = [False]

        defines_local = self.defines.copy()
        fuse_line_to_previous_line = False

        for i, line in enumerate(lines):
            defines_local['__LINE__'] = f'{i + 1}'
            stripped_line = line.strip()

            def handle_ifndef(condition):
                nonlocal skip_next_line_stack
                skip_next_line_stack.append(condition in defines_local)

            def handle_ifdef(condition):
                nonlocal skip_next_line_stack
                skip_next_line_stack.append(condition not in defines_local)

            def handle_endif():
                nonlocal skip_next_line_stack
                if skip_next_line_stack:
                    skip_next_line_stack.pop()

            def handle_else():
                nonlocal skip_next_line_stack
                if skip_next_line_stack:
                    skip_next_line_stack[-1] = not skip_next_line_stack[-1]

            def handle_define(parts):
                if len(parts) == 3:
                    defines_local[parts[1]] = parts[2]
                elif len(parts) == 2:
                    defines_local[parts[1]] = 'default'

            def handle_undef(parts):
                if len(parts) == 2 and parts[1] in defines_local:
                    del defines_local[parts[1]]

            def expand_using_defines(line):
                for key, value in defines_local.items():
                    line = line.replace(key, value)
                return line
            
            handlers = {
                '#if': lambda parts: handle_ifdef(parts[1]),
                '#ifdef': lambda parts: handle_ifdef(parts[1]),
                '#ifndef': lambda parts: handle_ifndef(parts[1]),
                '#endif': lambda parts: handle_endif(),
                '#else': lambda parts: handle_else(),
                '#define': lambda parts: handle_define(parts),
                '#undef': lambda parts: handle_undef(parts),
                'include': lambda parts: None #TODO: implement include support
            }

            parts = stripped_line.split()
            directive = parts[0] if parts else None
            
            if directive in handlers:
                handlers[directive](parts)
            elif not skip_next_line_stack[-1]:
                line = expand_using_defines(line)

                if fuse_line_to_previous_line:
                    output_lines[-1] = output_lines[-1].rstrip('&') + ' ' + line.lstrip().lstrip('&')
                else:
                    output_lines.append(line)

                fuse_line_to_previous_line = line.endswith('&')

        # TODO: this `local` call will be needed for the analysis later (how to handle it?)
        def remove_local_call(line):
            local_call_pattern = r'local\([^)]*\)'
            return re.sub(local_call_pattern, '', line) 
        
        output_lines = [remove_local_call(line) for line in output_lines]
        
        return '\n'.join(output_lines)
