"""
Fernet Encryption/Decryption Module for CrypTosca Pro
Menggunakan kunci simetris 32-byte (base64). Mendukung generate otomatis dan copy-paste manual.
"""

import streamlit as st
from cryptography.fernet import Fernet
import qrcode
import io

def run(log_history):
    st.markdown("## 🔐 Fernet Encryption / Decryption")

    # Penjelasan tentang Fernet
    st.markdown("""
📌 **Tentang Fernet:**
- Algoritma kriptografi modern dan **simetris**
- Menghasilkan token terenkripsi yang sudah menyimpan **integritas dan waktu**
- Menggunakan **kunci base64 44 karakter**
- Praktis dan aman digunakan di aplikasi modern

🔑 **Kunci Fernet:**
- Bisa di-*generate* otomatis (dari tombol)
- Bisa di-*paste* dari hasil sebelumnya
- Jika salah kunci, dekripsi akan gagal
""")

    # Pilih mode
    mode = st.radio("Pilih Mode", ["Enkripsi", "Dekripsi"])

    if mode == "Enkripsi":
        st.subheader("🧮 Buat atau Masukkan Kunci")
        if st.button("🔑 Buat Kunci Baru Otomatis"):
            key = Fernet.generate_key()
            st.session_state.fernet_key = key.decode()

        key_input = st.text_input("Masukkan atau tempel kunci (Base64)", value=st.session_state.get("fernet_key", ""))

        plaintext = st.text_area("Masukkan teks yang akan dienkripsi")

        if st.button("🔒 Enkripsi"):
            if not key_input or len(key_input) != 44:
                st.error("Kunci tidak valid. Harus 44 karakter Base64.")
                return
            if not plaintext:
                st.warning("Teks tidak boleh kosong.")
                return
            try:
                fernet = Fernet(key_input.encode())
                token = fernet.encrypt(plaintext.encode()).decode()
                st.success("✅ Hasil Enkripsi:")
                st.code(token)

                # QR Code dari hasil
                qr = qrcode.make(token)
                buf = io.BytesIO()
                qr.save(buf, format="PNG")
                st.image(buf.getvalue(), caption="📌 QR Code dari hasil enkripsi", use_container_width=False)

                st.info("💾 Simpan kunci ini untuk proses dekripsi:")
                st.code(key_input)
                log_history("Fernet", "Enkripsi", plaintext, token)
            except Exception as e:
                st.error(f"Kesalahan enkripsi: {e}")

    else:  # Dekripsi
        st.subheader("🔐 Masukkan Kunci yang Pernah Digunakan untuk Enkripsi")
        key_input = st.text_input("Tempelkan kunci (Base64)", "")
        ciphertext = st.text_area("Tempelkan teks terenkripsi (token)")

        if st.button("🔓 Dekripsi"):
            if not key_input or len(key_input) != 44:
                st.error("Kunci tidak valid. Harus 44 karakter Base64.")
                return
            if not ciphertext:
                st.warning("Teks terenkripsi tidak boleh kosong.")
                return
            try:
                fernet = Fernet(key_input.encode())
                decrypted = fernet.decrypt(ciphertext.encode()).decode()
                st.success("✅ Hasil Dekripsi:")
                st.code(decrypted)

                # QR Code dari hasil
                qr = qrcode.make(decrypted)
                buf = io.BytesIO()
                qr.save(buf, format="PNG")
                st.image(buf.getvalue(), caption="📌 QR Code dari hasil dekripsi", use_container_width=False)

                log_history("Fernet", "Dekripsi", ciphertext, decrypted)
            except Exception as e:
                st.error(f"Kesalahan dekripsi: {e}")
