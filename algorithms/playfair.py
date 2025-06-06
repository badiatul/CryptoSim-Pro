import streamlit as st

def create_matrix(key):
    key = "".join(sorted(set(key.upper().replace("J", "I")), key=lambda x: key.index(x)))
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    matrix = []
    for c in key:
        if c not in matrix:
            matrix.append(c)
    for c in alphabet:
        if c not in matrix:
            matrix.append(c)
    return [matrix[i:i+5] for i in range(0, 25, 5)]

def find_position(matrix, char):
    for i, row in enumerate(matrix):
        for j, c in enumerate(row):
            if c == char:
                return i, j
    return None, None

def process_text(text):
    text = text.upper().replace("J", "I").replace(" ", "")
    processed = ""
    i = 0
    while i < len(text):
        a = text[i]
        b = text[i+1] if i+1 < len(text) else "X"
        if a == b:
            processed += a + "X"
            i += 1
        else:
            processed += a + b
            i += 2
    if len(processed) % 2 != 0:
        processed += "X"
    return processed

def playfair_encrypt(text, key):
    matrix = create_matrix(key)
    text = process_text(text)
    result = ""
    for i in range(0, len(text), 2):
        a, b = text[i], text[i+1]
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)
        if row1 == row2:
            result += matrix[row1][(col1+1)%5] + matrix[row2][(col2+1)%5]
        elif col1 == col2:
            result += matrix[(row1+1)%5][col1] + matrix[(row2+1)%5][col2]
        else:
            result += matrix[row1][col2] + matrix[row2][col1]
    return result

def playfair_decrypt(text, key):
    matrix = create_matrix(key)
    result = ""
    for i in range(0, len(text), 2):
        a, b = text[i], text[i+1]
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)
        if row1 == row2:
            result += matrix[row1][(col1-1)%5] + matrix[row2][(col2-1)%5]
        elif col1 == col2:
            result += matrix[(row1-1)%5][col1] + matrix[(row2-1)%5][col2]
        else:
            result += matrix[row1][col2] + matrix[row2][col1]
    return result

def run():
    st.header("🔐 Playfair Cipher")
    mode = st.radio("Pilih mode", ["Enkripsi", "Dekripsi"])
    text = st.text_input("Masukkan teks")
    key = st.text_input("Masukkan kunci (huruf)")
    if st.button("Proses") and key.isalpha():
        result = playfair_encrypt(text, key) if mode == "Enkripsi" else playfair_decrypt(text, key)
        st.success(f"Hasil: {result}")
def run():
    import streamlit as st
    from datetime import datetime
    from .cipher_utils import playfair_encrypt as encrypt, playfair_decrypt as decrypt

    mode = st.radio("Pilih Mode", ["Enkripsi", "Dekripsi"])
    teks = st.text_area("Masukkan Teks")
    key = st.text_input("Masukkan Kunci")

    if st.button("🔐 Proses"):
        if mode == "Enkripsi":
            hasil = encrypt(teks, key)
        else:
            hasil = decrypt(teks, key)
        st.success(hasil)

        st.session_state.history.append({
            "algoritma": "Playfair Cipher",
            "mode": mode,
            "input": teks,
            "hasil": hasil,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
