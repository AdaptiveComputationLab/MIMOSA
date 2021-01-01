# MIMOSA
MIMOSA is a system for selecting and deploying covering combinations of artifact mitigations to maximize analysis throughput and accuracy. Mimosa project consists of four modules integrated to create an end-to-end pipeline for feedback-driven, low-overhead, and large-scale evasive malware analysis. MIMOSA is a collaborative result of [The Adaptive Computation Lab at Arizona State University (ASU)](https://github.com/AdaptiveComputationLab/), [Electerical Engineering and Computer Science Department of University of Michigan Ann Arbor (UMich)](http://web.eecs.umich.edu/~weimerw/), and [the Computer Security Lab at University of California Santa Barbara (UCSB)](https://seclab.cs.ucsb.edu/). 

# Workflow
In the following, we briefly describe each sub-project and our contribution in each of those. One of our major novelties is incorporating a cost model in producing configuration covers. 

* [covering-alg](./covering-alg/README.md): Algorithm receives a cost model, set of known artifacts, and their corresponding mitigation sterategies. Cost model should be decided by analyst and could be any non-negative cost function which denotes the development/analysis effort or analysis latency. Each artifact family comes with a mitigation sterategy represented as a configuration. Each configuration comes with a cost given the cost function. The covering algorithm then selects from the many possible configurations to produce a small set which optimize the trade-off between cost and coverage.
* [cuckoo](https://github.com/pwnslinger/cuckoo/tree/wip/patch_aux): Cuckoo is an automated malware analysis system. We added performance counter retrieval functionalities as auxiliary modules for quering Disk, CPU, and Memory utilization during an analysis session. These metrics used to create a cost model for our covering algorithm. 
* [VMCloak](https://github.com/AdaptiveComputationLab/vmcloak/): VMCloak is a VM orchestration, management, and provisioning framework that supports VirtualBox, VMWare Workstation, and Libvir-backend (KVM, QEMU, XEN) hypervisors. As an input, VMCloak receives a set of hardware (RAM, CPU, HDD-size), firmware (BIOS/EFI, SCSI), and software (a specific version of an application like Microsoft Office 2013) configurations and outputs a deployable ready to use snapshot per each hypervisor. Also, It comes with the support to automatically install various Operating Systems (Windows, Linux), translate configuration parameters for different hypervisor backend, and automatic network configuration. Consequently, VMCloak makes it pretty easy to create customized Virtual Machines in a completely automated manner. Our contribution in VMCloak is the following:  
    *  [dev/vmware](https://github.com/AdaptiveComputationLab/vmcloak/tree/dev/vmware) branch: Virtualization layer for VMware Workstation using vmrun utility including parser for vmx (VMWare VM configuration file), setting various VM attributes such as RAM, CPU, HDD to advanced settings like hypervisor-level options. 
    * [dev/kvm](https://github.com/AdaptiveComputationLab/vmcloak/tree/dev/kvm): Virtualization layer for KVM using libvirt utility. A customized XML parser for creating, modifying, and removing various settings of a VM from simple options like hardware to advanced para-virtualization technology settings. 
* [detox](https://github.com/AdaptiveComputationLab/detox/): Detox is a correlation engine for API trace and VM state logs received from each instance to infer semantic patterns on the success or failure of a malware execution. In particular, Detox detects if the process exits, if certain network communication patterns exist, or if certain process names are created. We conclude that a sample has executed successfully if it runs to termination under each environment.
* [dispatcher](https://github.com/AdaptiveComputationLab/dispatcher/): is a set of Ansible scripts that deploys the nodes on a cluster based on the covers set provided by the covering lattice algorithm. For instance, it configures the network and firewall rules on nodes, collects the analysis results of each analysis session and stores the results in the log collector. 

<div style="text-align:center"><figure><img src="./images/mimosa.svg"><figcaption>Fig.1 - MIMOSA pipeline consists of Covering algorithm, VMCloak, Dispatcher, and Detox</figcaption></figure></div>

# Additionals
Here we briefly go through some other scripts and tools we developed to help us during the research. 


# How to run?


# Reviewer
This repository contains all the code and experiments for the MIMOSA paper submitted to the TDSC journal. 