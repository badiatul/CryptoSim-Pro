import streamlit as st

def beaufort_cipher(text, key):
    text = text.upper()
    key = key.upper()
    result = ""
    key_index = 0
    for char in text:
        if char.isalpha():
            k = ord(key[key_index % len(key)]) - ord('A')
            c = (k - (ord(char) - ord('A'))) % 26
            result += chr(c + ord('A'))
            key_index += 1
        else:
            result += char
    return result

def run(log_history):
    st.header("🔐 Beaufort Cipher")
    st.markdown("""
    Beaufort Cipher mirip dengan Vigenère Cipher tetapi dengan perhitungan yang berbeda:  
    hasil = kunci - huruf. Algoritma ini **simetris**, jadi enkripsi dan dekripsi sama saja.
    """)

    text = st.text_area("📝 Masukkan Teks")
    key = st.text_input("🔑 Kunci (huruf)")

    if st.button("🚀 Jalankan Beaufort Cipher"):
        if not text.strip() or not key.strip().isalpha():
            st.warning("Teks dan kunci harus valid.")
            return
        result = beaufort_cipher(text, key)
        st.success("Hasil:")
        st.code(result)
        log_history("Beaufort Cipher", "Enkripsi/Dekripsi", text, result)
