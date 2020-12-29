import glob
import os
import re

from detection_engine.runner import Runner

class Differ(object):
    DIRS = ['vmware-vbox', 'vmware', 'virtualbox']
    def __init__(self, path):
        self.path = path
        self.abs_list = []

    def scan_dirs(self, backend):
        if os.path.exists(self.path):
            dirs = glob.glob(os.path.join(self.path, backend, '*/'))
            self.abs_list = list(map(lambda x: os.path.abspath(x), dirs))

    def diff(self):
        for backend in Differ.DIRS:
            self.scan_dirs(backend)
            for d in self.abs_list:
                match = re.findall(r'([a-f0-9]{40})', d)
                if match:
                    sample_hash = match[0]
                    for i in range(1, 9):
                        report_name = "%s-report-hopper%s.json"%(sample_hash, str(i))
                        ds_report = "%s-report-win7.json"%(sample_hash)
                        report_path = os.path.join(d, report_name)
                        ds_report_path = os.path.join(d, ds_report)
                        if os.path.exists(report_path):
                            print("running analysis on %s..."%os.path.basename(report_path))
                            Runner(report_path, ds_report_path).detect()

