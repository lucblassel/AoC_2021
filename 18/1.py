import re
import ast
import math


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
    # print("\t\t\t", f"Split: {num} -> {pair}")
    return f"{left}{pair}{right}"


def explode(match):
    string = match.string
    s, e = match.span()
    l, r = get_pair_values(string[s:e])
    left_n, right_n = string[:s], string[e:]
    left = re.sub(last_number, lambda m: add_number(m, l), left_n)
    right = re.sub(first_number, lambda m: add_number(m, r), right_n, 1)
    # print("\t\t\t", f"Exploding: [{l},{r}]")
    return f"{left}0{right}"


def reduce_number(number):
    modified = True
    reduced = number
    # print("\t", f"to reduce: {number}")
    while modified:
        reduced = "".join(reduced.split())  # clearing all whitespace
        # print("\t\t", f"parsing: {reduced}")
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


def do_homework(numbers, after=-1):
    result = numbers[0]

    for i, number in enumerate(numbers[1:]):
        temp = result
        result = reduce_number(add(result, number))
        # print()
        # print("\t", f"  {temp}")
        # print("\t", f"+ {number}")
        # print("\t", f"= {result}")
        # print()

        if after >= 0 and i >= after:
            break

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

    number = do_homework(assignment)
    mag = magnitude(ast.literal_eval(number))
    print(number, mag)


if __name__ == "__main__":
    main()
