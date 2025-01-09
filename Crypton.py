import numpy as np

Sbox = [
    [0xb1, 0x76, 0xac, 0x55, 0xed, 0x47, 0x33, 0x60, 0x9b, 0x1e, 0xa, 0xff, 0x89, 0x22, 0xd4, 0xc8],
    [0x9d, 0x3c, 0xc6, 0xf7, 0x61, 0x15, 0x78, 0xeb, 0xb0, 0x4f, 0xd2, 0x5e, 0x24, 0x8a, 0x9, 0xa3],
    [0xf6, 0x21, 0xd, 0x99, 0x1c, 0x64, 0x8b, 0x48, 0x53, 0xea, 0xae, 0xb2, 0x35, 0x7f, 0xc7, 0xd0],
    [0xc9, 0x61, 0x97, 0x6, 0x34, 0x2c, 0xef, 0x7a, 0xa2, 0x88, 0x50, 0xd3, 0x11, 0x4b, 0xfd, 0xbe],
    [0x8e, 0x5a, 0x42, 0x70, 0xdf, 0xab, 0xf4, 0x5, 0x27, 0xc1, 0x66, 0x3d, 0xb8, 0x9c, 0xe3, 0x19],
    [0x3a, 0x9e, 0x6f, 0x28, 0xc2, 0x3, 0xb7, 0xa9, 0x74, 0xd6, 0x41, 0x8c, 0xf0, 0x5d, 0x1b, 0xe5],
    [0x7, 0x14, 0xf9, 0xcd, 0x25, 0x31, 0x4a, 0x8f, 0xde, 0x7b, 0xb3, 0xa0, 0x6c, 0xe8, 0x96, 0x52],
    [0x43, 0xdb, 0x80, 0xe2, 0x58, 0xba, 0x1, 0xfc, 0x16, 0x94, 0x37, 0x69, 0xfa, 0xc5, 0x7e, 0x2d],
    [0x72, 0xbf, 0xee, 0x83, 0xaa, 0xd8, 0x95, 0xc4, 0x39, 0xc, 0x1d, 0x26, 0x5b, 0xf1, 0x40, 0x67],
    [0xa4, 0xe7, 0xb5, 0xdc, 0x79, 0x86, 0x6e, 0x32, 0xca, 0x23, 0xfb, 0x8, 0x4d, 0x10, 0x51, 0x9f],
    [0x6b, 0xc3, 0x38, 0x1f, 0x90, 0xfe, 0xa6, 0xbd, 0x1e, 0x57, 0x84, 0x45, 0x2, 0xd9, 0x2a, 0x7c],
    [0x18, 0x0, 0x2b, 0x6a, 0xf3, 0x92, 0xdd, 0x56, 0x4c, 0xb9, 0x75, 0xe4, 0xce, 0xa7, 0x3f, 0x81],
    [0xd5, 0x49, 0x54, 0xa1, 0x87, 0x7d, 0x12, 0x2e, 0xf, 0x30, 0x98, 0xcb, 0xe6, 0x63, 0xbc, 0xfa],
    [0x2f, 0xf2, 0x1a, 0x3b, 0xe, 0xc0, 0x59, 0xd7, 0x85, 0xae, 0xec, 0x71, 0x93, 0xb6, 0x68, 0x44],
    [0xe0, 0xa8, 0x73, 0x4e, 0xbb, 0x5f, 0xcc, 0x91, 0x6d, 0xf5, 0x29, 0x17, 0xda, 0x4, 0x82, 0x36],
    [0x5c, 0x8d, 0xd1, 0xb4, 0x46, 0xe9, 0x20, 0x13, 0xf8, 0x62, 0xcf, 0x9a, 0x77, 0x3e, 0xa5, 0xb]
]


def shift_byte(number, type, n):
    temp = number
    if type == "left":
        for i in range(n):
            temp = temp // 2 ** 7 + temp % 2 ** 7 * 2
        return temp
    else:
        for i in range(n):
            temp = temp // 2 + temp % 2 * 2 ** 7
        return temp


def shift_key(key_bits, shifts_number):
    key_int = int(''.join(map(str, key_bits)), 16)
    new_key = f"{bin(key_int).replace("0b", ""):>032}"
    for i in range(shifts_number):
        new_key = new_key[1:32] + new_key[0]
    key_arr = []
    for i in range(4):
        key_arr.append(f"{hex(int(new_key[i * 8:i * 8 + 8], 2)).replace("0x", ""):>02}")
    return key_arr


S0box = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
S1box = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
S2box = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
S3box = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]

for i in range(16):
    for j in range(16):
        temp = Sbox[i][j]
        S0box[i].append(shift_byte(temp, "left", 1))
        S1box[i].append(shift_byte(temp, "left", 3))
        index = i * 16 + j
        index2 = shift_byte(index, "left", 7)
        index3 = shift_byte(index, "left", 5)
        S2box[i].append(Sbox[index2 // 16][index2 % 16])
        S3box[i].append(Sbox[index3 // 16][index3 % 16])

m0 = 0xfc
m1 = 0xf3
m2 = 0xcf
m3 = 0x3f

M0 = int((str(hex(m3)) + str(hex(m2)) + str(hex(m1)) + str(hex(m0))).replace("0x", ""), 16)
M1 = int((str(hex(m0)) + str(hex(m3)) + str(hex(m2)) + str(hex(m1))).replace("0x", ""), 16)
M2 = int((str(hex(m1)) + str(hex(m0)) + str(hex(m3)) + str(hex(m2))).replace("0x", ""), 16)
M3 = int((str(hex(m2)) + str(hex(m1)) + str(hex(m0)) + str(hex(m3))).replace("0x", ""), 16)


def text_to_byte_box(text):
    Aline = ""
    for i in text:
        Aline += f"{str(hex(ord(i)).replace("0x", "")):>04}"
    while len(Aline) < 32:
        Aline = "0" + Aline
    A = [[], [], [], []]
    for i in range(4):
        for j in range(4):
            A[i].append(Aline[i * 8 + j * 2:i * 8 + j * 2 + 2])
    return A


def byte_box_to_text(A):
    text = ""
    for subA in A:
        for j in range(2):
            if int("0x" + subA[j * 2] + subA[j * 2 + 1], 0) != 0:
                text += chr(int("0x" + subA[j * 2] + subA[j * 2 + 1], 0))
    return text


def pi(A, round):
    B = []

    subA0 = int(''.join(map(str, A[0])), 16)
    subA1 = int(''.join(map(str, A[1])), 16)
    subA2 = int(''.join(map(str, A[2])), 16)
    subA3 = int(''.join(map(str, A[3])), 16)
    if round % 2 == 0:
        subB0 = f"{hex((subA3 & M3) ^ (subA2 & M2) ^ (subA1 & M1) ^ (subA0 & M0)).replace("0x", ""):>08}"
        B.append([subB0[i:i + 2] for i in range(0, len(subB0), 2)])
        subB1 = f"{hex((subA3 & M0) ^ (subA2 & M3) ^ (subA1 & M2) ^ (subA0 & M1)).replace("0x", ""):>08}"
        B.append([subB1[i:i + 2] for i in range(0, len(subB1), 2)])
        subB2 = f"{hex((subA3 & M1) ^ (subA2 & M0) ^ (subA1 & M3) ^ (subA0 & M2)).replace("0x", ""):>08}"
        B.append([subB2[i:i + 2] for i in range(0, len(subB2), 2)])
        subB3 = f"{hex((subA3 & M2) ^ (subA2 & M1) ^ (subA1 & M0) ^ (subA0 & M3)).replace("0x", ""):>08}"
        B.append([subB3[i:i + 2] for i in range(0, len(subB3), 2)])
    else:
        subB0 = f"{hex((subA3 & M1) ^ (subA2 & M0) ^ (subA1 & M3) ^ (subA0 & M2)).replace("0x", ""):>08}"
        B.append([subB0[i:i + 2] for i in range(0, len(subB0), 2)])
        subB1 = f"{hex((subA3 & M2) ^ (subA2 & M1) ^ (subA1 & M0) ^ (subA0 & M3)).replace("0x", ""):>08}"
        B.append([subB1[i:i + 2] for i in range(0, len(subB1), 2)])
        subB2 = f"{hex((subA3 & M3) ^ (subA2 & M2) ^ (subA1 & M1) ^ (subA0 & M0)).replace("0x", ""):>08}"
        B.append([subB2[i:i + 2] for i in range(0, len(subB2), 2)])
        subB3 = f"{hex((subA3 & M0) ^ (subA2 & M3) ^ (subA1 & M2) ^ (subA0 & M1)).replace("0x", ""):>08}"
        B.append([subB3[i:i + 2] for i in range(0, len(subB3), 2)])
    return B


def gamma(A, S0box, S1box, S2box, S3box, round):
    for i in range(4):
        for j in range(4):
            if round % 2 == 0:
                Sindex = (j + 2 + i) % 4
            else:
                Sindex = (j + i) % 4
            match Sindex:
                case 0:
                    S = S0box
                case 1:
                    S = S1box
                case 2:
                    S = S2box
                case 3:
                    S = S3box
            A[i][j] = f"{hex(S[int(A[i][j], 16) // 16][int(A[i][j], 16) % 16]).replace("0x", ""):>02}"
    return A


def tau(A, rot_num):
    return np.rot90(A, k=rot_num).tolist()


def sigma(A, K):
    for i in range(4):
        for j in range(4):
            A[i][j] = f"{hex(int(A[i][j], 16) ^ int(K[i][j], 16)).replace("0x", ""):>02}"
    return A


def round_keys(key_box):
    Kr_null = [["00"] * 4] * 4

    U_box = [[], [], [], []]
    V_box = [[], [], [], []]
    for i in range(4):
        for j in range(4):
            U_box[i].append(key_box[i][j][1])
            V_box[i].append(key_box[i][j][0])
    U_hatch = pi(U_box, 1)
    V_hatch = pi(V_box, 0)
    U_hatch = gamma(U_hatch, S0box, S1box, S2box, S3box, 1)
    V_hatch = gamma(V_hatch, S0box, S1box, S2box, S3box, 0)
    U_hatch = tau(U_hatch, 1)
    V_hatch = tau(V_hatch, 1)
    U_hatch = sigma(U_hatch, Kr_null)
    V_hatch = sigma(V_hatch, Kr_null)

    T0 = [0, 0, 0, 0]
    T1 = [0, 0, 0, 0]
    for i in range(4):
        for j in range(4):
            T0[i] ^= int(U_hatch[i][j], 16)
            T1[i] ^= int(V_hatch[i][j], 16)
    Ke = [[], [], [], [], [], [], [], []]
    for i in range(4):
        for j in range(4):
            Ke[i].append(f"{hex(int(U_hatch[i][j], 16) ^ T1[j]).replace("0x", ""):>02}")
            Ke[i + 4].append(f"{hex(int(V_hatch[i][j], 16) ^ T0[j]).replace("0x", ""):>02}")
    C0 = 0xa54ff53a
    for_Ci = 0x3c6ef372
    Mc0 = 0xacacacac
    Ci = (C0 + for_Ci) % 2 ** 32
    Kr = [[], [], [], [], [], [], [], [], [], [], [], [], []]

    # Формирование нулевого и первого ключа раунда
    for i in range(4):
        Kr[0].append([])
        Kr[1].append([])
        for j in range(4):
            temp = int(Ke[i][j], 16) ^ int(hex(C0).replace("0x", "")[i * 2:i * 2 + 2], 16) ^ int(
                f"{hex(shift_byte(Mc0, "left", i)).replace("0x", ""):>08}"[i * 2:i * 2 + 2], 16)
            Kr[0][i].append(f"{hex(temp).replace("0x", ""):>02}")

            temp = int(Ke[i + 4][j], 16) ^ int(hex(Ci).replace("0x", "")[i * 2:i * 2 + 2], 16) ^ int(
                f"{hex(shift_byte(Mc0, "left", i)).replace("0x", ""):>08}"[i * 2:i * 2 + 2], 16)
            Kr[1][i].append(f"{hex(temp).replace("0x", ""):>02}")

    # Формирование остальных 11 ключей
    for r in range(2, 13):
        Ci = (Ci + for_Ci) % 2 ** 32
        flag_round = r % 2 == 0
        if flag_round:
            Ke[0] = shift_key(Ke[0], 6)
            Ke[3] = shift_key(Ke[0], 6)
        else:
            Ke[4] = shift_key(Ke[0], 2)
            Ke[7] = shift_key(Ke[0], 2)
        for i in range(4):
            if flag_round:
                Ke[1][i] = f"{hex(shift_byte(int(Ke[2][i], 16), "left", 16)).replace("0x", ""):>02}"
                Ke[2][i] = f"{hex(shift_byte(int(Ke[2][i], 16), "left", 24)).replace("0x", ""):>02}"
            else:
                Ke[5][i] = f"{hex(shift_byte(int(Ke[2][i], 16), "left", 8)).replace("0x", ""):>02}"
                Ke[6][i] = f"{hex(shift_byte(int(Ke[2][i], 16), "left", 16)).replace("0x", ""):>02}"
            Kr[r].append([])
            for j in range(4):
                temp = int(Ke[i + flag_round * 4][j], 16) ^ int(hex(Ci).replace("0x", "")[i * 2:i * 2 + 2], 16) ^ int(
                    f"{hex(shift_byte(Mc0, "left", i)).replace("0x", ""):>08}"[i * 2:i * 2 + 2], 16)
                Kr[r][i].append(f"{hex(temp).replace("0x", ""):>02}")
    return Kr


def encrypt(text, key):
    texts = [text[i:i + 8] for i in range(0, len(text), 8)]
    fin_text = ""
    key = key[0:8]
    key_box = text_to_byte_box(key)
    Kr = round_keys(key_box)
    for subtext in texts:
        byte_box = text_to_byte_box(subtext)

        byte_box = sigma(byte_box, Kr[0])
        for i in range(12):
            round = i + 1
            byte_box = pi(byte_box, round)
            # byte_box = gamma(byte_box, S0box, S1box, S2box, S3box, round)
            byte_box = tau(byte_box, 1)
            byte_box = sigma(byte_box, Kr[round])
        byte_box = tau(byte_box, 1)
        byte_box = pi(byte_box, 0)
        byte_box = tau(byte_box, 1)

        fin_text += byte_box_to_text(byte_box)
    return fin_text.encode('utf-8', 'replace').decode()


def decrypt(text, key):
    texts = [text[i:i + 8] for i in range(0, len(text), 8)]
    fin_text = ""
    key = key[0:8]
    key_box = text_to_byte_box(key)
    Kr = round_keys(key_box)
    for subtext in texts:
        byte_box = text_to_byte_box(subtext)

        byte_box = tau(byte_box, -1)
        byte_box = pi(byte_box, 0)
        byte_box = tau(byte_box, -1)
        for i in range(12):
            round = i + 1
            byte_box = sigma(byte_box, Kr[13 - round])
            byte_box = tau(byte_box, -1)
            # byte_box = gamma(byte_box, S0box, S1box, S2box, S3box, round+1)
            byte_box = pi(byte_box, round + 1)
        byte_box = sigma(byte_box, Kr[0])

        fin_text += byte_box_to_text(byte_box)
    return fin_text

