import streamlit as st
import qrcode
import io
from PIL import Image
import math

def encrypt_columnar(text, key):
    key_order = sorted(list(enumerate(key)), key=lambda x: x[1])
    num_cols = len(key)
    num_rows = math.ceil(len(text) / num_cols)
    padded_text = text.ljust(num_cols * num_rows)

    matrix = [padded_text[i:i + num_cols] for i in range(0, len(padded_text), num_cols)]
    ciphertext = ''

    for idx, _ in key_order:
        for row in matrix:
            ciphertext += row[idx]
    return ciphertext

def decrypt_columnar(ciphertext, key):
    key_order = sorted(list(enumerate(key)), key=lambda x: x[1])
    num_cols = len(key)
    num_rows = math.ceil(len(ciphertext) / num_cols)

    col_lengths = [num_rows] * num_cols
    total_cells = num_rows * num_cols
    extra_cells = total_cells - len(ciphertext)

    for i in range(extra_cells):
        col_lengths[key_order[-(i + 1)][0]] -= 1

    matrix = [''] * num_cols
    pos = 0
    for idx, _ in key_order:
        length = col_lengths[idx]
        matrix[idx] = ciphertext[pos:pos + length]
        pos += length

    plaintext = ''
    for i in range(num_rows):
        for col in matrix:
            if i < len(col):
                plaintext += col[i]
    return plaintext.rstrip()

def run(log_history):
    st.header("🔐 Columnar Transposition Cipher")
    st.markdown("""
    Columnar Transposition Cipher menyusun huruf pesan ke dalam baris sesuai panjang kunci,  
    lalu membaca berdasarkan urutan abjad kunci secara kolom.

    - Misal kunci: `ZEBRA`, maka urutan kolom: `1 3 4 2 0` (berdasarkan abjad).
    - Karakter kosong diisi spasi jika perlu.
    """)

    mode = st.radio("Pilih Mode", ["Enkripsi", "Dekripsi"])
    text = st.text_area("📝 Masukkan Teks")
    key = st.text_input("🔑 Masukkan Kunci (huruf saja)")

    if st.button(f"🚀 Jalankan Columnar {mode}"):
        if not text.strip() or not key.strip().isalpha():
            st.warning("Teks dan kunci harus valid dan tidak kosong.")
            return

        try:
            result = encrypt_columnar(text.replace(" ", ""), key) if mode == "Enkripsi" else decrypt_columnar(text, key)
            st.success(f"Hasil {mode}:")
            st.code(result, language="text")

            # QR Code hanya saat enkripsi
            if mode == "Enkripsi":
                qr = qrcode.QRCode(version=1, box_size=10, border=4)
                qr.add_data(result)
                qr.make(fit=True)
                img_qr = qr.make_image(fill_color="black", back_color="white").convert("RGB")

                # Simpan ke buffer
                buf = io.BytesIO()
                img_qr.save(buf, format="PNG")
                byte_qr = buf.getvalue()

                st.image(img_qr, caption="📷 QR Code dari Hasil Enkripsi", use_container_width=True)
                st.download_button("⬇️ Unduh QR Code", data=byte_qr, file_name="columnar_qrcode.png", mime="image/png")

            log_history("Columnar Transposition Cipher", mode, text, result)

        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")
