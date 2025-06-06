import streamlit as st

def encrypt(text, rails):
    fence = [[] for _ in range(rails)]
    rail = 0
    var = 1

    for char in text:
        fence[rail].append(char)
        rail += var
        if rail == 0 or rail == rails - 1:
            var = -var
    return "".join(["".join(row) for row in fence])

def decrypt(cipher, rails):
    pattern = [None] * len(cipher)
    rail = 0
    var = 1

    for i in range(len(cipher)):
        pattern[i] = rail
        rail += var
        if rail == 0 or rail == rails - 1:
            var = -var

    result = [None] * len(cipher)
    index = 0
    for r in range(rails):
        for i in range(len(cipher)):
            if pattern[i] == r:
                result[i] = cipher[index]
                index += 1
    return "".join(result)

def run(log_history):
    st.header("🔐 Rail Fence Cipher")
    mode = st.radio("Pilih mode", ["Enkripsi", "Dekripsi"])
    text = st.text_input("Masukkan teks")
    rails = st.slider("Jumlah Rail", 2, 10, 3)

    if st.button("Proses"):
        if mode == "Enkripsi":
            result = encrypt(text, rails)
        else:
            result = decrypt(text, rails)
        st.success(f"Hasil: {result}")
        log_history("Rail Fence Cipher", mode, text, result)
