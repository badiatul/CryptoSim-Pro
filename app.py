import streamlit as st
import datetime
from algorithms import caesar, vigenere, railfence, playfair, hill, beaufort, columnar, lsb, ecc, chacha20, fernet

st.set_page_config(page_title="CryptoSim Pro", layout="centered", page_icon="\U0001F6E1\uFE0F")

# Mode terang/gelap
mode = st.sidebar.toggle("\U0001F319 Mode Gelap", value=False)

background_color = "#e0f2f1" if not mode else "#00332d"
sidebar_color = "#b2dfdb" if not mode else "#004d40"
primary_color = "#004d40" if not mode else "#e0f2f1"
button_color = "#26a69a" if not mode else "#00796b"
hover_color = "#00796b" if not mode else "#004d40"

st.markdown(f"""
    <style>
    body {{
        background-color: {background_color};
    }}
    html, .main, .block-container {{
        background-color: {background_color} !important;
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
    footer {{
        visibility: visible;
    }}
    </style>
""", unsafe_allow_html=True)

# Judul halaman utama
st.markdown(
    f"""
    <h1 style='text-align: center; color: {primary_color};'>CryptoSim Pro \U0001F6E1\uFE0F</h1>
    """,
    unsafe_allow_html=True,
)

# Inisialisasi sesi
if "history" not in st.session_state:
    st.session_state.history = []

# Fungsi log_history global
def log_history(alg, mode, input_text, result):
    st.session_state.history.append({
        "algoritma": alg,
        "mode": mode,
        "input": input_text,
        "hasil": result,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

# Sidebar pilih algoritma (dengan Beranda di awal)
menu = [
    "Beranda",
    "Caesar Cipher",
    "Vigen\u00e8re Cipher",
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

choice = st.sidebar.selectbox("\U0001F50D Pilih Algoritma", menu)

# Konten Beranda
if choice == "Beranda":
    st.markdown(f"""
    ## \U0001F44B Selamat Datang di **CryptoSim Pro!**

    Aplikasi ini dibuat untuk memenuhi tugas **UAS Pemrograman Kriptografi**.

    \U0001F510 Gunakan berbagai metode kriptografi klasik dan modern untuk proses enkripsi dan dekripsi teks.  
    \U0001F4C1 Anda juga dapat mengunggah file, menyimpan hasil, menghasilkan QR Code, dan melihat riwayat penggunaan.  
    ⛨️ Silakan pilih algoritma di sidebar untuk memulai simulasi.
    """)

# Jalankan algoritma sesuai pilihan
elif choice == "Caesar Cipher":
    caesar.run(log_history)
elif choice == "Vigen\u00e8re Cipher":
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

# Tampilkan riwayat & unduhan hanya jika bukan di Beranda
if choice != "Beranda":
    with st.expander("\U0001F553 Lihat Riwayat"):
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

    with st.expander("\u2B07\uFE0F Unduh Hasil Enkripsi/Dekripsi"):
        if st.session_state.history:
            last = st.session_state.history[-1]
            filename = f"{last['algoritma'].replace(' ', '_')}_{last['mode'].lower()}_{datetime.datetime.now().strftime('%H%M%S')}.txt"

            data_to_download = last["hasil"]
            if not isinstance(data_to_download, str):
                try:
                    data_to_download = str(data_to_download)
                except Exception:
                    data_to_download = "Tidak bisa menampilkan hasil dalam format teks."

            st.download_button(
                label="\U0001F4C4 Unduh Hasil Terakhir",
                data=data_to_download,
                file_name=filename,
                mime="text/plain"
            )
        else:
            st.warning("Belum ada hasil yang bisa diunduh.")

# Footer
st.markdown(f"<p style='text-align: center; color: grey;'>\u00a9 2025 CryptoSim Pro by Badiatul</p>", unsafe_allow_html=True)
