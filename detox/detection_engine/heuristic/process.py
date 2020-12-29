import logging

from . import Detection
from detection_engine.parser import ReportParser

l = logging.getLogger(name=__name__)
l.setLevel(logging.DEBUG)

class ProcessDetection(Detection):
    name = 'process'
    def __init__(self, report):
        super(ProcessDetection, self).__init__()
        if isinstance(report, ReportParser):
            self.report = report
        self.calls = dict()
        self.proc_map = {'vmware': ['vm3dmp.sys', 'vmusbmouse.sys', 'Vmhgfs.sys',
                                    'vmwareuser.exe', 'vmtoolsd.exe', 'vmmouse.sys'],
                         'virtualbox': ['vboxguest.sys', 'vboxmouse.sys',
                                        'vboxsf.sys', 'vboxvideo.sys',
                                        'Vboxservice.exe', 'vboxtray.exe']
                         }
        self.proc_enum = []
        self.init()

    def init(self):
        for p in self.report.processes:
            if p.call:
                p.call.sort(key=lambda x: x.time)
                self.calls[p.pid] = p.call


    def detect(self):
        ctr = 0
        ret = False
        proc_name = ''
        for _, apis in self.calls.items():
            for api in apis:
                if api.name == "Process32NextW":
                    ctr += 1
                    proc_name = api.args['process_name']
                    self.proc_enum.append(proc_name)
            for backend, procs in self.proc_map.items():
                if proc_name == '':
                    break
                if proc_name in procs:
                    l.debug("%s detected!"%proc_name)
                    ret = True
                    break
        return ret

