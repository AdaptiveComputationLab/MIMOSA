#!/usr/bin/env python
import glob
import os
import sys
import socket
import subprocess
import shutil
import re

from tqdm import tqdm

DIR="/localhome/%s/.cuckoo/storage/analyses/"%os.getenv('USER')
OUT_DIR = "/opt/share/results/"
hostname = socket.gethostname()

def rename(conf):
    for d in tqdm(glob.glob(DIR+"*")):
        if 'latest' in d or os.path.isfile(d):
            continue
        else:
            idx = re.findall(r'/analyses/([0-9]+)', d)
            if idx:
                idx = int(idx[0])
                result = subprocess.check_output(['sha1sum', os.path.join(d, 'binary')])
                sha1sum = result.split(' ')[0]
                hostname = socket.gethostname()
                DIR_NAME = "%s_%s"%(hostname, conf)
                HOST_DIR = os.path.join(OUT_DIR, DIR_NAME)
                if not os.path.exists(HOST_DIR):
                    os.makedirs(HOST_DIR)
                sample_path = os.path.join(OUT_DIR, HOST_DIR, sha1sum)
                if not os.path.exists(sample_path):
                    os.makedirs(sample_path)
                else:
                    continue
                report_path = os.path.join(d, "reports/report.json")
                if os.path.exists(report_path):
                    shutil.copy(report_path, os.path.join(sample_path,
                                                          "report.json"))
                    print("report %s copied successfully!"%sha1sum)
                disk_path = os.path.join(d, "shots/diskutil.csv")
                if os.path.exists(disk_path):
                    shutil.copy(disk_path, os.path.join(sample_path,
                                                          "diskutil.csv"))
                    print("diskutil.csv %s copied successfully!"%sha1sum)
                mem_path = os.path.join(d, "shots/memutil.csv")
                if os.path.exists(mem_path):
                    shutil.copy(mem_path, os.path.join(sample_path,
                                                          "memutil.csv"))
                    print("memutil.csv %s copied successfully!"%sha1sum)
                proc_path = os.path.join(d, "shots/procutil.csv")
                if os.path.exists(proc_path):
                    shutil.copy(proc_path, os.path.join(sample_path,
                                                          "procutil.csv"))
                    print("procutil.csv %s copied successfully!"%sha1sum)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        config = sys.argv[1]
        rename(config)
