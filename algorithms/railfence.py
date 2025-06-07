import streamlit as st

def encrypt_rail_fence(text, rails):
    fence = [[] for _ in range(rails)]
    rail = 0
    direction = 1
    for char in text:
        fence[rail].append(char)
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction *= -1
    return ''.join(''.join(row) for row in fence)

def decrypt_rail_fence(text, rails):
    pattern = list(range(rails)) + list(range(rails - 2, 0, -1))
    pattern = pattern * (len(text) // len(pattern) + 1)
    indexes = sorted(range(len(text)), key=lambda i: pattern[i])
    result = [''] * len(text)
    for i, char in zip(indexes, text):
        result[i] = char
    return ''.join(result)

def run(log_history):
    st.header("🔐 Rail Fence Cipher")
    st.markdown("""
    Rail Fence Cipher menyusun huruf pesan dalam bentuk zig-zag sesuai jumlah rel (baris).
    Huruf-huruf disusun berdasarkan rel lalu dibaca per rel secara horizontal.
    """)

    mode = st.radio("Pilih Mode", ["Enkripsi", "Dekripsi"])
    text = st.text_area("📝 Masukkan Teks")
    rails = st.number_input("🚆 Jumlah Rel", min_value=2, max_value=10, value=3)

    if st.button("🚀 Jalankan Rail Fence Cipher"):
        if not text.strip():
            st.warning("Teks tidak boleh kosong.")
            return
        result = encrypt_rail_fence(text, rails) if mode == "Enkripsi" else decrypt_rail_fence(text, rails)
        st.success(f"Hasil {mode}:")
        st.code(result)
        log_history("Rail Fence Cipher", mode, text, result)
