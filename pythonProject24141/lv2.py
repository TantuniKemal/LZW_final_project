from lv4tools import * # some operations tools
from LZW import *   #import LZW class
import math
import os
from PIL import Image # convert array
import numpy as np


def compute_entropy(pixel_values):

    from collections import Counter  # For counting occurrences of each pixel value
    counts = Counter(pixel_values)  # Count how many times each pixel value appears
    total = len(pixel_values)  # Total number of pixels
    entropy = 0.0  # Initialize entropy to zero
    for val in counts.values():  # Go through each unique pixel count
        p = val / total  # Probability of this pixel
        entropy -= p * math.log2(p)  # Subtract p*log2(p) from entropy
    return entropy  # Return the final entropy value

def lv2_encode(img_path):
    #Define the output file path
    out_path = "C:\\Users\\eersa\\PycharmProjects\\TaskSP\\project5\\pythonProject24141\\lv2Compressed.bin"

    #initilazie img with PIL format
    img=readPILimg(img_path)
    img=color2gray(img)

    #Convert the PIL image to a np array
    np_gray=PIL2np(img)
    height, width= np_gray.shape # get dimension

    #convert 1D arr from 2D
    flat_gray=np_gray.flatten() # flatten the grayscale pixels
    gray_string="".join(map(chr, flat_gray)) # convert pixel values to characters and join

    #initialize LZW class for compression
    lzw=LZWCoding("thumbs_up.bmp","text")

    #compress the grayscale data using LZW
    encode_gray_as_int=lzw.encode(gray_string)

    #convert the list of integers obtained from LZW to a binary string
    encode_img=lzw.int_list_to_binary_string(encode_gray_as_int)
    #add code length information to the compressed data
    encode_img=lzw.add_code_length_info(encode_img)
    #pad the data to ensure fixed length
    padded_encode_img=lzw.pad_encoded_data(encode_img)
    #convert to byte arr
    byte_arr=lzw.get_byte_array(padded_encode_img)

    #write the byte arr to the output file
    out_file = open(out_path, 'wb')  # binary mode
    out_file.write(bytes(byte_arr))
    out_file.close()

    #compute entropy
    entropy=compute_entropy(flat_gray)
    average_code_length=lzw.codelength
    original_size=len(flat_gray)
    compressed_size=os.path.getsize(out_path)

    #calculate compression ratio
    if compressed_size == 0:
        compression_ratio = 0
    else:
        # Calculate how many times smaller the compressed file is
        compression_ratio = original_size / compressed_size

    # some print operation to follow
    print(f"Average code length (bits): {average_code_length}")
    print(f"Original size (bytes): {original_size}")
    print(f"Compressed size (bytes): {compressed_size}")

    #collect the statistics in a dictionary
    stats = {
        "Entropy": entropy,
        "Average code length": average_code_length,
        "Input size": original_size,
        "Compressed size": compressed_size,
        "Compressed ratio": compression_ratio
    }
    #combine statistics into a text format
    stats_text = "\n".join([f"{key}: {value}" for key, value in stats.items()])
    return stats_text, out_path  # return text and output path

def lv2_decode(file_path):
    # path to the compressed file is received as an argument
    compressed_file = file_path

    # check if the file exists
    if not os.path.exists(compressed_file):
        print("Compressed file NOT found!")
        return None

    # open and read the compressed file rb mode
    with open(compressed_file, "rb") as file:
        encode_bytes = file.read()

    # perform LZW decompression
    lzw = LZWCoding("thumbs_up.bmp", "text")
    #convert each byte into its binary string representation ( 8 bits per byte)
    bit_string = "".join(format(byte, "08b") for byte in encode_bytes)
    #remove the padding added during compression ( if needed)
    bit_string = lzw.remove_padding(bit_string)
    #extract code length information from the bit string
    bit_string = lzw.extract_code_length_info(bit_string)
    #convert the bit string back into a list of integers (decode)
    bit2int = lzw.binary_string_to_int_list(bit_string)

    #decode the inage data from the list of integers
    decode_img = lzw.decode(bit2int)

    # take original size of image
    original_img = Image.open("thumbs_up.bmp")
    width, height = original_img.size

    # convert the decode image data back to pixel values as a list of int
    convert_pixels = [ord(ch) for ch in decode_img]
    try:
        #reshape the 1D pixel list into a 2D arr
        convert_array = np.array(convert_pixels, dtype=np.uint8).reshape(height, width)
    except ValueError as e:
        print(f"Error reshaping image: {e}")
        return None

    # convert numpy 2D arr back to into a grayscale img using PIL
    convert_img = Image.fromarray(convert_array, mode="L")
    #save
    convert_img.save("lv2_gray_decompression.bmp")

    stats = {
        "decompressed_img": "lv2_gray_decompression.bmp"
    }
    # return dict and PIL object
    return stats, convert_img


if __name__== '__main__':
    image_path="C:\\Users\\eersa\\PycharmProjects\\TaskSP\\project5\\pythonProject24141\\thumbs_up.bmp"
    file_path="C:\\Users\\eersa\\PycharmProjects\\TaskSP\\project5\\pythonProject24141\\lv2Compressed.bin"
    compstats,out_path =lv2_encode(image_path)
    print(compstats)

    print("\n")
    decomp,last=lv2_decode(file_path)
    print(decomp)





