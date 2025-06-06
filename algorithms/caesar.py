import streamlit as st

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

def run(log_history):
    st.subheader("🔐 Caesar Cipher")
    mode = st.radio("Pilih Mode", ["Enkripsi", "Dekripsi"])
    text = st.text_area("Masukkan Teks")
    shift = st.slider("Shift", 1, 25, 3)
    if st.button("Proses"):
        result = encrypt(text, shift) if mode == "Enkripsi" else decrypt(text, shift)
        st.success(result)
        log_history("Caesar Cipher", mode, text, result)
