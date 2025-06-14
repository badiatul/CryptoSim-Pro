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
st.markdown("<h1 style='text-align: center; color: black;'>CryptoSim Pro 🛡️</h1>", unsafe_allow_html=True)

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

# Sidebar menu
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
    "Fernet",
    "🎮 Challenge Mode"
]
choice = st.sidebar.selectbox("🔎 Pilih Algoritma", menu)

# Tampilan Beranda
if choice == "Beranda":
    st.markdown("## 👋 Selamat Datang di **CryptoSim Pro!**")
    st.markdown("""
    Aplikasi ini dibuat untuk memenuhi tugas **UAS Pemrograman Kriptografi**.

    🔐 Gunakan berbagai metode kriptografi klasik dan modern untuk proses enkripsi dan dekripsi teks.  
    📁 Anda juga dapat mengunggah file, menyimpan hasil, menghasilkan QR Code, dan mencoba tantangan.  
    🛡️ Silakan pilih algoritma di sidebar untuk memulai simulasi.
    """)

# Mode Tantangan
elif choice == "🎮 Challenge Mode":
    st.markdown("## 🎯 Tantangan Kriptografi")
    soal = "UJIAN AKHIR SUDAH DEKAT"
    st.write(f"Teks berikut telah dienkripsi dengan Caesar (shift=3):")
    chiper = caesar.encrypt(soal, 3)
    st.code(chiper)
    jawaban = st.text_input("Apa hasil dekripsinya?")
    if jawaban.strip().upper() == soal:
        st.success("✅ Benar!")
    elif jawaban:
        st.error("❌ Masih salah, coba lagi!")

# Jalankan algoritma
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

# Riwayat & Unduh + QR Code
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
            st.image(buf.getvalue(), caption="QR Code dari hasil", use_container_width=False)
        else:
            st.warning("Belum ada hasil yang bisa diunduh.")

# Footer
st.markdown("<p style='text-align: center; color: grey;'>© 2025 CryptoSim Pro by Badiatul</p>", unsafe_allow_html=True)

# CSS Style
st.markdown("""
<style>
body {
    background-color: #e0f2f1;
}
[data-testid="stSidebar"] {
    background-color: #b2dfdb;
}
h1, h2, h3, h4, h5, h6, p {
    color: #004d40;
}
.stButton > button {
    background-color: #26a69a;
    color: white;
    border-radius: 8px;
    border: none;
    font-weight: bold;
    padding: 0.5em 1em;
}
.stButton > button:hover {
    background-color: #00796b;
}
.stAlert > div {
    background-color: #b2dfdb !important;
    color: #004d40 !important;
}
div[data-testid="stExpander"] > div > div {
    background-color: #e0f2f1 !important;
    border-radius: 10px;
}
input, textarea, .stTextInput > div > div, .stTextArea > div > div, .stNumberInput > div > div {
    background-color: #f1f8e9;
    border-radius: 5px;
}
.stRadio > label, .stSelectbox > label {
    color: #004d40;
}
</style>
""", unsafe_allow_html=True)
