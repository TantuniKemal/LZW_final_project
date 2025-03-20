from numpy.ma.core import compressed

from LZW import *  # LZW sınıfını içe aktar
import os  # Dosya boyutlarını almak için kullanacağız

def lv1_encode(text_file_path):
    # LZW sınıfının örneğini oluştur
    lzw = LZWCoding('string', 'text')

    # Dosyayı oku
    with open(text_file_path, 'r') as file:
        text_content = file.read()  # Dosyanın içeriğini oku

    # Sıkıştırma işlemi
    print("\n--- Encode ---")
    compressed_file = lzw.compress_text_file(text_content)

    # Sıkıştırılmış dosyayı kaydet
    compressed_file_path = "compressed_file.lzw"
    with open(compressed_file_path, 'wb') as file:
        file.write(compressed_file)

    # Codelength hesapla
    codelength = len(compressed_file) * 8  # Byte cinsinden uzunluk, her bir byte 8 bit
    print(f"Codelength: {codelength} bit")

    # Compressed Ratio hesapla
    original_size = os.path.getsize(text_file_path)  # Orijinal dosyanın boyutunu al
    compressed_size = os.path.getsize(compressed_file_path)  # Sıkıştırılmış dosyanın boyutunu al
    compressed_ratio = compressed_size / original_size if original_size > 0 else 0  # Oranı hesapla
    print(f"Compressed Ratio: {compressed_ratio:.2f}")

    print(f"Sıkıştırılmış dosya kaydedildi: {compressed_file_path}")


def lv1_decode(compressed_file_path):
    compressed_file= compressed_file_path

    lzw = LZWCoding('string', 'text')

    # Sıkıştırılmış dosyayı oku
    with open(compressed_file, 'rb') as file:
        compressed_content = file.read()

    print("\n--- DECODE ---")
    decompressed_text = lzw.decompress_text_file(compressed_content)
    return  decompressed_text





if __name__ == '__main__':

    text_file_path = "C:\\Users\\eersa\\PycharmProjects\\TaskSP\\project5\\pythonProject24141\\example.txt"
    file_path= "C:\\Users\\eersa\\PycharmProjects\\TaskSP\\project5\\pythonProject24141\\lv1Compressed.bin"
    lv1_encode(text_file_path)



