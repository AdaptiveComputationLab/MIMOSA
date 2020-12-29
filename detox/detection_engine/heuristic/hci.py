import logging

from . import Detection
from detection_engine.parser import ReportParser

l = logging.getLogger(name=__name__)
l.setLevel(logging.DEBUG)

# detect by human interaction
class HCIDetection(Detection):
    name = 'hci'
    def __init__(self, report):
        super(HCIDetection, self).__init__()
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
        first = -1
        for _, apis in self.calls.items():
            for idx, api in enumerate(apis):
                if api.name == "GetCursorPos":
                    if first != -1:
                        if idx - first < 10:
                            ret = True
                            l.debug("detected vm using mouse human interaction!")
                            break
                    else:
                        first = idx
        return ret
