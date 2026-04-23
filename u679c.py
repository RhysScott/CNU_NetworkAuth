"""
Author: u697c
Ref: https://blog.csdn.net/guo666aoao/article/details/147273148?spm=1001.2014.3001.5502
"""

from Crypto.Cipher import DES
from Crypto.Util.Padding import pad
import binascii


 
def f_key(username):
    key_str = username[-4:] + username + "12345678"
    return key_str[:8].encode('utf-8')  # DES key must be 8 bytes
 
def encrypt_password(password, username):
    key = f_key(username)
    cipher = DES.new(key, DES.MODE_ECB)
    padded_password = pad(password.encode('utf-8'), DES.block_size)
    encrypted = cipher.encrypt(padded_password)
    return binascii.hexlify(encrypted).decode('utf-8')  # Hexadecimal string
 
def encrypt(username, password):
    encrypted = encrypt_password(password, username)
    return encrypted
