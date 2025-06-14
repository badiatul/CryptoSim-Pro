# app.py
import streamlit as st

st.set_page_config(page_title="CryptoSim Pro", layout="centered", page_icon="🛡️")

# Dark/light mode switch
mode = st.sidebar.toggle("🌙 Mode Gelap", value=False)

if mode:
    st.markdown("<style>body { background-color: #0d3b3e; color: white; }</style>", unsafe_allow_html=True)
else:
    st.markdown("<style>body { background-color: #e6f7f5; color: black; }</style>", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>CryptoSim Pro 🛡️</h1>", unsafe_allow_html=True)
st.markdown("### 👋 Selamat Datang di CryptoSim Pro!\n\n"
            "- Gunakan berbagai algoritma kriptografi klasik dan modern\n"
            "- Unggah file, lihat hasil, download, dan dapatkan QR Code\n"
            "- Silakan pilih algoritma di sidebar untuk memulai", unsafe_allow_html=True)
