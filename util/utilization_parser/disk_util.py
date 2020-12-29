import re

from utilization_parser.parser import Parser

class disk_util(Parser):
    def __init__(self, fname):
        super(disk_util, self).__init__(fname)
        self.content = open(self.filename).read()

    def parse(self):
        """Read performance counter for physical disk object."""
        ret = dict()
        r = re.compile(r'\"\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}\.\d{3}\",\"(?P<read>\d+\.\d+|\d+)\",\"(?P<write>\d+\.\d+|\d+)\"\n')
        ret['read'] = [float(m.group('read')) for m in r.finditer(self.content)]
        ret['write'] = [float(m.group('write')) for m in r.finditer(self.content)]

        return ret
