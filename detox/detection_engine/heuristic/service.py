import logging

from . import Detection
from detection_engine.parser import ReportParser

l = logging.getLogger(name=__name__)
l.setLevel(logging.DEBUG)

class ServiceDetection(Detection):
    name = 'service'
    def __init__(self, report):
        super(ServiceDetection, self).__init__()
        if isinstance(report, ReportParser):
            self.report = report
        self.service_map = {'vmware': ['vm3dmp', 'vmusbmouse', 'vmhgfs',
                                    'vmwareuser', 'vmtoolsd',
                                      'vmmouse', 'hgfs'],
                         'virtualbox': ['vboxguest', 'vboxmouse',
                                        'vboxsf', 'vboxvideo',
                                        'Vboxservice', 'vboxtray',
                                        'vboxguest'],
                        'parallels': ['prl_boot']
                         }

    def init(self):
        pass

    # service detection
    def detect(self):
        ret = False
        self.services = self.report.enumerate_services()
        for service in self.services.values():
            for s in service:
                if any([s.lower() in v for v in self.service_map.values()]):
                    l.debug('detected through service enumeration.')
                    ret = True
                    break
        return ret
