import streamlit as st
import datetime
from algorithms import caesar, vigenere, railfence, playfair, hill

st.set_page_config(page_title="CryptoSim Pro", layout="centered", page_icon="🛡️")

st.markdown(
    "<h1 style='text-align: center; color: green;'>CryptoSim Pro 🛡️</h1>",
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

# Sidebar pilih algoritma
menu = ["Caesar Cipher", "Vigenère Cipher", "Rail Fence Cipher", "Playfair Cipher", "Hill Cipher"]
choice = st.sidebar.selectbox("🔎 Pilih Algoritma", menu)

# Jalankan algoritma sesuai pilihan
if choice == "Caesar Cipher":
    caesar.run(log_history)
elif choice == "Vigenère Cipher":
    vigenere.run(log_history)
elif choice == "Rail Fence Cipher":
    railfence.run(log_history)
elif choice == "Playfair Cipher":
    playfair.run(log_history)
elif choice == "Hill Cipher":
    hill.run(log_history)

# Riwayat
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

# Unduhan
with st.expander("⬇️ Unduh Hasil Enkripsi/Dekripsi"):
    if st.session_state.history:
        last = st.session_state.history[-1]
        filename = f"{last['algoritma'].replace(' ', '_')}_{last['mode'].lower()}_{datetime.datetime.now().strftime('%H%M%S')}.txt"
        st.download_button(
            label="📄 Unduh Hasil Terakhir",
            data=last["hasil"],
            file_name=filename,
            mime="text/plain"
        )
    else:
        st.warning("Belum ada hasil yang bisa diunduh.")

st.markdown("<p style='text-align: center; color: grey;'>© 2025 CryptoSim Pro 💚</p>", unsafe_allow_html=True)
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
