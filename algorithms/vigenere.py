"""
Vigenère Cipher Module for CrypTosca
Vigenère Cipher menggunakan teknik substitusi polialfabetik berdasarkan huruf kunci.
Setiap huruf pada plaintext digeser sesuai nilai huruf pada kunci berulang.

- Karakter non-huruf tetap dipertahankan
- Kunci dianggap huruf besar, dan digeser berdasarkan alfabet A-Z
"""

import streamlit as st

def vigenere_cipher(text, key, mode):
    """Proses enkripsi atau dekripsi Vigenère Cipher"""
    result = ""
    key = key.upper()
    key_len = len(key)
    j = 0  # indeks kunci

    for char in text:
        if char.isalpha():
            k = ord(key[j % key_len]) - ord('A')
            if mode == "Dekripsi":
                k = -k
            base = ord('A') if char.isupper() else ord('a')
            shifted = (ord(char) - base + k) % 26
            result += chr(shifted + base)
            j += 1
        else:
            result += char  # pertahankan spasi, tanda baca, dll

    return result

def run(log_history):
    st.header("🔐 Vigenère Cipher")
    st.markdown("""
    Vigenère Cipher adalah algoritma klasik yang menggunakan kunci berupa **kata atau frasa**,  
    lalu mengenkripsi huruf-huruf dalam plaintext dengan pergeseran alfabet berdasarkan huruf-huruf pada kunci.

    - Kunci berulang secara siklik untuk mencocokkan panjang teks.
    - Hanya huruf yang diproses; karakter non-huruf dipertahankan apa adanya.
    """)

    mode = st.radio("📌 Pilih Mode", ["Enkripsi", "Dekripsi"])
    text = st.text_area("📝 Masukkan Teks")
    key = st.text_input("🔑 Masukkan Kunci (huruf saja)", max_chars=100)

    if st.button("🚀 Jalankan Vigenère Cipher"):
        if not text.strip():
            st.warning("Teks tidak boleh kosong.")
            return
        if not key.strip().isalpha():
            st.warning("Kunci hanya boleh terdiri dari huruf.")
            return
        try:
            result = vigenere_cipher(text, key, mode)
            st.success(f"✅ Hasil {mode}:")
            st.code(result, language="text")
            log_history("Vigenère Cipher", mode, text, result)
        except Exception as e:
            st.error(f"Terjadi kesalahan saat memproses: {e}")
