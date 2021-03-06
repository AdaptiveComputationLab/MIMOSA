# MIMOSA: Malware Instrumentation with Minimized Overhead for Stealthy Analysis
[![DOI](https://zenodo.org/badge/325234378.svg)](https://zenodo.org/badge/latestdoi/325234378)  
MIMOSA is a system for selecting and deploying covering combinations of artifact mitigations to maximize analysis throughput and accuracy. Mimosa project consists of four modules integrated to create an end-to-end pipeline for feedback-driven, low-overhead, and large-scale evasive malware analysis. MIMOSA is a collaborative result of [The Adaptive Computation Lab at Arizona State University (ASU)](https://github.com/AdaptiveComputationLab/), [Electerical Engineering and Computer Science Department of University of Michigan Ann Arbor (UMich)](http://web.eecs.umich.edu/~weimerw/), and [the Computer Security Lab at University of California Santa Barbara (UCSB)](https://seclab.cs.ucsb.edu/). 

# Workflow
Based on Fig 1, we briefly describe each sub-project and our contribution in each of those. One of our major novelties is incorporating a cost model in producing configuration covers. 

* [covering-alg](./covering-alg/README.md): Algorithm receives a cost model, set of known artifacts, and their corresponding mitigation sterategies. Cost model should be decided by analyst and could be any non-negative cost function which denotes the development/analysis effort or analysis latency. Each artifact family comes with a mitigation sterategy represented as a configuration. Each configuration comes with a cost given the cost function. The covering algorithm then selects from the many possible configurations to produce a small set which optimize the trade-off between cost and coverage.
* [cuckoo](https://github.com/pwnslinger/cuckoo/tree/wip/patch_aux): Cuckoo is an automated malware analysis system. We added performance counter retrieval functionalities as auxiliary modules for quering Disk, CPU, and Memory utilization during an analysis session. These metrics used to create a cost model for our covering algorithm. 
* [VMCloak](https://github.com/AdaptiveComputationLab/vmcloak/): VMCloak is a VM orchestration, management, and provisioning framework that supports VirtualBox, VMWare Workstation, and Libvir-backend (KVM, QEMU, XEN) hypervisors. As an input, VMCloak receives a set of hardware (RAM, CPU, HDD-size), firmware (BIOS/EFI, SCSI), and software (a specific version of an application like Microsoft Office 2013) configurations and outputs a deployable ready to use snapshot per each hypervisor. Also, It comes with the support to automatically install various Operating Systems (Windows, Linux), translate configuration parameters for different hypervisor backend, and automatic network configuration. Consequently, VMCloak makes it pretty easy to create customized Virtual Machines in a completely automated manner. Our contribution in VMCloak is the following:  
    *  [dev/vmware](https://github.com/AdaptiveComputationLab/vmcloak/tree/dev/vmware) branch: Virtualization layer for VMware Workstation using vmrun utility including parser for vmx (VMWare VM configuration file), setting various VM attributes such as RAM, CPU, HDD to advanced settings like hypervisor-level options. For more information on the VMWare integration please take a look at [docs/VMWare.md](./docs/VMWare.md)
    * [dev/kvm](https://github.com/AdaptiveComputationLab/vmcloak/tree/dev/kvm): Virtualization layer for KVM using libvirt utility. A customized XML parser for creating, modifying, and removing various settings of a VM from simple options like hardware to advanced para-virtualization technology settings. For more information on the KVM integration please take a look at [docs/KVM.md](./docs/KVM.md).
* [detox](https://github.com/AdaptiveComputationLab/detox/): Detox is a correlation engine for API trace and VM state logs received from each instance to infer semantic patterns on the success or failure of a malware execution. In particular, Detox detects if the process exits, if certain network communication patterns exist, or if certain process names are created. We conclude that a sample has executed successfully if it runs to termination under each environment.
* [dispatcher](https://github.com/AdaptiveComputationLab/dispatcher/): is a set of Ansible scripts that deploys the nodes on a cluster based on the covers set provided by the covering lattice algorithm. For instance, it configures the network and firewall rules on nodes, collects the analysis results of each analysis session and stores the results in the log collector. 

<div style="text-align:center"><figure><img src="./images/mimosa.svg"><figcaption>Fig.1 - MIMOSA pipeline consists of Covering algorithm, VMCloak, Dispatcher, and Detox</figcaption></figure></div>

# Documentation
Here we share the results of our experiments with the community. All of the results are reproduceable using the scripts provided in this repository. Also, we share a presentation file which demonstrates more in-depth information of the design. 

1. [Presentation](./docs/MIMOSA.pdf): Here is the link to the presentation prepared for the project and used as a weekly update sync up with the team members.  
2. [mimosa_cost_results.xlsx](./stats/mimosa_cost_results.xlsx): Results of running each sample under different configuration and their resulting I/O, Memory, CPU utilization per config per sample. These numbers are the basis of our cost model for covering algorithm described in [covering-alg/README.md](./covering-alg/README.md).
3. [mimosa_VMs.xlsx](./stats/mimosa_VMs.xlsx): Contains VM mapping, sample attributes, some plots, and  statistics. 

# Citing MIMOSA  
MIMOSA has been submitted for publication as a journal paper at the IEEE Transactions on Dependable and Secure Computing (TDSC). Until its acceptance you can cite this research using the following:  

```tex
@misc{2101.07328,
Author = {Mohsen Ahmadi and Kevin Leach and Ryan Dougherty and Stephanie Forrest and Westley Weimer},
Title = {MIMOSA: Reducing Malware Analysis Overhead with Coverings},
Year = {2021},
Eprint = {arXiv:2101.07328},
}
```  

# Acknowledgement
We gratefully acknowledges the partial support of [NSF(CCF 1908633)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1908633), DARPA ([FA8750-19C-0003](https://govtribe.com/award/federal-contract-award/definitive-contract-fa875019c0003), [N6600120C4020](https://www.federalcompass.com/award-contract/N6600120C4020)),AFRL  ([FA8750-19-1-0501](https://govtribe.com/award/federal-idv-award/indefinite-delivery-contract-fa875019d0004)),  and  the  Santa  Fe  Institute.  Any opinions, findings, and conclusions in this paper are those of the authors and do not necessarily reflect the views of oursponsors. The  opinions  in  the  work  are  solely  of  the  authors, and do not necessarily reflect those of the U.S. Army, U.S.Army  Research  Labs,  the  U.S.  Military  Academy, or the Department of Defense (DoD).  
We also thank the anonymous reviewers for their valuable  comments  and  suggestions,  and  the  Avira  company,Alexander  Vukcevic,  Director  of  Protection  Labs  and  QA, and Shahab Hamzeloofard for helping us with determining provenance of our malware samples.
