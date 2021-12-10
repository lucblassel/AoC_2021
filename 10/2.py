input_ = "./data.txt"

OPENINGS = {"{", "[", "(", "<"}

MATCHES = {"}": "{", "]": "[", ")": "(", ">": "<"}
REV_MATCHES = {v: k for k, v in MATCHES.items()}
POINTS = {"}": 3, "]": 2, ")": 1, ">": 4}


def check_line(line):
    stack = []
    for char in line:
        if char in OPENINGS:
            stack.append(char)
        else:
            if MATCHES.get(char) != stack[-1]:
                return None
            stack.pop()
    return stack


def get_points(stack):
    score = 0
    for char in stack[::-1]:
        score *= 5
        score += POINTS.get(REV_MATCHES.get(char))
    return score


def main():
    points = []
    with open(input_, "r") as file:
        for line in file:
            stack = check_line(line.strip())
            if stack is not None:
                points.append(get_points(stack))
    points.sort()
    print(points, points[len(points) // 2])


if __name__ == "__main__":
    main()
