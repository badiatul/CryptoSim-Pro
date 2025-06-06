```python
import streamlit as st
from datetime import datetime
import numpy as np

def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def encrypt(text, key):
    text = text.upper().replace(" ", "")
    while len(text) % 2 != 0:
        text += 'X'
    result = ""
    for i in range(0, len(text), 2):
        pair = [ord(text[i]) - 65, ord(text[i+1]) - 65]
        res = np.dot(key, pair) % 26
        result += chr(res[0]+65) + chr(res[1]+65)
    return result

def decrypt(text, key):
    det = int(np.round(np.linalg.det(key)))
    det_inv = mod_inverse(det % 26, 26)
    if det_inv is None:
        return "Kunci tidak memiliki invers modulo."

    adj = np.round(np.linalg.inv(key) * det).astype(int) % 26
    key_inv = (det_inv * adj) % 26

    text = text.upper().replace(" ", "")
    result = ""
    for i in range(0, len(text), 2):
        pair = [ord(text[i]) - 65, ord(text[i+1]) - 65]
        res = np.dot(key_inv, pair) % 26
        result += chr(res[0]+65) + chr(res[1]+65)
    return result

def run(log_history):
    st.header("🔐 Hill Cipher")
    mode = st.radio("Pilih mode", ["Enkripsi", "Dekripsi"])
    text = st.text_input("Masukkan teks")
    a = st.number_input("Key A", value=3)
    b = st.number_input("Key B", value=3)
    c = st.number_input("Key C", value=2)
    d = st.number_input("Key D", value=5)

    key = np.array([[a, b], [c, d]])

    if st.button("Proses"):
        result = encrypt(text, key) if mode == "Enkripsi" else decrypt(text, key)
        st.success(f"Hasil: {result}")
        log_history("Hill Cipher", mode, text, result)
```
