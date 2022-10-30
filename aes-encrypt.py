import argparse 
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes 
from cryptography.hazmat.primitives import padding 
 
""" 
#manual test case 
In = b"alicexoxox:bobko0oo0l:hangjun" #test case by using Q.2b 
mode = "ecb" #Can be replaced with CBC\ECB\GCM 
key = os.urandom(16) 
IV = os.urandom(16) 
""" 
parser = argparse.ArgumentParser() 
parser.add_argument('-key', type=argparse.FileType('r'), help='key') 
parser.add_argument('-input', type=argparse.FileType('rb', 0), help='input') 
parser.add_argument('-mode', type=str, default="ecb", help='mode') 
parser.add_argument('-IV', type=argparse.FileType('r'), help='iv') 
parser.add_argument('-gcm_arg', type=argparse.FileType('rb', 0), help='gcm_arg') 
parser.add_argument('-out', type=argparse.FileType('wb', 0), help='output') 
 
params = parser.parse_args() 
 
def hex2bin(hex): 
    return bytes.fromhex(hex) 
 
def write_file(file, data): 
    file.write(data) 
 
def aes_encrypt(key,mode,In,IV,*gcm_arg): 
    if mode == "cbc": 
        encryptor = Cipher(algorithms.AES(key), modes.CBC(IV)).encryptor() 
    elif mode == "ecb": 
        encryptor = Cipher(algorithms.AES(key), modes.ECB()).encryptor() 
    elif mode == "gcm": 
        encryptor = Cipher(algorithms.AES(key), modes.GCM(IV)).encryptor() 
        encryptor.authenticate_additional_data(*gcm_arg) 
 
    padder = padding.PKCS7(128).padder() 
    In = padder.update(In) + padder.finalize() 
    out = encryptor.update(In) + encryptor.finalize() 
    return out 
 
key = hex2bin(params.key.read()) 
input = params.input.read() 
mode = params.mode 
IV = hex2bin(params.IV.read()) if params.IV else None 
 
gcm_arg = params.gcm_arg.read() if params.gcm_arg else None 
 
out = aes_encrypt(key,mode,input,IV, gcm_arg) 
 
write_file(params.out, out)