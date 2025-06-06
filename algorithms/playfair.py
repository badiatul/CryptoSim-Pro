import streamlit as st

def prepare_input(text):
    text = text.upper().replace('J', 'I')
    prepared = ''
    i = 0
    while i < len(text):
        a = text[i]
        b = text[i+1] if i+1 < len(text) else 'X'
        if a == b:
            prepared += a + 'X'
            i += 1
        else:
            prepared += a + b
            i += 2
    if len(prepared) % 2 != 0:
        prepared += 'X'
    return prepared

def create_matrix(key):
    key = key.upper().replace('J', 'I')
    seen = set()
    matrix = []
    for char in key + 'ABCDEFGHIKLMNOPQRSTUVWXYZ':
        if char not in seen:
            seen.add(char)
            matrix.append(char)
    return [matrix[i:i+5] for i in range(0, 25, 5)]

def find_pos(matrix, char):
    for i, row in enumerate(matrix):
        if char in row:
            return i, row.index(char)

def process_pair(a, b, matrix, mode):
    ax, ay = find_pos(matrix, a)
    bx, by = find_pos(matrix, b)
    if ax == bx:
        return (matrix[ax][(ay+1)%5], matrix[bx][(by+1)%5]) if mode == 'Enkripsi' else (matrix[ax][(ay-1)%5], matrix[bx][(by-1)%5])
    elif ay == by:
        return (matrix[(ax+1)%5][ay], matrix[(bx+1)%5][by]) if mode == 'Enkripsi' else (matrix[(ax-1)%5][ay], matrix[(bx-1)%5][by])
    else:
        return matrix[ax][by], matrix[bx][ay]

def cipher(text, key, mode):
    matrix = create_matrix(key)
    text = prepare_input(text)
    result = ''
    for i in range(0, len(text), 2):
        a, b = process_pair(text[i], text[i+1], matrix, mode)
        result += a + b
    return result

def run(log_history):
    st.subheader("🔐 Playfair Cipher")
    mode = st.radio("Pilih Mode", ["Enkripsi", "Dekripsi"])
    text = st.text_area("Masukkan Teks")
    key = st.text_input("Masukkan Kunci")
    if st.button("Proses") and key:
        result = cipher(text, key, mode)
        st.success(result)
        log_history("Playfair Cipher", mode, text, result)
