import logging

from . import Detection
from detection_engine.parser import ReportParser

l = logging.getLogger(name=__name__)
l.setLevel(logging.DEBUG)

class CPUDetection(Detection):
    name = 'cpu'
    def __init__(self, report):
        super(CPUDetection, self).__init__()
        if isinstance(report, ReportParser):
            self.report = report
        self.calls = dict()
        self.init()

    def init(self):
        for p in self.report.processes:
            if p.call:
                p.call.sort(key=lambda x: x.time)
                self.calls[p.pid] = p.call

    # driver detection
    def detect(self):
        ret = False
        for _, apis in self.calls.items():
            for api in apis:
                if api.name == "GetSystemInfo":
                    cpu_count = api.args['processor_count']
                    if cpu_count < 2:
                        ret = True
                        l.debug("detected vm using number of cpus!")
        return ret
