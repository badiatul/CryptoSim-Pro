"""
Fernet Symmetric Encryption
Metode enkripsi simetris yang aman dan mudah digunakan dari library cryptography.
Menerapkan AES 128 CBC dengan HMAC untuk integritas data.
Key yang digunakan adalah base64 URL-safe 32 byte.

Catatan penting:
- Key harus base64 URL-safe 32 byte (biasanya 44 karakter string)
- Key dapat dibuat dengan fungsi Fernet.generate_key()
- Data hasil enkripsi berupa string base64
"""

import streamlit as st
from cryptography.fernet import Fernet

def run(log_history):
    st.subheader("🔐 Fernet Symmetric Encryption")

    mode = st.radio("Pilih Mode", ["Enkripsi", "Dekripsi"])

    if mode == "Enkripsi":
        plaintext = st.text_area("Masukkan Teks")
        key_input = st.text_input("Masukkan Key (base64 URL-safe 44 karakter)", max_chars=44)

        if st.button("Enkripsi"):
            try:
                if not key_input:
                    st.error("Key tidak boleh kosong")
                    return
                fernet = Fernet(key_input)
                encrypted = fernet.encrypt(plaintext.encode()).decode()
                st.success("Hasil Enkripsi (base64):")
                st.code(encrypted)
                log_history("Fernet", "Enkripsi", plaintext, encrypted)
            except Exception as e:
                st.error(f"Error: {e}")

    else:  # Dekripsi
        ciphertext = st.text_area("Masukkan Ciphertext (base64)")
        key_input = st.text_input("Masukkan Key (base64 URL-safe 44 karakter)", max_chars=44)

        if st.button("Dekripsi"):
            try:
                if not key_input:
                    st.error("Key tidak boleh kosong")
                    return
                fernet = Fernet(key_input)
                decrypted = fernet.decrypt(ciphertext.encode()).decode()
                st.success("Hasil Dekripsi:")
                st.code(decrypted)
                log_history("Fernet", "Dekripsi", ciphertext, decrypted)
            except Exception as e:
                st.error(f"Error: {e}")
