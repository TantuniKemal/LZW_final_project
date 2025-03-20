from lv4tools import *
from LZW import *
import os
from PIL import Image
import numpy as np
from collections import Counter
import math

def compute_entropy(pixel_values):
    counts = Counter(pixel_values)
    total = len(pixel_values)
    entropy = 0.0
    for val in counts.values():
        p = val / total
        entropy -= p * math.log2(p)
    return entropy

def color_difference(np_img):
    """Calculate color difference between neighboring pixels in R, G, B channels."""
    height, width, _ = np_img.shape
    diff_img = np.zeros_like(np_img, dtype=np.uint8)

    for i in range(3):  # For R, G, B channels
        for y in range(height):
            for x in range(width - 1):  # Calculate horizontal color difference
                diff_img[y, x, i] = abs(int(np_img[y, x, i]) - int(np_img[y, x + 1, i]))

        for y in range(height - 1):  # Calculate vertical color difference
            for x in range(width):
                diff_img[y, x, i] = max(diff_img[y, x, i], abs(int(np_img[y, x, i]) - int(np_img[y + 1, x, i])))

    return diff_img

def lv5_encode(img_path):
    out_path = "C:\\Users\\eersa\\PycharmProjects\\TaskSP\\project5\\pythonProject24141\\lv5DiffCompressed.bin"
    img = readPILimg(img_path)
    np_img = PIL2np(img)

    height, width, _ = np_img.shape
    compressed_data = {}
    lzw = LZWCoding(img_path, "text")

    entropy_values = {}

    with open(out_path, 'wb') as out_file:
        out_file.write(height.to_bytes(4, 'big'))  # Yükseklik
        out_file.write(width.to_bytes(4, 'big'))  # Genişlik

        for i, comp in enumerate("RGB"):
            # Apply color difference
            channel = color_difference(np_img)[:, :, i].flatten()  # Apply color difference
            channel_string = "".join(map(chr, channel))
            encoded_as_int = lzw.encode(channel_string)

            encoded_binary = lzw.int_list_to_binary_string(encoded_as_int)
            encoded_binary = lzw.add_code_length_info(encoded_binary)
            padded_encoded_binary = lzw.pad_encoded_data(encoded_binary)
            byte_arr = lzw.get_byte_array(padded_encoded_binary)

            out_file.write(len(byte_arr).to_bytes(4, 'big'))  # Bileşen boyutunu kaydet
            out_file.write(bytes(byte_arr))  # Sıkıştırılmış veriyi yaz

            compressed_data[comp] = len(byte_arr)
            entropy_values[comp] = compute_entropy(channel)

    original_size = height * width * 3  # RGB toplam boyut
    average_code_length = lzw.codelength
    compressed_size = os.path.getsize(out_path)

    if compressed_size == 0:
        compression_ratio = 0
    else:
        compression_ratio = original_size / compressed_size

    print(f"Original size (bytes): {original_size}")
    print(f"Compressed size (bytes): {compressed_size}")

    stats = {
        "Entropy (R)": entropy_values['R'],
        "Entropy (G)": entropy_values['G'],
        "Entropy (B)": entropy_values['B'],
        "Average code length": average_code_length,
        "Input size": original_size,
        "Compressed size": compressed_size,
        "Compressed ratio": compression_ratio
    }

    stats_text = "\n".join([f"{key}: {value}" for key, value in stats.items()])
    return stats_text, out_path

def lv5_decode(file_path):
    compressed_file = file_path
    if not os.path.exists(compressed_file):
        print("Compressed file NOT found!")
        return None

    with open(compressed_file, "rb") as file:
        height = int.from_bytes(file.read(4), 'big')
        width = int.from_bytes(file.read(4), 'big')

        decompressed_channels = []
        lzw = LZWCoding(compressed_file, "text")

        for _ in "RGB":
            size = int.from_bytes(file.read(4), 'big')
            compressed_data = file.read(size)

            bit_string = "".join(format(byte, "08b") for byte in compressed_data)
            bit_string = lzw.remove_padding(bit_string)
            bit_string = lzw.extract_code_length_info(bit_string)

            decoded_ints = lzw.binary_string_to_int_list(bit_string)
            decoded_string = lzw.decode(decoded_ints)
            decoded_pixels = [ord(ch) for ch in decoded_string]
            channel_array = np.array(decoded_pixels, dtype=np.uint8).reshape(height, width)
            decompressed_channels.append(channel_array)

    reconstructed_img = np.stack(decompressed_channels, axis=-1)
    final_img = Image.fromarray(reconstructed_img, mode="RGB")
    final_img.save("lv5_rgb_diff_decompressed.bmp")

    stats = {
        "decompressed_img": "lv5_rgb_diff_decompressed.bmp"
    }

    return stats, final_img

if __name__ == '__main__':
    image_path = "C:\\Users\\eersa\\PycharmProjects\\TaskSP\\project5\\pythonProject24141\\thumbs_up.bmp"
    file_path = "C:\\Users\\eersa\\PycharmProjects\\TaskSP\\project5\\pythonProject24141\\lv5DiffCompressed.bin"
    comp_stats, out_path= lv5_encode(image_path)
    print(comp_stats)

    print("\nDecoding...")
    decomp_stats, img = lv5_decode(file_path)
    print(decomp_stats)
