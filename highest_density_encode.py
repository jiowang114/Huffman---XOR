# file_to_dna.py
import argparse

# 2bit <-> 碱基映射表
bit2dna = {
    '00': 'A',
    '01': 'T',
    '10': 'C',
    '11': 'G'
}

dna2bit = {v: k for k, v in bit2dna.items()}

# -----------------------------
# Encode: 文件 -> DNA
# -----------------------------
def file_to_dna(input_file, output_file):
    dna_seq = []

    with open(input_file, 'rb') as f:
        byte_data = f.read()
        print("字节数：", len(byte_data))

    for byte in byte_data:
        bits = format(byte, '08b')  # 8位二进制
        for i in range(0, 8, 2):
            dna_seq.append(bit2dna[bits[i:i+2]])

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(''.join(dna_seq))

    print(f"编码完成，共生成 {len(dna_seq)} nt")

# -----------------------------
# Decode: DNA -> 文件
# -----------------------------
def dna_to_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        dna_seq = f.read().replace('\n','').strip()
        print("碱基数：", len(dna_seq))

    byte_list = []
    for i in range(0, len(dna_seq), 4):
        bits = ''
        for base in dna_seq[i:i+4]:
            bits += dna2bit[base]
        byte_list.append(int(bits, 2))

    with open(output_file, 'wb') as f:
        f.write(bytes(byte_list))

    print(f"解码完成，还原字节数：{len(byte_list)}")

# -----------------------------
# 命令行接口
# -----------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="文件 <-> DNA 编码/解码（2bit → 碱基）")
    subparsers = parser.add_subparsers(dest='command')

    # Encode
    encode_parser = subparsers.add_parser('encode', help="将文件编码为 DNA")
    encode_parser.add_argument('input_file', help="输入文件路径")
    encode_parser.add_argument('output_file', help="输出 DNA 文件路径")

    # Decode
    decode_parser = subparsers.add_parser('decode', help="将 DNA 解码回原文件")
    decode_parser.add_argument('input_file', help="输入 DNA 文件路径")
    decode_parser.add_argument('output_file', help="输出原始文件路径")

    args = parser.parse_args()

    if args.command == 'encode':
        file_to_dna(args.input_file, args.output_file)
    elif args.command == 'decode':
        dna_to_file(args.input_file, args.output_file)
    else:
        parser.print_help()
