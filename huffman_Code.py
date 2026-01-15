import sys
import heapq
import pickle
from collections import Counter


# -----------------------------
# Huffman Tree Node
# -----------------------------
class Node:
    def __init__(self, value=None, freq=0):
        self.value = value
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


# -----------------------------
# Build Huffman Tree
# -----------------------------
def build_huffman_tree(freq_dict):
    heap = [Node(v, f) for v, f in freq_dict.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        a = heapq.heappop(heap)
        b = heapq.heappop(heap)
        parent = Node(freq=a.freq + b.freq)
        parent.left = a
        parent.right = b
        heapq.heappush(heap, parent)

    return heap[0]


# -----------------------------
# Generate Huffman Codes
# -----------------------------
def generate_codes(node, prefix="", codebook=None):
    if codebook is None:
        codebook = {}

    if node.value is not None:
        codebook[node.value] = prefix
        return codebook

    generate_codes(node.left, prefix + "0", codebook)
    generate_codes(node.right, prefix + "1", codebook)
    return codebook


# -----------------------------
# Bit packing
# -----------------------------
def bits_to_bytes(bitstring):
    padding = (8 - len(bitstring) % 8) % 8
    bitstring += "0" * padding

    out = bytearray()
    for i in range(0, len(bitstring), 8):
        out.append(int(bitstring[i:i+8], 2))

    return bytes(out), padding


# -----------------------------
# Compression
# -----------------------------
def huffman_compress(input_path, output_path):
    with open(input_path, "rb") as f:
        data = f.read()

    freq = Counter(data)
    tree = build_huffman_tree(freq)
    codebook = generate_codes(tree)

    bitstring = "".join(codebook[b] for b in data)
    bit_len = len(bitstring)

    compressed, _ = bits_to_bytes(bitstring)

    with open(output_path, "wb") as f:
        table = pickle.dumps(codebook)
        f.write(len(table).to_bytes(4, "big"))
        f.write(table)
        f.write(bit_len.to_bytes(4, "big"))
        f.write(compressed)

    print(f"[OK] Compressed -> {output_path}")


# -----------------------------
# Decompression
# -----------------------------
def huffman_decompress(input_path, output_path):
    with open(input_path, "rb") as f:
        table_size = int.from_bytes(f.read(4), "big")
        codebook = pickle.loads(f.read(table_size))
        bit_len = int.from_bytes(f.read(4), "big")
        compressed_data = f.read()

    reverse = {v: k for k, v in codebook.items()}

    bitstring = "".join(f"{b:08b}" for b in compressed_data)
    bitstring = bitstring[:bit_len]

    decoded = bytearray()
    buf = ""
    for bit in bitstring:
        buf += bit
        if buf in reverse:
            decoded.append(reverse[buf])
            buf = ""

    with open(output_path, "wb") as f:
        f.write(decoded)

    print(f"[OK] Decompressed -> {output_path}")


# -----------------------------
# CLI
# -----------------------------
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage:")
        print("  python huffman.py compress   input.bin output.huf")
        print("  python huffman.py decompress input.huf output.bin")
        sys.exit(1)

    mode, inp, out = sys.argv[1:]

    if mode == "compress":
        huffman_compress(inp, out)
    elif mode == "decompress":
        huffman_decompress(inp, out)
    else:
        print("Mode must be: compress | decompress")
