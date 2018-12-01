import sys

cycle = 0
history = []
with open('input/day1.txt') as f:
    for line in f:
        cycle += int(line)
        history.append(cycle)
print("Part 1:", cycle)

min_steps = sys.maxsize
for f1 in history:
    for f2 in history:
        d = f2 - f1
        if d >= cycle and d % cycle == 0:
            steps = d // cycle
            if steps < min_steps:
                first_repeat = f2
                min_steps = steps
print("Part 2:", first_repeat)
