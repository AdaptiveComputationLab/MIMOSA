import logging
import ntpath

from . import Detection
from detection_engine.parser import ReportParser

l = logging.getLogger(name=__name__)
l.setLevel(logging.DEBUG)

class DriverDetection(Detection):
    name = 'driver'
    def __init__(self, report):
        super(DriverDetection, self).__init__()
        if isinstance(report, ReportParser):
            self.report = report
        self.calls = dict()
        self.suspec_api = ['GetFileAttributesW', 'GetFileAttributesA', 'NtCreateFile']
        self.driver_map = {'vmware': ['vm3dmp.sys', 'vmusbmouse.sys', 'Vmhgfs.sys',
                                    'vmwareuser.exe', 'vmtoolsd.exe',
                                      'vmmouse.sys', 'HGFS'],
                         'virtualbox': ['vboxguest.sys', 'vboxmouse.sys',
                                        'vboxsf.sys', 'vboxvideo.sys',
                                        'Vboxservice.exe', 'vboxtray.exe',
                                        'VBoxGuest'],
                        'parallels': ['prl_boot.sys']
                         }
        self.drivers = []
        self.init()

    def init(self):
        for p in self.report.processes:
            if p.call:
                p.call.sort(key=lambda x: x.time)
                self.calls[p.pid] = p.call

    # driver detection
    def detect(self):
        ret = False
        drv_name = ''
        for _, apis in self.calls.items():
            for api in apis:
                if api.name in self.suspec_api:
                    file_path = api.args['filepath_r']
                    drv_name = ntpath.basename(file_path)
                    if any([drv_name in v for v in self.driver_map.values()]):
                        ret = True
                        self.drivers.append(drv_name)
                        l.debug("%s detected!"%drv_name)
        return ret
