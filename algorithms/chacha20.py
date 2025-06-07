"""
ChaCha20 Symmetric Encryption
Algoritma enkripsi simetris modern yang cepat dan aman,
menggunakan nonce dan key 256-bit (32 byte key, 12 byte nonce).

Catatan penting:
- Key harus berupa hex 64 karakter (32 byte)
- Nonce harus berupa hex 24 karakter (12 byte)
- Contoh pembuatan key/nonce dengan os.urandom di Python:
    import os
    os.urandom(32).hex()  # untuk key
    os.urandom(12).hex()  # untuk nonce
"""
import streamlit as st
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import binascii

def encrypt_chacha20(key, nonce, plaintext):
    algorithm = algorithms.ChaCha20(key, nonce)
    cipher = Cipher(algorithm, mode=None, backend=default_backend())
    encryptor = cipher.encryptor()
    ct = encryptor.update(plaintext.encode())
    return ct

def decrypt_chacha20(key, nonce, ciphertext):
    algorithm = algorithms.ChaCha20(key, nonce)
    cipher = Cipher(algorithm, mode=None, backend=default_backend())
    decryptor = cipher.decryptor()
    pt = decryptor.update(ciphertext)
    return pt.decode(errors='ignore')

def run(log_history):
    st.subheader("🔐 ChaCha20 Symmetric Encryption")

    mode = st.radio("Pilih Mode", ["Enkripsi", "Dekripsi"])

    if mode == "Enkripsi":
        plaintext = st.text_area("Masukkan Teks")
        key_input = st.text_input("Masukkan Key (32 byte hex, contoh: 00ff...)", max_chars=64)
        nonce_input = st.text_input("Masukkan Nonce (12 byte hex, contoh: 00ff...)", max_chars=24)

        if st.button("Enkripsi"):
            try:
                key = binascii.unhexlify(key_input)
                nonce = binascii.unhexlify(nonce_input)
                ct = encrypt_chacha20(key, nonce, plaintext)
                hasil = binascii.hexlify(ct).decode()
                st.success("Hasil Enkripsi (hex):")
                st.code(hasil)
                log_history("ChaCha20", "Enkripsi", plaintext, hasil)
            except Exception as e:
                st.error(f"Error: {e}")

    else:  # Dekripsi
        ciphertext_hex = st.text_area("Masukkan Ciphertext (hex)")
        key_input = st.text_input("Masukkan Key (32 byte hex)")
        nonce_input = st.text_input("Masukkan Nonce (12 byte hex)")

        if st.button("Dekripsi"):
            try:
                key = binascii.unhexlify(key_input)
                nonce = binascii.unhexlify(nonce_input)
                ciphertext = binascii.unhexlify(ciphertext_hex)
                pt = decrypt_chacha20(key, nonce, ciphertext)
                st.success("Hasil Dekripsi:")
                st.code(pt)
                log_history("ChaCha20", "Dekripsi", ciphertext_hex, pt)
            except Exception as e:
                st.error(f"Error: {e}")
