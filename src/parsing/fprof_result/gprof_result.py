

# WARNING:
# class is tailored to parse the output of gprof located in '~/data/gprof.out'

from parsing.fprof_result.call_record import CallDetailRecord


class GProfResult:
    def __init__(self):
        from parsing.fprof_result.call_record import FunctionCall

        self._call_records: list[FunctionCall] = None
        self._dict_call_records: dict[str, FunctionCall] = {}

    def get_result(self, module: str, function: str):
        
        key = f'{module}.{function}'

        if key in self._dict_call_records:
            return self._dict_call_records[key]

        for record in self._call_records:
            if record.is_for(module, function):
                self._dict_call_records[key] = record
                return record
            
    
    def set_root_function(self, module: str, function: str):
        self._root_function = self.get_result(module, function)

        for func in self._call_records:
            func.set_not_visited_from_root()

        queue = [self._root_function]
        visited_functions = set()

        while len(queue) != 0:
            current_function = queue.pop(0)
            visited_functions.add(current_function)

            current_function.set_visited_from_root()

            for callee in current_function.get_called_functions():
                if callee not in visited_functions:
                    queue.append(callee)


    @staticmethod
    def load_from(filepath: str) -> 'GProfResult':
        from parsing.fprof_result.call_record import FunctionCall
        
        gprof_result = GProfResult()

        content = open(filepath).read().split('\n')

        flat_profile_lines = GProfResult._get_flat_profile_lines(content)
        call_results_objects = [FunctionCall(line, gprof_result) for line in flat_profile_lines]

        call_detail_lines = GProfResult._get_call_detail_records(content)
        call_detail_objects = [CallDetailRecord(line) for line in call_detail_lines]


        for call_result in call_results_objects:
            for call_detail in call_detail_objects:
                if call_result.can_register(call_detail):
                    call_result.register(call_detail)
                    break

        gprof_result._call_records = call_results_objects
        return gprof_result
    
    @staticmethod
    def _get_flat_profile_lines(content: list[str]) -> list[str]:
        # lines start from 5th line and end when an empty line is found

        lines = []
        for line in content[5:]:
            if line.strip() == '':
                break

            lines.append(line)

        return lines

    @staticmethod
    def _get_call_detail_records(content: list[str]) -> list[str]:
        records_part = '\n'.join(content).split('index % time    self  children    called     name\n')[1]
        records = records_part.split('-----------------------------------------------\n')[:-1]

        return records





