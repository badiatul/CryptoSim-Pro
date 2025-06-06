import streamlit as st
import numpy as np

def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def matrix_mod_inv(matrix, mod):
    det = int(np.round(np.linalg.det(matrix)))
    det_inv = mod_inverse(det % mod, mod)
    if det_inv is None:
        return None
    matrix_inv = np.round(det_inv * np.linalg.inv(matrix) * det).astype(int) % mod
    return matrix_inv

def text_to_nums(text):
    return [ord(c.upper()) - ord('A') for c in text if c.isalpha()]

def nums_to_text(nums):
    return ''.join(chr(int(n % 26) + ord('A')) for n in nums)

def hill_encrypt(text, key_matrix):
    nums = text_to_nums(text)
    while len(nums) % 2 != 0:
        nums.append(ord('X') - ord('A'))
    pairs = np.array(nums).reshape(-1, 2)
    result = []
    for pair in pairs:
        encrypted = np.dot(key_matrix, pair) % 26
        result.extend(encrypted)
    return nums_to_text(result)

def hill_decrypt(text, key_matrix):
    matrix_inv = matrix_mod_inv(key_matrix, 26)
    if matrix_inv is None:
        return "Matrix tidak bisa dibalik!"
    nums = text_to_nums(text)
    pairs = np.array(nums).reshape(-1, 2)
    result = []
    for pair in pairs:
        decrypted = np.dot(matrix_inv, pair) % 26
        result.extend(decrypted)
    return nums_to_text(result)

def run():
    st.header("🔐 Hill Cipher")
    mode = st.radio("Pilih mode", ["Enkripsi", "Dekripsi"])
    text = st.text_input("Masukkan teks")
    m11 = st.number_input("Kunci [0,0]", value=3)
    m12 = st.number_input("Kunci [0,1]", value=3)
    m21 = st.number_input("Kunci [1,0]", value=2)
    m22 = st.number_input("Kunci [1,1]", value=5)
    key_matrix = np.array([[m11, m12], [m21, m22]])
    if st.button("Proses"):
        result = hill_encrypt(text, key_matrix) if mode == "Enkripsi" else hill_decrypt(text, key_matrix)
        st.success(f"Hasil: {result}")
def run():
    import streamlit as st
    from datetime import datetime
    from .cipher_utils import hill_encrypt as encrypt, hill_decrypt as decrypt

    mode = st.radio("Pilih Mode", ["Enkripsi", "Dekripsi"])
    teks = st.text_area("Masukkan Teks")
    key = st.text_input("Masukkan Matriks Kunci (misal: 2 3; 1 4)")

    if st.button("🔐 Proses"):
        if mode == "Enkripsi":
            hasil = encrypt(teks, key)
        else:
            hasil = decrypt(teks, key)
        st.success(hasil)

        st.session_state.history.append({
            "algoritma": "Hill Cipher",
            "mode": mode,
            "input": teks,
            "hasil": hasil,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
