"""
ECC Encryption/Decryption Module for CryptoSim Pro
Menggunakan kurva brainpoolP256r1 dengan metode XOR sederhana terhadap shared secret.
Hasil enkripsi diencode dalam Base64 agar aman untuk ditampilkan dan disimpan.
"""

import streamlit as st
import base64
from tinyec import registry
import secrets

# Gunakan kurva eliptik brainpoolP256r1
curve = registry.get_curve('brainpoolP256r1')

# Fungsi untuk mengenkripsi teks
def ecc_encrypt(pubKey, plaintext):
    plaintext_bytes = plaintext.encode('utf-8')
    shared_secret = pubKey.x.to_bytes(32, 'big')  # shared secret berupa bilangan dari x
    encrypted = bytes([_a ^ _b for _a, _b in zip(plaintext_bytes, shared_secret)])
    return base64.b64encode(encrypted).decode('utf-8')  # encode ke base64 untuk tampil & simpan

# Fungsi untuk mendekripsi teks
def ecc_decrypt(privKey, pubKey, ciphertext_b64):
    ciphertext = base64.b64decode(ciphertext_b64)
    shared_secret = (privKey * pubKey).x.to_bytes(32, 'big')
    decrypted = bytes([_a ^ _b for _a, _b in zip(ciphertext, shared_secret)])
    return decrypted.decode('utf-8', errors='ignore')

# Fungsi utama yang akan dijalankan di Streamlit
def run(log_history):
    st.markdown("## 🔐 ECC Encryption / Decryption")

        st.info("""
ECC adalah metode kriptografi modern yang menggunakan titik-titik pada kurva eliptik untuk mengenkripsi dan mendekripsi data. Kelebihannya adalah:

🔐 **Keamanan tinggi** — ECC menawarkan tingkat keamanan setara RSA tetapi dengan ukuran kunci yang jauh lebih kecil.  
⚡ **Lebih cepat dan efisien** — Cocok untuk perangkat terbatas seperti smartphone atau IoT.  
🔑 **Kunci Publik dan Privat** — Proses enkripsi dilakukan dengan kunci publik, dan dekripsi hanya bisa dilakukan dengan kunci privat.

Pada demo ini:
- **Shared secret** dibentuk dari hasil operasi `private_key * public_key`.
- Teks dienkripsi dengan metode XOR terhadap shared secret (untuk kemudahan demo).
- Hasil enkripsi dikonversi ke **base64** agar bisa ditampilkan dan diunduh dengan aman.
    """)

    st.markdown("### 🧮 Generate Key Pair")
    privKey = secrets.randbelow(curve.field.n)
    pubKey = privKey * curve.g

    # Tampilkan kunci publik dan privat
    st.write("**Public Key:**")
    st.code(f"({pubKey.x}, {pubKey.y})", language="python")
    st.write("**Private Key:**")
    st.code(f"{privKey}", language="python")

    mode = st.radio("Pilih Mode", ["Enkripsi", "Dekripsi"])

    if mode == "Enkripsi":
        plaintext = st.text_area("Masukkan teks yang akan dienkripsi")
        if st.button("Enkripsi"):
            if plaintext:
                encrypted = ecc_encrypt(pubKey, plaintext)
                st.success("✅ Enkripsi berhasil!")
                st.code(encrypted, language="text")
                log_history("ECC", "Enkripsi", plaintext, encrypted)
            else:
                st.warning("⚠️ Masukkan teks terlebih dahulu.")
    else:  # Dekripsi
        ciphertext_b64 = st.text_area("Masukkan ciphertext (base64)")
        pubkey_x = st.text_input("Masukkan X dari Public Key")
        pubkey_y = st.text_input("Masukkan Y dari Public Key")
        priv_input = st.text_input("Masukkan Private Key", type="password")

        if st.button("Dekripsi"):
            if ciphertext_b64 and pubkey_x and pubkey_y and priv_input:
                try:
                    pubKey_decrypt = curve.point_class(int(pubkey_x), int(pubkey_y), curve)
                    privKey_decrypt = int(priv_input)
                    decrypted = ecc_decrypt(privKey_decrypt, pubKey_decrypt, ciphertext_b64)
                    st.success("✅ Dekripsi berhasil!")
                    st.code(decrypted, language="text")
                    log_history("ECC", "Dekripsi", ciphertext_b64, decrypted)
                except Exception as e:
                    st.error(f"❌ Gagal mendekripsi: {e}")
            else:
                st.warning("⚠️ Lengkapi semua isian terlebih dahulu untuk dekripsi.")
