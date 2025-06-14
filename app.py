import streamlit as st
import datetime
import qrcode
from io import BytesIO
from algorithms import (
    caesar, vigenere, railfence, playfair, hill,
    beaufort, columnar, lsb, ecc, chacha20, fernet
)

# Konfigurasi Halaman
st.set_page_config(page_title="CryptoSim Pro", layout="centered", page_icon="🛡️")

# Toggle Mode Gelap/Terang
mode = st.sidebar.toggle("🌙 Mode Gelap", value=False)

# Tema berdasarkan mode
primary_color = "#004d40" if not mode else "#ffffff"
background_color = "#e0f2f1" if not mode else "#121212"
sidebar_color = "#b2dfdb" if not mode else "#1e1e1e"
font_color = "#004d40" if not mode else "#e0f7fa"
button_color = "#26a69a" if not mode else "#2e8b57"
hover_color = "#00796b" if not mode else "#43a047"

# Gaya CSS dinamis
st.markdown(f"""
<style>
body {{
    background-color: {background_color};
}}
[data-testid="stSidebar"] {{
    background-color: {sidebar_color};
}}
h1, h2, h3, h4, h5, h6, p {{
    color: {primary_color};
}}
.stButton > button {{
    background-color: {button_color};
    color: white;
    border-radius: 8px;
    border: none;
    font-weight: bold;
    padding: 0.5em 1em;
}}
.stButton > button:hover {{
    background-color: {hover_color};
}}
.stAlert > div {{
    background-color: {sidebar_color} !important;
    color: {primary_color} !important;
}}
div[data-testid="stExpander"] > div > div {{
    background-color: {background_color} !important;
    border-radius: 10px;
}}
input, textarea, .stTextInput > div > div, .stTextArea > div > div, .stNumberInput > div > div {{
    background-color: #f1f8e9;
    border-radius: 5px;
    color: black;
}}
.stRadio > label, .stSelectbox > label {{
    color: {primary_color};
}}
</style>
""", unsafe_allow_html=True)

# Judul
st.markdown("<h1 style='text-align: center;'>CryptoSim Pro 🛡️</h1>", unsafe_allow_html=True)

# Inisialisasi sesi
if "history" not in st.session_state:
    st.session_state.history = []

# Fungsi log riwayat
def log_history(alg, mode, input_text, result):
    st.session_state.history.append({
        "algoritma": alg,
        "mode": mode,
        "input": input_text,
        "hasil": result,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

# Sidebar menu algoritma
menu = [
    "Beranda",
    "Caesar Cipher",
    "Vigenère Cipher",
    "Rail Fence Cipher",
    "Playfair Cipher",
    "Hill Cipher",
    "Beaufort Cipher",
    "Columnar Transposition Cipher",
    "LSB Steganography",
    "ECC",
    "ChaCha20",
    "Fernet"
]
choice = st.sidebar.selectbox("🔎 Pilih Algoritma", menu)

# Halaman Beranda
if choice == "Beranda":
    st.markdown("## 👋 Selamat Datang di **CryptoSim Pro!**")
    st.markdown("""
    Aplikasi ini dibuat untuk memenuhi tugas **UAS Pemrograman Kriptografi**.

    🔐 Gunakan berbagai metode kriptografi klasik dan modern untuk proses enkripsi dan dekripsi teks.  
    📁 Anda juga dapat mengunggah file, menyimpan hasil, menghasilkan QR Code, dan melihat riwayat penggunaan.  
    🛡️ Silakan pilih algoritma di sidebar untuk memulai simulasi.
    """)

# Jalankan algoritma sesuai pilihan
elif choice == "Caesar Cipher":
    caesar.run(log_history)
elif choice == "Vigenère Cipher":
    vigenere.run(log_history)
elif choice == "Rail Fence Cipher":
    railfence.run(log_history)
elif choice == "Playfair Cipher":
    playfair.run(log_history)
elif choice == "Hill Cipher":
    hill.run(log_history)
elif choice == "Beaufort Cipher":
    beaufort.run(log_history)
elif choice == "Columnar Transposition Cipher":
    columnar.run(log_history)
elif choice == "LSB Steganography":
    lsb.run(log_history)
elif choice == "ECC":
    ecc.run(log_history)
elif choice == "ChaCha20":
    chacha20.run(log_history)
elif choice == "Fernet":
    fernet.run(log_history)

# Riwayat dan Unduh
if choice != "Beranda":
    with st.expander("🕘 Lihat Riwayat"):
        if st.session_state.history:
            for item in reversed(st.session_state.history[-10:]):
                st.markdown(f"""
                <div style='background-color:#e6ffe6;padding:10px;border-radius:10px;margin-bottom:10px;'>
                    <strong>{item['timestamp']}</strong><br>
                    <em>{item['algoritma']}</em> ({item['mode']})<br>
                    <b>Input:</b> {item['input']}<br>
                    <b>Hasil:</b> {item['hasil']}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Belum ada riwayat.")

    with st.expander("⬇️ Unduh Hasil & QR Code"):
        if st.session_state.history:
            last = st.session_state.history[-1]
            hasil = str(last["hasil"])
            filename = f"{last['algoritma'].replace(' ', '_')}_{last['mode'].lower()}_{datetime.datetime.now().strftime('%H%M%S')}.txt"

            st.download_button("📄 Unduh Hasil Terakhir", data=hasil, file_name=filename, mime="text/plain")

            qr = qrcode.make(hasil)
            buf = BytesIO()
            qr.save(buf)
            st.image(buf.getvalue(), caption="QR Code dari hasil", use_container_width=True)
        else:
            st.warning("Belum ada hasil yang bisa diunduh.")

# Footer
st.markdown(f"<p style='text-align: center; color: grey;'>© 2025 CryptoSim Pro by Badiatul</p>", unsafe_allow_html=True)
