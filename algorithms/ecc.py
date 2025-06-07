"""
ECC (Elliptic Curve Cryptography)
Menggunakan kunci privat & publik untuk mengenkripsi dan mendekripsi pesan
Simulasi dengan kurva 'secp192r1' dan metode titik kurva eliptik
"""

import streamlit as st
from tinyec import registry
import secrets
import hashlib

curve = registry.get_curve('secp192r1')

def encrypt_ECC(msg, pubKey):
    msg_bytes = msg.encode()
    privKey = secrets.randbelow(curve.field.n)
    sharedECCKey = privKey * pubKey
    secret = hashlib.sha256(int(sharedECCKey.x).to_bytes(24, 'big')).digest()
    ciphertext = bytes([msg_bytes[i] ^ secret[i % len(secret)] for i in range(len(msg_bytes))])
    return (privKey * curve.g, ciphertext)

def decrypt_ECC(encryptedMsg, privKey):
    sharedECCKey = privKey * encryptedMsg[0]
    secret = hashlib.sha256(int(sharedECCKey.x).to_bytes(24, 'big')).digest()
    decryptedMsg = bytes([encryptedMsg[1][i] ^ secret[i % len(secret)] for i in range(len(encryptedMsg[1]))])
    return decryptedMsg.decode(errors="ignore")

def run(log_history):
    st.subheader("🔐 ECC (Elliptic Curve Cryptography)")

    mode = st.radio("Pilih Mode", ["Enkripsi", "Dekripsi"])

    if mode == "Enkripsi":
        message = st.text_area("Masukkan Teks")
        if st.button("Enkripsi"):
            pubKey = secrets.randbelow(curve.field.n) * curve.g
            encrypted = encrypt_ECC(message, pubKey)
            hasil = f"{encrypted[0].x},{encrypted[0].y}||{encrypted[1].hex()}"
            st.success("Hasil Enkripsi:")
            st.code(hasil)
            log_history("ECC", "Enkripsi", message, hasil)

    else:  # Dekripsi
        data = st.text_area("Masukkan Hasil Enkripsi (format: x,y||hex_cipher)")
        priv = st.number_input("Masukkan Private Key (integer)", min_value=1)
        if st.button("Dekripsi"):
            try:
                pub_point, hex_cipher = data.split("||")
                x, y = map(int, pub_point.split(","))
                shared_point = curve.point_class(x, y, curve)
                cipher_bytes = bytes.fromhex(hex_cipher)
                decrypted = decrypt_ECC((shared_point, cipher_bytes), priv)
                st.success("Hasil Dekripsi:")
                st.code(decrypted)
                log_history("ECC", "Dekripsi", data, decrypted)
            except:
                st.error("Format input salah atau kunci tidak valid.")
