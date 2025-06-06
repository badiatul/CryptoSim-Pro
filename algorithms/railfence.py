import streamlit as st

def encrypt(text, rails):
    fence = [['' for _ in range(len(text))] for _ in range(rails)]
    rail = 0
    var = 1
    for i in range(len(text)):
        fence[rail][i] = text[i]
        rail += var
        if rail == 0 or rail == rails - 1:
            var = -var
    result = ''.join([''.join(r) for r in fence])
    return result

def decrypt(text, rails):
    pattern = list(range(rails)) + list(range(rails - 2, 0, -1))
    pattern = pattern * (len(text) // len(pattern) + 1)
    fence = [['' for _ in range(len(text))] for _ in range(rails)]
    indexes = sorted(range(len(text)), key=lambda i: pattern[i])
    idx = 0
    for r in range(rails):
        for i in range(len(text)):
            if pattern[i] == r:
                fence[r][i] = text[idx]
                idx += 1
    result = ''
    rail = 0
    var = 1
    for i in range(len(text)):
        result += fence[rail][i]
        rail += var
        if rail == 0 or rail == rails - 1:
            var = -var
    return result

def run():
    st.header("🔐 Rail Fence Cipher")
    mode = st.radio("Pilih mode", ["Enkripsi", "Dekripsi"])
    text = st.text_input("Masukkan teks")
    rails = st.slider("Jumlah rel", 2, 10, 3)
    if st.button("Proses"):
        result = encrypt(text, rails) if mode == "Enkripsi" else decrypt(text, rails)
        st.success(f"Hasil: {result}")
