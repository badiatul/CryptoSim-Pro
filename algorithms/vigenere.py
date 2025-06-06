import streamlit as st

def generate_key(text, key):
    key = list(key)
    if len(key) == 0:
        return "A" * len(text)
    while len(key) < len(text):
        key.append(key[len(key) % len(key)])
    return "".join(key)

def encrypt(text, key):
    key = generate_key(text, key)
    cipher = ""
    for i in range(len(text)):
        if text[i].isalpha():
            offset = 65 if text[i].isupper() else 97
            cipher += chr((ord(text[i]) + ord(key[i]) - 2 * offset) % 26 + offset)
        else:
            cipher += text[i]
    return cipher

def decrypt(cipher, key):
    key = generate_key(cipher, key)
    text = ""
    for i in range(len(cipher)):
        if cipher[i].isalpha():
            offset = 65 if cipher[i].isupper() else 97
            text += chr((ord(cipher[i]) - ord(key[i]) + 26) % 26 + offset)
        else:
            text += cipher[i]
    return text

def run(log_history):
    st.header("🔐 Vigenère Cipher")
    mode = st.radio("Pilih mode", ["Enkripsi", "Dekripsi"])
    text = st.text_input("Masukkan teks")
    key = st.text_input("Masukkan kunci")
    if st.button("Proses"):
        result = encrypt(text, key) if mode == "Enkripsi" else decrypt(text, key)
        st.success(f"Hasil: {result}")
        log_history("Vigenère Cipher", mode, text, result)
