import streamlit as st
import datetime
from algorithms import caesar  # tambahkan algoritma lain jika ada, contoh: vigenere, hill, dll

# Konfigurasi dasar aplikasi
st.set_page_config(page_title="CryptoSim Pro", layout="centered", page_icon="🛡️")

# Muat CSS eksternal
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Mode terang/gelap (switch di sidebar)
mode = st.sidebar.toggle("🌙 Mode Gelap", value=False)

# Fungsi log riwayat enkripsi/dekripsi
def log_history(algo, mode, input_text, result):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("history.log", "a") as f:
        f.write(f"{now} | {algo} | {mode} | {input_text} -> {result}\n")

# Sidebar: menu algoritma
st.sidebar.title("🧠 Pilih Algoritma")
menu = st.sidebar.radio("Algoritma:", ["Beranda", "Caesar Cipher"])  # tambahkan lainnya jika tersedia

# Halaman Beranda
if menu == "Beranda":
    st.markdown("<h1 style='text-align: center;'>CryptoSim Pro 🛡️</h1>", unsafe_allow_html=True)
    st.markdown("""
    ### 👋 Selamat Datang di CryptoSim Pro!

    Aplikasi ini memungkinkan Anda:
    - 🔐 Menggunakan berbagai algoritma kriptografi klasik & modern
    - 📂 Mengunggah file teks dan melihat hasil enkripsi/dekripsi
    - 📥 Mendapatkan output, mengunduh hasil, dan QR Code

    > Silakan pilih algoritma di sidebar untuk memulai eksplorasi Anda!
    """, unsafe_allow_html=True)

# Halaman Caesar Cipher
elif menu == "Caesar Cipher":
    caesar.run(log_history)
