from advent import read_file, timer
import functools


def hex_to_bin(h):
    s = ''
    for c in h:
        b = bin(int(c, 16))[2:]
        while len(b) % 4:
            b = '0' + b
        s += b
    return s


def read_packet(packet):
    p = dict()
    p["bin"] = packet
    p["version"] = int(packet[:3], 2)
    p["type"] = int(packet[3:6], 2)

    if p["type"] == 4:
        n = 7
        b = packet[n:n+4]

        while packet[n-1] == '1':
            n += 5
            b += packet[n:n+4]

        p["number"] = int(b, 2)
        p["stop"] = n + 4

    else:
        p["I"] = int(packet[6], 2)

        if p["I"]:
            p["L"] = int(packet[7:18], 2)  # Number of subpackets
        else:
            p["L"] = int(packet[7:22], 2)  # Length of subpackets

        n = 18 if p["I"] else 22
        p["sub_packets"] = []
        while (p["I"] and len(p["sub_packets"]) < p["L"]) or n < p["L"] + 22:
            p["sub_packets"].append(read_packet(packet[n:]))
            n += p["sub_packets"][-1]["stop"]

        p["stop"] = n

    return p


def solve(packet):
    match packet["type"]:
        case 4:
            return packet["number"]
        case 0:
            return sum(solve(p) for p in packet["sub_packets"])
        case 1:
            return functools.reduce(lambda a, b: a * b, (solve(p) for p in packet["sub_packets"]))
        case 2:
            return min(solve(p) for p in packet["sub_packets"])
        case 3:
            return max(solve(p) for p in packet["sub_packets"])
        case 5:
            return int(solve(packet["sub_packets"][0]) > solve(packet["sub_packets"][1]))
        case 6:
            return int(solve(packet["sub_packets"][0]) < solve(packet["sub_packets"][1]))
        case 7:
            return int(solve(packet["sub_packets"][0]) == solve(packet["sub_packets"][1]))


def version_sum(packet):
    if "sub_packets" in packet:
        return packet["version"] + sum(version_sum(p) for p in packet["sub_packets"])
    return packet["version"]


@timer
def p1(ins):
    packet = hex_to_bin(ins)
    p = read_packet(packet)

    return version_sum(p)


@timer
def p2(ins):
    packet = hex_to_bin(ins)
    p = read_packet(packet)

    return solve(p)


f = read_file("./Input/Input16")
p1(f)
p2(f)
