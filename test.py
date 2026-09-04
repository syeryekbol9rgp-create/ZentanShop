from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher = Fernet(key)

text = b"codoo zarna vne 20K"

encrypted = cipher.encrypt(text)
print("Encrypted:", encrypted)

decrypted = cipher.decrypt(encrypted)
print("Decrypted:", decrypted.decode())


