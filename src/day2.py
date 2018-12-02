def main():
    # Iterate over each line in the file
    checksum = [0, 0]
    common = []
    with open('input/day2.txt') as f:
        history = []
        for line in f:

            # Update part1 and part2
            line = line.strip()
            part1(line, checksum)
            part2(line, history, common)
            history.append(line)

    print('Part 1:', checksum[0] * checksum[1])
    print('Part 2:', common)

def part1(line, checksum):
    # Count how often each character appears
    counts = {}
    for c in line:
        if c in counts:
            counts[c] += 1
        else:
            counts[c] = 1

    # Check if any character appears exactly twice or thrice
    twice, thrice = 0, 0
    for count in counts.values():

        # Twice and thrice only count once each
        if count == 2:
            twice = 1
        elif count == 3:
            thrice = 1

    # Update the checksum
    checksum[0] += twice
    checksum[1] += thrice

def part2(line, history, common):
    # For each prior line
    for prev in history:

        # Count how many characters differ
        count = 0
        for i, (a, b) in enumerate(zip(prev, line)):
            if a != b:
                split = i
                count += 1

        # Add lines that differ by only 1
        if count == 1:
            common.append(line[:split] + line[split+1:])

if __name__ == '__main__':
    main()