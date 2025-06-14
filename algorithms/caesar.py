import streamlit as st

def caesar_cipher(text, key, mode):
    result = ""
    for char in text:
        if char.isalpha():
            shift = key if mode == "Enkripsi" else -key
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result

def run(log_history):
    st.header("🔐 Caesar Cipher")
     st.write("Fitur ini sedang dikembangkan.")
    st.markdown("""
    Caesar Cipher adalah metode kriptografi klasik yang menggeser setiap huruf dalam teks
    sebanyak `k` posisi. Misalnya, jika `k = 3`, maka `A` menjadi `D`, `B` menjadi `E`, dst.

    - Gunakan **Enkripsi** untuk menyandikan pesan.
    - Gunakan **Dekripsi** untuk mengembalikan pesan semula.
    """)

    mode = st.radio("Pilih Mode", ["Enkripsi", "Dekripsi"])
    text = st.text_area("📝 Masukkan Teks")
    key = st.number_input("🔑 Kunci (angka)", min_value=1, max_value=25, value=3)

    if st.button("🚀 Jalankan Caesar Cipher"):
        if not text.strip():
            st.warning("Teks tidak boleh kosong.")
            return
        result = caesar_cipher(text, key, mode)
        st.success(f"Hasil {mode}:")
        st.code(result)
        log_history("Caesar Cipher", mode, text, result)
