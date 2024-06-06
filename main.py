# CRYP-256

import sys
import random


class CRYP256:
    def __init__(self):
        self.key = ""
        self.filename = ""
        self.text = ""

    def encrypt(self, message):
        encrypted_message = bytearray()
        key_length = len(self.key)
        
        for i in range(len(message)):
            encrypted_byte = message[i] ^ ord(self.key[i % key_length])
            encrypted_message.append(encrypted_byte)
        
        random.seed(self.key)
        shuffled_indices = list(range(len(encrypted_message)))
        random.shuffle(shuffled_indices)
        
        index_map = {i: shuffled_indices[i] for i in range(len(shuffled_indices))}
        
        reordered_message = bytearray(len(encrypted_message))
        for original_index, shuffled_index in index_map.items():
            reordered_message[shuffled_index] = encrypted_message[original_index]
        
        return reordered_message


    def decrypt(self, encrypted_message):
        random.seed(self.key)
        shuffled_indices = list(range(len(encrypted_message)))
        random.shuffle(shuffled_indices)
        
        index_map = {shuffled_indices[i]: i for i in range(len(shuffled_indices))}
        
        reordered_message = bytearray(len(encrypted_message))
        for shuffled_index, original_index in index_map.items():
            reordered_message[original_index] = encrypted_message[shuffled_index]
        
        decrypted_message = bytearray()
        key_length = len(self.key)
        for i in range(len(reordered_message)):
            decrypted_byte = reordered_message[i] ^ ord(self.key[i % key_length])
            decrypted_message.append(decrypted_byte)
        
        return decrypted_message
    
    def EncryptFile(self):
        r1 = open(self.filename, "rb")
        encrypted_message = self.encrypt(r1.read())

        for i in range(9):
            encrypted_message = self.encrypt(encrypted_message)
        r1.close()

        r2 = open(self.filename + ".CRYP256", "wb")
        r2.write(encrypted_message)
        r2.close()

    def DecryptFile(self):
        r1 = open(self.filename, "rb")
        encrypted_message = self.decrypt(r1.read())

        for i in range(9):
            encrypted_message = self.decrypt(encrypted_message)
        r1.close()

        r2 = open(self.filename[0:self.filename.find(".CRYP256")], "wb")
        r2.write(encrypted_message)
        r2.close()

    def ArgsStart(self):
        self.filename = sys.argv[1]
        self.key = sys.argv[2]

        if self.filename.endswith(".CRYP256"):
            self.DecryptFile()
        else:
            self.EncryptFile()


CRYP256().ArgsStart()
