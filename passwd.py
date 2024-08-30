import base64
import os
from ConfigManager import ConfigManager
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

backend = default_backend()
configMgr = ConfigManager()
rawBaseKey = "librecall_basekey"
passhash = ""
basekey = configMgr.get("BASEKEY")

def deriveKey(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=backend
    )
    return kdf.derive(password.encode())

def encrypt(password, plaintext):
    if type(plaintext) != str:
        plaintext = str(plaintext)
    salt = configMgr.get("SALT")
    salt = base64.b64decode(salt)
    if not salt:
        return
    iv = b'\xd5\xa7l\x1f0U\xd5\x1e\xeez\x18\xc8'
    derivedKey = deriveKey(password, salt)
    cipher = Cipher(algorithms.AES(derivedKey), modes.GCM(iv), backend=backend)
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
    encryptedData = salt + iv + ciphertext + encryptor.tag
    return base64.urlsafe_b64encode(encryptedData).decode()

def decrypt(password, data):
    data = base64.urlsafe_b64decode(data)
    
    salt = data[:16]
    iv = data[16:28]
    tag = data[-16:]
    ciphertext = data[28:-16]

    savedSalt = base64.b64decode(configMgr.get("SALT"))
    derivedKey = deriveKey(password, salt)
    cipher = Cipher(algorithms.AES(derivedKey), modes.GCM(iv, tag), backend=backend)
    decryptor = cipher.decryptor()
    rawData = decryptor.update(ciphertext) + decryptor.finalize()
    
    return rawData.decode()

def getSHA256(bytes):
    digest = hashes.Hash(hashes.SHA256(), backend=backend)
    digest.update(bytes)
    shaHex = digest.finalize().hex()
    return shaHex

def verifyPassword(password):
    return (encrypt(password, rawBaseKey) == basekey)

def setPassword(password):
    global passhash, basekey
    passhash = password
    basekey = encrypt(password, rawBaseKey)
    configMgr.set("BASEKEY", basekey)