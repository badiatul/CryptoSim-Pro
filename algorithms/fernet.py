"""
Fernet Encryption/Decryption Module for CryptoSim Pro
Menggunakan kunci simetris 32-byte base64.
Tersedia fitur: generate otomatis, unggah kunci, salin & simpan kunci.
"""

import streamlit as st
from cryptography.fernet import Fernet
import base64

def run(log_history):
    st.markdown("## 🔐 Fernet Encryption / Decryption")
    
    # Penjelasan singkat
    with st.expander("📖 Penjelasan Tentang Kunci"):
        st.markdown("""
        - Fernet menggunakan **kunci simetris** (kunci yang sama untuk enkripsi dan dekripsi).
        - Format kunci adalah **Base64**, terdiri dari 44 karakter.
        - Kamu bisa membuat kunci otomatis atau mengunggah kunci dari file.
        - **Simpan kunci baik-baik**, karena jika hilang, data tidak bisa didekripsi kembali.
        """)

    # Pilih mode
    mode = st.radio("Pilih Mode", ["Enkripsi", "Dekripsi"])

    if mode == "Enkripsi":
        st.subheader("🧮 Generate Key")
        if st.button("🔑 Buat Kunci Baru Otomatis"):
            key = Fernet.generate_key()
            st.session_state.fernet_key = key  # simpan untuk digunakan nanti
            st.success(f"Kunci berhasil dibuat: `{key.decode()}`")

            st.download_button(
                label="📥 Unduh Kunci",
                data=key,
                file_name="fernet_key.key",
                mime="application/octet-stream"
            )

        if "fernet_key" in st.session_state:
            key = st.session_state.fernet_key
            fernet = Fernet(key)

            plaintext = st.text_area("Masukkan teks yang akan dienkripsi")
            if st.button("🔒 Enkripsi"):
                if plaintext:
                    token = fernet.encrypt(plaintext.encode()).decode()
                    st.success(f"Hasil Enkripsi:\n\n{token}")
                    log_history("Fernet", "Enkripsi", plaintext, token)
                else:
                    st.warning("Teks tidak boleh kosong.")
        else:
            st.info("Silakan buat kunci terlebih dahulu untuk memulai enkripsi.")

    else:  # Dekripsi
        st.subheader("📤 Unggah Kunci")
        uploaded_file = st.file_uploader("Unggah file kunci .key (base64)", type=["key"])
        if uploaded_file:
            key = uploaded_file.read()
            try:
                fernet = Fernet(key)
                ciphertext = st.text_area("Masukkan teks terenkripsi (token)")
                if st.button("🔓 Dekripsi"):
                    if ciphertext:
                        try:
                            decrypted = fernet.decrypt(ciphertext.encode()).decode()
                            st.success(f"Hasil Dekripsi:\n\n{decrypted}")
                            log_history("Fernet", "Dekripsi", ciphertext, decrypted)
                        except Exception as e:
                            st.error(f"Gagal mendekripsi: {e}")
                    else:
                        st.warning("Teks terenkripsi tidak boleh kosong.")
            except Exception:
                st.error("Kunci tidak valid. Pastikan file yang diunggah adalah kunci Fernet base64 32-byte.")
        else:
            st.info("Silakan unggah file kunci yang valid untuk memulai dekripsi.")
