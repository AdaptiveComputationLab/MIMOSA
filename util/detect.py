#!/usr/bin/env python
import sys
import os
import json
import re
import glob
import logging
import hashlib

from bitarray import bitarray

logging.basicConfig(level=logging.DEBUG)
l = logging.getLogger(__name__)

# bit_mapping
PROCESS_DETECTION = 0
DEBUGGER_PRESENT = 1
CPUID = 2
RDTSC = 3
CPU_COUNT = 4
INVALID_INST = 5
TICK_COUNT = 6
HCI = 7
BIOS = 8
DRIVER_CHECK = 9
SCSI_CHECK = 10
HDD_SIZE = 11
MEM_SIZE = 12
MAC_ADDR = 13
ACPI = 14

DEFAULT = '0'*15

process_map = {'vmware': ['vm3dmp.sys', 'vmusbmouse.sys', 'Vmhgfs.sys',
                'vmwareuser.exe', 'vmtoolsd.exe', 'vmmouse.sys'],
                'virtualbox': ['vboxguest.sys', 'vboxmouse.sys',
                    'vboxsf.sys', 'vboxvideo.sys',
                    'Vboxservice.exe', 'vboxtray.exe']
            }

mitigations = set([PROCESS_DETECTION, DEBUGGER_PRESENT, CPUID, RDTSC, CPU_COUNT,
                   INVALID_INST, TICK_COUNT, HCI, BIOS, DRIVER_CHECK,
                   SCSI_CHECK, HDD_SIZE, MEM_SIZE, MAC_ADDR, ACPI])

behavior_map = {DEBUGGER_PRESENT: ["debugger", "debug"], INVALID_INST: ["Switching processor"],
                RDTSC: ["rdtsc", "timing analysis detection", "rdtsc_GetTickCount"],
                HDD_SIZE: ["disk", "IOCTL_DISK_GET_LENGTH_INFO"],
                MEM_SIZE: ["memory"], BIOS: ["bios"], ACPI: ["ACPI"],
                SCSI_CHECK: ["HDD"], DRIVER_CHECK: ["drivers"],
                HCI: ["mouse", "keyboard"], TICK_COUNT: ["rdtsc_GetTickCount"],
                CPU_COUNT: ["processor detection"]
                }

mitigation_map = {'hopper1_kvm_patched_conf1': bitarray('110011011110011'),
                  'hopper1_kvm_patched_conf2': bitarray('110011011110101'),
                  'hopper2_vmware_conf3': bitarray('111010011110011'),
                  'hopper4_vmware_conf2': bitarray('110000010100101'),
                  'hopper5_vmware_conf2_vmtools': bitarray('010010010000101'),
                  'hopper6_kvm_legacy_conf1': bitarray('110011011100111'),
                  'hopper6_kvm_legacy_conf2': bitarray('110001011100001'),
                  'hopper3_vbox_conf1': bitarray('111011011111100'),
                  'hopper3_vbox_conf2': bitarray('110001010111010'),
                  'hopper8_vbox_conf1_guestadditions': bitarray('010001011011000'),
                  'hopper8_vbox_conf2_guestadditions': bitarray('010011010011011'),
                  'hopper7_qemu_legacy_conf1': bitarray('111111111110011'),
                  'hopper7_qemu_legacy_conf2': bitarray('111011011110101')
                  }

def proc_map(report):
    proc_list = []
    ret = 'unknown'
    for r in report:
        m = re.findall(r'processes: ([\w\d.]+) ', r)
        if m:
            proc_name = m[0]
            proc_list.append(proc_name)
    for backend, procs in process_map.items():
        for p in proc_list:
            if p in procs:
                if ret != 'unknown' and ret != backend:
                    ret = 'both'
                    break
                else:
                    l.debug("%s detected by process name."%backend)
                    ret = backend
    return ret

def get_sha1sum(fpath):
    BLOCKSIZE = 65536
    hasher = hashlib.sha1()
    with open(fpath, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    return str(hasher.hexdigest())

def main(path):
    malware_map = dict()
    mitigation_rate = dict()
    hash_bitmap = dict()
    if os.path.exists(os.path.expanduser(path)):
        dir_list = glob.glob(path+"/*")
        for d in dir_list:
            if not os.path.isdir(d):
                continue
            # flag to prevent checking evasion techniques count for samples per
            # configs
            checked = False
            proc_flag = False
            for config, bitmap in mitigation_map.items():
                l.debug("%s -> %s"%(config, bitmap.to01()))
                m = re.findall(r'/([0-9a-f]{40})', d)
                if m:
                    sha1sum = m[0]
                report_path = os.path.join(d, sha1sum+"-report-win7.json")
                report = json.loads(open(report_path).read())
                if os.path.exists(report_path):
                    if 'malicious_activity' in report['data'].keys():
                        sha1 = get_sha1sum(os.path.join(d, sha1sum+".bin"))
                        if sha1 not in malware_map.keys():
                            malware_map[sha1] = dict()
                            malware_map[sha1][config] = bitarray(DEFAULT)
                        else:
                            malware_map[sha1][config] = bitarray(DEFAULT)
                        mal_activity = report['data']['malicious_activity']
                        evlist = list(map(lambda x: re.findall(r'Evasion: (.*)', x), mal_activity))
                        evasion_list = [x[0].lower() for x in evlist if len(x)]
                        bitmap_sample = malware_map[sha1][config]
                        if any("Searching for specific processes".lower() in x for x in
                            evasion_list):
                            proc_flag = True
                            backend = proc_map(evasion_list)
                            l.debug("detected backend: %s"% backend)
                            if backend == 'both':
                                bitmap_sample[PROCESS_DETECTION] = True
                            elif backend == 'vmware' and 'vmware' in config:
                                bitmap_sample[PROCESS_DETECTION] = True
                            elif backend == 'virtualbox' and 'vbox' in config:
                                bitmap_sample[PROCESS_DETECTION] = True
                            if not checked:
                                if PROCESS_DETECTION not in mitigation_rate.keys():
                                    mitigation_rate[PROCESS_DETECTION] = 1
                                else:
                                    mitigation_rate[PROCESS_DETECTION] += 1
                        for artifact, item in behavior_map.items():
                            # detected this artifact existed in this sample
                            if any(x.lower() in y for x in item for y in evasion_list):
                                # check if config has any protection against it?
                                if bitmap_sample[artifact] == False:
                                    bitmap_sample[artifact] = True
                                    l.debug(item)
                                if not checked:
                                    if artifact not in mitigation_rate.keys():
                                        mitigation_rate[artifact] = 1
                                    else:
                                        mitigation_rate[artifact] += 1

                    bitmap.invert()
                    result = bitmap_sample & bitmap
                    l.debug("bitmap_sample = %s"%bitmap_sample.to01())
                    if proc_flag:
                        bitmap_sample[PROCESS_DETECTION] = True
                    hash_bitmap[sha1] = [bitmap_sample.to01(), ", ".join(evasion_list)]
                    import ipdb; ipdb.set_trace()
                    # revert the action
                    bitmap.invert()
                    if result.count() != 0:
                        # there're some artifacts has not been mitigated and
                        # sample can detect those
                        malware_map[sha1][config] = False
                    else:
                        # defeated the malware anti-vm detection techniques
                        malware_map[sha1][config] = True
                else:
                    l.debug('%s not found!'%report_path)
                    exit(1)
                checked = True

    with open("./evasion_results.csv", "w") as f:
        configs = "; ".join(mitigation_map.keys())
        csv_header = "sha1sum; %s\n"%configs
        f.write(csv_header)
        for sha1sum, configs in malware_map.items():
            line_writer = "%s; %s\n" % (sha1sum, "; ".join([str(x) for x in
                                                          configs.values()]))
            f.write(line_writer)

    with open("./mitigation_rate.csv", "w") as fd:
        header = "artifact; count #\n"
        fd.write(header)
        for artifact, count in mitigation_rate.items():
            if artifact == PROCESS_DETECTION:
                fd.write("PROCESS_DETECTION; %s\n"%count)
            elif artifact == DEBUGGER_PRESENT:
                fd.write("DEBUGGER_PRESENT; %s\n"% count)
            elif artifact == CPUID:
                fd.write("CPUID; %s\n"% count)
            elif artifact == RDTSC:
                fd.write("RDTSC; %s\n"% count)
            elif artifact == CPU_COUNT:
                fd.write("CPU_COUNT; %s\n"% count)
            elif artifact == INVALID_INST:
                fd.write("INVALID_INST; %s\n"% count)
            elif artifact == TICK_COUNT:
                fd.write("TICK_COUNT; %s\n"% count)
            elif artifact == HCI:
                fd.write("HCI; %s\n"% count)
            elif artifact == BIOS:
                fd.write("BIOS; %s\n"% count)
            elif artifact == DRIVER_CHECK:
                fd.write("DRIVER_CHECK; %s\n"% count)
            elif artifact == SCSI_CHECK:
                fd.write("SCSI_CHECK; %s\n"% count)
            elif artifact == HDD_SIZE:
                fd.write("HDD_SIZE; %s\n"% count)
            elif artifact == MEM_SIZE:
                fd.write("MEM_SIZE; %s\n"% count)
            elif artifact == MAC_ADDR:
                fd.write("MAC_ADDR; %s\n"% count)
            elif artifact == ACPI:
                fd.write("ACPI DSDT; %s\n"% count)
            else:
                l.debug("not listed in the defined default mapping!")

    with open("./hash_bitmap.csv", "w") as f:
        header = "sha1sum; evasion; bitmap\n"
        f.write(header)
        for sha1sum, alist in hash_bitmap.items():
            bitmap = alist[0]
            evasion = alist[1]
            f.write("%s; %s; %s\n"%(sha1sum, evasion, bitmap.zfill(15)))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
