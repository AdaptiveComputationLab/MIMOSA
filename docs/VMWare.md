# VMWare integration in vmcloak
In the VMWare configs that I generated, I tried to fix one of the parameters that I considered to be a more well-known pattern for VM detection. For example, one of the most popular techniques is to check for MAC address Vendor ID which are the first three bytes of MAC and in the following, you can find the hardcoded MAC addresses mapped to various different VMWare products:  
 
 | # | Range of Prefix | Vendor | Virtual Machine |
 |:-:|:---------------:|:------:|:---------------:|
 |1  | 00:50:56 | VMWare | VMware vSphere, VMware Workstation, VMware ESX Server|
 |2  | 00:50:56:80:00:00 - 00:50:56:BF:FF:FF | VMWare |  VMware vSphere managed by vCenter Server | 
 |3  | 00:0C:29 | VMWare | Standalone VMware vSphere, VMware Workstation, VMware Horizon | 
 |4  | 00:05:69 | VMWare | VMware ESX, VMware GSX Server |

## Analysis tools detection heuristic
Some of the malware samples tend to check for the existence of a set of process names in their blacklist. This predefined list is nothing but a curated list of process names mapped to agents of analysis tools (Hypervisor drivers, process, malware analysis tools) in the guest environment. In the following you can find a list that we found malware samples using these artifacts usually look for:  


| Analysis tool | Process name | Details | 
| :------:      | :-----:      | :-----: |
| VMWare Workstation | vm3dmp.sys, vmusbmouse.sys,Vmhgfs.sys, vmwareuser.exe, vmtoolsd.exe, vmmouse.sys | Vmmouse is the mouse driver of vmware installed on guest, part of VMWare tools service |
| Virtualbox | vboxguest.sys, vboxmouse.sys, vboxsf.sys, vboxvideo.sys, Vboxservice.exe, vboxtray.exe | |
| Sandbox IE | Sbiesvc.exe, sbiedll.exe, sbiectrl.exe | 
|  Virtual PC | Vpcmap.exe, vmsrvc.exe | Virtual Machine Additions, Virtual Pc Integration Components | 
| Xen | xenservice.exe | |

