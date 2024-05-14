# CRYP-256

switch = [55, 100, 48, 57, 97, 49, 101, 56, 99, 102, 50, 98, 51, 52, 53, 54]

def SwitchChar(text):
    output = ""
    for char in text:
        if '0' <= char <= '9':
            index = ord(char) - 48
        elif 'a' <= char <= 'f':
            index = ord(char) - 97 + 10
        else:
            output += char
            continue
        output += chr(switch[index])
    return output

def SwitchBackChar(text):
    output = ""
    for char in text:
        ascii_val = ord(char)
        if ascii_val in switch:
            index = switch.index(ascii_val)
            if index < 10:
                output += chr(index + 48)
            else:
                output += chr(index - 10 + 97)
        else:
            output += char
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




text = "hello"

key = "P9HebdWQwqzgT4YUDpQkd6T6dd8JKNCJD2DSdklSnldDDnekcnVLFHBERBX"
en = encrypt(text)
s = SwitchChar(en)
sb = SwitchBackChar(s)
de = decrypt(sb)



print(f"raw text      : {text}")
print(f"encrypt text  : {en}")
print(f"switch        : {s}")
print(f"switch Back   : {sb}")
print(f"decrypt text  : {de}")
