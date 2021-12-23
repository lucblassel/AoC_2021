from collections import defaultdict

# Test case
ALG = "..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#"
IMG = """#..#.
#....
##..#
..#..
..###"""

C = {"#": 1, ".": 0}


def parse_image(image_s):
    pixels = defaultdict(int)
    for y, line in enumerate(image_s.split("\n")):
        for x, char in enumerate(line):
            pixels[(x, y)] = int(char == "#")
    return pixels


def get_lookup_table(img, round_num, alg):
    if alg[0] == "." or round_num % 2 == 0:
        lookup = defaultdict(lambda: C[alg[0]])
    else:
        lookup = defaultdict(lambda: C[alg[-1]])
    for k, v in img.items():
        lookup[k] = v
    return lookup


def process_pixel(lookup, x, y, alg):
    n = ""
    for y_inc in (-1, 0, 1):
        for x_inc in (-1, 0, 1):
            coord = (x + x_inc, y + y_inc)
            n += f"{lookup[coord]}"
    num = int(n, 2)
    return 1 if alg[num] == "#" else 0


def expand(image):
    keys = image.keys()
    xs, ys = [x[0] for x in keys], [x[1] for x in keys]
    bounds_x = (min(xs) - 1, max(xs) + 2)
    bounds_y = (min(ys) - 1, max(ys) + 2)
    for x in range(*bounds_x):
        for y in range(*bounds_y):
            _ = image[(x, y)]


def iterate_bounds(image):
    keys = image.keys()
    xs, ys = [x[0] for x in keys], [x[1] for x in keys]
    bounds_x = (min(xs) - 1, max(xs) + 2)
    bounds_y = (min(ys) - 1, max(ys) + 2)
    for x in range(*bounds_x):
        for y in range(*bounds_y):
            yield x, y


def process_image(image, lookup, round_num, alg):

    new_img = get_lookup_table(dict(), round_num, alg)

    for coords in iterate_bounds(image):
        new_img[coords] = process_pixel(lookup, *coords, alg)

    return new_img


def to_str(image):
    keys = image.keys()
    xs, ys = [x[0] for x in keys], [x[1] for x in keys]
    bounds_x = (min(xs), max(xs) + 1)
    bounds_y = (min(ys), max(ys) + 1)
    lines = []
    for y in range(*bounds_y):
        lines.append("")
        for x in range(*bounds_x):
            p = "#" if image[(x, y)] == 1 else "."
            lines[-1] += p
    return "\n".join(lines)


def parse_data(filename):
    with open(filename, "r") as file:
        alg = file.__next__().strip()
        img = ""
        for line in file:
            if line.strip() != "":
                img += line
        return alg, img


def main():
    alg, img_str = parse_data("./data.txt")
    img = parse_image(img_str)

    # alg = ALG
    # img = parse_image(IMG)

    print(to_str(img))
    for i in range(50):
        print(f"\nround_num {i+1}")
        lookup = get_lookup_table(img, i + 1, alg)
        img = process_image(img, lookup, i + 1, alg)

    print(to_str(img))
    print(sum(img.values()))


if __name__ == "__main__":
    main()
