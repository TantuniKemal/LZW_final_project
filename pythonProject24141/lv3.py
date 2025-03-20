import numpy as np
from PIL import Image
import os
from LZW import LZWCoding
import math

def compute_entropy(pixel_values):

    from collections import Counter  # For counting occurrences of each pixel value
    counts = Counter(pixel_values)  # Count how many times each pixel value appears
    total = len(pixel_values)  # Total number of pixels
    entropy = 0.0  # Initialize entropy to zero
    for val in counts.values():  # Go through each unique pixel count
        p = val / total  # Probability of this pixel
        entropy -= p * math.log2(p)  # Subtract p*log2(p) from entropy
    return entropy  # Return the final entropy value

def readPILimg(img_path):
    return Image.open(img_path)

def color2gray(img):
    return img.convert("L")  # Gri tonlamaya çevir

def PIL2np(img):
    return np.array(img, dtype=np.uint8)

def grayscale_difference(np_gray):
    """Görüntüde yatay ve dikey komşu piksellerin farkını alır."""
    height, width = np_gray.shape
    diff_gray = np.zeros((height, width), dtype=np.uint8)

    for y in range(height):
        for x in range(width - 1):  # Sağ komşu farkı
            diff_gray[y, x] = abs(int(np_gray[y, x]) - int(np_gray[y, x + 1]))

    for y in range(height - 1):  # Alt komşu farkı
        for x in range(width):
            diff_gray[y, x] = max(diff_gray[y, x], abs(int(np_gray[y, x]) - int(np_gray[y + 1, x])))

    return diff_gray

def lv3_encode(img_path):
    out_path = "lv3DiffCompressed.bin"
    img = readPILimg(img_path)
    img = color2gray(img)
    np_gray = PIL2np(img)

    height, width = np_gray.shape
    diff_gray = grayscale_difference(np_gray)

    # 1D diziye çevir
    flat_gray = diff_gray.flatten()
    gray_string = "".join(map(chr, flat_gray))

    # LZW sıkıştırma
    lzw = LZWCoding("thumbs_up.bmp", "text")
    encode_gray_as_int = lzw.encode(gray_string)

    encode_img = lzw.int_list_to_binary_string(encode_gray_as_int)
    encode_img = lzw.add_code_length_info(encode_img)
    padded_encode_img = lzw.pad_encoded_data(encode_img)
    byte_arr = lzw.get_byte_array(padded_encode_img)

    # Sıkıştırılmış veriyi dosyaya yaz
    with open(out_path, 'wb') as out_file:
        out_file.write(bytes(byte_arr))

    # Sıkıştırma istatistikleri
    entropy=compute_entropy(flat_gray)
    original_size = len(flat_gray)
    average_code_length = lzw.codelength
    compressed_size = os.path.getsize(out_path)

    if compressed_size == 0:
        compression_ratio = 0
    else:
        # Calculate how many times smaller the compressed file is
        compression_ratio = original_size / compressed_size

    stats = {
        "Entropy": entropy,
        "Average code length": average_code_length,
        "Input size": original_size,
        "Compressed size": compressed_size,
        "Compressed ratio": compression_ratio
    }
    stats_text = "\n".join([f"{key}: {value}" for key, value in stats.items()])
    return stats_text, out_path  # Return the statistics

def lv3_decode(file_path):
    compressed_file = file_path
    if not os.path.exists(compressed_file):
        print("Compressed file NOT found!")
        return None

    with open(compressed_file, "rb") as file:
        encode_bytes = file.read()

    lzw = LZWCoding("thumbs_up.bmp", "text")
    bit_string = "".join(format(byte, "08b") for byte in encode_bytes)
    bit_string = lzw.remove_padding(bit_string)
    bit_string = lzw.extract_code_length_info(bit_string)

    bit2int = lzw.binary_string_to_int_list(bit_string)
    decode_img = lzw.decode(bit2int)

    original_img = Image.open("thumbs_up.bmp")
    width, height = original_img.size

    # Piksel değerlerini geri al
    convert_pixels = [ord(ch) for ch in decode_img]
    convert_array = np.array(convert_pixels, dtype=np.uint8).reshape(height, width)

    # Görüntüyü kaydet
    convert_img = Image.fromarray(convert_array, mode="L")
    convert_img.save("lv3_diff_gray_decompression.bmp")

    stats = {
        "decompressed_img": "lv3_diff_gray_decompression.bmp"
    }
    return stats, convert_img

if __name__ == '__main__':
    image_path = "thumbs_up.bmp"
    file_path = "C:\\Users\\eersa\\PycharmProjects\\TaskSP\\project5\\pythonProject24141\\lv3DiffCompressed.bin"
    compstats, out_path = lv3_encode(image_path)
    print("Compression Stats:", compstats)

    print("\nDecompressing...\n")
    decomp = lv3_decode(file_path)
    print("Decompression Stats:", decomp)
