import streamlit as st
import numpy as np

def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def hill_encrypt(text, key_matrix):
    text = text.upper().replace(" ", "")
    while len(text) % 2 != 0:
        text += 'X'
    result = ""
    for i in range(0, len(text), 2):
        pair = [ord(text[i]) - 65, ord(text[i+1]) - 65]
        res = np.dot(key_matrix, pair) % 26
        result += chr(res[0] + 65) + chr(res[1] + 65)
    return result

def hill_decrypt(text, key_matrix):
    det = int(np.round(np.linalg.det(key_matrix)))
    det_inv = mod_inverse(det % 26, 26)
    if det_inv is None:
        return "Matrix tidak dapat dibalik."
    adj = np.round(det * np.linalg.inv(key_matrix)).astype(int) % 26
    inv_matrix = (det_inv * adj) % 26
    return hill_encrypt(text, inv_matrix)

def run(log_history):
    st.subheader("🔐 Hill Cipher (2x2)")
    mode = st.radio("Pilih Mode", ["Enkripsi", "Dekripsi"])
    text = st.text_area("Masukkan Teks")
    a = st.number_input("Key[0][0]", 0, 25, 3)
    b = st.number_input("Key[0][1]", 0, 25, 3)
    c = st.number_input("Key[1][0]", 0, 25, 2)
    d = st.number_input("Key[1][1]", 0, 25, 5)
    if st.button("Proses"):
        key_matrix = np.array([[a, b], [c, d]])
        result = hill_encrypt(text, key_matrix) if mode == "Enkripsi" else hill_decrypt(text, key_matrix)
        st.success(result)
        log_history("Hill Cipher", mode, text, result)
