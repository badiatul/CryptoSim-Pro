from PIL import Image

def embed_lsb(message: str, image_path: str, output_path: str) -> None:
    img = Image.open(image_path)
    encoded = img.copy()
    width, height = img.size
    message += chr(0)  # Tambahkan karakter null sebagai penanda akhir

    binary_message = ''.join([format(ord(char), '08b') for char in message])
    data_index = 0
    max_capacity = width * height * 3

    if len(binary_message) > max_capacity:
        raise ValueError("Pesan terlalu panjang untuk disisipkan ke dalam gambar.")

    for y in range(height):
        for x in range(width):
            pixel = list(img.getpixel((x, y)))
            for n in range(3):  # RGB
                if data_index < len(binary_message):
                    pixel[n] = pixel[n] & ~1 | int(binary_message[data_index])
                    data_index += 1
            encoded.putpixel((x, y), tuple(pixel))
    
    encoded.save(output_path)

def extract_lsb(image_path: str) -> str:
    img = Image.open(image_path)
    binary_data = ""
    for y in range(img.height):
        for x in range(img.width):
            pixel = img.getpixel((x, y))
            for n in range(3):  # RGB
                binary_data += str(pixel[n] & 1)

    chars = [chr(int(binary_data[i:i+8], 2)) for i in range(0, len(binary_data), 8)]
    message = ''.join(chars)
    return message.split(chr(0))[0]  # Stop at null character
