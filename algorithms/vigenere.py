import streamlit as st

def vigenere_encrypt(text, key):
    key = key.upper()
    key_stream = (key * (len(text) // len(key) + 1))[:len(text)]
    result = ''
    for t, k in zip(text, key_stream):
        if t.isalpha():
            base = ord('A') if t.isupper() else ord('a')
            offset = ord(k) - ord('A')
            result += chr((ord(t) - base + offset) % 26 + base)
        else:
            result += t
    return result

def vigenere_decrypt(text, key):
    key = key.upper()
    key_stream = (key * (len(text) // len(key) + 1))[:len(text)]
    result = ''
    for t, k in zip(text, key_stream):
        if t.isalpha():
            base = ord('A') if t.isupper() else ord('a')
            offset = ord(k) - ord('A')
            result += chr((ord(t) - base - offset) % 26 + base)
        else:
            result += t
    return result

def run():
    st.header("🔐 Vigenère Cipher")
    mode = st.radio("Pilih mode", ["Enkripsi", "Dekripsi"])
    text = st.text_input("Masukkan teks")
    key = st.text_input("Masukkan kunci (huruf)")
    if st.button("Proses") and key.isalpha():
        result = vigenere_encrypt(text, key) if mode == "Enkripsi" else vigenere_decrypt(text, key)
        st.success(f"Hasil: {result}")
