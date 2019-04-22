import GF2nPY

# S_BOX=[[0x9,0x4,0xa,0xb],[0xd,0x1,0x8,0x5],[0x6,0x2,0x0,0x3],[0xc,0xe,0xf,0x7]]
# S_BOX_INV=[[0xa,0x5,0x9,0xb],[0x1,0x7,0x8,0xf],[0x6,0x0,0x2,0x3],[0xc,0x4,0xd,0xe]]
# def transfer(s_box_hex):
#     '''
#     Transfer s-box hex list into binary list
#     '''
#     result=[]
#     tmp=[]
#     for line in s_box_hex:
#         for item in line:
#             tmp.append(bin(int(item))[2:])
#         result.append(tmp)
#         tmp=[]
#     return result
S_BOX = [['1001', '0100', '1010', '1011'], ['1101', '0001', '1000', '0101'], ['0110', '0010', '0000', '0011'], ['1100', '1110', '1111', '0111']]
S_BOX_INV = [['1010', '0101', '1001', '1011'], ['0001', '0111', '1000', '1111'], ['0110', '0000', '0010', '0011'], ['1100', '0100', '1101', '1110']]


def do_s_box(row, col, box=S_BOX):
    '''
    do_s_box('00','10')='1010'
    '''
    return box[int(row, 2)][int(col, 2)]


class KEY:
    key = ""

    def __init__(self, key):
        if self.check(key):
            self.key = key

    @staticmethod
    def check(key):
        if (len(key) != 16):
            raise ValueError("S-AES key must be 16-bit. ")
        if not (isinstance(key, str)):
            raise TypeError("S-AES key must be string. ")
        for item in key:
            if item not in ["0", "1"]:
                raise TypeError("S-AES key paramter must be 0-1 binary. ")
        return True

    def get_sub_key(self):
        '''
        key=KEY('0010110101010101')
        key.get_sub_key()=['0010110101010101', '1011110011101001', '101000111001010']
        '''
        sub_key_list = []
        # K0 = key
        sub_key_list.append(self.get())
        w2 = GF2nPY.Bin.bin_add(self.left(), self.g(self.right(), 0), 8)
        w3 = GF2nPY.Bin.bin_add(w2, self.right(), 8)
        sub_key_list.append(w2 + w3)
        w4 = GF2nPY.Bin.bin_add(w2, self.g(w3, 1), 8)
        w5 = GF2nPY.Bin.bin_add(w4, w3, 8)
        sub_key_list.append(w4 + w5)
        return sub_key_list

    @staticmethod
    def g(right, r):
        '''
        Do SubNib and RorNib
        '''
        Rcon = ["10000000", "00110000"]
        tmp = right[4:] + right[:4]
        tmp = do_s_box(tmp[:2], tmp[2:4]) + do_s_box(tmp[4:6], tmp[6:])
        return GF2nPY.Bin.bin_add(tmp, Rcon[r], 8)

    def put(self, key):
        self.__init__(key)

    def get(self):
        return self.key

    def left(self):
        return self.key[:8]

    def right(self):
        return self.key[8:]


class MESSAGE:
    message = ""

    def __init__(self, message):
        if self.check(message):
            self.message = message

    @staticmethod
    def check(message):
        if (len(message) != 16):
            raise ValueError("S-AES plain txt must be 16-bit. ")
        if not (isinstance(message, str)):
            raise TypeError("S-AES key must be string. ")
        for item in message:
            if item not in ["0", "1"]:
                raise TypeError("S-AES plain txt paramter must be 0-1 binary. ")
        return True

    def get(self):
        return self.message


class AES:
    message = MESSAGE("0000000000000000")
    key = KEY("0000000000000000")

    def __init__(self, message, key):
        if (isinstance(message, MESSAGE) and isinstance(key, KEY)):
            self.message = message
            self.key = key
        else:
            raise TypeError("Argument must be the compared object. ")

    def encrypt(self):
        subkey = self.key.get_sub_key()
        # round 1: 轮密钥加
        tmp = GF2nPY.Bin.bin_add(subkey[0], self.message.get(), 16)
        # round 2: 半字节替代、行移位、列混淆、轮密钥加
        tmp = GF2nPY.Bin.bin_add(subkey[1], self.mc(self.sr(self.ns(tmp))), 16)
        # round 3: 半字节替代、行移位、轮密钥加
        tmp = GF2nPY.Bin.bin_add(subkey[2], self.sr(self.ns(tmp)), 16)
        return tmp

    @staticmethod
    def ns(m_16):
        '''
        半字节替代
        ns("0010110101010101")='1010111000010001'
        '''
        result = ""
        for i in range(4):
            result += do_s_box(m_16[i * 4:i * 4 + 2], m_16[i * 4 + 2:i * 4 + 4])
        return result

    @staticmethod
    def ns_inv(m_16):
        '''
        半字节替代求逆
        ns_inv("1010111000010001")='0010110101010101'
        '''
        result = ""
        for i in range(4):
            result += do_s_box(m_16[i * 4:i * 4 + 2], m_16[i * 4 + 2:i * 4 + 4], S_BOX_INV)
        return result

    @staticmethod
    def sr(m_16):
        '''
        行移位
        sr("0010110111010001")='0010110100011101"
        '''
        return m_16[:4] + m_16[12:16] + m_16[8:12] + m_16[4:8]

    @staticmethod
    def mc(m_16):
        '''
        列混淆
        mc('0110010011000000')='0011010001110011'
        '''
        gf24 = GF2nPY.GF2nField(4, "10011")
        s00 = GF2nPY.Bin.bin_add(m_16[:4], gf24.multiply(bin(4)[2:], m_16[4:8]), 4)
        s10 = GF2nPY.Bin.bin_add(m_16[4:8], gf24.multiply(bin(4)[2:], m_16[:4]), 4)
        s01 = GF2nPY.Bin.bin_add(m_16[8:12], gf24.multiply(bin(4)[2:], m_16[12:16]), 4)
        s11 = GF2nPY.Bin.bin_add(m_16[12:16], gf24.multiply(bin(4)[2:], m_16[8:12]), 4)
        return s00 + s10 + s01 + s11

    @staticmethod
    def mc_inv(m_16):
        '''
        列混淆逆变换
        mc('0011010001110011')='0110010011000000'
        '''
        gf24 = GF2nPY.GF2nField(4, "10011")
        s00 = GF2nPY.Bin.bin_add(gf24.multiply(bin(9)[2:], m_16[:4]), gf24.multiply(bin(2)[2:], m_16[4:8]), 4)
        s10 = GF2nPY.Bin.bin_add(gf24.multiply(bin(2)[2:], m_16[:4]), gf24.multiply(bin(9)[2:], m_16[4:8]), 4)
        s01 = GF2nPY.Bin.bin_add(gf24.multiply(bin(9)[2:], m_16[8:12]), gf24.multiply(bin(2)[2:], m_16[12:16]), 4)
        s11 = GF2nPY.Bin.bin_add(gf24.multiply(bin(2)[2:], m_16[8:12]), gf24.multiply(bin(9)[2:], m_16[12:16]), 4)
        return s00 + s10 + s01 + s11

    def decrypt(self):
        subkey = self.key.get_sub_key()
        # round 1
        tmp = GF2nPY.Bin.bin_add(subkey[2], self.message.get(), 16)
        # round 2
        tmp = GF2nPY.Bin.bin_add(subkey[1], self.ns_inv(self.sr(tmp)), 16)
        # round 3
        tmp = GF2nPY.Bin.bin_add(subkey[0], self.ns_inv(self.sr(self.mc_inv(tmp))), 16)
        return tmp


if __name__ == "__main__":
    key = KEY("1010011100111011")
    plain_text = MESSAGE("0110111101101011")

    cipher = AES(plain_text, key)
    print(cipher.encrypt())

    encrypted_text = MESSAGE("0000011100111000")
    decipher = AES(encrypted_text, key)
    print(decipher.decrypt())
