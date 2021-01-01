# Utilities
Here I describe the utilities we used for automating the test, drawing the graphics, collecting the artifacts, etc.

1. [pafish_test.py](./pafish_test.py): this script runs [pafish](https://github.com/a0rtega/pafish) on each VM instance to make sure the artifacts successfully mitigated inside the guest OS. Script simply runs the pafish and send the logs back to dispatcher module by communicating through the agent. 

2. [collector.py](./collector.py): simply connects to each server in the cluster and downloads the following files for further processing by the [detox](../detox/README.md) engine and our covering algorithm:  
    * **diskutil.csv**: disk utilization for physical disk over the span of malware runtime inside the VM instance. It contains the following information per each line:  

        * \PhysicalDisk(0 C:)\Disk Read Bytes/sec: The average time, in seconds, to read a block of data  
        * \PhysicalDisk(0 C:)\Disk Write Bytes/sec: The average time, in seconds, to write a block of data

    * **memutil.csv**: queries the `Committed Bytes`, `Available Bytes`, and `Cached Bytes` from Memory object performance counter. In the following, you can find the detailed description for each of these counters and how we use it for our cost function <sup>[1](#typeperf)</sup>:
        
        * \Memory\Committed Bytes: The % Committed Bytes in Use performance counter represents the ratio of Memory\\Committed Bytes to the Memory\\Commit Limit. Committed Bytes is the amount of committed virtual memory while Commit Limit is the amount of virtual memory that can be committed without having to extend the paging file(s). When this performance threshold has been exceeded, it often indicates that the page file could not be expanded, or expanded fast enough, to satisfy application memory requirements.  

        * \Memory\Available Bytes: Reports the amount of memory in MB that is available for the operating system to use. Available MBytes is the amount of memory that is available for use by applications and processes.

        * \Memory\Cache Bytes: It is the total of these four individual counters: 
            * Memory: System Cache Resident Bytes  
            * Memory: System Driver Resident Bytes  
            * Memory: System Code Resident Bytes  
            * Memory: Pool Paged Resident Bytes  
        
    * **procutil.csv**: shows the percentage of the time that the processor takes to execute a non-idle thread during a sample interval. In other words, this counter shows processor activity. % Processor Time is calculated by subtracting the percentage of time to execute an idle thread from 100%. <sup>[2](#proctime)</sup>

3. [connector.py](./connector.py): driver for connecting to each hopper culster node to run and collect information. One use case of that is to run pafish experiments and collect the logs. 

4. [utilization parser](./utilization_parser)

5. [detect.py](./detect.py): creates the detection bitmap and calculates whether a malware sample could successfully run through termination under the instance config or not. There are variables which can be configured. For example, `mitigation_map` is a dictionary of configurations mapped to mitigated artifacts. If you take  a look at paper, in Table 3, List of tested configurations and the artifacts they mitigate. Each column corresponds to whether a specific category of artifact is mitigated in thatconfiguration.
    
    Results of this script are as the following: 

    * **evasion_results.csv**: Each row shows a sample ran under different instance configurations and their corresponding results. To better interpret the results, False means that specific config mitigated all the artifacts the sample at that row was looking for to escape the environment. Here is a snippet of our results for two samples as a show case. 
        
        | sha1sum | qemu_patched_conf1 | qemu_patched_conf2 | vmware_conf3 | vmware_conf2 | vmware_conf2_vmtools | qemu_legacy_conf1 | qemu_legacy_conf2 | vbox_conf1 | vbox_conf2 | vbox_conf1_guestadditions | vbox_conf2_guestadditions | qemu_legacy_conf1 | qemu_legacy_conf2 |
        |:---------:|:-------------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|
        | 208fa49421ba32c2a19c338dc75548451d3cee92 | True | True | True | False | False | False | False | True | False | False | False | True | True |  
        | 3cae64dda3c6f609d46131872ab32536fbdbbcbe | False | False | False | False | False | False | False | True | False | False | False | False | False |


    * **hash_bitmap**: This file contains sha1sum of each sample following with type of the evasion and evasion techniques used in the form of a bitmap. Each bit constructs a different meaning in our convention which is as the following:

        | Bits | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | a | b | c | d | e | 
        |:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
        |Meaning| PROCESS_DETECTION | DEBUGGER_PRESENT | CPUID | RDTSC | CPU_COUNT | INVALID_INST | TICK_COUNT | HCI | BIOS | DRIVER_CHECK | SCSI_CHECK | HDD_SIZE | MEM_SIZE | MAC_ADDR | ACPI |
            
    * **mitigation_rate**: Shows the percentage of artifact distribtion in our sample set. For the 1535 samples we have here is the distribution:  

        | Artifact | Count # | 
        |:--------:|:-------:|
        |PROCESS_DETECTION| 648|
        | DEBUGGER_PRESENT |  503 |
        | RDTSC | 322 |
        | CPU_COUNT | 2 | 
        | INVALID_INST | 9 |
        | TICK_COUNT | 212 |
        | HCI | 174 | 
        | BIOS | 954 |
        | DRIVER_CHECK | 110 | 
        |  SCSI_CHECK | 592 |
        | HDD_SIZE | 234 |
        | MEM_SIZE | 188 | 
        | ACPI DSDT | 72 |
6. [plots](./plots/plots.ipynb): Generate plots and diagrams for the paper. 

---
## References
<a name="typeperf">[1] </a> https://github.com/craignicholson/typeperf#server-level-monitoring  
<a name="proctime">[2] </a> https://blog.heroix.com/blog/windows-cpu-metric-guide