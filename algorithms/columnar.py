# algorithms/columnar.py
import streamlit as st

def encrypt(plaintext, key):
    key_order = sorted(range(len(key)), key=lambda k: key[k])
    columns = ['' for _ in range(len(key))]
    for i, char in enumerate(plaintext):
        columns[i % len(key)] += char
    ciphertext = ''.join([columns[i] for i in key_order])
    return ciphertext

def decrypt(ciphertext, key):
    key_order = sorted(range(len(key)), key=lambda k: key[k])
    n_rows = len(ciphertext) // len(key)
    n_extra = len(ciphertext) % len(key)
    
    columns = ['' for _ in range(len(key))]
    pos = 0
    for i in range(len(key)):
        col_len = n_rows + (1 if key_order.index(i) < n_extra else 0)
        columns[i] = ciphertext[pos:pos + col_len]
        pos += col_len

    plaintext = ''
    for i in range(n_rows + 1):
        for j in key_order:
            if i < len(columns[j]):
                plaintext += columns[j][i]
    return plaintext

def run(log_history):
    st.subheader("🔐 Columnar Transposition Cipher")
    mode = st.radio("Mode", ["Enkripsi", "Dekripsi"])
    text = st.text_area("Masukkan teks (tanpa spasi)")
    key = st.text_input("Masukkan kunci (huruf saja)")

    if st.button("Proses"):
        if not key.isalpha():
            st.error("Kunci harus berupa huruf.")
            return
        if mode == "Enkripsi":
            result = encrypt(text.replace(" ", ""), key.upper())
        else:
            result = decrypt(text.replace(" ", ""), key.upper())
        st.success(result)
        log_history("Columnar Transposition Cipher", mode, text, result)
