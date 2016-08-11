import os, sys

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
            events[timestamp] = line
            
    
# sort based on timestamp
print(header)
for ts, line in sorted(events.items()):
    print(line)