import streamlit as st
import base64
from tinyec import registry
import secrets

curve = registry.get_curve('brainpoolP256r1')

def compress_point(point):
    return hex(point.x) + hex(point.y % 2)[2:]

def ecc_encrypt(pubKey, plaintext):
    plaintext_bytes = plaintext.encode('utf-8')
    shared_secret = pubKey.x.to_bytes(32, 'big')
    encrypted = bytes([_a ^ _b for _a, _b in zip(plaintext_bytes, shared_secret)])
    return base64.b64encode(encrypted).decode('utf-8')

def ecc_decrypt(privKey, ciphertext_b64):
    ciphertext = base64.b64decode(ciphertext_b64)
    shared_secret = (privKey * curve.g).x.to_bytes(32, 'big')
    decrypted = bytes([_a ^ _b for _a, _b in zip(ciphertext, shared_secret)])
    return decrypted.decode('utf-8', errors='ignore')

def run(log_history):
    st.markdown("## 🔐 ECC Encryption / Decryption")

    st.info("""

ECC adalah metode kriptografi modern yang menggunakan kurva eliptik untuk mengenkripsi dan mendekripsi data.

🧠 **Keunggulan ECC**:
- Keamanan tinggi meski dengan kunci pendek
- Proses lebih cepat dan ringan
- Cocok untuk perangkat terbatas (IoT, mobile)

ECC bekerja dengan:
- **Private Key**: angka acak rahasia
- **Public Key**: hasil dari operasi private key × titik awal kurva (G)
- **Shared Secret**: digunakan untuk mengenkripsi teks (dengan XOR untuk demo ini)
""")

    st.markdown("### 🧮 Generate Key Pair")
    privKey = secrets.randbelow(curve.field.n)
    pubKey = privKey * curve.g

    st.write("**Public Key:**")
    st.code(f"({pubKey.x}, {pubKey.y})", language="python")
    st.write("**Private Key:**")
    st.code(f"{privKey}", language="python")

    mode = st.radio("📌 Pilih Mode", ["Enkripsi", "Dekripsi"])

    if mode == "Enkripsi":
        plaintext = st.text_area("✍️ Masukkan teks yang akan dienkripsi")
        if st.button("🔒 Enkripsi"):
            if plaintext:
                encrypted = ecc_encrypt(pubKey, plaintext)
                st.success("✅ Enkripsi berhasil!")
                st.code(encrypted, language="text")
                log_history("ECC", "Enkripsi", plaintext, encrypted)
            else:
                st.warning("Masukkan teks untuk dienkripsi.")
    else:
        ciphertext_b64 = st.text_area("📥 Masukkan ciphertext (base64) untuk didekripsi")
        if st.button("🔓 Dekripsi"):
            if ciphertext_b64:
                try:
                    decrypted = ecc_decrypt(privKey, ciphertext_b64)
                    st.success("✅ Dekripsi berhasil!")
                    st.code(decrypted, language="text")
                    log_history("ECC", "Dekripsi", ciphertext_b64, decrypted)
                except Exception as e:
                    st.error(f"❌ Gagal dekripsi: {e}")
            else:
                st.warning("Masukkan teks terenkripsi dalam base64.")
