"""
ECC Encryption/Decryption Module for CryptoSim Pro
Menggunakan encoding Base64 untuk hasil enkripsi agar kompatibel dengan Streamlit dan unduhan.
"""

import streamlit as st
import base64
from tinyec import registry
import secrets

curve = registry.get_curve('brainpoolP256r1')

def compress_point(point):
    return hex(point.x) + hex(point.y % 2)[2:]

def ecc_encrypt(pubKey, plaintext):
    plaintext_bytes = plaintext.encode('utf-8')
    # Simple XOR dengan shared secret (contoh demo)
    shared_secret = pubKey.x.to_bytes(32, 'big')
    encrypted = bytes([_a ^ _b for _a, _b in zip(plaintext_bytes, shared_secret)])
    # encode ke base64 string supaya aman simpan & tampil
    return base64.b64encode(encrypted).decode('utf-8')

def ecc_decrypt(privKey, ciphertext_b64):
    ciphertext = base64.b64decode(ciphertext_b64)
    shared_secret = privKey.public_key.x.to_bytes(32, 'big')
    decrypted = bytes([_a ^ _b for _a, _b in zip(ciphertext, shared_secret)])
    return decrypted.decode('utf-8', errors='ignore')

def run(log_history):
    st.markdown("## ECC Encryption / Decryption")
    
    privKey = secrets.randbelow(curve.field.n)
    pubKey = privKey * curve.g
    
    st.write("**Public Key:**", f"({pubKey.x}, {pubKey.y})")
    st.write("**Private Key:**", privKey)
    
    mode = st.radio("Pilih Mode", ["Enkripsi", "Dekripsi"])
    
    if mode == "Enkripsi":
        plaintext = st.text_area("Masukkan teks yang akan dienkripsi")
        if st.button("Enkripsi"):
            if plaintext:
                encrypted = ecc_encrypt(pubKey, plaintext)
                st.success(f"Hasil Enkripsi (base64): {encrypted}")
                log_history("ECC", "Enkripsi", plaintext, encrypted)
            else:
                st.warning("Masukkan teks untuk dienkripsi.")
    else:  # Dekripsi
        ciphertext_b64 = st.text_area("Masukkan teks base64 yang akan didekripsi")
        if st.button("Dekripsi"):
            if ciphertext_b64:
                try:
                    decrypted = ecc_decrypt(privKey, ciphertext_b64)
                    st.success(f"Hasil Dekripsi: {decrypted}")
                    log_history("ECC", "Dekripsi", ciphertext_b64, decrypted)
                except Exception as e:
                    st.error(f"Gagal dekripsi: {e}")
            else:
                st.warning("Masukkan teks base64 untuk didekripsi.")
