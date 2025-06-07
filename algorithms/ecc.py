"""
ECC (Elliptic Curve Cryptography) Algorithm Module for CryptoSim Pro

Penjelasan singkat:
ECC adalah algoritma kriptografi modern yang menggunakan konsep kurva eliptik
untuk enkripsi dan dekripsi. Algoritma ini menghasilkan kunci publik dan privat
berbasis titik pada kurva, serta enkripsi data yang aman dan efisien.

Syarat:
- Plaintext dapat berupa string biasa (ASCII/UTF-8).
- Kunci private ECC di-generate otomatis.
- Hasil enkripsi berupa bytes yang di-encode ke base64 agar bisa disimpan dan ditampilkan sebagai string.

Referensi: https://github.com/galenlynch/tinyec
"""

import streamlit as st
import base64
from tinyec import registry
import secrets

def ecc_encrypt(pubKey, plaintext):
    # Enkripsi plaintext string ke bytes menggunakan XOR dengan shared secret
    plaintext_bytes = plaintext.encode('utf-8')
    shared_secret = pubKey.x.to_bytes(32, 'big')  # bisa variasi shared secret
    encrypted = bytes([_a ^ _b for _a, _b in zip(plaintext_bytes, shared_secret)])
    return encrypted

def ecc_decrypt(privKey, ciphertext):
    shared_secret = privKey.public_key.x.to_bytes(32, 'big')
    decrypted = bytes([_a ^ _b for _a, _b in zip(ciphertext, shared_secret)])
    return decrypted.decode('utf-8', errors='ignore')

def run(log_history):
    st.header("ECC Encryption & Decryption")

    curve = registry.get_curve('brainpoolP256r1')
    privKey = secrets.randbelow(curve.field.n)
    pubKey = privKey * curve.g

    st.write("**Public Key:**", (pubKey.x, pubKey.y))
    st.write("**Private Key:**", privKey)

    mode = st.radio("Pilih Mode", ["Enkripsi", "Dekripsi"])

    if mode == "Enkripsi":
        plaintext = st.text_area("Masukkan teks yang akan dienkripsi")
        if st.button("Enkripsi"):
            if plaintext:
                ciphertext_bytes = ecc_encrypt(pubKey, plaintext)
                ciphertext_b64 = base64.b64encode(ciphertext_bytes).decode()
                st.success("Teks berhasil dienkripsi!")
                st.code(ciphertext_b64, language='text')
                log_history("ECC", mode, plaintext, ciphertext_b64)
            else:
                st.warning("Masukkan teks terlebih dahulu.")

    else:  # Dekripsi
        ciphertext_b64 = st.text_area("Masukkan ciphertext base64 untuk didekripsi")
        if st.button("Dekripsi"):
            if ciphertext_b64:
                try:
                    ciphertext_bytes = base64.b64decode(ciphertext_b64)
                    plaintext = ecc_decrypt(privKey, ciphertext_bytes)
                    st.success("Teks berhasil didekripsi!")
                    st.code(plaintext, language='text')
                    log_history("ECC", mode, ciphertext_b64, plaintext)
                except Exception as e:
                    st.error("Gagal mendekripsi. Pastikan format ciphertext benar.")
            else:
                st.warning("Masukkan ciphertext terlebih dahulu.")
