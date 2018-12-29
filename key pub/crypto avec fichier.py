from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.serialization import load_pem_private_key


def load_key_private():
    with open("key_private.pem", 'rb') as pem_in:
        pemlines = pem_in.read()
    privkey = load_pem_private_key(pemlines, None, backend=default_backend())
    return privkey


def load_key_public():
    with open("key_pub.pem", 'rb') as pem_in:
        pemlines = pem_in.read()
        pubkey = load_pem_public_key(pemlines, backend=default_backend())
    return pubkey


public_key = load_key_public()
private_key = load_key_private()

print(public_key)
print(private_key)

message = "Voici le message Ahahaha l va etre longVoici le"
print (message)

messagecipher = public_key.encrypt(message.encode('utf-8'), padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                 algorithm=hashes.SHA256(),
                                 label=None))


print(messagecipher)

messagedecipher = private_key.decrypt(messagecipher, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                 algorithm=hashes.SHA256(),
                                 label=None))
messagedecipher = messagedecipher.decode('utf-8')

print(messagedecipher)

