from PIL import Image
import streamlit as st

def embed_lsb(message: str, image_path: str, output_path: str) -> None:
    img = Image.open(image_path)
    encoded = img.copy()
    width, height = img.size
    message += chr(0)  # Null terminator

    binary_message = ''.join([format(ord(c), '08b') for c in message])
    data_index = 0
    max_capacity = width * height * 3

    if len(binary_message) > max_capacity:
        raise ValueError("Pesan terlalu panjang untuk disisipkan ke dalam gambar.")

    for y in range(height):
        for x in range(width):
            pixel = list(img.getpixel((x, y)))
            for n in range(3):
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
            for n in range(3):
                binary_data += str(pixel[n] & 1)

    chars = [chr(int(binary_data[i:i+8], 2)) for i in range(0, len(binary_data), 8)]
    return ''.join(chars).split(chr(0))[0]

def run(log_history):
    st.subheader("🖼️ LSB Steganography")
    mode = st.radio("Pilih Mode", ("Sisipkan Pesan", "Ekstrak Pesan"))

    if mode == "Sisipkan Pesan":
        uploaded_image = st.file_uploader("Unggah Gambar PNG", type=["png"])
        secret_message = st.text_area("Masukkan Pesan Rahasia")
        if st.button("Sisipkan"):
            if uploaded_image and secret_message:
                with open("temp_input.png", "wb") as f:
                    f.write(uploaded_image.read())
                try:
                    embed_lsb(secret_message, "temp_input.png", "temp_output.png")
                    with open("temp_output.png", "rb") as f:
                        st.download_button("Unduh Gambar Stego", f, file_name="gambar_tersembunyi.png")
                    st.success("✅ Pesan berhasil disisipkan.")
                    log_history("LSB Steganography", "Sisipkan", secret_message, "[Gambar]")
                except Exception as e:
                    st.error(f"❌ Terjadi kesalahan: {e}")

    elif mode == "Ekstrak Pesan":
        uploaded_image = st.file_uploader("Unggah Gambar PNG", type=["png"])
        if st.button("Ekstrak"):
            if uploaded_image:
                with open("temp_extract.png", "wb") as f:
                    f.write(uploaded_image.read())
                try:
                    extracted = extract_lsb("temp_extract.png")
                    st.text_area("Pesan Tersembunyi", value=extracted, height=150)
                    log_history("LSB Steganography", "Ekstrak", "[Gambar]", extracted)
                except Exception as e:
                    st.error(f"❌ Gagal mengekstrak: {e}")
