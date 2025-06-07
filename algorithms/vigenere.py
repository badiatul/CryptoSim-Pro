import streamlit as st

def vigenere_cipher(text, key, mode):
    result = ""
    key = key.upper()
    key_len = len(key)
    j = 0
    for char in text:
        if char.isalpha():
            k = ord(key[j % key_len]) - ord('A')
            if mode == "Dekripsi":
                k = -k
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + k) % 26 + base)
            j += 1
        else:
            result += char
    return result

def run(log_history):
    st.header("🔐 Vigenère Cipher")
    st.markdown("""
    Vigenère Cipher adalah metode kriptografi dengan kunci berbentuk kata.  
    Setiap huruf pada kunci digunakan untuk mengenkripsi satu huruf pada pesan.

    - Misal plaintext: `HELLO` dan key: `KEY` → Enkripsi akan bergantian menggunakan `K`, `E`, `Y`, ...
    """)

    mode = st.radio("Pilih Mode", ["Enkripsi", "Dekripsi"])
    text = st.text_area("📝 Masukkan Teks")
    key = st.text_input("🔑 Kunci (huruf)")

    if st.button("🚀 Jalankan Vigenère Cipher"):
        if not text.strip() or not key.strip().isalpha():
            st.warning("Teks dan kunci harus valid.")
            return
        result = vigenere_cipher(text, key, mode)
        st.success(f"Hasil {mode}:")
        st.code(result)
        log_history("Vigenère Cipher", mode, text, result)
