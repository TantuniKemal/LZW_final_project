from lv4tools import *
from LZW import *
import os
from PIL import Image
import numpy as np
from collections import Counter

def compute_entropy(pixel_values):
      # For counting occurrences of each pixel value
    counts = Counter(pixel_values)  # Count how many times each pixel value appears
    total = len(pixel_values)  # Total number of pixels
    entropy = 0.0  # Initialize entropy to zero
    for val in counts.values():  # Go through each unique pixel count
        p = val / total  # Probability of this pixel
        entropy -= p * math.log2(p)  # Subtract p*log2(p) from entropy
    return entropy  # Return the final entropy value

def lv4_encode(img_path):
    #path to the output file
    out_path = "C:\\Users\\eersa\\PycharmProjects\\TaskSP\\project5\\pythonProject24141\\lv4Compressed.bin"

    img = readPILimg(img_path)  # read img
    np_img = PIL2np(img)  # convert to the img to a np arr

    height, width, _ = np_img.shape  # taking size of img

    compressed_data = {}  # dict to store compressed data
    lzw = LZWCoding(img_path, "text")

    #dict for entropy value for R G B
    entropy_values = {}

    # open the output file for writing
    with open(out_path, 'wb') as out_file:
        out_file.write(height.to_bytes(4, 'big'))  # height
        out_file.write(width.to_bytes(4, 'big'))  # width

        for i, comp in enumerate("RGB"):  # process each color channel (R, G ,B)
            # flatten the color channel and convert to a string
            channel = np_img[:, :, i].flatten()
            channel_string = "".join(map(chr, channel))
            #perform LZW encoding on the channel string
            encoded_as_int = lzw.encode(channel_string)
            #convert the encoded int to a binary string
            encoded_binary = lzw.int_list_to_binary_string(encoded_as_int)
            #add code length and pad the encoded data
            encoded_binary = lzw.add_code_length_info(encoded_binary)
            padded_encoded_binary = lzw.pad_encoded_data(encoded_binary)
            # convert the padded binary data to byte arr
            byte_arr = lzw.get_byte_array(padded_encoded_binary)
            # write the length of encoded data and the data itself to the output
            out_file.write(len(byte_arr).to_bytes(4, 'big'))  # write size of the component
            out_file.write(bytes(byte_arr))

            #store the siz of each compressed component int the dict
            compressed_data[comp] = len(byte_arr)
            # again for each store entropy value
            entropy_values[comp] = compute_entropy(channel)

    #compute original size of the img
    original_size = height * width * 3  # RGB toplam boyut
    # get the average code length
    average_code_length = lzw.codelength
    #get compreseed szie of the output file
    compressed_size = os.path.getsize(out_path)

    if compressed_size == 0:
        compression_ratio = 0
    else:
        # calculate ratio
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
    return stats_text,  out_path


def lv4_decode(file_path):
    #path compressed file
    compressed_file = file_path
    if not os.path.exists(compressed_file):
        print("Compressed file NOT found!")
        return None

    # open the compreseed file for reading in rb
    with open(compressed_file, "rb") as file:
        # read the height and width of the image from the file
        height = int.from_bytes(file.read(4), 'big')
        width = int.from_bytes(file.read(4), 'big')

        #list to store decompreseed color channel
        decompressed_channels = []
        # create LZW class object
        lzw = LZWCoding(compressed_file, "text")

        for _ in "RGB":
            #read size of the compressed data for current channel
            size = int.from_bytes(file.read(4), 'big')  # read component size
            compressed_data = file.read(size)  # readt actual compressed data size

            #convert the compressed data to a binary string
            bit_string = "".join(format(byte, "08b") for byte in compressed_data)
            #remove any padding added during encoding
            bit_string = lzw.remove_padding(bit_string)
            #extract code length info
            bit_string = lzw.extract_code_length_info(bit_string)

            #convert the binary string back to a list of int
            decoded_ints = lzw.binary_string_to_int_list(bit_string)
            # decode the int to get orginal string of pixel values
            decoded_string = lzw.decode(decoded_ints)
            # convert the decoded str of characters to their pixel values
            decoded_pixels = [ord(ch) for ch in decoded_string]
            #reshape the decoded pixels into the original img channel shape
            channel_array = np.array(decoded_pixels, dtype=np.uint8).reshape(height, width)
            #append the decompreseed channel to the list
            decompressed_channels.append(channel_array)

    # stact the decompressed channel ( R, G , B ) to reconstruct the img
    reconstructed_img = np.stack(decompressed_channels, axis=-1)  # R, G, B stack
    final_img = Image.fromarray(reconstructed_img, mode="RGB") # creat a PIL img
    final_img.save("lv4_rgb_decompressed.bmp") # save the  decompressed img

    stats = {
        "decompressed_img": "lv4_rgb_decompressed.bmp"}

    return  stats, final_img


if __name__ == '__main__':
    image_path = "C:\\Users\\eersa\\PycharmProjects\\TaskSP\\project5\\pythonProject24141\\thumbs_up.bmp"
    file_path = "C:\\Users\\eersa\\PycharmProjects\\TaskSP\\project5\\pythonProject24141\\lv4Compressed.bin"
    comp_stats, outpath = lv4_encode(image_path)
    print(comp_stats)

    print("\nDecoding...")
    decomp_stats, img = lv4_decode(file_path)
    print(decomp_stats)