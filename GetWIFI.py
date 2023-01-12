import pywifi
from Crypto.Cipher import AES
from getpass import getpass

def get_WPASS():
    wifi = pywifi.PyWiFi()
    interface = wifi.interfaces()[0]
    interface.scan()
    bsses = interface.scan_results()
    WLIST = []
    for bss in bsses:
        WLIST.append((bss.ssid, bss.key))
    return WLIST

def encrypt_file(file_path, key):
    with open(file_path, "rb") as f:
        data = f.read()
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    with open(file_path, "wb") as f:
        [f.write(x) for x in (cipher.nonce, tag, ciphertext)]
        
def decrypt_file(file_path, key):
    with open(file_path, "rb") as f:
        nonce, tag, ciphertext = [f.read(x) for x in (16, 16, -1)]
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)
    with open(file_path, "wb") as f:
        f.write(data)

WPASS = get_WPASS()

with open("WPASS.txt", "w") as f:
    for wifi in WPASS:
        f.write(f"SSID: {wifi[0]}\nPassword: {wifi[1]}\n\n")
        
key = getpass("Input an encryption key here: ").encode()
encrypt_file("WPASS.txt", key)
print("Done, WPass saved and encrypted.")
