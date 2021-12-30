import math
import re

test_input = """\
on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682\
"""


class Cuboid:
    regex = re.compile(
        r"(.*) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)"
    )

    def __init__(self, state, x_s, x_e, y_s, y_e, z_s, z_e):
        self.state = state
        self.x_s, self.x_e = x_s, x_e
        self.y_s, self.y_e = y_s, y_e
        self.z_s, self.z_e = z_s, z_e

    @property
    def volume(self):
        return (self.x_e - self.x_s) * (self.y_e - self.y_s) * (self.z_e - self.z_s)

    @property
    def valid(self):
        return self.x_s < self.x_e and self.y_s < self.y_e and self.z_s < self.z_e

    @classmethod
    def from_string(cls, string, min_coord=-math.inf, max_coord=math.inf):
        state, x_s_s, x_e_s, y_s_s, y_e_s, z_s_s, z_e_s = Cuboid.regex.match(
            string
        ).groups()
        x_s, x_e, y_s, y_e, z_s, z_e = (
            int(x_s_s),
            int(x_e_s),
            int(y_s_s),
            int(y_e_s),
            int(z_s_s),
            int(z_e_s),
        )
        return Cuboid(
            state,
            max(x_s, min_coord),
            min(x_e, max_coord) + 1,
            max(y_s, min_coord),
            min(y_e, max_coord) + 1,
            max(z_s, min_coord),
            min(z_e, max_coord) + 1,
        )

    def intersects(self, other):
        return (
            self.x_s < other.x_e
            and self.x_e > other.x_s
            and self.y_s < other.y_e
            and self.y_e > other.y_s
            and self.z_s < other.z_e
            and self.z_e > other.z_s
        )

    def contains(self, other):
        return (
            self.x_s <= other.x_s
            and self.x_e >= other.x_e
            and self.y_s <= other.y_s
            and self.y_e >= other.y_e
            and self.z_s <= other.z_s
            and self.z_e >= other.z_e
        )

    def substract(self, other):

        if not self.intersects(other):
            return [self]
        elif other.contains(self):
            return []

        xs = sorted([self.x_s, self.x_e, other.x_s, other.x_e])
        ys = sorted([self.y_s, self.y_e, other.y_s, other.y_e])
        zs = sorted([self.z_s, self.z_e, other.z_s, other.z_e])

        splits = []
        for x_s, x_e in zip(xs, xs[1:]):
            for y_s, y_e in zip(ys, ys[1:]):
                for z_s, z_e in zip(zs, zs[1:]):
                    cuboid = Cuboid("?", x_s, x_e, y_s, y_e, z_s, z_e)
                    if self.contains(cuboid) and not cuboid.intersects(other):
                        splits.append(cuboid)

        return splits


def reboot(string):
    steps = [
        cuboid
        for line in string.split("\n")
        if (
            cuboid := Cuboid.from_string(line.strip(), min_coord=-50, max_coord=50)
        ).valid
    ]

    cuboids = []
    for cuboid_step in steps:
        cuboids = [
            split for cuboid in cuboids for split in cuboid.substract(cuboid_step)
        ]
        if cuboid_step.state == "on":
            cuboids.append(cuboid_step)

    return sum(cube.volume for cube in cuboids)


def main():
    print(reboot(test_input))
    with open("./data.txt", "r") as file:
        data = file.read().strip()
    print(reboot(data))


if __name__ == "__main__":
    main()
