import os
import sys
# import random


class CRYP256:
    def __init__(self):
        self.key = ""

    def encrypt(self, message):
        encrypted_message = bytearray()
        key_length = len(self.key)
        
        for i in range(len(message)):
            encrypted_byte = message[i] ^ ord(self.key[i % key_length])
            encrypted_message.append(encrypted_byte)
        
        return encrypted_message

    def decrypt(self, encrypted_message):
        return self.encrypt(encrypted_message)  # XOR encryption is symmetric


    def args_start(self):
        message = b"Hello, World!"
        self.key = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz$#"

        print("raw message      :", message)
        encrypted_message = self.encrypt(message)
        print("Encrypted message:", encrypted_message)

        decrypted_message = self.decrypt(encrypted_message)
        print("Decrypted message:", decrypted_message.decode())




CRYP256().args_start()
