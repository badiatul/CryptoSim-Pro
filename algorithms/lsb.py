import streamlit as st
from PIL import Image
import io

def encode_lsb(image: Image.Image, message: str) -> Image.Image:
    binary_message = ''.join([format(ord(char), '08b') for char in message]) + '1111111111111110'
    encoded = image.copy()
    pixels = encoded.load()

    data_index = 0
    for y in range(encoded.height):
        for x in range(encoded.width):
            if data_index >= len(binary_message):
                return encoded
            r, g, b = pixels[x, y]
            r = (r & ~1) | int(binary_message[data_index])
            data_index += 1
            if data_index < len(binary_message):
                g = (g & ~1) | int(binary_message[data_index])
                data_index += 1
            if data_index < len(binary_message):
                b = (b & ~1) | int(binary_message[data_index])
                data_index += 1
            pixels[x, y] = (r, g, b)
    return encoded

def decode_lsb(image: Image.Image) -> str:
    pixels = image.load()
    binary_data = ''
    for y in range(image.height):
        for x in range(image.width):
            r, g, b = pixels[x, y]
            binary_data += str(r & 1)
            binary_data += str(g & 1)
            binary_data += str(b & 1)
    bytes_data = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    message = ''
    for byte in bytes_data:
        if byte == '11111110':
            break
        message += chr(int(byte, 2))
    return message

def run(log_history):
    st.subheader("🔏 LSB Steganography")
    mode = st.radio("Mode", ["Enkripsi", "Dekripsi"])

    if mode == "Enkripsi":
        uploaded = st.file_uploader("Unggah gambar (PNG)", type=["png"])
        message = st.text_area("Pesan yang akan disisipkan")

        if uploaded and message:
            image = Image.open(uploaded)
            result_image = encode_lsb(image, message)
            buf = io.BytesIO()
            result_image.save(buf, format="PNG")
            byte_im = buf.getvalue()

            st.image(result_image, caption="Hasil Enkripsi")
            st.download_button("📥 Unduh Gambar Terenkripsi", byte_im, file_name="stego_image.png", mime="image/png")
            log_history("LSB Steganography", "Enkripsi", f"[Gambar] + {message}", "Gambar terenkripsi")
    
    elif mode == "Dekripsi":
        uploaded = st.file_uploader("Unggah gambar terenkripsi (PNG)", type=["png"])
        if uploaded:
            image = Image.open(uploaded)
            decoded_message = decode_lsb(image)
            st.text_area("Pesan Tersembunyi", decoded_message)
            log_history("LSB Steganography", "Dekripsi", "[Gambar terenkripsi]", decoded_message)
