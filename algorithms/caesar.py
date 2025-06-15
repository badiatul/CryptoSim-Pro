import streamlit as st
import qrcode
import io
from PIL import Image

def encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result

def decrypt(text, shift):
    return encrypt(text, -shift)

def run(log_history):
    st.header("🔐 Caesar Cipher")
    text = st.text_area("Masukkan teks:")
    shift = st.number_input("Shift:", 1, 25, 3)
    mode = st.radio("Pilih mode:", ["Enkripsi", "Dekripsi"])

    if st.button("Proses"):
        if mode == "Enkripsi":
            result = encrypt(text, shift)
        else:
            result = decrypt(text, shift)

        st.success(result)
        log_history("Caesar Cipher", mode, text, result)

        # QR Code result
        qr = qrcode.make(result)
        buf = io.BytesIO()
        qr.save(buf, format="PNG")
        st.image(buf.getvalue(), caption="QR Code dari hasil", use_container_width=False)
