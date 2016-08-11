import os, sys
import math

def print_line(name, values):
    line = name + '\t'
    for v in values:
        line += str(v) + '\t'
    print(line)

def get_percentile(sorted_values, percentile):
    return sorted_values[int(math.ceil(len(sorted_values) * percentile/100.0))-1]

top_dir = os.path.join('primary', 'net')
try:
    machine_id = os.listdir(top_dir)[0]
except OSError, KeyError:
    sys.exit("Could not find expected directory structure.")

machine_dir = os.path.join(top_dir, machine_id)
header = None
events = {}
for fn in os.listdir(machine_dir):
    linenum = 0
    with open(os.path.join(machine_dir, fn)) as input:
        for line in input:
            linenum += 1
            if linenum == 1:
                # header line, save it if not yet saved
                if not header:
                    header = line
                continue
            elif linenum == 2:
                # this line is the machine ID again
                continue
            
            timestamp = int(line.split()[0])
            # save all remaining columns in the dictionary
            events[timestamp] = line.split()[1:]
            
print(header)

timestamps = sorted(events.keys())
print("period " + str(timestamps[0]) + ' - '+ str(timestamps[-1]))

num_cols = len(header.split()) - 1
count = [0] * num_cols
min = [float('inf')] * num_cols
max = [None] * num_cols
sum = [0] * num_cols

all_values = [[None for i in range(len(timestamps))] for j in range(num_cols)]
for vals in events.values():
    index = 0
    for val in vals:
        val = float(val)
        all_values[index][count[index]] = val
        count[index] += 1
        if min[index] > val:
            min[index] = val
        if max[index] < val:
            max[index] = val
        sum[index] += val
        index += 1
        
sorted_values = [sorted(all_values[i]) for i in range(num_cols)]
std_dev = [0] * num_cols
for i in range(num_cols):
    for j in range(len(timestamps)):
        std_dev[i] += (all_values[i][j] - sum[i]/count[i])**2
    std_dev[i] = math.sqrt(std_dev[i]/count[i])
    
print_line('count', count)
print_line('min', min)
print_line('max', max)
print_line('mean', [sum[i]/count[i] for i in range(num_cols)])
print_line('std-dev', std_dev)
print_line('50-percentile', [get_percentile(sorted_values[i], 50.0) for i in range(num_cols)])
print_line('75-percentile', [get_percentile(sorted_values[i], 75.0) for i in range(num_cols)])
print_line('95-percentile', [get_percentile(sorted_values[i], 95.0) for i in range(num_cols)])
print_line('99-percentile', [get_percentile(sorted_values[i], 99.0) for i in range(num_cols)])
print_line('99.9-percentile', [get_percentile(sorted_values[i], 99.9) for i in range(num_cols)])