import streamlit as st

def create_matrix(key):
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    key = key.upper().replace("J", "I")
    seen = set()
    matrix = []
    for char in key + alphabet:
        if char not in seen:
            seen.add(char)
            matrix.append(char)
    return [matrix[i:i+5] for i in range(0, 25, 5)]

def process_text(text):
    text = text.upper().replace("J", "I")
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

def find_position(matrix, char):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == char:
                return i, j

def playfair_encrypt(text, key):
    matrix = create_matrix(key)
    text = process_text(text)
    result = ""
    for i in range(0, len(text), 2):
        a, b = text[i], text[i+1]
        ax, ay = find_position(matrix, a)
        bx, by = find_position(matrix, b)
        if ax == bx:
            result += matrix[ax][(ay+1)%5] + matrix[bx][(by+1)%5]
        elif ay == by:
            result += matrix[(ax+1)%5][ay] + matrix[(bx+1)%5][by]
        else:
            result += matrix[ax][by] + matrix[bx][ay]
    return result

def playfair_decrypt(text, key):
    matrix = create_matrix(key)
    result = ""
    for i in range(0, len(text), 2):
        a, b = text[i], text[i+1]
        ax, ay = find_position(matrix, a)
        bx, by = find_position(matrix, b)
        if ax == bx:
            result += matrix[ax][(ay-1)%5] + matrix[bx][(by-1)%5]
        elif ay == by:
            result += matrix[(ax-1)%5][ay] + matrix[(bx-1)%5][by]
        else:
            result += matrix[ax][by] + matrix[bx][ay]
    return result

def run(log_history):
    st.header("🔐 Playfair Cipher")
    mode = st.radio("Pilih mode", ["Enkripsi", "Dekripsi"])
    text = st.text_input("Masukkan teks")
    key = st.text_input("Masukkan kunci")
    if st.button("Proses"):
        result = playfair_encrypt(text, key) if mode == "Enkripsi" else playfair_decrypt(text, key)
        st.success(f"Hasil: {result}")
        log_history("Playfair Cipher", mode, text, result)
