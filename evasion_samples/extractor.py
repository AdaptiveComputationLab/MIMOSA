#!/usr/bin/env python3
from zipfile import ZipFile
import os
import shutil

PASSWD = b"MalwareBehaviorReports"
SAMPLES_PATH = '/var/malware/wild-samples.zip'
REPORT_PATH = '/var/malware/wild-reports.zip'
MAL_DICT = dict()

def main():

    with open('./vmevasion_samples.md5') as f:
        malware_list = f.read().strip().split('\n')

    with ZipFile(SAMPLES_PATH, 'r') as zf:
        inflst = zf.infolist()
        for inf in inflst:
            for mal in malware_list:
                if mal in inf.filename:
                    if mal in MAL_DICT.keys():
                        MAL_DICT[mal]['sample_path'] = inf.filename
                    else:
                        MAL_DICT[mal] = {'sample_path':'', 'report_path': []}
                        MAL_DICT[mal]['sample_path'] = inf.filename

        with ZipFile(REPORT_PATH, 'r') as f:
            inflst = f.infolist()
            for inf in inflst:
                for mal in malware_list:
                    if mal in inf.filename and 'win7.json' in inf.filename:
                        MAL_DICT[mal]['report_path'].append(inf.filename)

            for mal, dlist in MAL_DICT.items():
                os.makedirs(mal, exist_ok=True)
                sample = os.path.basename(dlist['sample_path'])
                src = zf.open(dlist['sample_path'], pwd=PASSWD)
                dst = open(os.path.join(mal, sample), 'wb')
                with src, dst:
                    shutil.copyfileobj(src, dst)

                for rp in dlist['report_path']:
                    rep_file = os.path.basename(rp)
                    src = f.open(rp, pwd=PASSWD)
                    dst = open(os.path.join(mal, rep_file), 'wb')
                    with src, dst:
                        shutil.copyfileobj(src, dst)


if __name__ == '__main__':
    main()
