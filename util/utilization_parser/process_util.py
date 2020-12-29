import re

from utilization_parser.parser import Parser

class process_util(Parser):
    def __init__(self, fname):
        super(process_util, self).__init__(fname)
        self.content = open(self.filename).read()

    def parse(self, process="*"):
            """Read performance counter for process object."""
            RE_PROC = r'\"\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}\.\d{3}\",(.*)\n'
            if not self.content:
                return
            data_list = re.findall(RE_PROC, self.content)
            if not data_list:
                return
            process_list = re.findall(r'Process\(([\w\d#.-]+)\)\\% Processor Time', self.content)
            process_count = len(process_list)
            process_PID = data_list[0].replace('\"','').split(',')[:process_count]
            cpu_usage = {p:[] for p in process_list}
            samples = len(data_list)

            for sample in range(samples):
                utilization = data_list[sample].replace('\"','').split(',')[process_count:]
                for process, t in zip(process_list, utilization):
                    if t == " ":
                        t = 0
                    cpu_usage[process].append(t)

            ret = list(map(float, cpu_usage["_Total"]))

            return ret
