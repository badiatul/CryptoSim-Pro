import streamlit as st

def format_key(text, key):
    key = list(key)
    if len(key) == len(text):
        return "".join(key)
    else:
        for i in range(len(text) - len(key)):
            key.append(key[i % len(key)])
    return "".join(key)

def encrypt(text, key):
    key = format_key(text, key)
    cipher = ""
    for i in range(len(text)):
        if text[i].isalpha():
            offset = 65 if text[i].isupper() else 97
            cipher += chr((ord(text[i]) + ord(key[i]) - 2*offset) % 26 + offset)
        else:
            cipher += text[i]
    return cipher

def decrypt(cipher, key):
    key = format_key(cipher, key)
    text = ""
    for i in range(len(cipher)):
        if cipher[i].isalpha():
            offset = 65 if cipher[i].isupper() else 97
            text += chr((ord(cipher[i]) - ord(key[i])) % 26 + offset)
        else:
            text += cipher[i]
    return text

def run(log_history):
    st.subheader("🔐 Vigenère Cipher")
    mode = st.radio("Pilih Mode", ["Enkripsi", "Dekripsi"])
    text = st.text_area("Masukkan Teks")
    key = st.text_input("Masukkan Kunci (A-Z)")
    if st.button("Proses") and key:
        result = encrypt(text, key) if mode == "Enkripsi" else decrypt(text, key)
        st.success(result)
        log_history("Vigenère Cipher", mode, text, result)
