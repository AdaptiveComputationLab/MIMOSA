#!/usr/bin/env python3
import numpy as np
import glob
import os
import sys
import re
#import json

from tqdm import tqdm
from utilization_parser.process_util import process_util
from utilization_parser.disk_util import disk_util
from utilization_parser.mem_util import mem_util

def main():
    if len(sys.argv) > 1:
        path = sys.argv[1]
        if os.path.exists(path):
            with open("%s.csv"% path, "w") as f:
                f.write("""sha1sum; disk_read_avg; disk_read_std; disk_write_avg; disk_write_std; proc_avg; proc_std; mem_commit_avg; mem_commit_std; mem_available_avg; mem_available_std; mem_cache_avg; mem_cache_std\n""")
                for d in tqdm(glob.glob(path+"/*")):
                    if os.path.isfile(d):
                        continue
                    else:
                        line_writer = ""
                        sha1sum = re.findall(r'/([0-9a-f]+)', d)[0]
                        line_writer += "%s; "%sha1sum
                        disk_path = os.path.join(d, "diskutil.csv")
                        proc_path = os.path.join(d, "procutil.csv")
                        mem_path = os.path.join(d, "memutil.csv")
                        #report_path = os.path.join(d, "report.json")
                        if os.path.exists(disk_path):
                            d = disk_util(fname=disk_path)
                            d_util = d.parse()
                            read = d_util['read']
                            write = d_util['write']
                            if not read:
                                line_writer += "nan; nan; nan; nan; "
                            else:
                                # average read/write
                                disk_read_avg = np.average(read)
                                disk_write_avg = np.average(write)
                                # std read/write
                                disk_read_std = np.std(read)
                                disk_write_std = np.std(write)
                                line_writer += "%s; %s; %s; %s; " % (disk_read_avg,
                                                                 disk_read_std,
                                                                 disk_write_avg,
                                                                 disk_write_std)
                        else:
                            # x means missing data!
                            line_writer += "x; x; x; x; "
                        if os.path.exists(proc_path):
                            p = process_util(proc_path)
                            # return _Total
                            p_util = p.parse()
                            if not p_util:
                                line_writer += "nan; nan; "
                            else:
                                total_avg = np.average(p_util)
                                total_std = np.average(p_util)
                                line_writer += "%s; %s; " % (total_avg, total_std)
                        else:
                            line_writer += "x; x; "
                        if os.path.exists(mem_path):
                            mem = mem_util(mem_path)
                            m = mem.parse()
                            if not m['commit']:
                                line_writer += "nan; nan; nan; nan; nan; nan\n"
                            else:
                                commit_avg = np.average(m['commit'])
                                available_avg = np.average(m['available'])
                                cache_avg = np.average(m['cache'])
                                commit_std = np.std(m['commit'])
                                available_std = np.std(m['available'])
                                cache_std = np.std(m['cache'])
                                line_writer += "%s; %s; %s; %s; %s; %s\n" % \
                                (commit_avg, commit_std, available_avg,
                                available_std, cache_avg, cache_std)
                        else:
                            line_writer += "x; x; x; x; x; x\n"
                        #if os.path.exists(report_path):
                        #    report = json.load(open(report_path))
                        #    start = float(report["info"]["started"])
                        #    end = float(report["info"]["ended"])
                        #    duration = float(end - start)
                        #    line_writer += "%s\n" % duration
                        #else:
                        #    line_writer += "x\n"

                        f.write(line_writer)


if __name__ == "__main__":
    main()
