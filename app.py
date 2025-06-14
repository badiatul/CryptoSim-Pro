import streamlit as st
import datetime
from algorithms import caesar  # dan algoritma lainnya

st.set_page_config(page_title="CryptoSim Pro", layout="centered", page_icon="🛡️")

# Load custom CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Sidebar toggle (boleh tetap digunakan)
mode = st.sidebar.toggle("🌙 Mode Gelap", value=False)

# Fungsi logging
def log_history(algo, mode, input_text, result):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("history.log", "a") as f:
        f.write(f"{now} | {algo} | {mode} | {input_text} -> {result}\n")

# Menu algoritma
st.sidebar.title("🧠 Pilih Algoritma")
menu = st.sidebar.radio("Algoritma:", ["Beranda", "Caesar Cipher"])

# Routing algoritma
if menu == "Beranda":
    st.markdown("<h1 style='text-align: center;'>CryptoSim Pro 🛡️</h1>", unsafe_allow_html=True)
    st.markdown("### 👋 Selamat Datang di CryptoSim Pro!\n\n"
                "- Gunakan berbagai algoritma kriptografi klasik dan modern\n"
                "- Unggah file, lihat hasil, download, dan dapatkan QR Code\n"
                "- Silakan pilih algoritma di sidebar untuk memulai", unsafe_allow_html=True)
elif menu == "Caesar Cipher":
    caesar.run(log_history)
