# KVM integration in vmcloak
In order to deceive anti-VM tricks, I noticed malware samples relying on checking some particular values in registry keys located in the following addresses:  

```
HKEY_LOCAL_MACHINE\HARDWARE\DEVICEMAP\Scsi\Scsi Port 0\Scsi Bus 0\Target Id 0\Logical Unit Id 0 [Identifier=”QEMU HARDDISK”]
HKEY_LOCAL_MACHINE\HARDWARE\DEVICEMAP\Scsi\Scsi Port 0\Scsi Bus 0\Target Id 1\Logical Unit Id 0 [Identifier=”QEMU DVD-ROM”]  
HKEY_LOCAL_MACHINE\HARDWARE\DESCRIPTION\System\SystemBiosVersion
```  
For the BIOS version, we have control over it by setting the value in Sysinfo of the domain and changing the `smbios=”sysinfo”`, while the Identifier string which for example QCOW2 disk has been created based on that cannot permanently be manipulated by setting the flag in VM configuration time. Instead, we need to *re-compile* the QEMU project and selectively modify the constants which malware samples are looking for. All the patches are located under [dispatcher/roles/cuckoo/files/qemu-patch.sh](https://github.com/AdaptiveComputationLab/dispatcher/blob/136d4f0495533974e4d96e26bc361bcac88bae87/roles/cuckoo/files/qemu-patch.sh) file.   
So far, just for QEMU, we have 4 config files which basically one of them doesn’t have any sort of modification enabled, one is modified in config but still has artifacts left in registry keys, the most secured one doesn’t have any artifact left in the system also. 

We limited our experiments to windows7x86 with the following configuration setup among different instances:
```
    "ram_size": "1024",
    "vram_size": "1024",
    "hdd_size": "",
    "cpus": "2",
    "hdd_adapter": "buslogic",
    "hdd_vdev": "lsisas1068"
```

Extra configurations added to the KVM for each instance is as the following:
```
    "bios.vendor": "Apple Inc.",
    "bios.version": "MB52.88Z.0088.B05.0904162222",
    "bios.date": "08/10/13",
    "bios.release": "5.9",
    "system.manufacturer": "Dell Inc.",
    "system.product": "XPS 15 9570",
    "system.version": "3.0",
    "system.serial": "33HGZW2",
    "system.uuid": "4C4C4544-0033-4810-8047-B3C04F5A5732",
    "system.sku": "087C",
    "system.family": "XPS",
    "baseBoard.manufacturer": "Dell Inc.",
    "baseBoard.product": "0D0T05",
    "baseBoard.version": "A00",
    "baseBoard.serial": "/33HGZW2/CNCMK0095T040B/",
    "baseBoard.asset": "BaseBoard Asset Tag#",
    "baseBoard.location": "Board Loc In",
    "chassis.manufacturer": "Dell Inc.",
    "chassis.version": "Mac-F22788AA",
    "chassis.serial": "33HGZW2",
    "chassis.asset": "Chassis Tag#",
    "chassis.sku": "Notebook",
    "oemStrings.entry": [
        "String 1: Dell System",
        "String 2: 1[087C]",
        "String 3: 3[1.0]",
        "String 4: 12[www.dell.com]",
        "String 5: 14[1]",
        "String 6: 15[0]",
        "String 7: 27[6741092018]"]
```


Since some specific artifacts like SCSI bus identifier won’t be persistent even after updating the registry key values, I decided to selectively find those specific constants in QEMU source-code and updating them to another string, and finally re-compiling the whole solution for the pipeline (->kvm->libvirt).

Based on some manual analysis I’ve done on anti-VM samples targeting QEMU, I found the following additional constants can also be used to detect the execution environment in which a regular user doesn’t have access to change those if relies on the original version of QEMU for creating disk and adding other peripherals to the system.

IDE/SCSI Disk Identifiers located at the following source-codes: 
* https://github.com/qemu/qemu/blob/master/hw/ide/core.c#L2505-#L2511  
* https://github.com/qemu/qemu/blob/master/hw/scsi/scsi-disk.c#L2422  
* https://github.com/qemu/qemu/blob/master/hw/ide/atapi.c#L785-#L796  
* https://github.com/qemu/qemu/blob/master/target/i386/kvm.c#L1417   
