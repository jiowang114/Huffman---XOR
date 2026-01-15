# 在命令行运行
# Huffman最好输入中文文件
# Usage example：

PS F:> python huffman_Code.py compress .\Original.txt .\Original.txt.huf
[OK] Compressed -> .\Original.txt.huf

PS F:> python highest_density_encode.py encode .\Original.txt.huf .\Original.txt.dna
字节数： 2701
编码完成，共生成 10804 nt

PS F:> python .\XOR.py encode .\Original.txt.dna --output_file .\Original_xor.dna --seed 0
Encoded XOR DNA saved to .\Original_xor.dna (seed=0)

PS F:> python .\XOR.py decode .\Original_xor.dna --output_file .\Original_xor_decode.dna --seed 0
Decoded DNA saved to .\Original_xor_decode.dna (seed=0)
