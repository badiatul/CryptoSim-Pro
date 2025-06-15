import streamlit as st
import qrcode
import io
from PIL import Image

def columnar_encrypt(plaintext, key):
    key_order = sorted(list(key))
    num_cols = len(key)
    num_rows = (len(plaintext) + num_cols - 1) // num_cols
    padded = plaintext.ljust(num_cols * num_rows)
    matrix = [list(padded[i:i + num_cols]) for i in range(0, len(padded), num_cols)]
    ciphertext = ''
    for char in key_order:
        col_idx = key.index(char)
        for row in matrix:
            ciphertext += row[col_idx]
    return ciphertext

def columnar_decrypt(ciphertext, key):
    key_order = sorted(list(key))
    num_cols = len(key)
    num_rows = (len(ciphertext) + num_cols - 1) // num_cols
    num_full_cols = len(ciphertext) % num_cols
    if num_full_cols == 0:
        num_full_cols = num_cols

    col_lengths = [num_rows] * num_cols
    for i in range(num_cols):
        if key_order[i] in key[num_full_cols:]:
            col_lengths[key.index(key_order[i])] -= 1

    col_data = {}
    k = 0
    for char in key_order:
        idx = key.index(char)
        col_data[idx] = list(ciphertext[k:k + col_lengths[idx]])
        k += col_lengths[idx]

    plaintext = ''
    for i in range(num_rows):
        for j in range(num_cols):
            if i < len(col_data[j]):
                plaintext += col_data[j][i]
    return plaintext.strip()

def run(log_history):
    st.header("🔐 Columnar Transposition Cipher")
    st.markdown("""
    Columnar Transposition Cipher mengenkripsi teks dengan menulis dalam baris sesuai jumlah kolom kunci, lalu membacanya kolom per kolom sesuai urutan abjad dari kunci.
    
    - **Contoh kunci:** `KEYWORD`, `SECRET`, `CIPHER`
    """)

    mode = st.radio("Pilih Mode", ["Enkripsi", "Dekripsi"])
    text = st.text_area("📝 Masukkan Teks", height=150)
    key = st.text_input("🔑 Masukkan Kunci (huruf tanpa spasi)", max_chars=20)

    if st.button(f"🚀 Jalankan {mode}"):
        if not text.strip() or not key.strip():
            st.warning("Teks dan kunci tidak boleh kosong.")
            return

        try:
            if mode == "Enkripsi":
                result = columnar_encrypt(text.replace(" ", ""), key)
            else:
                result = columnar_decrypt(text.replace(" ", ""), key)

            st.success(f"Hasil {mode}:")
            st.code(result)

            log_history("Columnar Transposition Cipher", mode, text, result)

            # 🔳 Tambahkan QR Code jika mode Enkripsi
            if mode == "Enkripsi":
                qr = qrcode.QRCode(version=1, box_size=10, border=4)
                qr.add_data(result)
                qr.make(fit=True)
                img_qr = qr.make_image(fill_color="black", back_color="white")

                buf = io.BytesIO()
                img_qr.save(buf, format="PNG")
                byte_qr = buf.getvalue()

                st.image(img_qr, caption="📷 QR Code dari Hasil Enkripsi", use_container_width=True)
                st.download_button("⬇️ Unduh QR Code", data=byte_qr, file_name="columnar_qrcode.png", mime="image/png")

        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")
