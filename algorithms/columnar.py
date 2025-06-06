# algorithms/columnar.py
import streamlit as st

def encrypt(text, key):
    num_cols = len(key)
    num_rows = (len(text) + num_cols - 1) // num_cols
    padded_text = text.ljust(num_rows * num_cols)
    table = [padded_text[i::num_rows] for i in range(num_rows)]
    sorted_key = sorted([(k, i) for i, k in enumerate(key)])
    return ''.join([table[i][j] for k, i in sorted_key for j in range(num_rows)])

def decrypt(ciphertext, key):
    num_cols = len(key)
    num_rows = (len(ciphertext) + num_cols - 1) // num_cols
    sorted_key = sorted([(k, i) for i, k in enumerate(key)])
    columns = [''] * num_cols
    idx = 0
    for k, i in sorted_key:
        columns[i] = ciphertext[idx:idx + num_rows]
        idx += num_rows
    return ''.join(''.join(row) for row in zip(*columns)).strip()

def run(log_history):
    st.subheader("📤 Columnar Transposition Cipher")
    mode = st.radio("Mode", ["Enkripsi", "Dekripsi"])
    text = st.text_area("Masukkan teks")
    key = st.text_input("Masukkan kunci")

    if st.button("Proses"):
        if not key:
            st.error("Kunci tidak boleh kosong.")
            return
        result = encrypt(text, key) if mode == "Enkripsi" else decrypt(text, key)
        st.success(result)
        log_history("Columnar Transposition Cipher", mode, text, result)
# algorithms/columnar.py
import streamlit as st

def run(log_history):
    st.subheader("📤 Columnar Transposition Cipher")
    st.write("Ini hanya uji coba awal, fungsi belum aktif.")
    if st.button("Test Log"):
        log_history("Columnar Cipher", "Test Mode", "abc", "xyz")
        st.success("Berhasil ditambahkan ke riwayat.")
