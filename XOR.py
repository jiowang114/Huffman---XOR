import random
import argparse

# -----------------------------
# Base <-> Value mapping
# -----------------------------
BASE_TO_VAL = {'A': 0, 'T': 1, 'G': 2, 'C': 3}
VAL_TO_BASE = {v: k for k, v in BASE_TO_VAL.items()}

# -----------------------------
# File read / write
# -----------------------------
def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().replace('\n','').strip()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

# -----------------------------
# Pseudo-random DNA generator
# -----------------------------
def generate_random_dna(length, seed):
    random.seed(seed)
    bases = ['A','T','G','C']
    return ''.join(random.choices(bases, k=length))

# -----------------------------
# XOR operation (encode)
# -----------------------------
def encode_xor(dna_seq, random_seq):
    return ''.join(VAL_TO_BASE[(BASE_TO_VAL[s]+BASE_TO_VAL[r])%4] for s,r in zip(dna_seq, random_seq))

# XOR operation (decode)
def decode_xor(xor_seq, random_seq):
    # 使用减法 mod 4 还原原序列
    return ''.join(VAL_TO_BASE[(BASE_TO_VAL[x] - BASE_TO_VAL[r])%4] for x,r in zip(xor_seq, random_seq))

# -----------------------------
# Encode / Decode
# -----------------------------
def encode_file(input_file, output_file, seed):
    dna_seq = read_file(input_file)
    random_seq = generate_random_dna(len(dna_seq), seed)
    xor_seq = encode_xor(dna_seq, random_seq)
    write_file(output_file, xor_seq)
    print(f"Encoded XOR DNA saved to {output_file} (seed={seed})")

def decode_file(xor_file, output_file, seed):
    xor_seq = read_file(xor_file)
    random_seq = generate_random_dna(len(xor_seq), seed)
    original_seq = decode_xor(xor_seq, random_seq)
    write_file(output_file, original_seq)
    print(f"Decoded DNA saved to {output_file} (seed={seed})")

# -----------------------------
# Main CLI
# -----------------------------
def main():
    parser = argparse.ArgumentParser(description="DNA XOR Encoder/Decoder (reversible)")
    subparsers = parser.add_subparsers(dest='command')

    # Encode
    encode_parser = subparsers.add_parser('encode')
    encode_parser.add_argument('input_file')
    encode_parser.add_argument('--output_file', default='encoded.xor.dna')
    encode_parser.add_argument('--seed', type=int, default=0, help="Random seed for reproducible XOR")

    # Decode
    decode_parser = subparsers.add_parser('decode')
    decode_parser.add_argument('xor_file')
    decode_parser.add_argument('--output_file', default='decoded.dna')
    decode_parser.add_argument('--seed', type=int, required=True, help="Same seed used during encode")

    args = parser.parse_args()

    if args.command=='encode':
        encode_file(args.input_file, args.output_file, args.seed)
    elif args.command=='decode':
        decode_file(args.xor_file, args.output_file, args.seed)
    else:
        parser.print_help()

if __name__=="__main__":
    main()
