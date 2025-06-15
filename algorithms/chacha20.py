"""
ChaCha20 Encryption/Decryption Module for CryptoSim Pro
Menggunakan PyCryptodome untuk proses kriptografi.
"""

import streamlit as st
from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes
import base64

def chacha20_encrypt(key, plaintext):
    cipher = ChaCha20.new(key=key)
    ciphertext = cipher.encrypt(plaintext.encode())
    return {
        "nonce": base64.b64encode(cipher.nonce).decode(),
        "ciphertext": base64.b64encode(ciphertext).decode()
    }

def chacha20_decrypt(key, nonce_b64, ciphertext_b64):
    nonce = base64.b64decode(nonce_b64)
    ciphertext = base64.b64decode(ciphertext_b64)
    cipher = ChaCha20.new(key=key, nonce=nonce)
    decrypted = cipher.decrypt(ciphertext)
    return decrypted.decode('utf-8', errors='ignore')

def run(log_history):
    st.markdown("## 🔐 ChaCha20 Encryption / Decryption")

    st.info("""
**📌 Tentang ChaCha20:**
- Algoritma enkripsi simetris modern yang cepat dan aman
- Digunakan dalam protokol seperti TLS, VPN, dan aplikasi mobile
- Menggunakan **key 256-bit (32 byte)** dan **nonce 96-bit (12 byte)**

🔑 Kunci harus sepanjang **32 karakter ASCII** (misalnya `12345678901234567890123456789012`)
""")

    key_input = st.text_input("Masukkan Kunci (32 karakter)", type="password", max_chars=32)
    if key_input and len(key_input) != 32:
        st.warning("Kunci harus tepat 32 karakter.")

    mode = st.radio("📌 Pilih Mode", ["Enkripsi", "Dekripsi"])

    if key_input and len(key_input) == 32:
        key = key_input.encode()

        if mode == "Enkripsi":
            plaintext = st.text_area("✍️ Masukkan teks yang akan dienkripsi")
            if st.button("🔒 Enkripsi"):
                result = chacha20_encrypt(key, plaintext)
                st.success("✅ Enkripsi berhasil!")
                st.code(f"Nonce: {result['nonce']}\nCiphertext: {result['ciphertext']}")
                log_history("ChaCha20", "Enkripsi", plaintext, f"Nonce: {result['nonce']}, Ciphertext: {result['ciphertext']}")
        
        else:
            nonce_b64 = st.text_input("📥 Masukkan Nonce (base64)")
            ciphertext_b64 = st.text_area("📥 Masukkan Ciphertext (base64)")
            if st.button("🔓 Dekripsi"):
                try:
                    decrypted = chacha20_decrypt(key, nonce_b64, ciphertext_b64)
                    st.success("✅ Dekripsi berhasil!")
                    st.code(decrypted)
                    log_history("ChaCha20", "Dekripsi", f"Nonce: {nonce_b64}, Ciphertext: {ciphertext_b64}", decrypted)
                except Exception as e:
                    st.error(f"❌ Gagal dekripsi: {e}")

                    # QR Code result
                    qr = qrcode.make(result)
                    buf = io.BytesIO()
                    qr.save(buf, format="PNG")
                    st.image(buf.getvalue(), caption="QR Code dari hasil", use_container_width=False)
