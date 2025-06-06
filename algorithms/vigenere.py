import streamlit as st
from utils import log_history

def extend_key(text, key):
    key = key.upper()
    return (key * (len(text) // len(key))) + key[:len(text) % len(key)]

def encrypt(text, key):
    text = text.upper()
    key = extend_key(text, key)
    result = ""
    for i in range(len(text)):
        if text[i].isalpha():
            result += chr((ord(text[i]) + ord(key[i]) - 2*65) % 26 + 65)
        else:
            result += text[i]
    return result

def decrypt(text, key):
    text = text.upper()
    key = extend_key(text, key)
    result = ""
    for i in range(len(text)):
        if text[i].isalpha():
            result += chr((ord(text[i]) - ord(key[i]) + 26) % 26 + 65)
        else:
            result += text[i]
    return result

def run():
    st.header("🔐 Vigenère Cipher")
    mode = st.radio("Pilih mode", ["Enkripsi", "Dekripsi"])
    text = st.text_area("Masukkan teks")
    key = st.text_input("Masukkan kunci (huruf)")

    if st.button("Proses") and key.isalpha():
        result = encrypt(text, key) if mode == "Enkripsi" else decrypt(text, key)
        st.success(f"Hasil: {result}")
        log_history("Vigenère Cipher", mode, text, result)
