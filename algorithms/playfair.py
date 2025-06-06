import streamlit as st

def create_matrix(key):
    key = key.upper().replace("J", "I")
    seen = set()
    new_key = ""
    for c in key:
        if c.isalpha() and c not in seen:
            seen.add(c)
            new_key += c

    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    for c in alphabet:
        if c not in seen:
            new_key += c

    matrix = [list(new_key[i:i+5]) for i in range(0, 25, 5)]
    return matrix

def find_position(matrix, char):
    for i, row in enumerate(matrix):
        for j, c in enumerate(row):
            if c == char:
                return i, j
    return None, None

def process_text(text):
    text = text.upper().replace("J", "I").replace(" ", "")
    result = ""
    i = 0
    while i < len(text):
        a = text[i]
        b = text[i+1] if i+1 < len(text) else "X"
        if a == b:
            result += a + "X"
            i += 1
        else:
            result += a + b
            i += 2
    if len(result) % 2 != 0:
        result += "X"
    return result

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

def run(log_history):
    st.header("🔐 Playfair Cipher")
    mode = st.radio("Pilih mode", ["Enkripsi", "Dekripsi"])
    text = st.text_input("Masukkan teks")
    key = st.text_input("Masukkan kunci (huruf)")

    if st.button("Proses") and key.isalpha() and key != "":
        if mode == "Enkripsi":
            result = playfair_encrypt(text, key)
        else:
            result = playfair_decrypt(text, key)
        st.success(f"Hasil: {result}")
        log_history("Playfair Cipher", mode, text, result)
