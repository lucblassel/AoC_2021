input_ = "./data.txt"

OPENINGS = {"{", "[", "(", "<"}

MATCHES = {"}": "{", "]": "[", ")": "(", ">": "<"}

POINTS = {"}": 1197, "]": 57, ")": 3, ">": 25137}


def check_line(line):
    stack = []
    for char in line:
        if char in OPENINGS:
            stack.append(char)
        else:
            if MATCHES.get(char) != stack[-1]:
                return char
            stack.pop()
    return None


def main():
    points = 0
    with open(input_, "r") as file:
        for line in file:
            invalid = check_line(line.strip())
            points += POINTS.get(invalid, 0)
    print(points)


if __name__ == "__main__":
    main()
