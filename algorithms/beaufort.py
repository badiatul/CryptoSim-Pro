# algorithms/beaufort.py
import streamlit as st

def encrypt(text, key):
    result = ''
    for i in range(len(text)):
        if text[i].isalpha():
            shift = (ord(key[i % len(key)].upper()) - ord(text[i].upper())) % 26
            result += chr(ord('A') + shift)
        else:
            result += text[i]
    return result

def decrypt(text, key):
    # Sama saja dengan encrypt di Beaufort
    return encrypt(text, key)

def run(log_history):
    st.subheader("🔐 Beaufort Cipher")
    mode = st.radio("Mode", ["Enkripsi", "Dekripsi"])
    text = st.text_area("Masukkan teks")
    key = st.text_input("Masukkan kunci (huruf saja)")

    if st.button("Proses"):
        if not key.isalpha():
            st.error("Kunci harus berupa huruf.")
            return
        result = encrypt(text.upper(), key.upper()) if mode == "Enkripsi" else decrypt(text.upper(), key.upper())
        st.success(result)
        log_history("Beaufort Cipher", mode, text, result)
