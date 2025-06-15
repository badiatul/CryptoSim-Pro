"""
Hill Cipher Module for CrypTosca Pro
Menggunakan matriks kunci persegi (2x2 atau 3x3) untuk mengenkripsi atau mendekripsi blok huruf teks.
Kunci harus memiliki invers modulo 26 agar dapat digunakan untuk dekripsi.
"""

import streamlit as st
import numpy as np

def mod_inverse(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def matrix_mod_inv(matrix, mod):
    det = int(round(np.linalg.det(matrix)))
    inv_det = mod_inverse(det % mod, mod)
    if inv_det is None:
        return None
    matrix_mod = np.round(np.linalg.inv(matrix) * det).astype(int) * inv_det
    return matrix_mod % mod

def text_to_matrix(text, n):
    text = ''.join(filter(str.isalpha, text.upper()))
    while len(text) % n != 0:
        text += 'X'
    return [list(map(lambda c: ord(c) - 65, text[i:i+n])) for i in range(0, len(text), n)]

def matrix_to_text(matrix):
    return ''.join(chr(int(round(val)) % 26 + 65) for row in matrix for val in row)

def hill_cipher(text, key_matrix, mode):
    n = key_matrix.shape[0]
    blocks = text_to_matrix(text, n)
    if mode == "Dekripsi":
        key_matrix = matrix_mod_inv(key_matrix, 26)
        if key_matrix is None:
            return "Kunci tidak dapat dibalik. Gunakan matriks lain."
    result_blocks = [(np.dot(block, key_matrix) % 26).tolist() for block in blocks]
    return matrix_to_text(result_blocks)

def run(log_history):
    st.header("🔐 Hill Cipher")
    st.markdown("""
    Hill Cipher adalah algoritma klasik yang menggunakan **aljabar linear** untuk mengenkripsi teks dalam blok huruf menggunakan matriks.

    🔢 **Kunci** berupa matriks persegi, contohnya:
    ```
    3,3
    2,5
    ```
    🧮 Enkripsi dilakukan dengan:
    > C = P × K mod 26  
    dan dekripsi dengan:
    > P = C × K⁻¹ mod 26

    ❗ Pastikan determinan matriks memiliki **invers modulo 26**, jika tidak maka dekripsi tidak dapat dilakukan.
    """)

    mode = st.radio("Pilih Mode", ["Enkripsi", "Dekripsi"])
    text = st.text_area("📝 Masukkan Teks (huruf saja)")
    key_input = st.text_area("🔑 Masukkan Matriks Kunci (pisahkan dengan koma dan baris baru)", placeholder="Contoh:\n3,3\n2,5")

    if st.button("🚀 Jalankan Hill Cipher"):
        if not text.strip() or not key_input.strip():
            st.warning("Teks dan kunci tidak boleh kosong.")
            return
        try:
            rows = key_input.strip().split("\n")
            key_matrix = np.array([[int(num) for num in row.split(",")] for row in rows])
            if key_matrix.shape[0] != key_matrix.shape[1]:
                st.error("Matriks harus persegi (2x2, 3x3, dll).")
                return
        except:
            st.error("Format matriks salah. Gunakan angka dan koma dengan benar.")
            return
        result = hill_cipher(text, key_matrix, mode)
        st.success(f"Hasil {mode}:")
        st.code(result)
        log_history("Hill Cipher", mode, text, result)
