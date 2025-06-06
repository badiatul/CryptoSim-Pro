import streamlit as st

def run(log_history):
    st.subheader("🔐 Beaufort Cipher")

    mode = st.radio("Pilih Mode", ["Enkripsi", "Dekripsi"])
    text = st.text_area("Masukkan Teks")
    key = st.text_input("Masukkan Kunci")

    if st.button("Proses"):
        if mode == "Enkripsi":
            result = beaufort_encrypt(text, key)
        else:
            result = beaufort_decrypt(text, key)

        st.success(result)
        log_history("Beaufort Cipher", mode, text, result)

def beaufort_encrypt(text, key):
    # Tambahkan logika enkripsi Beaufort di sini
    return "Hasil enkripsi"

def beaufort_decrypt(text, key):
    # Tambahkan logika dekripsi Beaufort di sini
    return "Hasil dekripsi"
