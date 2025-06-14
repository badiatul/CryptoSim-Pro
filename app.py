import streamlit as st
import datetime
import base64
import qrcode

# --- Import algoritma ---
try:
    from algorithms import (
        caesar, vigenere, railfence, playfair, hill,
        beaufort, columnar, lsb, ecc, chacha20, fernet
    )
except Exception as e:
    st.error(f"❌ Gagal import algoritma: {e}")

# --- Konfigurasi halaman ---
st.set_page_config(
    page_title="CryptoSim Pro",
    layout="centered",
    page_icon="🛡️"
)

# --- CSS Kustom ---
try:
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("⚠️ File style.css tidak ditemukan.")

# --- Tema Gelap/Terang ---
is_dark = st.sidebar.toggle("🌙 Mode Gelap", value=False)
mode = "dark" if is_dark else "light"
st.markdown(f'<body class="{mode}">', unsafe_allow_html=True)

# --- Pilihan Algoritma ---
menu = st.sidebar.selectbox(
    "🔍 Pilih Algoritma",
    (
        "Beranda",
        "Caesar Cipher", "Vigenère Cipher", "Rail Fence Cipher",
        "Playfair Cipher", "Hill Cipher", "Beaufort Cipher",
        "Columnar Transposition",
        "LSB Steganography", "ECC", "ChaCha20", "Fernet"
    )
)

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

    🔐 Gunakan berbagai metode kriptografi klasik & modern.  
    📁 Simpan hasil & lihat riwayat.  
    🛡️ Pilih algoritma di sidebar untuk mulai simulasi.
    """)
    st.markdown("<br><center>© 2025 CryptoSim Pro by Badiatul</center>", unsafe_allow_html=True)

# --- Halaman Algoritma ---
else:
    try:
        if menu == "Caesar Cipher":
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
        else:
            st.error("❌ Algoritma tidak dikenali.")
    except AttributeError as e:
        st.error(f"❌ File algoritma belum punya fungsi `run()`: {e}")
    except Exception as e:
        st.error(f"❌ Gagal menjalankan algoritma: {e}")

# --- Fungsi QR Code (opsional) ---
def generate_qr(data):
    qr = qrcode.make(data)
    return qr

# --- Akhiri body tag ---
st.markdown("</body>", unsafe_allow_html=True)
