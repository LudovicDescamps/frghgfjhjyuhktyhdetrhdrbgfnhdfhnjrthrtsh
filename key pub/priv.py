
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.serialization import load_pem_private_key


fileprivkey = open("key_private.pem", 'wb')

privatekey = rsa.generate_private_key(backend=default_backend(),
                                    public_exponent=65537,
                                    key_size=4096)





pem = privatekey.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption())


fileprivkey.write(pem)
fileprivkey.close()

print(pem)

filepubkey = open("key_pub.pem", 'wb')

publickey = privatekey.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo)

public_key = load_pem_public_key(publickey, backend=default_backend())

print(publickey)

filepubkey.write(publickey)

private_key = load_pem_private_key(pem, None, backend=default_backend())

filepubkey.close()
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