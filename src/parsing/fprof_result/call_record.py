import re

class _FunctionNames:
    @staticmethod
    def get_module_and_name(full_name: str):
        try:
            parts = full_name.split(' ')[0].split('_MOD_')
            return parts[0][2:], parts[1]
        except:
            return _FunctionNames._get_weird_edge_case(full_name)
        
    def _get_weird_edge_case(full_name: str):
        return {
            # key         : (module, function)
            'pfesat.4744': ('<unknown>', 'pfesat.4744'),
            'MAIN__': ('<main>', 'MAIN'),
            # this is used in case of recursive calls somehow (I want need it in the analysis anyway)
            '<cycle': ('<cycle>', 'cycle'),
            
        }[full_name]

class CallDetailLine:
    def __init__(self, line, is_main):
        self.line = line
        self._func_idx, self._time_pct = self._parse_fst_two_cols(line, is_main) 

        self._self_time, self._children_time, self._called, self._function_full_name = self._parse_rest_cols(line, is_main)
        self.module, self.function = _FunctionNames.get_module_and_name(self._function_full_name)

    def _parse_fst_two_cols(self, line, is_main):
        if not is_main:
            return None, None
        
        parts = re.split(r'\s+', line.strip())
        return int(parts[0][1:-1]), float(parts[1])

    def _parse_rest_cols(self, line, is_main):
        parts = re.split(r'\s+', line.strip())

        if is_main:
            parts = parts[2:]

        return float(parts[0]), float(parts[1]), parts[2], parts[3]


class CallDetailRecord:
    def __init__(self, description: str):
        self.description_lines = description.split('\n')
        
        self._caller_lines, self._main_function_full_name, self._called_lines \
            = self._parse_description_lines(self.description_lines)

    def is_for(self, module: str, function: str):
        return self._main_function_full_name.module == module and self._main_function_full_name.function == function
    
    def _parse_description_lines(self, description_lines) -> tuple[list[CallDetailLine], CallDetailLine, list[CallDetailLine]]:
        caller_lines = []
        main_function_full_name = None
        called_lines = []

        append_to = caller_lines

        for line in description_lines:
            if '<spontaneous>' in line or line.strip() == '':
                continue
            
            if line.startswith('['):
                append_to = called_lines
                main_function_full_name = CallDetailLine(line, is_main=True)

            else:
                call_line = CallDetailLine(line, is_main=False)
                append_to.append(call_line)
            
        return caller_lines, main_function_full_name, called_lines
   
class FunctionCallResult:
    def __init__(self, description_from_flat_profile: str, gprof_result):
        from parsing.fprof_result.gprof_result import GProfResult
        
        self._call_detail_record = None
        self.gprof_result : GProfResult = gprof_result

        self._run_time_pct, self._cumulative_run_time, \
            self._self_run_time, self._calls, self._ks_per_call_self, \
            self._ks_per_call_total, self._function_full_name = \
                self._parse_description_line(description_from_flat_profile) 
        
        self.module, self.function = _FunctionNames.get_module_and_name(self._function_full_name)

    def function_full_keyname(self):
        return self._function_full_name

    def is_for(self, module: str, function: str):
        return self.module == module and self.function == function
    
    def can_register(self, call_detail_record: CallDetailRecord):
        return call_detail_record.is_for(self.module, self.function)

    def register(self, call_detail_record: CallDetailRecord):
        if not self.can_register(call_detail_record):
            raise Exception("Record is not for this function")
        
        self._call_detail_record = call_detail_record


    def _parse_description_line(self, description: str):
        #   %   cumulative   self              self     total           
        # time   seconds   seconds    calls  Ks/call  Ks/call  name    

        parts = re.split(r'\s+', description.strip())

        # weird edge case: (second line)
        # 0.00   6175.13     0.01        1     0.00     0.00  __mod_vertint_MOD_intlinprof
        # 0.00   6175.14     0.01                             __mod_cbmz_linearalgebra_MOD_kppdecomp
        if len(parts) == 4:
            parts = parts[:3] + ['0', '0', '0'] + parts[3:]

        run_time_pct = float(parts[0])
        cumulative_run_time = float(parts[1])
        self_run_time = float(parts[2])
        calls = int(parts[3])
        ks_per_call_self = float(parts[4])
        ks_per_call_total = float(parts[5])
        function_full_name = parts[6]

        return run_time_pct, cumulative_run_time, self_run_time, \
            calls, ks_per_call_self, ks_per_call_total, function_full_name

