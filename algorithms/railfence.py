import streamlit as st

def encrypt(text, key):
    rail = ["" for _ in range(key)]
    dir_down = False
    row = 0
    for char in text:
        rail[row] += char
        if row == 0 or row == key - 1:
            dir_down = not dir_down
        row += 1 if dir_down else -1
    return ''.join(rail)

def decrypt(cipher, key):
    rail = [['\n' for _ in range(len(cipher))] for _ in range(key)]
    dir_down = None
    row, col = 0, 0
    for i in range(len(cipher)):
        if row == 0:
            dir_down = True
        if row == key - 1:
            dir_down = False
        rail[row][col] = '*'
        col += 1
        row += 1 if dir_down else -1

    index = 0
    for i in range(key):
        for j in range(len(cipher)):
            if rail[i][j] == '*' and index < len(cipher):
                rail[i][j] = cipher[index]
                index += 1

    result = []
    row, col = 0, 0
    for i in range(len(cipher)):
        if row == 0:
            dir_down = True
        if row == key - 1:
            dir_down = False
        if rail[row][col] != '*':
            result.append(rail[row][col])
            col += 1
        row += 1 if dir_down else -1
    return ''.join(result)

def run(log_history):
    st.header("🔐 Rail Fence Cipher")
    mode = st.radio("Pilih mode", ["Enkripsi", "Dekripsi"])
    text = st.text_input("Masukkan teks")
    key = st.slider("Jumlah Rel (Rails)", 2, 10, 3)
    if st.button("Proses"):
        result = encrypt(text, key) if mode == "Enkripsi" else decrypt(text, key)
        st.success(f"Hasil: {result}")
        log_history("Rail Fence Cipher", mode, text, result)
