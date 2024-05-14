# CRYP-256


key = "P9HebdWQwqzgT4YUDpQkd6T6dd8JKNCJD2DSdklSnldDDnekcnVLFHBERBX"

# switch = [146, 131, 31, 251, 26, 220, 109, 127, 37, 61, 174, 217, 161, 226, 233, 24, 71, 96, 147, 21, 171, 66, 122, 209, 78, 123, 206, 39, 22, 155, 145, 143, 208, 230, 241, 255, 172, 141, 124, 232, 214, 23, 234, 119, 81, 52, 19, 140, 101, 176, 32, 256, 135, 192, 70, 253, 229, 240, 151, 55, 2, 210, 191, 163, 91, 252, 134, 69, 228, 105, 223, 248, 142, 57, 177, 120, 59, 204, 84, 104, 138, 92, 38, 137, 95, 128, 164, 106, 186, 222, 6, 93, 152, 94, 182, 250, 25, 60, 207, 245, 64, 75, 72, 157, 45, 99, 166, 193, 154, 50, 65, 4, 74, 246, 67, 126, 97, 5, 8, 242, 200, 183, 144, 221, 83, 159, 56, 53, 12, 27, 90, 133, 187, 243, 175, 236, 225, 121, 170, 103, 188, 110, 237, 49, 189, 173, 118, 17, 54, 7, 88, 51, 98, 169, 62, 180, 194, 107, 239, 76, 244, 148, 224, 48, 153, 216, 190, 33, 156, 20, 11, 247, 85, 149, 16, 212, 1, 9, 10, 130, 179, 73, 41, 219, 215, 86, 160, 114, 168, 30, 28, 80, 197, 185, 87, 0, 203, 235, 205, 254, 165, 79, 89, 34, 18, 58, 40, 150, 231, 82, 181, 68, 162, 47, 184, 195, 238, 113, 167, 35, 227, 196, 46, 3, 199, 102, 213, 136, 112, 211, 108, 125, 132, 202, 139, 29, 43, 178, 158, 42, 249, 111, 115, 116, 13, 63, 201, 198, 44, 117, 36, 100, 218, 15, 77, 129, 14]
switch = [89, 109, 35, 92, 69, 71, 60, 57, 36, 97, 119, 47, 91, 38, 52, 65, 85, 106, 33, 82, 112, 122, 53, 83, 51, 113, 117, 44, 100, 55, 67, 43, 40, 105, 101, 93, 80, 74, 39, 111, 49, 86, 115, 118, 37, 58, 42, 102, 110, 120, 45, 124, 62, 114, 72, 70, 34, 77, 41, 104, 63, 121, 46, 99, 54, 88, 107, 98, 64, 66, 59, 125, 61, 87, 75, 90, 50, 123, 79, 103, 81, 73, 68, 48, 78, 116, 56, 76, 108, 84]

def SwitchChar(text):
    output = ""
    for pp in text:
        try:
            output += chr(switch[ord(pp)])
        except:
            pass

    return output

def SwitchBackChar(text):
    output = ""
    for char in text:
        try:
            index = switch.index(ord(char))
            output += chr(index)
        except:
            pass

    return output


def encrypt(text):
    encrypted_hex = ""
    key_index = 0
    for char in text:
        ascii2 = ord(char)
        ascii1 = ord(key[key_index])
        encrypted_char = ascii1 ^ ascii2
        encrypted_hex += format(encrypted_char, '02x')
        key_index = (key_index + 1) % len(key)
    return encrypted_hex

def decrypt(encrypted_text):
    decrypted_text = ""
    key_index = 0
    for i in range(0, len(encrypted_text), 2):
        hex_pair = encrypted_text[i:i+2]
        encrypted_char = int(hex_pair, 16)
        ascii2 = ord(key[key_index])
        decrypted_char = chr(encrypted_char ^ ascii2)
        decrypted_text += decrypted_char
        key_index = (key_index + 1) % len(key)
    return decrypted_text






text = "111111111111111"

en = encrypt(text)
de = decrypt(en)

print(f"raw text      : {text}")
print(f"encrypt text  : {en}")
print(f"decrypt text  : {de}")
