from pprint import pprint


def get_packet_header(bits):
    version, bits = bits[:3], bits[3:]
    id_, bits = bits[:3], bits[3:]
    return version, id_, bits


def hex_to_bin(hex_):
    numBits = len(hex_) * 4
    return bin(int(hex_, 16))[2:].zfill(numBits)


def parse_literal(bits):
    num = ""
    while True:
        chunk, bits = bits[:5], bits[5:]
        num += chunk[1:]
        if chunk[0] == "0":
            return num, bits
    return num, bits


def parse_operator(bits, depth):
    sub = []
    # Bit length subpackets
    if bits[0] == "0":
        length, bits = int(bits[1:16], 2), bits[16:]
        chunk, bits = bits[:length], bits[length:]
        while len(chunk) > 0:
            packet, chunk = parse_packet(chunk, depth + 1)
            sub.append(packet)

    # Number of subpackets
    else:
        num, bits = int(bits[1:12], 2), bits[12:]
        for i in range(num):
            packet, bits = parse_packet(bits, depth + 1)
            sub.append(packet)

    return sub, bits


def parse_packet(bits, depth=1):
    if len(bits) < 11:
        return dict(), ""
    packet = dict()
    version, id_, bits = get_packet_header(bits)
    V, T = int(version, 2), int(id_, 2)
    packet["version"] = V
    packet["type"] = T
    if id_ == "100":
        num, bits = parse_literal(bits)
        packet["value"] = int(num, 2)
    else:
        sub, bits = parse_operator(bits, depth)
        packet["value"] = sub

    return packet, bits


def add_version(packet):
    s = 0

    if packet["type"] == "litteral":
        return packet["version"]

    s += packet["version"]

    for subpack in packet["value"]:
        s += add_version(subpack)
    return s


def eval_packet(packet):
    tp = packet["type"]

    if tp == 0:  # sum
        return sum(eval_packet(subpack) for subpack in packet["value"])

    if tp == 1:  # product
        p = 1
        for subpack in packet["value"]:
            p *= eval_packet(subpack)
        return p

    if tp == 2:  # minimum
        return min(eval_packet(subpack) for subpack in packet["value"])

    if tp == 3:  # maximum
        return max(eval_packet(subpack) for subpack in packet["value"])

    if tp == 4:  # literal
        return packet["value"]

    # Comparison operators
    v0, v1 = eval_packet(packet["value"][0]), eval_packet(packet["value"][1])

    if tp == 5:  # greater than
        return int(v0 > v1)

    if tp == 6:  # less than
        return int(v0 < v1)

    if tp == 7:  # equal to
        return int(v0 == v1)


def testing():

    packets = [
        "C200B40A82",
        "04005AC33890",
        "880086C3E88112",
        "CE00C43D881120",
        "D8005AC2A8F0",
        "F600BC2D8F",
        "9C005AC2F8F0",
        "9C0141080250320F1802104A08",
    ]

    for hex_ in packets:
        bits = hex_to_bin(hex_)
        print(hex_)
        packet, bits = parse_packet(bits)
        # pprint(packet)
        res = eval_packet(packet)
        print(res)
        print()


def main():
    with open("./data.txt", "r") as file:
        hex_ = file.readlines()[0].strip()
        bits = hex_to_bin(hex_)
        packet, _ = parse_packet(bits)
        print(eval_packet(packet))


if __name__ == "__main__":
    # testing()
    main()
