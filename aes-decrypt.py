import argparse
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding 

"""
out = b'\x85\r\xa6\x87_\x03\xdb\x9a\xcce\xf5\x8a\x98\x18`\xad'
key = b'\xa0\x05\x83N\xf2n\x1d\x90\x14\xa5\x82\x0f\xd2\xc5Sh'
IV = b'h\x84F\xb9\x80\xdf\x00\xb6\xd5Q\x0f\xc1\x9d\xd1\x13z'
# test case
mode = "cbc" #Can be replaced with ecb/cbc/gcm
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

def aes_decrypt(key,mode,In,IV,*gcm_arg):
	if mode == "cbc":
		decryptor = Cipher(algorithms.AES(key), modes.CBC(IV)).decryptor()
	elif mode == "ecb":
		decryptor = Cipher(algorithms.AES(key), modes.ECB()).decryptor()
	elif mode == "gcm":
		decryptor = Cipher(algorithms.AES(key), modes.GCM(IV)).decryptor()
		decryptor.authenticate_additional_data(*gcm_arg)

	In = decryptor.update(In)
	unpadder = padding.PKCS7(128).unpadder()
	out = unpadder.update(In) + unpadder.finalize()
	return out

key = hex2bin(params.key.read()) if params.key else None
input = params.input.read() 
mode = params.mode 
IV = hex2bin(params.IV.read()) if params.IV else None

gcm_arg = params.gcm_arg.read() if params.gcm_arg else None

out = aes_decrypt(key,mode,input,IV, gcm_arg)

write_file(params.out, out)