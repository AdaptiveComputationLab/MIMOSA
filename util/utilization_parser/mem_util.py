import re

from utilization_parser.parser import Parser

class mem_util(Parser):
    def __init__(self, fname):
        super(mem_util, self).__init__(fname)
        self.content = open(self.filename).read()

    def parse(self, process="*"):
        """Read performance counter for memory object."""
        ret = dict()
        r = re.compile(r'\"\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}\.\d{3}\",\"(?P<commit>\d+)\",\"(?P<avail>\d+)\"\,\"(?P<cache>\d+)\"\n')
        ret['commit'] = [float(m.group('commit')) for m in r.finditer(self.content)]
        ret['available'] = [float(m.group('avail')) for m in r.finditer(self.content)]
        ret['cache'] = [float(m.group('cache')) for m in r.finditer(self.content)]

        return ret
