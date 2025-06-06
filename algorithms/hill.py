import streamlit as st
from utils import log_history
import numpy as np

def mod_inverse(a, m):
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return None

def encrypt(text, matrix):
    text = text.upper().replace(" ", "")
    while len(text) % 2 != 0:
        text += "X"

    result = ""
    for i in range(0, len(text), 2):
        pair = [ord(text[i]) - 65, ord(text[i+1]) - 65]
        res = np.dot(matrix, pair) % 26
        result += chr(res[0] + 65) + chr(res[1] + 65)
    return result

def decrypt(text, matrix):
    det = int(np.round(np.linalg.det(matrix))) % 26
    inv_det = mod_inverse(det, 26)
    if inv_det is None:
        return "Matriks tidak memiliki invers modulo 26"

    adj = np.round(np.linalg.inv(matrix) * det).astype(int)
    inv_matrix = (inv_det * adj) % 26

    result = ""
    for i in range(0, len(text), 2):
        pair = [ord(text[i]) - 65, ord(text[i+1]) - 65]
        res = np.dot(inv_matrix, pair) % 26
        result += chr(res[0] + 65) + chr(res[1] + 65)
    return result

def run():
    st.header("🔐 Hill Cipher")
    mode = st.radio("Pilih mode", ["Enkripsi", "Dekripsi"])
    text = st.text_area("Masukkan teks (jumlah huruf genap)")
    
    m11 = st.number_input("Matriks M[0][0]", value=3)
    m12 = st.number_input("Matriks M[0][1]", value=3)
    m21 = st.number_input("Matriks M[1][0]", value=2)
    m22 = st.number_input("Matriks M[1][1]", value=5)
    
    matrix = np.array([[m11, m12], [m21, m22]])

    if st.button("Proses"):
        result = encrypt(text, matrix) if mode == "Enkripsi" else decrypt(text, matrix)
        st.success(f"Hasil: {result}")
        log_history("Hill Cipher", mode, text, result)
