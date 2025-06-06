```python
import streamlit as st
from datetime import datetime

def repeat_key(key, length):
    return (key * (length // len(key) + 1))[:length]

def encrypt(text, key):
    text = text.upper()
    key = repeat_key(key.upper(), len(text))
    result = ""
    for t, k in zip(text, key):
        if t.isalpha():
            result += chr(((ord(t) - 65 + ord(k) - 65) % 26) + 65)
        else:
            result += t
    return result

def decrypt(text, key):
    text = text.upper()
    key = repeat_key(key.upper(), len(text))
    result = ""
    for t, k in zip(text, key):
        if t.isalpha():
            result += chr(((ord(t) - 65 - (ord(k) - 65)) % 26) + 65)
        else:
            result += t
    return result

def run(log_history):
    st.header("🔐 Vigenère Cipher")
    mode = st.radio("Pilih mode", ["Enkripsi", "Dekripsi"])
    text = st.text_input("Masukkan teks")
    key = st.text_input("Masukkan kunci (huruf)")
    if st.button("Proses") and key.isalpha():
        result = encrypt(text, key) if mode == "Enkripsi" else decrypt(text, key)
        st.success(f"Hasil: {result}")
        log_history("Vigenère Cipher", mode, text, result)
```
