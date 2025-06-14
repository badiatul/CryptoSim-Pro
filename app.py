import streamlit as st
import datetime
from algorithms import caesar, vigenere, railfence, playfair, hill, beaufort, columnar, lsb, ecc, chacha20, fernet
import base64
import os
from PIL import Image
import qrcode

# Konfigurasi halaman
st.set_page_config(page_title="CryptoSim Pro", layout="centered", page_icon="🛡️")

# --- CSS Kustom ---
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- Tema Gelap/Terang ---
is_dark = st.sidebar.toggle("🌙 Mode Gelap", value=False)
mode = "dark" if is_dark else "light"
st.markdown(f'<body class="{mode}">', unsafe_allow_html=True)

# --- Sidebar Pilihan Algoritma ---
menu = st.sidebar.selectbox("🔍 Pilih Algoritma", (
    "Beranda", "Caesar Cipher", "Vigenère Cipher", "Rail Fence Cipher",
    "Playfair Cipher", "Hill Cipher", "Beaufort Cipher", "Columnar Transposition",
    "LSB Steganography", "ECC", "ChaCha20", "Fernet"
))

# --- Fungsi Simpan Riwayat ---
def log_history(algo, proses, plaintext, key, hasil):
    with open("riwayat.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now()} | {algo} | {proses} | {plaintext} | {key} | {hasil}\n")

# --- Halaman Beranda ---
if menu == "Beranda":
    st.markdown("<h1 style='text-align: center;'>CryptoSim Pro 🛡️</h1>", unsafe_allow_html=True)
    st.markdown("### 👋 Selamat Datang di CryptoSim Pro!")
    st.markdown("""
    Aplikasi ini dibuat untuk memenuhi tugas **UAS Pemrograman Kriptografi**.

    🔐 Gunakan berbagai metode kriptografi klasik dan modern untuk proses enkripsi dan dekripsi teks.  
    📁 Anda juga dapat mengunggah file, menyimpan hasil, menghasilkan QR Code, dan melihat riwayat penggunaan.  
    🛡️ Silakan pilih algoritma di sidebar untuk memulai simulasi.
    """)
    st.markdown("<br><center>© 2025 CryptoSim Pro by Badiatul</center>", unsafe_allow_html=True)

# --- Algoritma Lainnya (dengan file terpisah) ---
elif menu == "Caesar Cipher":
    caesar.run(log_history)
elif menu == "Vigenère Cipher":
    vigenere.run(log_history)
elif menu == "Rail Fence Cipher":
    railfence.run(log_history)
elif menu == "Playfair Cipher":
    playfair.run(log_history)
elif menu == "Hill Cipher":
    hill.run(log_history)
elif menu == "Beaufort Cipher":
    beaufort.run(log_history)
elif menu == "Columnar Transposition":
    columnar.run(log_history)
elif menu == "LSB Steganography":
    lsb.run(log_history)
elif menu == "ECC":
    ecc.run(log_history)
elif menu == "ChaCha20":
    chacha20.run(log_history)
elif menu == "Fernet":
    fernet.run(log_history)

# --- QR Code Generator (opsional bisa ditampilkan setelah hasil enkripsi) ---
def generate_qr(data):
    qr = qrcode.make(data)
    return qr

# --- Akhiri body tag (untuk class light/dark) ---
st.markdown("</body>", unsafe_allow_html=True)
