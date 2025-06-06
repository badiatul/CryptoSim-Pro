# algorithms/columnar.py
import streamlit as st

def encrypt(text, key):
    n_cols = len(key)
    n_rows = (len(text) + n_cols - 1) // n_cols
    matrix = [['' for _ in range(n_cols)] for _ in range(n_rows)]
    
    index = 0
    for i in range(n_rows):
        for j in range(n_cols):
            if index < len(text):
                matrix[i][j] = text[index]
                index += 1
    
    key_order = sorted(list(enumerate(key)), key=lambda x: x[1])
    ciphertext = ''
    for idx, _ in key_order:
        for row in matrix:
            ciphertext += row[idx]
    return ciphertext

def decrypt(text, key):
    n_cols = len(key)
    n_rows = (len(text) + n_cols - 1) // n_cols
    matrix = [['' for _ in range(n_cols)] for _ in range(n_rows)]

    key_order = sorted(list(enumerate(key)), key=lambda x: x[1])
    index = 0
    for idx, _ in key_order:
        for i in range(n_rows):
            if index < len(text):
                matrix[i][idx] = text[index]
                index += 1

    plaintext = ''
    for row in matrix:
        for char in row:
            plaintext += char
    return plaintext.strip()

def run(log_history):
    st.subheader("📤 Columnar Transposition Cipher")
    mode = st.radio("Mode", ["Enkripsi", "Dekripsi"])
    text = st.text_area("Masukkan teks")
    key = st.text_input("Masukkan kunci (huruf, minimal 2 karakter)")

    if st.button("Proses"):
        if len(key) < 2 or not key.isalpha():
            st.error("Kunci harus berupa huruf dan minimal 2 karakter.")
            return

        result = encrypt(text.replace(" ", ""), key.lower()) if mode == "Enkripsi" else decrypt(text, key.lower())
        st.success(result)
        log_history("Columnar Transposition Cipher", mode, text, result)
