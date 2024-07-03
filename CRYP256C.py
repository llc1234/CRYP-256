import os
import sys


class CRYP256C:
    def __init__(self):
        self.filename = "start.txt"
        self.key = ""
        self.all_keys = []
        self.data_list = []
        self.switch = [
            b'\x38', b'\x39', b'\x3a', b'\x3b', b'\x0c', b'\x0d', b'\x0e', b'\x0f',
            b'\x3c', b'\x3d', b'\x3e', b'\x3f', b'\x28', b'\x29', b'\x2a', b'\x2b', 
            b'\x2c', b'\x2d', b'\x2e', b'\x2f', b'\x30', b'\x31', b'\x32', b'\x33',
            b'\x08', b'\x09', b'\x0a', b'\x0b', b'\x74', b'\x75', b'\x76', b'\x77',
            b'\x00', b'\x01', b'\x02', b'\x03', b'\x04', b'\x05', b'\x06', b'\x07',
            b'\x10', b'\x11', b'\x12', b'\x13', b'\x14', b'\x15', b'\x16', b'\x17',
            b'\x20', b'\x21', b'\x22', b'\x23', b'\x24', b'\x25', b'\x26', b'\x27',
            b'\x18', b'\x19', b'\x1a', b'\x1b', b'\x1c', b'\x1d', b'\x1e', b'\x1f',
            b'\x34', b'\x35', b'\x36', b'\x37', b'\x70', b'\x71', b'\x72', b'\x73', 
            b'\xe0', b'\xe1', b'\xe2', b'\xe3', b'\xe4', b'\xe5', b'\xe6', b'\xe7',
            b'\xc8', b'\xc9', b'\xca', b'\xcb', b'\xcc', b'\xcd', b'\xce', b'\xcf',
            b'\xe8', b'\xe9', b'\xea', b'\xeb', b'\xec', b'\xed', b'\xee', b'\xef',
            b'\xd0', b'\xd1', b'\xd2', b'\xd3', b'\xd4', b'\xd5', b'\xd6', b'\xd7',
            b'\xb0', b'\xb1', b'\xb2', b'\xb3', b'\xb4', b'\xb5', b'\xb6', b'\xb7',
            b'\xf0', b'\xf1', b'\xf2', b'\xf3', b'\xf4', b'\xf5', b'\xf6', b'\xf7',
            b'\xf8', b'\xf9', b'\xfa', b'\xfb', b'\xfc', b'\xfd', b'\xfe', b'\xff',
            b'\xb8', b'\xb9', b'\xba', b'\xbb', b'\xbc', b'\xbd', b'\xbe', b'\xbf',
            b'\x88', b'\x89', b'\x8a', b'\x8b', b'\x8c', b'\x8d', b'\x8e', b'\x8f',
            b'\xd8', b'\xd9', b'\xda', b'\xdb', b'\xdc', b'\xdd', b'\xde', b'\xdf',
            b'\x78', b'\x79', b'\x7a', b'\x7b', b'\x7c', b'\x7d', b'\x7e', b'\x7f',
            b'\x50', b'\x51', b'\x52', b'\x53', b'\x54', b'\x55', b'\x56', b'\x57',
            b'\x60', b'\x61', b'\x62', b'\x63', b'\x64', b'\x65', b'\x66', b'\x67',
            b'\x90', b'\x91', b'\x92', b'\x93', b'\x94', b'\x95', b'\x96', b'\x97',
            b'\x68', b'\x69', b'\x6a', b'\x6b', b'\x6c', b'\x6d', b'\x6e', b'\x6f',
            b'\x98', b'\x99', b'\x9a', b'\x9b', b'\x9c', b'\x9d', b'\x9e', b'\x9f',
            b'\x80', b'\x81', b'\x82', b'\x83', b'\x84', b'\x85', b'\x86', b'\x87',
            b'\xa8', b'\xa9', b'\xaa', b'\xab', b'\xac', b'\xad', b'\xae', b'\xaf',
            b'\xc0', b'\xc1', b'\xc2', b'\xc3', b'\xc4', b'\xc5', b'\xc6', b'\xc7',
            b'\x58', b'\x59', b'\x5a', b'\x5b', b'\x5c', b'\x5d', b'\x5e', b'\x5f',
            b'\x48', b'\x49', b'\x4a', b'\x4b', b'\x4c', b'\x4d', b'\x4e', b'\x4f',
            b'\x40', b'\x41', b'\x42', b'\x43', b'\x44', b'\x45', b'\x46', b'\x47',
            b'\xa0', b'\xa1', b'\xa2', b'\xa3', b'\xa4', b'\xa5', b'\xa6', b'\xa7'
        ]

    def hash128(self, input_string):
        h1 = 0x12345678
        h2 = 0x9abcdef0
        
        prime1 = 0x45d9f3b
        prime2 = 0x41c6ce57
        
        for i in range(0, len(input_string), 8):
            chunk = input_string[i:i+8]
            
            chunk_value = 0
            for c in chunk:
                chunk_value = (chunk_value << 8) + ord(c)
            
            h1 = (h1 ^ chunk_value) * prime1
            h2 = (h2 ^ chunk_value) * prime2
            
            h1 = h1 & 0xffffffff
            h2 = h2 & 0xffffffff
        
        final_hash = (h1 << 32) | h2

        return f'{final_hash:008x}'
    
    def split_data(self):
        r = open(self.filename, "rb")
        data = r.read()
        r.close()

        for i in range(0, len(data), 64):
            # print(data[i:i+64])
            self.data_list.append(data[i:i+64])

    def XORGate(self, message):
        encrypted_message = bytearray()
        key_length = len(self.key)
        
        for i in range(len(message)):
            encrypted_byte = message[i] ^ ord(self.key[i % key_length])
            encrypted_message.append(encrypted_byte)
        
        return encrypted_message
    
    def switch_bytes(self, input_bytes):
        output_bytes = bytearray()
        for byte in input_bytes:
            switched_byte = self.switch[byte]
            output_bytes.append(switched_byte[0])
        return bytes(output_bytes)

    def reverse_switch_bytes(self, input_bytes):
        reverse_switch = {value[0]: index for index, value in enumerate(self.switch)}
        output_bytes = bytearray()
        for byte in input_bytes:
            original_byte = reverse_switch[byte]
            output_bytes.append(original_byte)
        return bytes(output_bytes)

    def start_mix_up(self):
        r = open(self.filename, "wb")
        
        for pp in self.data_list:
            self.key = self.all_keys[0]
            text = self.XORGate(pp)
            text = self.switch_bytes(text)
            self.key = self.all_keys[1]
            text = self.XORGate(text)
            text = self.switch_bytes(text)
            self.key = self.all_keys[2]
            text = self.XORGate(text)
            text = self.switch_bytes(text)
            self.key = self.all_keys[3]
            text = self.XORGate(text)

            r.write(text)

        r.close()

    def start_mix_down(self):
        r = open(self.filename, "wb")
        
        for pp in self.data_list:
            self.key = self.all_keys[3]
            text = self.XORGate(pp)
            text = self.reverse_switch_bytes(text)
            self.key = self.all_keys[2]
            text = self.XORGate(text)
            text = self.reverse_switch_bytes(text)
            self.key = self.all_keys[1]
            text = self.XORGate(text)
            text = self.reverse_switch_bytes(text)
            self.key = self.all_keys[0]
            text = self.XORGate(text)

            r.write(text)

        r.close()

    def encrypt(self):
        self.split_data()
        self.start_mix_up()

        os.rename(self.filename, self.filename + ".CRYP256C")

    def decrypt(self):
        self.split_data()
        self.start_mix_down()

        os.rename(self.filename, self.filename.replace(".CRYP256C", ""))

    def en_of_de(self):
        if self.filename.endswith(".CRYP256C"):
            self.decrypt()
        else:
            self.encrypt()

    def key_generator(self, start_seed):
        k = self.hash128(start_seed)

        for i in range(4):
            k = self.hash128(k)
            self.all_keys.append(k)

        # print(self.all_keys)

    def start(self):
        if len(sys.argv) != 3:
            print("Usage: sudo python3 CRYP256C.py <filename/.txt/.png/.jpg> <key/sha640>")
            print("Example: sudo python3 CRYP256C.py cat.png 3f307c4a23b754bc8e6f874a4b49303a10")
            sys.exit(1)

        self.filename = sys.argv[1]
        self.key_generator(self.hash128(sys.argv[2]))

        # print("filename:   ", self.filename)
        # print("key     :   ", self.key)

        self.en_of_de()


CRYP256C().start()