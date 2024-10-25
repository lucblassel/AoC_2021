from itertools import combinations
from functools import reduce
import numpy as np


def rotations():
    R1 = np.array([[0, 0, -1], [0, 1, 0], [1, 0, 0]])
    R2 = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]])
    R3 = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
    perms = []
    gotten = set()
    mpow = np.linalg.matrix_power
    for x in range(4):
        for y in range(4):
            for z in range(4):
                p = mpow(R1, x) @ mpow(R2, y) @ mpow(R3, z)
                if str(p) in gotten:
                    continue
                else:
                    perms.append(p)
                    gotten.add(str(p))
    return perms


class Scanner:
    def __init__(self, beacons):
        self.beacons = beacons
        self.rotation = None
        self.position = None
        self.compute_distances()

    def compute_distances(self):
        self.distances = dict()
        for p1, p2 in combinations(self.beacons, 2):
            d = ((p1 - p2) ** 2).sum()
            self.distances[int(d)] = np.array([p1, p2])

    def beacon_set(self):
        if self.position is None or self.rotation is None:
            b = self.beacons
        else:
            b = self.beacons @ self.rotation + self.position

        return set(tuple(beacon) for beacon in b)


def get_overlaps(scanners: list[Scanner]):
    overlaps = dict()
    for (i, s1), (j, s2) in combinations(enumerate(scanners), 2):
        if len(common := s1.distances.keys() & s2.distances.keys()) >= 66:
            overlaps[(i, j)] = common
    return overlaps


PERMS = rotations()


def get_relative_position(pair1, pair2):
    # Points are in the same order between pairs
    l1 = pair1[0] - pair2[0]
    l2 = pair1[1] - pair2[1]
    if (l1 == l2).all():
        return l1

    # Points are in the opposite order between pairs
    l1 = pair1[0] - pair2[1]
    l2 = pair1[1] - pair2[0]
    if (l1 == l2).all():
        return l1

    # the rotation between overlapping pairs is not right
    return None


def locate_scanners(scanners):
    overlaps = get_overlaps(scanners)
    # result = scanners[0].beacon_set()

    # Process the first scanner
    scanners[0].position = np.zeros(3, dtype=np.int32)
    scanners[0].rotation = np.eye(3, 3, dtype=np.int32)
    processed = 1

    while processed < len(scanners):
        for (s1, s2), dists in overlaps.items():
            # Check that one scanner's position is resolved and the other's is not
            if (scanners[s1].position is None) == (scanners[s2].position is None):
                continue

            dists = list(dists)
            # Set the resolved scanner as reference
            ref, other = (s1, s2) if (scanners[s1].position is not None) else (s2, s1)

            # Get matching, overlaping pairwise distance
            ref_pair = scanners[ref].distances[dists[0]]
            other_pair = scanners[other].distances[dists[0]]

            ref_rotated = ref_pair @ scanners[ref].rotation
            for r in PERMS:
                other_rotated = other_pair @ r
                pos = get_relative_position(ref_rotated, other_rotated)

                # Not the right rotation
                if pos is None:
                    continue

                # We found the right rotation
                pos += scanners[ref].position  # Add offset to ref scanner
                scanners[other].rotation = r
                scanners[other].position = pos

                # result |= scanners[otr].beacon_set()

                processed += 1


def parse_data(path):
    scanners = []
    with open(path, "r") as file:
        for line in file:
            if line.startswith("---"):  # Add new scanner
                scanners.append([])
            elif line.strip() == "":  # Separator line
                continue
            else:
                scanners[-1].append([int(x) for x in line.strip().split(",")])

    return [Scanner(np.array(x, dtype=np.int32)) for x in scanners]


def manhattan(scanner_pair):
    return np.abs(scanner_pair[0].position - scanner_pair[1].position).sum()


if __name__ == "__main__":
    scanners = parse_data("./data.txt")

    # Deduce locations of all scanners
    locate_scanners(scanners)

    unique_beacons = set.union(*(scanner.beacon_set() for scanner in scanners))
    max_dist = reduce(max, map(manhattan, combinations(scanners, 2)))

    print(f"1: {len(unique_beacons)}")
    print(f"2: {max_dist}")
