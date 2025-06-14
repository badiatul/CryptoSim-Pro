import streamlit as st
import datetime
import qrcode
import io
from PIL import Image
from algorithms import caesar, vigenere, railfence, playfair, hill, beaufort, columnar, lsb, ecc, chacha20, fernet

# ------------------- Konfigurasi Awal -------------------
st.set_page_config(page_title="CryptoSim Pro", layout="centered", page_icon="🛡️")

# ------------------- Autentikasi Sederhana -------------------
def login():
    st.title("🔐 Login ke CryptoSim Pro")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Masuk"):
        if username == "admin" and password == "crypto2025":
            st.session_state.authenticated = True
        else:
            st.error("Username atau password salah.")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if not st.session_state.authenticated:
    login()
    st.stop()

# ------------------- Toggle Tema -------------------
theme = st.sidebar.radio("🎨 Pilih Tema", ["Light", "Dark"])

# ------------------- Gaya CSS Berdasarkan Tema -------------------
light_css = """
<style>
body { background-color: #e0f2f1; }
[data-testid="stSidebar"] { background-color: #b2dfdb; }
h1, h2, h3, h4, h5, h6, p { color: #004d40; }
.stButton > button { background-color: #26a69a; color: white; border-radius: 8px; }
</style>
"""
dark_css = """
<style>
body { background-color: #263238; }
[data-testid="stSidebar"] { background-color: #37474f; }
h1, h2, h3, h4, h5, h6, p { color: #eceff1; }
.stButton > button { background-color: #546e7a; color: white; border-radius: 8px; }
</style>
"""

st.markdown(dark_css if theme == "Dark" else light_css, unsafe_allow_html=True)

# ------------------- Header -------------------
st.markdown("""
<h1 style='text-align: center;'>CryptoSim Pro 🛡️</h1>
""", unsafe_allow_html=True)

# ------------------- Inisialisasi -------------------
if "history" not in st.session_state:
    st.session_state.history = []

def log_history(alg, mode, input_text, result):
    st.session_state.history.append({
        "algoritma": alg,
        "mode": mode,
        "input": input_text,
        "hasil": result,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

# ------------------- Menu -------------------
menu = ["Beranda", "Caesar Cipher", "Vigenère Cipher", "Rail Fence Cipher", "Playfair Cipher",
         "Hill Cipher", "Beaufort Cipher", "Columnar Transposition Cipher", "LSB Steganography",
         "ECC", "ChaCha20", "Fernet", "Challenge Mode"]
choice = st.sidebar.selectbox("🔎 Pilih Algoritma", menu)

# ------------------- Fitur Unggah File -------------------
if choice != "Beranda" and choice != "Challenge Mode":
    uploaded_file = st.file_uploader("📂 Unggah File Teks (Opsional)", type=["txt"])
    if uploaded_file:
        uploaded_text = uploaded_file.read().decode("utf-8")
        st.text_area("📄 Isi File:", uploaded_text, height=150, key="file_input")

# ------------------- Routing Algoritma -------------------
if choice == "Beranda":
    st.markdown("## 👋 Selamat Datang di **CryptoSim Pro!**")
    st.markdown("""
    🔐 Gunakan metode kriptografi klasik & modern.
    📁 Unggah file, lihat riwayat, atau tampilkan hasil dalam QR code.
    🧠 Mode Challenge tersedia di sidebar untuk kuis enkripsi!
    """)
elif choice == "Challenge Mode":
    st.subheader("🎮 Mode Challenge")
    challenge_text = "HELLOCRYPTO"
    encrypted = caesar.encrypt(challenge_text, 3)
    st.write("Teks terenkripsi:", encrypted)
    answer = st.text_input("Tebak teks asli?")
    if st.button("Cek Jawaban"):
        if answer.upper() == challenge_text:
            st.success("Benar! Kamu berhasil mendekripsi.")
        else:
            st.error("Belum tepat. Coba lagi!")
elif choice == "Caesar Cipher":
    caesar.run(log_history)
elif choice == "Vigenère Cipher":
    vigenere.run(log_history)
elif choice == "Rail Fence Cipher":
    railfence.run(log_history, visual=True)
elif choice == "Playfair Cipher":
    playfair.run(log_history)
elif choice == "Hill Cipher":
    hill.run(log_history, visual=True)
elif choice == "Beaufort Cipher":
    beaufort.run(log_history)
elif choice == "Columnar Transposition Cipher":
    columnar.run(log_history, visual=True)
elif choice == "LSB Steganography":
    lsb.run(log_history)
elif choice == "ECC":
    ecc.run(log_history)
elif choice == "ChaCha20":
    chacha20.run(log_history)
elif choice == "Fernet":
    fernet.run(log_history)

# ------------------- Riwayat & Unduhan & QR Code -------------------
if choice != "Beranda" and choice != "Challenge Mode":
    with st.expander("🕘 Riwayat Penggunaan"):
        if st.session_state.history:
            for item in reversed(st.session_state.history[-10:]):
                st.markdown(f"""
                <div style='background-color:#f1f8e9;padding:10px;border-radius:10px;margin-bottom:10px;'>
                    <strong>{item['timestamp']}</strong><br>
                    <em>{item['algoritma']}</em> ({item['mode']})<br>
                    <b>Input:</b> {item['input']}<br>
                    <b>Hasil:</b> {item['hasil']}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Belum ada riwayat.")

    with st.expander("⬇️ Unduh & QR Code"):
        if st.session_state.history:
            last = st.session_state.history[-1]
            data_to_download = str(last["hasil"])
            filename = f"{last['algoritma'].replace(' ', '_')}_{last['mode']}.txt"
            st.download_button("📄 Unduh Hasil", data=data_to_download, file_name=filename)

            # QR Code
            img = qrcode.make(data_to_download)
            buf = io.BytesIO()
            img.save(buf)
            st.image(buf.getvalue(), caption="🔳 QR Code dari hasil")
        else:
            st.warning("Belum ada hasil untuk diunduh atau buat QR.")

# ------------------- Footer -------------------
st.markdown("""
<p style='text-align: center; color: grey;'>© 2025 CryptoSim Pro by Badiatul</p>
""", unsafe_allow_html=True)
