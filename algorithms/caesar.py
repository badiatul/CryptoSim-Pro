import streamlit as st
from utils import log_history


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
    text = st.text_input("Masukkan teks")
    shift = st.slider("Pergeseran (Shift)", 1, 25, 3)
    if st.button("Proses"):
        result = encrypt(text, shift) if mode == "Enkripsi" else decrypt(text, shift)
        st.success(f"Hasil: {result}")
def run():
    import streamlit as st
    from datetime import datetime
    from .cipher_utils import caesar_encrypt as encrypt, caesar_decrypt as decrypt  # pastikan sesuai

    mode = st.radio("Pilih Mode", ["Enkripsi", "Dekripsi"])
    teks = st.text_area("Masukkan Teks")
    key = st.number_input("Masukkan Key", min_value=1, max_value=25, value=3)

    if st.button("🔐 Proses"):
        if mode == "Enkripsi":
            hasil = encrypt(teks, key)
        else:
            hasil = decrypt(teks, key)
        st.success(hasil)

        st.session_state.history.append({
            "algoritma": "Caesar Cipher",
            "mode": mode,
            "input": teks,
            "hasil": hasil,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
