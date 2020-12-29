### knock-knock  
A parser for integrity checking the VM config success rate in fooling the
malware sample to convince it to run under VM environment. It's obvious we're
only controlling hypervisor or VM related HW configuration and we don't employ
any specific anti-anti-vm trick inside the VM itself. So, it's obvious in many
cases we might loose accuracy which I documented some of those cases here just
as an example: 

- [EnumWindows
  trick](https://www.blueliv.com/cyber-security-and-cyber-threat-intelligence-blog-blueliv/research/old-tricks-still-work/) 
  It’s one of the few functions during which the kernel makes calls to user
  mode. Cuckoo loses traceability of the analysis during the callback execution
  partly due to this behavior. During this unmonitored time, the packer can run
  anti-VM, anti-sandbox, or any kind of checks “hidden” from the sandbox. 

  ```json
    {
        "category": "misc", 
        "status": 1, 
        "stacktrace": [], 
        "api": "EnumWindows", 
        "return_value": 1, 
        "arguments": {}, 
        "time": 1571598086.271203, 
        "tid": 3532, 
        "flags": {}
    }, 
    ...
    a bunch of Nt* calls.. 
  ``` 

- Delay Execution 
    ```json 
    {
        "category": "synchronisation", 
        "status": 1, 
        "stacktrace": [], 
        "api": "NtDelayExecution", 
        "return_value": 0, 
        "arguments": {
            "skipped": 0, 
            "milliseconds": 15
        }, 
        "time": 1571605764.578625, 
        "tid": 2228, 
        "flags": {}
    }, 
    {
        "category": "synchronisation", 
        "status": 1, 
        "stacktrace": [], 
        "api": "NtDelayExecution", 
        "return_value": 0, 
        "arguments": {
            "skipped": 0, 
            "milliseconds": 15
        }, 
        "time": 1571605764.594625, 
        "tid": 2228, 
        "flags": {}
    }, 
    ``` 

#### Virtualbox analysis: 

- **process detection**: 
  I ran the analysis on two different environments with different configurations.
  1. `hopper1`: win7x86\_conf1 configured for QEMU HDD/DVD artifacts removed +
     BIOS is almost secure (`dmidecode`) 
  2. `hopper8`: win7x86\_conf1\_vboxGA running a vulnerable version of
     Virtualbox including Guest Additions installed, but BIOS data has been
     modified 


