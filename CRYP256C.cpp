#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <iomanip>
#include <cstring>
#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <iomanip>
#include <algorithm>
#include <cstring>
#include <cstdint>


uint32_t left_rotate(uint32_t n, uint32_t b) {
    return ((n << b) | (n >> (32 - b))) & 0xffffffff;
}


std::string sha640(const std::string& data) {
    uint32_t h0 = 0x67452301;
    uint32_t h1 = 0xEFCDAB89;
    uint32_t h2 = 0x98BADCFE;
    uint32_t h3 = 0x10325476;
    uint32_t h4 = 0xC3D2E1F0;
    uint32_t h5 = 0x76543210;
    uint32_t h6 = 0xFEDCBA98;
    uint32_t h7 = 0x89ABCDEF;
    uint32_t h8 = 0x01234567;
    uint32_t h9 = 0x3C2D1E0F;

    uint64_t original_byte_len = data.size();
    uint64_t original_bit_len = original_byte_len * 8;

    std::vector<uint8_t> padded_data(data.begin(), data.end());
    padded_data.push_back(0x80);

    while ((padded_data.size() * 8) % 1024 != 896) {
        padded_data.push_back(0x00);
    }

    for (int k = 7; k >= 0; --k) {
        padded_data.push_back(static_cast<uint8_t>((original_bit_len >> (k * 8)) & 0xff));
    }

    for (size_t chunk_offset = 0; chunk_offset < padded_data.size(); chunk_offset += 128) {
        uint32_t w[160] = { 0 };
        for (int j = 0; j < 16; ++j) {
            w[j] = (padded_data[chunk_offset + j * 4] << 24) |
                (padded_data[chunk_offset + j * 4 + 1] << 16) |
                (padded_data[chunk_offset + j * 4 + 2] << 8) |
                (padded_data[chunk_offset + j * 4 + 3]);
        }

        for (int j = 16; j < 160; ++j) {
            w[j] = left_rotate(w[j - 6] ^ w[j - 16] ^ w[j - 29] ^ w[j - 30], 1);
        }

        uint32_t a = h0, b = h1, c = h2, d = h3, e = h4;
        uint32_t f = h5, g = h6, h = h7, i = h8, j = h9;

        for (int k = 0; k < 160; ++k) {
            uint32_t func, constant;
            if (k <= 39) {
                func = (b & c) | ((~b) & d);
                constant = 0x5A827999;
            }
            else if (k <= 79) {
                func = b ^ c ^ d;
                constant = 0x6ED9EBA1;
            }
            else if (k <= 119) {
                func = (b & c) | (b & d) | (c & d);
                constant = 0x8F1BBCDC;
            }
            else {
                func = b ^ c ^ d;
                constant = 0xCA62C1D6;
            }

            uint32_t temp = (left_rotate(a, 5) + func + e + constant + w[k]) & 0xffffffff;
            e = d;
            d = c;
            c = left_rotate(b, 30);
            b = a;
            a = temp;

            temp = (left_rotate(f, 5) + func + j + constant + w[k]) & 0xffffffff;
            j = i;
            i = h;
            h = left_rotate(g, 30);
            g = f;
            f = temp;
        }

        h0 = (h0 + a) & 0xffffffff;
        h1 = (h1 + b) & 0xffffffff;
        h2 = (h2 + c) & 0xffffffff;
        h3 = (h3 + d) & 0xffffffff;
        h4 = (h4 + e) & 0xffffffff;
        h5 = (h5 + f) & 0xffffffff;
        h6 = (h6 + g) & 0xffffffff;
        h7 = (h7 + h) & 0xffffffff;
        h8 = (h8 + i) & 0xffffffff;
        h9 = (h9 + j) & 0xffffffff;
    }

    std::stringstream ss;
    ss << std::hex << std::setfill('0');
    ss << std::setw(8) << h0 << std::setw(8) << h1 << std::setw(8) << h2 << std::setw(8) << h3
        << std::setw(8) << h4 << std::setw(8) << h5 << std::setw(8) << h6 << std::setw(8) << h7
        << std::setw(8) << h8 << std::setw(8) << h9;
    return ss.str();
}



class CRYP256 {
public:
    CRYP256() {
        key = "";
        switch_ = {
            0x38, 0x39, 0x3a, 0x3b, 0x0c, 0x0d, 0x0e, 0x0f, 0x3c, 0x3d, 0x3e, 0x3f, 0x28, 0x29, 0x2a, 0x2b,
            0x2c, 0x2d, 0x2e, 0x2f, 0x30, 0x31, 0x32, 0x33, 0x08, 0x09, 0x0a, 0x0b, 0x74, 0x75, 0x76, 0x77,
            0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17,
            0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x18, 0x19, 0x1a, 0x1b, 0x1c, 0x1d, 0x1e, 0x1f,
            0x34, 0x35, 0x36, 0x37, 0x70, 0x71, 0x72, 0x73, 0xe0, 0xe1, 0xe2, 0xe3, 0xe4, 0xe5, 0xe6, 0xe7,
            0xc8, 0xc9, 0xca, 0xcb, 0xcc, 0xcd, 0xce, 0xcf, 0xe8, 0xe9, 0xea, 0xeb, 0xec, 0xed, 0xee, 0xef,
            0xd0, 0xd1, 0xd2, 0xd3, 0xd4, 0xd5, 0xd6, 0xd7, 0xb0, 0xb1, 0xb2, 0xb3, 0xb4, 0xb5, 0xb6, 0xb7,
            0xf0, 0xf1, 0xf2, 0xf3, 0xf4, 0xf5, 0xf6, 0xf7, 0xf8, 0xf9, 0xfa, 0xfb, 0xfc, 0xfd, 0xfe, 0xff,
            0xb8, 0xb9, 0xba, 0xbb, 0xbc, 0xbd, 0xbe, 0xbf, 0x88, 0x89, 0x8a, 0x8b, 0x8c, 0x8d, 0x8e, 0x8f,
            0xd8, 0xd9, 0xda, 0xdb, 0xdc, 0xdd, 0xde, 0xdf, 0x78, 0x79, 0x7a, 0x7b, 0x7c, 0x7d, 0x7e, 0x7f,
            0x50, 0x51, 0x52, 0x53, 0x54, 0x55, 0x56, 0x57, 0x60, 0x61, 0x62, 0x63, 0x64, 0x65, 0x66, 0x67,
            0x90, 0x91, 0x92, 0x93, 0x94, 0x95, 0x96, 0x97, 0x68, 0x69, 0x6a, 0x6b, 0x6c, 0x6d, 0x6e, 0x6f,
            0x98, 0x99, 0x9a, 0x9b, 0x9c, 0x9d, 0x9e, 0x9f, 0x80, 0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87,
            0xa8, 0xa9, 0xaa, 0xab, 0xac, 0xad, 0xae, 0xaf, 0xc0, 0xc1, 0xc2, 0xc3, 0xc4, 0xc5, 0xc6, 0xc7,
            0x58, 0x59, 0x5a, 0x5b, 0x5c, 0x5d, 0x5e, 0x5f, 0x48, 0x49, 0x4a, 0x4b, 0x4c, 0x4d, 0x4e, 0x4f,
            0x40, 0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47, 0xa0, 0xa1, 0xa2, 0xa3, 0xa4, 0xa5, 0xa6, 0xa7
        };
    }

    void make_keys() {
        std::string k = key;
        for (int i = 0; i < 5; ++i) {
            k = sha640(k);
            keys.push_back(k);
        }
    }

    std::vector<uint8_t> switch_the_switch() {
        std::vector<uint8_t> key_ints;
        for (size_t i = 0; i < key.length(); i += 2) {
            key_ints.push_back(std::stoi(key.substr(i, 2), nullptr, 16));
        }

        std::vector<uint8_t> mixed_switch = switch_;
        size_t key_len = key_ints.size();

        for (size_t i = 0; i < mixed_switch.size(); ++i) {
            size_t swap_with = key_ints[i % key_len] % mixed_switch.size();
            std::swap(mixed_switch[i], mixed_switch[swap_with]);
        }

        return mixed_switch;
    }

    std::vector<uint8_t> switch_bytes(const std::vector<uint8_t>& input_bytes) {
        std::vector<uint8_t> output_bytes;
        for (auto byte : input_bytes) {
            output_bytes.push_back(switch_[byte]);
        }
        return output_bytes;
    }

    std::vector<uint8_t> reverse_switch_bytes(const std::vector<uint8_t>& input_bytes) {
        std::vector<uint8_t> reverse_switch(256);
        for (size_t i = 0; i < switch_.size(); ++i) {
            reverse_switch[switch_[i]] = i;
        }

        std::vector<uint8_t> output_bytes;
        for (auto byte : input_bytes) {
            output_bytes.push_back(reverse_switch[byte]);
        }
        return output_bytes;
    }

    std::vector<uint8_t> xor_gate(const std::vector<uint8_t>& message) {
        std::vector<uint8_t> encrypted_message;
        size_t key_length = key.length();
        for (size_t i = 0; i < message.size(); ++i) {
            encrypted_message.push_back(message[i] ^ key[i % key_length]);
        }
        return encrypted_message;
    }

    void encrypt_file() {
        std::ifstream file(filename, std::ios::binary);
        std::vector<uint8_t> data((std::istreambuf_iterator<char>(file)), std::istreambuf_iterator<char>());
        file.close();

        key = keys[0];
        auto enc = xor_gate(data);
        enc = switch_bytes(enc);

        key = keys[1];
        enc = xor_gate(enc);
        enc = switch_bytes(enc);

        key = keys[2];
        enc = xor_gate(enc);
        enc = switch_bytes(enc);

        key = keys[3];
        enc = xor_gate(enc);
        enc = switch_bytes(enc);

        key = keys[4];
        enc = xor_gate(enc);
        enc = switch_bytes(enc);

        std::ofstream out_file(filename, std::ios::binary);
        out_file.write(reinterpret_cast<char*>(enc.data()), enc.size());
        out_file.close();

        std::string new_filename = filename + ".CRYP256";
        int output = rename(filename.c_str(), new_filename.c_str());
    }

    void decrypt_file() {
        std::ifstream file(filename, std::ios::binary);
        std::vector<uint8_t> data((std::istreambuf_iterator<char>(file)), std::istreambuf_iterator<char>());
        file.close();

        key = keys[4];
        auto dec = reverse_switch_bytes(data);
        dec = xor_gate(dec);

        key = keys[3];
        dec = reverse_switch_bytes(dec);
        dec = xor_gate(dec);

        key = keys[2];
        dec = reverse_switch_bytes(dec);
        dec = xor_gate(dec);

        key = keys[1];
        dec = reverse_switch_bytes(dec);
        dec = xor_gate(dec);

        key = keys[0];
        dec = reverse_switch_bytes(dec);
        dec = xor_gate(dec);

        std::ofstream out_file(filename, std::ios::binary);
        out_file.write(reinterpret_cast<char*>(dec.data()), dec.size());
        out_file.close();

        std::string new_filename = filename.substr(0, filename.find(".CRYP256"));
        int output = rename(filename.c_str(), new_filename.c_str());
    }

    void args_start(int argc, char* argv[]) {
        if (argc != 3) {
            std::cerr << "Usage: sudo ./CRYP256 <filename/.txt/.png/.jpg> <key/sha640>" << std::endl;
            std::cerr << "Example: sudo ./CRYP256 cat.png 3f307c4a23b754bc8e6f4a119ca4558e0e06d99287810e175ed870cea26fccd2b1354a4b49303a10" << std::endl;
            exit(1);
        }

        filename = argv[1];
        key = sha640(argv[2]);
        switch_ = switch_the_switch();
        make_keys();

        if (filename.find(".CRYP256") != std::string::npos) {
            decrypt_file();
        }
        else {
            encrypt_file();
        }
    }

private:
    std::string key;
    std::vector<std::string> keys;
    std::vector<uint8_t> switch_;
    std::string filename;
};


int main(int argc, char* argv[]) {
    CRYP256 cryp256;
    cryp256.args_start(argc, argv);
    return 0;
}
