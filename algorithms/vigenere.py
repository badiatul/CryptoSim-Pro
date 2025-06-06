import streamlit as st

def generate_key(text, key):
    key = key.upper()
    key_extended = ""
    key_index = 0
    for char in text:
        if char.isalpha():
            key_extended += key[key_index % len(key)]
            key_index += 1
        else:
            key_extended += char
    return key_extended

def encrypt(text, key):
    text = text.upper()
    key = generate_key(text, key)
    result = ""
    for t, k in zip(text, key):
        if t.isalpha():
            c = (ord(t) + ord(k) - 2 * 65) % 26 + 65
            result += chr(c)
        else:
            result += t
    return result

def decrypt(text, key):
    text = text.upper()
    key = generate_key(text, key)
    result = ""
    for t, k in zip(text, key):
        if t.isalpha():
            c = (ord(t) - ord(k) + 26) % 26 + 65
            result += chr(c)
        else:
            result += t
    return result

def run(log_history):
    st.header("🔐 Vigenère Cipher")
    mode = st.radio("Pilih mode", ["Enkripsi", "Dekripsi"])
    text = st.text_input("Masukkan teks")
    key = st.text_input("Masukkan kunci (huruf)")

    if st.button("Proses") and key.isalpha() and key != "":
        if mode == "Enkripsi":
            result = encrypt(text, key)
        else:
            result = decrypt(text, key)
        st.success(f"Hasil: {result}")
        log_history("Vigenère Cipher", mode, text, result)
