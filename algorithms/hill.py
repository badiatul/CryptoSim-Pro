import streamlit as st
import numpy as np

def mod_inverse(matrix, modulus):
    det = int(np.round(np.linalg.det(matrix)))
    det_inv = pow(det, -1, modulus)
    matrix_mod_inv = det_inv * np.round(det * np.linalg.inv(matrix)).astype(int) % modulus
    return matrix_mod_inv

def text_to_matrix(text):
    return [ord(c.upper()) - 65 for c in text]

def matrix_to_text(matrix):
    return ''.join([chr(int(round(num)) % 26 + 65) for num in matrix])

def encrypt(text, key):
    text = text.upper().replace(" ", "")
    while len(text) % 2 != 0:
        text += 'X'
    key_matrix = np.array(key)
    result = ""
    for i in range(0, len(text), 2):
        pair = np.array(text_to_matrix(text[i:i+2]))
        enc = np.dot(key_matrix, pair) % 26
        result += matrix_to_text(enc)
    return result

def decrypt(cipher, key):
    key_matrix = np.array(key)
    inv_key = mod_inverse(key_matrix, 26)
    result = ""
    for i in range(0, len(cipher), 2):
        pair = np.array(text_to_matrix(cipher[i:i+2]))
        dec = np.dot(inv_key, pair) % 26
        result += matrix_to_text(dec)
    return result

def run(log_history):
    st.header("🔐 Hill Cipher")
    mode = st.radio("Pilih mode", ["Enkripsi", "Dekripsi"])
    text = st.text_input("Masukkan teks")
    matrix_input = st.text_input("Masukkan matriks kunci 2x2 (misal: 3,3,2,5)")
    if st.button("Proses"):
        try:
            values = list(map(int, matrix_input.split(',')))
            if len(values) != 4:
                st.error("Matriks harus terdiri dari 4 angka")
                return
            key = [[values[0], values[1]], [values[2], values[3]]]
            result = encrypt(text, key) if mode == "Enkripsi" else decrypt(text, key)
            st.success(f"Hasil: {result}")
            log_history("Hill Cipher", mode, text, result)
        except:
            st.error("Format matriks tidak valid")
