"""
Rail Fence Cipher Module for CrypTosca
Algoritma Rail Fence menyusun karakter dalam bentuk zig-zag berdasarkan jumlah rel.
- Teks disusun secara vertikal bergelombang dan dibaca horizontal per baris.
- Cocok untuk enkripsi sederhana berbasis pola urutan.
"""

import streamlit as st

def encrypt_rail_fence(text, rails):
    """Enkripsi dengan Rail Fence Cipher menggunakan pola zig-zag"""
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
    """Dekripsi dengan Rail Fence Cipher berdasarkan pola posisi zig-zag"""
    # Tentukan pola rail untuk tiap karakter
    pattern = []
    rail = 0
    direction = 1
    for _ in text:
        pattern.append(rail)
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction *= -1

    # Hitung jumlah karakter di setiap rail
    rail_counts = [pattern.count(r) for r in range(rails)]

    # Ambil bagian teks sesuai urutan rail
    pos = 0
    rails_data = []
    for count in rail_counts:
        rails_data.append(list(text[pos:pos+count]))
        pos += count

    # Susun ulang teks berdasarkan urutan zig-zag
    result = []
    rail_indices = [0] * rails
    for r in pattern:
        result.append(rails_data[r][rail_indices[r]])
        rail_indices[r] += 1

    return ''.join(result)

def run(log_history):
    st.header("🔐 Rail Fence Cipher")
    st.markdown("""
    Rail Fence Cipher adalah metode enkripsi transposisi yang menyusun karakter dalam pola zig-zag  
    sesuai jumlah **rel** atau baris yang ditentukan. Teks kemudian dibaca per baris dari atas ke bawah.

    - Jumlah rel menentukan tinggi pola zig-zag
    - Semakin banyak rel, pola enkripsi semakin kompleks
    """)

    mode = st.radio("📌 Pilih Mode", ["Enkripsi", "Dekripsi"])
    text = st.text_area("📝 Masukkan Teks")
    rails = st.number_input("🚆 Jumlah Rel", min_value=2, max_value=10, value=3)

    if st.button("🚀 Jalankan Rail Fence Cipher"):
        if not text.strip():
            st.warning("Teks tidak boleh kosong.")
            return
        try:
            if mode == "Enkripsi":
                result = encrypt_rail_fence(text, rails)
            else:
                result = decrypt_rail_fence(text, rails)

            st.success(f"✅ Hasil {mode}:")
            st.code(result, language="text")

            log_history("Rail Fence Cipher", mode, text, result)
        except Exception as e:
            st.error(f"Terjadi kesalahan saat memproses: {e}")
