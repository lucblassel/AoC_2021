import functools

instructions = []
digits = []

def print_digits():
    print(
        "".join(f"{d}" for d in digits)
    )

def parse_blocks(filename: str):
    blocks = []
    with open(filename, "r") as file:
        for i, line in enumerate(file):
            if i % 18 == 0:
                blocks.append([])
            blocks[-1].append(line.strip())
    return blocks

def execute_block(z: int, w: int, block: list[str]) -> int:
    registers = dict(x=0, y=0, z=z, w=w)
    for i, line in enumerate(block):
        if i == 0:
            continue

        op, reg, arg = line.split()
        if arg in registers:
            val = registers[arg]
        else:
            val = int(arg)

        if op == "mul":
            registers[reg] *= val
        elif op == "div":
            registers[reg] = int(registers[reg] / val)
        elif op == "mod":
            registers[reg] = registers[reg] % val
        elif op == "eql":
            registers[reg] = int(registers[reg] == val)
        elif op == "add":
            registers[reg] += val

    return registers["z"]

@functools.cache
def search(level: int, z: int) -> bool:
    global digits

    if z >= 1e6: return False
    
    if level == len(instructions):
        if z == 0:
            print_digits()
            return True
        return False

    for digit in range(1, 10):
        digits.append(digit)
        new_z = execute_block(z, digit, instructions[level])
        if search(level + 1, new_z):
            return True
        digits = digits[:-1]
    return False


def main():
    global instructions
    instructions = parse_blocks("./data.txt")
    search(0, 0)


if __name__ == "__main__":
    main()