# Covering arrays algorithm 
This script finds the "Pareto frontier" (i.e., choices of configs that don't dominate each other), attached. At the top I have a dict of configs, with the coverage on each, and the time for each (which right now is installation + machine deploy + cuckoo deploy, just for testing). 

You need the bitmap\_evasion.csv file (also attached) for it to work. To
generate this file please take a look at the [detect.py](../util/detect.py) code. 

For example, with the input costs as are in the file now, it gives this output: 

```{(('vbox_conf1',), 1195, 599.0), (('vbox_conf1', 'qemu_qemu_legacy_conf1'), 1537, 2306.9), (('vbox_conf2', 'qemu_qemu_legacy_conf1'), 1349, 2187.0), (('vbox_conf2',), 307, 479.1), (('qemu_qemu_legacy_conf1',), 1246, 1707.9), (('vmware_conf3', 'vbox_conf1'), 1215, 1236.6)}```

where the first element of each tuple is the choice(s) of configs, then the # of passed samples, and then the total time.

Whereas if I use the input costs being only installation + machine deploy, it gives this output: 

```{(('vbox_conf1',), 1195, 496.1), (('vbox_conf2', 'qemu_qemu_legacy_conf1'), 1349, 1248.8), (('vbox_conf2',), 307, 378.1), (('qemu_qemu_legacy_conf1',), 1246, 870.6999999999999), (('vbox_conf1', 'qemu_qemu_legacy_conf1'), 1537, 1366.8)}```

We can add additional dimensions to the problem, such as the other types of costs that are independent of the time taken (I think you mentioned harddrive resources, etc.).

## Features added 
- [x] add additional dimensions: I added an extra dimension for resources (obviously fake values). If you need to add an extra dimension beyond what is here, you need to do the following:  

    * Add an element to each of the lists in the config_costs dict at the top; 
    * In the for loop at line 50, you need to add a variable for that corresponding dimension; and 
    * In the append at line 65, you need to add a 2-tuple for that variable, depending on what you want. If a "high" value is better, then put that string; if a "low" value is better, then put that instead (see the example I have there). I have a "high" value in the case that you want throughput as a parameter or something. 


- [x] If you want to add a config, you will have to:  
    * Add the corresponding column in the attached csv file; and  
    * Add the corresponding config in the config_costs dict at the top. 
    
    It then pretty prints the pareto frontier. I doubt you would need to modify anything else other than the costs. With the extra dimension I added, it gives an already interesting frontier. 


