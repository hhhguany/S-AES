'''
S Box gengerater
'''
import GF2nPY
import math


class SBOX():
    '''
    Example:
    sbox = SBOX(16)
    print(sbox.get())
    '''
    sbox = []
    bit = 0

    def __init__(self, bit_len):
        if int(math.sqrt(bit_len)) != math.sqrt(bit_len):
            raise ValueError("Invalid bit length")
        self.bit = bit_len
        self.init_sbox()
        self.generate_sbox_16()

    def init_sbox(self):
        value = 0
        for i in range(int(math.sqrt(self.bit))):
            tmp = []
            for j in range(int(math.sqrt(self.bit))):
                tmp.append(value)
                value += 1
            self.sbox.append(tmp)

    def generate_sbox_16(self):
        gf24 = GF2nPY.GF2nField(4, "10011")

        #1 Do inverse
        result = []
        for line in self.sbox:
            tmp = []
            for item in line:
                tmp.append(gf24.inverse(bin(item)[2:]))
            result.append(tmp)

        #2 Do mix
        self.sbox = []
        for line in result:
            tmp = []
            for item in line:
                item = GF2nPY.Bin.padding_0(item, 4)
                b0 = GF2nPY.Bin.bin_add(item[0], GF2nPY.Bin.bin_add(item[2], GF2nPY.Bin.bin_add(item[3], "1", 1), 1), 1)
                b1 = GF2nPY.Bin.bin_add(item[0], GF2nPY.Bin.bin_add(item[1], item[3], 1), 1)
                b2 = GF2nPY.Bin.bin_add(item[0], GF2nPY.Bin.bin_add(item[1], item[2], 1), 1)
                b3 = GF2nPY.Bin.bin_add(item[1], GF2nPY.Bin.bin_add(item[2], GF2nPY.Bin.bin_add(item[3], "1", 1), 1), 1)
                tmp.append(int(b0 + b1 + b2 + b3, 2))
            self.sbox.append(tmp)

    def get(self):
        return self.sbox
