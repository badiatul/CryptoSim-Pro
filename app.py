import streamlit as st
import datetime
from algorithms import caesar, vigenere, railfence, playfair, hill

st.set_page_config(page_title="CryptoSim Pro", layout="centered", page_icon="🛡️")

st.markdown(
    "<h1 style='text-align: center; color: green;'>CryptoSim Pro 🛡️</h1>",
    unsafe_allow_html=True,
)

menu = ["Caesar Cipher", "Vigenère Cipher", "Rail Fence Cipher", "Playfair Cipher", "Hill Cipher"]
choice = st.sidebar.selectbox("🔎 Pilih Algoritma", menu)

# Inisialisasi riwayat
if "history" not in st.session_state:
    st.session_state.history = []

# Fungsi untuk menyimpan riwayat
def log_history(alg, mode, input_text, result):
    st.session_state.history.append({
        "algoritma": alg,
        "mode": mode,
        "input": input_text,
        "hasil": result,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

# Halaman utama algoritma
if choice == "Caesar Cipher":
    caesar.run()
elif choice == "Vigenère Cipher":
    vigenere.run()
elif choice == "Rail Fence Cipher":
    railfence.run()
elif choice == "Playfair Cipher":
    playfair.run()
elif choice == "Hill Cipher":
    hill.run()

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

# Fitur download
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

st.markdown(
    "<p style='text-align: center; color: grey;'>© 2025 CryptoSim Pro by Sayangmu 💚</p>",
    unsafe_allow_html=True
)
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
st.sidebar.title("🧰 Menu Tambahan")

if st.sidebar.button("🕘 Lihat Riwayat"):
    st.subheader("Riwayat Enkripsi / Dekripsi")
    if "history" in st.session_state and st.session_state["history"]:
        for item in reversed(st.session_state["history"]):
            st.markdown(f"**{item['timestamp']}** - {item['algoritma']} ({item['mode']})")
            st.text(f"Input: {item['input']}")
            st.text(f"Hasil: {item['hasil']}")
            st.markdown("---")
    else:
        st.info("Belum ada riwayat.")

if "last_result" in st.session_state and st.session_state["last_result"]:
    st.sidebar.download_button("⬇️ Unduh Hasil Terakhir", st.session_state["last_result"], file_name="hasil_terakhir.txt")
