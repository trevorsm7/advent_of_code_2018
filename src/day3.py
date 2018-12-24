import re
import unittest

def main():
    history = []
    box_ids = []
    overlaps = []
    total_area = 0
    with open('input/day3.txt') as f:
        for line in f:
            box, rect = parse_line(line)
            remainder = [rect]
            for other in history:
                overlap = get_overlap(rect, other)
                if overlap:
                    remainder = remove_overlaps(overlap, overlaps)
                    total_area += get_area(remainder)
                    overlaps.extend(remainder)
            history.append(rect)
            box_ids.append(box)
    #print_rects(history)
    #print_rects(overlaps)
    print('Part 1:', total_area)

    valid_claim = None
    for box, rect in zip(box_ids, history):
        if not contains_overlap(rect, overlaps):
            valid_claim = box
            break
    print('Part 2:', valid_claim)

# Fuck Python for not having labelled break/continue
def contains_overlap(rect, overlaps):
    for overlap in overlaps:
        if get_overlap(rect, overlap):
            return True
    return False

def parse_line(line):
    # Read numbers (as str) only
    box, x, y, w, h = re.findall(r"[\d']+", line)
    x1 = int(x)
    x2 = x1 + int(w)
    y1 = int(y)
    y2 = y1 + int(h)
    return box, (x1, y1, x2, y2)

def get_overlap(rect, other):
    x1 = max(rect[0], other[0])
    x2 = min(rect[2], other[2])
    y1 = max(rect[1], other[1])
    y2 = min(rect[3], other[3])
    if x2 <= x1 or y2 <= y1:
        return None
    return (x1, y1, x2, y2)

def remove_overlaps(rect, overlaps):
    parts = [rect]
    for other in overlaps:
        remainder = []
        for part in parts:
            overlap = get_overlap(part, other)
            if overlap:
                remainder.extend(remove_overlap(part, overlap))
            else:
                remainder.append(part)
        parts = remainder
    return parts

# NOTE this is NOT valid if the overlap isn't fully contained in rect
def remove_overlap(rect, overlap):
    remainder = []
    if overlap[0] > rect[0]:
        remainder.append((rect[0], rect[1], overlap[0], rect[3]))
    if overlap[1] > rect[1]:
        remainder.append((overlap[0], rect[1], overlap[2], overlap[1]))
    if overlap[2] < rect[2]:
        remainder.append((overlap[2], rect[1], rect[2], rect[3]))
    if overlap[3] < rect[3]:
        remainder.append((overlap[0], overlap[3], overlap[2], rect[3]))
    return remainder

def get_area(rect):
    # Loop over lists
    if isinstance(rect, list):
        sum = 0
        for e in rect:
            sum += get_area(e)
        return sum

    # Compute area of tuple
    x1, y1, x2, y2 = rect
    return (x2 - x1) * (y2 - y1)

def rect_contains(rect, x, y):
    return x >= rect[0] and x < rect[2] and y >= rect[1] and y < rect[3]

def any_rect_contains(rects, x, y):
    return any([rect_contains(rect, x, y) for rect in rects])

def print_rects(rects):
    for y in range(0, 9):
        print(''.join(['#' if any_rect_contains(rects, x, y) else '.' for x in range(0, 9)]))

class TestDay3(unittest.TestCase):
    def test_get_overlap(self):
        rect1 = (0, 0, 4, 4)
        rect2 = (0, 2, 2, 4)
        rect3 = (2, 0, 4, 2)
        rect4 = (0, 0, 4, 2)
        rect5 = (2, 0, 6, 2)
        self.assertEqual(get_overlap(rect1, rect2), rect2)
        self.assertEqual(get_overlap(rect1, rect3), rect3)
        self.assertEqual(get_overlap(rect2, rect3), None)
        self.assertEqual(get_overlap(rect4, rect5), rect3)
    
    def test_get_area(self):
        rect1 = (0, 0, 4, 4)
        rect2 = (0, 2, 2, 4)
        self.assertEqual(get_area(rect1), 16)
        self.assertEqual(get_area(rect2), 4)

if __name__ == '__main__':
    main()