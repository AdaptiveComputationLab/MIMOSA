import itertools
import collections

config_costs = {#							  total time 	resources 
	'hopper1_kvm_patched_conf1': 			[536.4 + 180.8,	35000],
	'hopper1_kvm_patched_conf2': 			[536.4 + 180.8,	25000],
	'hopper2_vmware_conf3': 				[477 + 60.7, 	10000],
	'hopper4_vmware_conf2': 				[477 + 644.6, 	4000],
	'hopper5_vmware_conf2_vmtools':			[477 + 73.5,	39000],
	'hopper7_qemu_legacy_conf1': 			[538.1 + 327.4, 52000],
	'hopper7_qemu_legacy_conf2': 			[538.1 + 327.4, 42000],
	'hopper8_vbox_conf1_guestadditions': 	[422.7 + 142, 	13666],
	'hopper8_vbox_conf2_guestadditions':	[422.7 + 142,	12345],
	'hopper3_vbox_conf1': 					[422.7 + 73.4,	54321],
	'hopper3_vbox_conf2': 					[304.7 + 73.4,	22222],
	'hopper6_kvm_legacy_conf1': 			[543.3 + 327.4,	12321],
	'hopper6_kvm_legacy_conf2': 			[543.3 + 327.4, 99999]
}

config_names = {}

# configs is a dict
# 	where keys are the names of configs
# 	and values are a list of whether the sample passed or not
configs = {}
with open('fixed_evasion.csv') as f:
	lines = f.readlines()
	names = lines[0].split(',')[1:]
	for idx, name in enumerate(names):
		configs[idx] = []
		config_names[idx] = name.strip()

	for line in lines[1:]:
		s = line.split(',')[1:]
		for idx, elem in enumerate(s):
			if elem == "FALSE":
				configs[idx].append(0)
			elif elem == "TRUE":
				configs[idx].append(1)

# if number of samples changes, it has to change here
num_configs = len(config_costs)
num_samples = 1535

results = []
for i in range(1, num_configs+1):
	print('Working subsets of size', i)
	for subset in itertools.combinations(range(num_configs), i):
		total_time = 0.0
		resources = 0.0
		for identifier in subset:
			name = config_names[identifier]
			# TODO: this will have to change
			total_time += config_costs[name][0]
			resources += config_costs[name][1]
		

		num_covered = 0
		for sample_id in range(num_samples):
			for config_id in subset:
				covered = configs[config_id][sample_id]
				if covered == 1:
					num_covered += 1
					break
		# TODO: add more dimensions here
		results.append((subset, 
			('high',num_covered), 
			('low',total_time),
			('low',resources)
		))



def dominates(row, candidateRow):
	for x in range(1, len(row)):
		if row[x][0] == 'high' and row[x][1] < candidateRow[x][1]:
			return False
		if row[x][0] == 'low' and row[x][1] > candidateRow[x][1]:
			return False
	return True

def pareto_frontier(inputPoints):
    paretoPoints = set()
    candidateRowNr = 0
    dominatedPoints = set()
    while True:
        candidateRow = inputPoints[candidateRowNr]
        inputPoints.remove(candidateRow)
        rowNr = 0
        nonDominated = True
        while len(inputPoints) != 0 and rowNr < len(inputPoints):
            row = inputPoints[rowNr]
            if dominates(candidateRow, row):
                inputPoints.remove(row)
                dominatedPoints.add(tuple(row))
            elif dominates(row, candidateRow):
                nonDominated = False
                dominatedPoints.add(tuple(candidateRow))
                rowNr += 1
            else:
                rowNr += 1

        if nonDominated:
            paretoPoints.add(tuple(candidateRow))

        if len(inputPoints) == 0:
            break
    return paretoPoints

pareto = pareto_frontier(results)
for pt in pareto:
	subset, *costs = pt
	print('{', end='')
	print(', '.join(config_names[i] for i in subset),end='')
	print('} -> ', end='')
	print(', '.join(str(i[1]) for i in costs))