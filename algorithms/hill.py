import streamlit as st
import numpy as np

def mod26_inv(matrix):
    det = int(round(np.linalg.det(matrix))) % 26
    det_inv = None
    for i in range(26):
        if (det * i) % 26 == 1:
            det_inv = i
            break
    if det_inv is None:
        return None
    matrix_mod_inv = (det_inv * np.round(det * np.linalg.inv(matrix)).astype(int)) % 26
    return matrix_mod_inv

def process_text(text):
    text = text.upper().replace(" ", "")
    while len(text) % 2 != 0:
        text += "X"
    return text

def text_to_matrix(text):
    return np.array([ord(c) - 65 for c in text]).reshape(-1, 2).T

def matrix_to_text(matrix):
    return "".join([chr(int(c) + 65) for c in matrix.T.flatten()])

def hill_encrypt(text, key_matrix):
    text = process_text(text)
    text_matrix = text_to_matrix(text)
    encrypted_matrix = (key_matrix.dot(text_matrix)) % 26
    return matrix_to_text(encrypted_matrix)

def hill_decrypt(text, key_matrix):
    inv_key = mod26_inv(key_matrix)
    if inv_key is None:
        return None
    text_matrix = text_to_matrix(text)
    decrypted_matrix = (inv_key.dot(text_matrix)) % 26
    return matrix_to_text(decrypted_matrix)

def run(log_history):
    st.header("🔐 Hill Cipher")
    mode = st.radio("Pilih mode", ["Enkripsi", "Dekripsi"])
    text = st.text_input("Masukkan teks")
    key_input = st.text_input("Masukkan kunci matriks 2x2 (pisah dengan koma, misal: 3,3,2,5)")

    if st.button("Proses"):
        try:
            key_list = list(map(int, key_input.split(',')))
            if len(key_list) != 4:
                st.error("Kunci harus berisi 4 angka dipisah koma.")
                return
            key_matrix = np.array(key_list).reshape(2, 2)
        except:
            st.error("Format kunci salah.")
            return

        if mode == "Enkripsi":
            result = hill_encrypt(text, key_matrix)
            if result is None:
                st.error("Kunci matriks tidak invertible modulo 26.")
                return
        else:
            result = hill_decrypt(text, key_matrix)
            if result is None:
                st.error("Kunci matriks tidak invertible modulo 26.")
                return
        st.success(f"Hasil: {result}")
        log_history("Hill Cipher", mode, text, result)
