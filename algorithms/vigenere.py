import streamlit as st
from utils import log_history


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
def run():
    import streamlit as st
    from datetime import datetime
    from .cipher_utils import vigenere_encrypt as encrypt, vigenere_decrypt as decrypt

    mode = st.radio("Pilih Mode", ["Enkripsi", "Dekripsi"])
    teks = st.text_area("Masukkan Teks")
    key = st.text_input("Masukkan Kunci (kata)")

    if st.button("🔐 Proses"):
        if mode == "Enkripsi":
            hasil = encrypt(teks, key)
        else:
            hasil = decrypt(teks, key)
        st.success(hasil)

        st.session_state.history.append({
            "algoritma": "Vigenère Cipher",
            "mode": mode,
            "input": teks,
            "hasil": hasil,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
