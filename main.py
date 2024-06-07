import os
import threading


i = 0


def inc(stri):
    global i

    i += 1
    os.system(stri)
    i -= 1

for root, dirs, files in os.walk("."):
    for file in files:

        if file == "CRYP256.py" or file == "main.py":
            pass
        else:
            while (i > 5): pass

            #   print(f'python CRYP256.py "{file}" 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8')
            # threading.Thread(target=lambda: inc(f'python CRYP256.py "{file}" 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8')).start()
            inc(f'python CRYP256.py "{file}" 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8')
            
            if file.endswith(".CRYP256"):
                print(f"{file} :: DecryptFile")
            else:
                print(f"{file} :: EncryptFile")