import SAESPY
import SBOXPY
import argparse


def get_arges():
    parser = argparse.ArgumentParser(description="S-AES 加解密软件", epilog="henrt@hejunlin.cn")
    function = parser.add_mutually_exclusive_group()
    function.add_argument("-gsb", "--generate_sbox", action="store_true", help="生成S-AES的S-Box", default=False)
    function.add_argument("-e", "--encrypt", action="store_true", help="加密", default=False)
    function.add_argument("-d", "--decrypt", action="store_true", help="16-bit 解密", default=False)
    parser.add_argument("-k", "--key", type=str, help="密钥", default="0110111101101011")
    parser.add_argument("-m", "--message", type=str, help="16-bit 消息", default="0000011100111000")
    arguments = parser.parse_args()
    return arguments


def main():
    arguments = get_arges()
    try:
        if arguments.generate_sbox:
            sb = SBOXPY.SBOX(16)
            print(sb.get())
        if arguments.encrypt:
            message = SAESPY.MESSAGE(arguments.message)
            key = SAESPY.KEY(arguments.key)
            cipher = SAESPY.AES(message, key)
            print(cipher.encrypt())
        if arguments.decrypt:
            message = SAESPY.MESSAGE(arguments.message)
            key = SAESPY.KEY(arguments.key)
            decipher = SAESPY.AES(message, key)
            print(decipher.decrypt())
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()