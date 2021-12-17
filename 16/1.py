from pprint import pprint

input_ = "./test.txt"


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
        # print(chunk, end=" ")
        num += chunk[1:]
        if chunk[0] == "0":
            # print(f"({bits})")
            return num, bits
    return num, bits


def parse_operator(bits, depth):
    sub = []
    # Bit length subpackets
    if bits[0] == "0":
        length, bits = int(bits[1:16], 2), bits[16:]
        chunk, bits = bits[:length], bits[length:]
        # print("0", length, chunk, f"({bits})")
        # print(depth * "  ", f"subpackets total len->{length}")
        while len(chunk) > 0:
            packet, chunk = parse_packet(chunk, depth + 1)
            sub.append(packet)

    # Number of subpackets
    else:
        num, bits = int(bits[1:12], 2), bits[12:]
        # print("1", num, f"({bits})")
        # print(depth * "  ", f"{num} subpackets")
        for i in range(num):
            # print()
            # print(depth * "  ", f"parsing subpacket {i+1}")
            packet, bits = parse_packet(bits, depth + 1)
            sub.append(packet)

    return sub, bits


def parse_packet(bits, depth=1):
    # print("\nPARSE PACKET\n")
    if len(bits) < 11:
        return dict(), ""
    packet = dict()
    # print()
    # print(depth * "  ", bits)
    version, id_, bits = get_packet_header(bits)
    V, T = int(version, 2), int(id_, 2)
    packet["version"] = V
    if id_ == "100":
        packet["type"] = "litteral"
        # print(depth * "  ", f"Literal (V:{V},T:{T})")
        # print(depth * "  ", version, id_, end=" ")
        num, bits = parse_literal(bits)
        # print(depth * "  ", f"Literal {int(num, 2)}")
        packet["value"] = int(num, 2)
    else:
        packet["type"] = f"operator {bits[0]}"
        # print(depth * "  ", f"Operator (V:{V},T:{T})")
        # print(depth * "  ", version, id_, end=" ")
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


def testing():

    packets = [
        "D2FE28",
        "38006F45291200",
        "EE00D40C823060",
        "8A004A801A8002F478",
        "620080001611562C8802118E34",
        "C0015000016115A2E0802F182340",
        "A0016C880162017C3686B18A3D4780",
    ]

    for hex_ in packets:
        bits = hex_to_bin(hex_)
        print(hex_)
        packets, bits = parse_packet(bits)
        print(add_version(packets))
        print()


def main():
    with open("./data.txt", "r") as file:
        hex_ = file.readlines()[0].strip()
        bits = hex_to_bin(hex_)
        packets, _ = parse_packet(bits)
        print(add_version(packets))


if __name__ == "__main__":
    main()
