import struct

# s = 0
# for i, el in enumerate(a[::-1]):
#     s += el * (2**i)
#     print(el, i, 2 ** i, s)
# s.to_bytes(length=int(np.ceil(np.log2(s)))//8 + 1, byteorder='big')

class SHA1Hash:
    def __init__(self, data):
        self.data = data
        self.h = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0]

    @staticmethod
    def bits_to_byte(b: []):
        chunked_list = list()
        chunk_size = 8
        for i in range(0, len(b), chunk_size):
            chunked_list.append(b[i:i + chunk_size])
        # print(chunked_list)
        for n, a in enumerate(chunked_list):
            s = 0
            for i, el in enumerate(a[::-1]):
                s += el * (2**i)
                # print(el, i, 2 ** i, s)
            # s = s.to_bytes(length=1, byteorder='big')
            chunked_list[n] = s
        # print(chunked_list)
        # print(bytearray(chunked_list))
        return bytearray(chunked_list)

    @staticmethod
    def rotate(n, b, l):
        return ((n << b) | (n >> (l - b))) & (2 ** l - 1)

    def padding(self):
        length = len(self.data) * 8
        print('length ', length)
        last_block_length = (len(self.data) * 8) % 512
        print('last block length', last_block_length)
        pad = [1, *[0]*(512 + 447 - last_block_length if 447 - last_block_length < 0 else 447 - last_block_length)]
        pad = self.bits_to_byte(pad) + length.to_bytes(length=8, byteorder='big')
        print(len(pad), pad)
        padded_data = self.data + pad
        print('padded data length', len(padded_data))
        return padded_data

    def split_blocks(self):
        return [self.padded_data[i : i + 64] for i in range(0, len(self.padded_data), 64)]

    def expand_block(self, block):
        w = list(struct.unpack(">16L", block)) + [0] * 64
        for i in range(16, 80):
            w[i] = self.rotate((w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16]), 1, 32)
        return w

    def final_hash(self):
        self.padded_data = self.padding()
        self.blocks = self.split_blocks()
        print(self.blocks)
        for block in self.blocks:
            expanded_block = self.expand_block(block)
            # print(expanded_block)
            a, b, c, d, e = self.h
            for i in range(0, 80):
                if 0 <= i < 20:
                    f = (b & c) | ((~b) & d)
                    k = 0x5A827999
                elif 20 <= i < 40:
                    f = b ^ c ^ d
                    k = 0x6ED9EBA1
                elif 40 <= i < 60:
                    f = (b & c) | (b & d) | (c & d)
                    k = 0x8F1BBCDC
                elif 60 <= i < 80:
                    f = b ^ c ^ d
                    k = 0xCA62C1D6
                a, b, c, d, e = (
                    self.rotate(a, 5, 32) + f + e + k + expanded_block[i] & 0xFFFFFFFF,
                    a,
                    self.rotate(b, 30, 32),
                    c,
                    d,
                )
            self.h = (
                self.h[0] + a & 0xFFFFFFFF,
                self.h[1] + b & 0xFFFFFFFF,
                self.h[2] + c & 0xFFFFFFFF,
                self.h[3] + d & 0xFFFFFFFF,
                self.h[4] + e & 0xFFFFFFFF,
            )
        print('{:x} {:x} {:x} {:x} {:x}'.format(*self.h))
        return int.from_bytes(b''.join([h.to_bytes(length=4, byteorder='big') for h in self.h]), byteorder='big')

if __name__ == "__main__":
    input_string = "The quick brown fox jumps over the lazy dog"
    hash_input = bytes(input_string, "utf-8")
    print('hash input ', hash_input)
    print('{:x}'.format(SHA1Hash(hash_input).final_hash()))