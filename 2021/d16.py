from aocd.models import Puzzle
from functools import reduce


def to_binary(h):
  return bin(int(h, 16))[2:].zfill(len(h) * 4)


def to_int(bin):
    return int(bin, base=2)


def read_n(it, n):
    return ''.join(next(it) for _ in range(n))


class LiteralPacket:
    def __init__(self, version, type_id, packet_len, contents) -> None:
        self._version = version
        self._type_id = type_id
        self._packet_len = packet_len
        self._contents = contents
    
    @property
    def version(self):
        return self._version
    
    @property
    def value(self):
        return to_int(self._contents)
    
    def __len__(self):
        return self._packet_len


class OperatorPacket:
    def __init__(self, version, type_id, packet_len, sub_packets) -> None:
        self._version = version
        self._type_id = type_id
        self._packet_len = packet_len
        self._sub_packets = sub_packets
        self._value = None
    
    def _apply_op(self):
        sub_packet_values = map(lambda packet: packet.value,
                                self._sub_packets)
    
        if self._type_id == 0:
            return sum(sub_packet_values)
        elif self._type_id == 1:
            return reduce(lambda x, y: x * y, sub_packet_values)
        elif self._type_id == 2:
            return min(sub_packet_values)
        elif self._type_id == 3:
            return max(sub_packet_values)
        elif self._type_id == 5:
            a, b = sub_packet_values
            return 1 if a > b else 0
        elif self._type_id == 6:
            a, b = sub_packet_values
            return 1 if a < b else 0
        elif self._type_id == 7:
            a, b = sub_packet_values
            return 1 if a == b else 0

    @property
    def value(self):
        if self._value is None:
            self._value = self._apply_op()
        return self._value
    
    def __len__(self):
        return self._packet_len

    @property
    def sub_packets(self):
        return self._sub_packets
    
    @property
    def version(self):
        return self._version


def parse_literal(packet_it, version, type_id):
    contents = []
    packet_len = 6

    # more to come
    while read_n(packet_it, 1) == '1':
        contents.append(read_n(packet_it, 4))
        packet_len += 5
    
    # last group
    contents.append(read_n(packet_it, 4))
    packet_len += 5
    return LiteralPacket(version, type_id, packet_len, ''.join(contents))


def parse_operator(packet_it, version, type_id):
    # one bit is read to identify length type ID
    # 6 are for version and type id
    packet_len = 1 + 6
    sub_packets = []

    if read_n(packet_it, 1) == '0':
        total_sub_len = to_int(read_n(packet_it, 15))
        packet_len += 15 + total_sub_len
        it = iter(read_n(packet_it, total_sub_len))

        while total_sub_len > 0:
            sub_packets.append(parse_packet(it))
            total_sub_len -= len(sub_packets[-1])
    else:
        num_sub_packets = to_int(read_n(packet_it, 11))
        packet_len += 11

        for _ in range(num_sub_packets):
            sub_packets.append(parse_packet(packet_it))
            packet_len += len(sub_packets[-1])
    
    return OperatorPacket(version, type_id, packet_len, sub_packets)


def parse_packet(packet_it):
    version = to_int(read_n(packet_it, 3))
    type_id = to_int(read_n(packet_it, 3))

    return (parse_literal(packet_it, version, type_id)
            if type_id == 4 else
            parse_operator(packet_it, version, type_id))


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=16)
    data = puzzle.input_data

    #data = '8A004A801A8002F478'
    #data = '620080001611562C8802118E34'
    #data = 'C0015000016115A2E0802F182340'
    #data = '38006F45291200'
    #data = 'C200B40A82'

    # convert hex to binary
    packet = ''.join(map(to_binary, data))
    root_packet = parse_packet(iter(packet))

    # part 1
    versions = []
    Q = [root_packet]

    while Q:
        packet = Q.pop()
        versions.append(packet.version)

        if isinstance(packet, OperatorPacket):
            Q.extend(packet.sub_packets)
    
    print(sum(versions))

    # part 2
    print(root_packet.value)
