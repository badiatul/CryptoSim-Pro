"""
Playfair Cipher Module for CrypTosca
Menggunakan matriks 5x5 untuk mengenkripsi dan mendekripsi pasangan huruf.
- Menghapus karakter non-huruf
- Mengganti huruf 'J' menjadi 'I'
- Menyisipkan 'X' pada pasangan huruf yang sama atau jika panjang teks ganjil
"""

import streamlit as st
import re

def clean_text(text):
    """Ubah teks ke huruf besar, ganti J jadi I, dan hilangkan non-huruf"""
    text = text.upper().replace("J", "I")
    return re.sub(r'[^A-Z]', '', text)

def prepare_plaintext(text):
    """Siapkan pasangan huruf Playfair: hilangkan non-huruf, tangani huruf ganda, dan ganjil"""
    text = clean_text(text)
    result = ''
    i = 0
    while i < len(text):
        a = text[i]
        b = text[i+1] if i+1 < len(text) else 'X'
        if a == b:
            result += a + 'X'
            i += 1
        else:
            result += a + b
            i += 2
    if len(result) % 2 != 0:
        result += 'X'
    return result

def generate_matrix(key):
    """Buat matriks 5x5 dari kunci unik"""
    key = clean_text(key)
    seen = set()
    matrix_key = ''
    for char in key + "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if char not in seen:
            seen.add(char)
            matrix_key += char
    return [list(matrix_key[i:i+5]) for i in range(0, 25, 5)]

def find_position(matrix, char):
    """Temukan posisi karakter dalam matriks"""
    for i, row in enumerate(matrix):
        if char in row:
            return i, row.index(char)
    return None, None  # Fallback defensif

def process_pair(a, b, matrix, mode):
    """Proses pasangan huruf berdasarkan aturan Playfair"""
    ax, ay = find_position(matrix, a)
    bx, by = find_position(matrix, b)

    if ax is None or bx is None:
        return a, b

    if ax == bx:  # Baris sama
        if mode == "Enkripsi":
            return matrix[ax][(ay+1)%5], matrix[bx][(by+1)%5]
        else:
            return matrix[ax][(ay-1)%5], matrix[bx][(by-1)%5]
    elif ay == by:  # Kolom sama
        if mode == "Enkripsi":
            return matrix[(ax+1)%5][ay], matrix[(bx+1)%5][by]
        else:
            return matrix[(ax-1)%5][ay], matrix[(bx-1)%5][by]
    else:  # Persegi
        return matrix[ax][by], matrix[bx][ay]

def cipher(text, key, mode):
    """Enkripsi atau Dekripsi dengan Playfair Cipher"""
    matrix = generate_matrix(key)
    if mode == "Enkripsi":
        text = prepare_plaintext(text)
    else:
        text = clean_text(text)

    result = ''
    for i in range(0, len(text), 2):
        a, b = process_pair(text[i], text[i+1], matrix, mode)
        result += a + b
    return result

def run(log_history):
    st.header("🔐 Playfair Cipher")
    st.markdown("""
    Playfair Cipher menggunakan **matriks 5x5** untuk mengenkripsi teks dengan pasangan huruf.

    - Huruf **J** diubah menjadi **I**
    - Jika pasangan huruf sama, akan disisipkan **X**
    - Jika panjang teks ganjil, ditambahkan **X** di akhir

    💡 **Contoh kunci:** `MONARCHY`, `SECURE`, `KEYWORD`
    """)

    mode = st.radio("📌 Pilih Mode", ["Enkripsi", "Dekripsi"])
    key_input = st.text_input("🔑 Masukkan Kunci", max_chars=25)
    text_input = st.text_area("📄 Masukkan Teks", height=150)

    if st.button(f"🚀 Jalankan {mode}"):
        if not key_input.strip():
            st.error("Kunci tidak boleh kosong.")
            return
        if not text_input.strip():
            st.error("Teks input tidak boleh kosong.")
            return

        try:
            result = cipher(text_input, key_input, mode)
            st.success("✅ Hasil:")
            st.code(result, language="text")
            log_history("Playfair Cipher", mode, text_input, result)
        except Exception as e:
            st.error(f"Terjadi kesalahan saat memproses: {e}")
