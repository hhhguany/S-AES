# S-AES
A home work for S-AES, write with python.

## Usage
```
> python .\saes.py
> usage: saes.py [-h] [-gsb | -e | -d] [-k KEY] [-m MESSAGE]

  S-AES 加解密软件

  optional arguments:
    -h, --help            show this help message and exit
    -gsb, --generate_sbox
                          生成S-AES的S-Box
    -e, --encrypt         加密
    -d, --decrypt         16-bit 解密
    -k KEY, --key KEY     密钥
    -m MESSAGE, --message MESSAGE
                          16-bit 消息
```

## Example
- Generate S-AES S-Box
```
> python .\saes.py -gsb
> [[9, 4, 10, 11], [13, 1, 8, 5], [6, 2, 0, 3], [12, 14, 15, 7]]
```
- Encrypt
```
> python .\saes.py -d -k 0110111101101011 -m 0000011100111000
> 0101110011010100
```
- Decrypt
```
> python .\saes.py -e -k 0110111101101011 -m 0101110011010100
> 0000011100111000
```