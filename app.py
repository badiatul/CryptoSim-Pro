import streamlit as st
import datetime
import qrcode
from io import BytesIO
from PIL import Image

from algorithms import caesar, vigenere, railfence, playfair, hill, beaufort, columnar, lsb, ecc, chacha20, fernet

# Konfigurasi halaman
st.set_page_config(page_title="CryptoSim Pro", layout="centered", page_icon="🛡️")

# Load style dari file style.css
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Inisialisasi session state
if "history" not in st.session_state:
    st.session_state.history = []
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# Toggle mode gelap-terang
dark_mode = st.sidebar.toggle("🌙 Mode Gelap", value=st.session_state.dark_mode)
st.session_state.dark_mode = dark_mode

# Sidebar algoritma
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

# Fungsi untuk mencatat riwayat
def log_history(alg, mode, input_text, result):
    st.session_state.history.append({
        "algoritma": alg,
        "mode": mode,
        "input": input_text,
        "hasil": result,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

# Konten Beranda
if choice == "Beranda":
    st.markdown("## 👋 Selamat Datang di **CryptoSim Pro!**")
    st.markdown("""
    Aplikasi ini dibuat untuk memenuhi tugas **UAS Pemrograman Kriptografi**.

    🔐 Gunakan berbagai metode kriptografi klasik dan modern untuk proses enkripsi dan dekripsi teks.  
    📁 Anda juga dapat mengunggah file, menyimpan hasil, menghasilkan QR Code, dan melihat riwayat penggunaan.  
    🛡️ Silakan pilih algoritma di sidebar untuk memulai simulasi.
    """)

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

# Riwayat & Unduhan
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

    with st.expander("⬇️ Unduh Hasil Enkripsi/Dekripsi"):
        if st.session_state.history:
            last = st.session_state.history[-1]
            filename = f"{last['algoritma'].replace(' ', '_')}_{last['mode'].lower()}_{datetime.datetime.now().strftime('%H%M%S')}.txt"
            data_to_download = str(last["hasil"])
            st.download_button(
                label="📄 Unduh Hasil Terakhir",
                data=data_to_download,
                file_name=filename,
                mime="text/plain"
            )
        else:
            st.warning("Belum ada hasil yang bisa diunduh.")

    with st.expander("🔲 Tampilkan QR Code dari Hasil"):
        if st.session_state.history:
            last_result = st.session_state.history[-1]["hasil"]
            if isinstance(last_result, str) and last_result.strip():
                qr = qrcode.make(last_result)
                buf = BytesIO()
                qr.save(buf, format="PNG")
                st.image(Image.open(buf), caption="QR Code dari hasil terakhir", use_column_width=True)
            else:
                st.warning("Tidak ada hasil valid untuk diubah menjadi QR Code.")
        else:
            st.info("Belum ada hasil yang bisa ditampilkan.")

# Footer
st.markdown("<p style='text-align: center; color: grey;'>© 2025 CryptoSim Pro by Badiatul</p>", unsafe_allow_html=True)
