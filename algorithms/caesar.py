import streamlit as st
from utils import log_history  # pastikan utils.py ada dan berisi fungsi log_history

def encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            result += chr((ord(char) - offset + shift) % 26 + offset)
        else:
            result += char
    return result

def decrypt(text, shift):
    return encrypt(text, -shift)

def run():
    st.header("🔐 Caesar Cipher")
    mode = st.radio("Pilih mode", ["Enkripsi", "Dekripsi"])
    text = st.text_area("Masukkan teks")
    shift = st.slider("Pergeseran (Shift)", 1, 25, 3)

    if st.button("Proses"):
        result = encrypt(text, shift) if mode == "Enkripsi" else decrypt(text, shift)
        st.success(f"Hasil: {result}")

        # Simpan ke riwayat
        log_history("Caesar Cipher", mode, text, result)
