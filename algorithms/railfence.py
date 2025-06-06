import streamlit as st
from utils import log_history


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
def run():
    import streamlit as st
    from datetime import datetime
    from .cipher_utils import railfence_encrypt as encrypt, railfence_decrypt as decrypt

    mode = st.radio("Pilih Mode", ["Enkripsi", "Dekripsi"])
    teks = st.text_area("Masukkan Teks")
    key = st.number_input("Masukkan Jumlah Rel", min_value=2, value=3)

    if st.button("🔐 Proses"):
        if mode == "Enkripsi":
            hasil = encrypt(teks, int(key))
        else:
            hasil = decrypt(teks, int(key))
        st.success(hasil)

        st.session_state.history.append({
            "algoritma": "Rail Fence Cipher",
            "mode": mode,
            "input": teks,
            "hasil": hasil,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
log_history("Railfence Cipher", mode, text, result)
