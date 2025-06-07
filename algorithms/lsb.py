import streamlit as st
from PIL import Image
import numpy as np
import io

def embed_message(img: Image.Image, message: str) -> Image.Image:
    """Sisipkan pesan ke dalam gambar menggunakan LSB pada kanal biru"""
    encoded = img.copy()
    width, height = encoded.size
    max_bytes = width * height // 8
    message += chr(0)  # terminator
    binary_message = ''.join(f"{ord(c):08b}" for c in message)

    if len(binary_message) > width * height:
        raise ValueError("Pesan terlalu panjang untuk gambar ini.")

    pixels = np.array(encoded)
    flat_blue = pixels[:, :, 2].flatten()

    for i in range(len(binary_message)):
        flat_blue[i] = (flat_blue[i] & 0xFE) | int(binary_message[i])

    pixels[:, :, 2] = flat_blue.reshape(height, width)
    return Image.fromarray(pixels)

def extract_message(img: Image.Image) -> str:
    """Ekstrak pesan dari gambar menggunakan LSB pada kanal biru"""
    pixels = np.array(img)
    flat_blue = pixels[:, :, 2].flatten()
    bits = [str(b & 1) for b in flat_blue]

    chars = []
    for i in range(0, len(bits), 8):
        byte = ''.join(bits[i:i+8])
        char = chr(int(byte, 2))
        if char == chr(0):  # terminator
            break
        chars.append(char)

    return ''.join(chars)

def run(log_history):
    st.header("🖼️ LSB Steganography")
    st.markdown("""
    LSB (Least Significant Bit) Steganografi adalah teknik menyisipkan data ke dalam citra digital  
    dengan mengganti bit terakhir dari kanal warna (umumnya kanal biru) pada setiap piksel.

    - **Mode Enkripsi** akan menyisipkan pesan teks ke dalam gambar.
    - **Mode Dekripsi** akan membaca pesan tersembunyi dari gambar yang telah disisipkan.

    ⚠️ Ukuran gambar harus cukup untuk menampung pesan.
    """)

    mode = st.radio("Pilih Mode", ["Enkripsi", "Dekripsi"])

    uploaded_file = st.file_uploader("📁 Unggah Gambar (PNG)", type=["png"])
    message = ""

    if mode == "Enkripsi":
        message = st.text_area("💬 Masukkan Pesan yang Ingin Disisipkan", max_chars=1000)

    if st.button(f"🚀 Jalankan {mode}"):
        if not uploaded_file:
            st.error("Silakan unggah gambar terlebih dahulu.")
            return

        try:
            image = Image.open(uploaded_file).convert("RGB")
        except Exception as e:
            st.error(f"Gagal membuka gambar: {e}")
            return

        if mode == "Enkripsi":
            if not message.strip():
                st.error("Pesan tidak boleh kosong.")
                return
            try:
                encoded_img = embed_message(image, message)
                st.success("✅ Pesan berhasil disisipkan!")
                st.image(encoded_img, caption="Gambar Hasil Enkripsi", use_column_width=True)

                # Simpan ke buffer untuk diunduh
                buf = io.BytesIO()
                encoded_img.save(buf, format="PNG")
                byte_img = buf.getvalue()

                st.download_button("⬇️ Unduh Gambar Hasil", data=byte_img, file_name="hasil_lsb.png", mime="image/png")

                log_history("LSB Steganography", "Enkripsi", message, "[Gambar terenkripsi]")
            except Exception as e:
                st.error(f"Gagal menyisipkan pesan: {e}")

        else:  # Dekripsi
            try:
                extracted = extract_message(image)
                if extracted:
                    st.success("✅ Pesan berhasil diambil:")
                    st.code(extracted, language="text")
                    log_history("LSB Steganography", "Dekripsi", "[Gambar dengan pesan tersembunyi]", extracted)
                else:
                    st.warning("Tidak ditemukan pesan di dalam gambar.")
            except Exception as e:
                st.error(f"Gagal mengekstrak pesan: {e}")
