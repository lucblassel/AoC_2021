import re
import ast
import math
import itertools

pair_matcher = re.compile(r"(\[\d+,\d+\])")
last_number = re.compile(r"(\d+)(?!.*\d+)")
first_number = re.compile(r"(?<!\d)(\d+)")
split_matcher = re.compile(r"(?<!\d{2})(\d{2})(.*)")


def get_pair_depth(match):
    s = match.string[: match.start()]
    return s.count("[") - s.count("]")


def get_pair_values(pair_string):
    l, r = ast.literal_eval(pair_string)
    return l, r


def add_number(matchobj, number):
    num_s = matchobj.groups()[0]
    return f"{int(num_s) + number}"


def split(match):
    string = match.string
    left = string[: match.start()]
    num_s, right = match.groups()
    num = int(num_s)
    pair = [math.floor(num / 2), math.ceil(num / 2)]
    return f"{left}{pair}{right}"


def explode(match):
    string = match.string
    s, e = match.span()
    l, r = get_pair_values(string[s:e])
    left_n, right_n = string[:s], string[e:]
    left = re.sub(last_number, lambda m: add_number(m, l), left_n)
    right = re.sub(first_number, lambda m: add_number(m, r), right_n, 1)
    return f"{left}0{right}"


def reduce_number(number):
    modified = True
    reduced = number
    while modified:
        reduced = "".join(reduced.split())  # clearing all whitespace
        has_exploded = False
        modified = False

        for pair_match in pair_matcher.finditer(reduced):
            if get_pair_depth(pair_match) >= 4:
                has_exploded, modified = True, True
                reduced = explode(pair_match)
                break

        if has_exploded:
            continue

        for split_match in split_matcher.finditer(reduced):
            modified = True
            reduced = split(split_match)
            break

    return reduced


def add(number1, number2):
    return f"[{number1},{number2}]"


def do_homework(numbers):
    result = numbers[0]

    for number in numbers[1:]:
        result = reduce_number(add(result, number))

    return result


def magnitude(number):
    if isinstance(number, int):
        return number
    return 3 * magnitude(number[0]) + 2 * magnitude(number[1])


def main():

    # test case
    assignment = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]""".split(
        "\n"
    )

    with open("./data.txt", "r") as file:
        assignment = file.readlines()

    mag_max = 0
    for n1, n2 in itertools.product(assignment, repeat=2):
        if n1 == n2:
            continue
        res = reduce_number(add(n1, n2))
        mag_max = max(mag_max, magnitude(ast.literal_eval(res)))

    print(mag_max)


if __name__ == "__main__":
    main()
