import streamlit as st

def columnar_encrypt(text, key):
    key_order = sorted(list(key))
    col_order = [key.index(k) for k in key_order]
    rows = [text[i:i+len(key)] for i in range(0, len(text), len(key))]
    if len(rows[-1]) < len(key):
        rows[-1] += ' ' * (len(key) - len(rows[-1]))
    return ''.join(''.join(row[i] for row in rows) for i in col_order)

def columnar_decrypt(text, key):
    n_cols = len(key)
    n_rows = len(text) // n_cols
    key_order = sorted(list(key))
    col_order = [key.index(k) for k in key_order]
    cols = [''] * n_cols
    i = 0
    for idx in col_order:
        cols[idx] = text[i:i+n_rows]
        i += n_rows
    return ''.join(''.join(row) for row in zip(*cols))

def run(log_history):
    st.header("🔐 Columnar Transposition Cipher")
    st.markdown("""
    Columnar Transposition Cipher menyusun pesan dalam bentuk tabel, lalu membacanya berdasarkan urutan abjad kunci.
    """)

    mode = st.radio("Pilih Mode", ["Enkripsi", "Dekripsi"])
    text = st.text_area("📝 Masukkan Teks")
    key = st.text_input("🔑 Kunci (huruf unik)")

    if st.button("🚀 Jalankan Columnar Cipher"):
        if not text.strip() or not key.strip().isalpha():
            st.warning("Teks dan kunci tidak boleh kosong.")
            return
        result = columnar_encrypt(text, key) if mode == "Enkripsi" else columnar_decrypt(text, key)
        st.success(f"Hasil {mode}:")
        st.code(result)
        log_history("Columnar Transposition Cipher", mode, text, result)
