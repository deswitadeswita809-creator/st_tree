import streamlit as st

# ==============================
# KELAS NODE KATEGORI
# ==============================

class KategoriNode:
    def __init__(self, nama_kategori):
        self.nama = nama_kategori
        self.sub_kategori = []

    def tambah_sub(self, node_kategori):
        self.sub_kategori.append(node_kategori)

# Mengubah fungsi print menjadi return agar bisa di tampilkan di web
    def tampilkan_tree_string(self, level=0):
        indentasi = "    " * level
        simbol = "↳ " if level > 0 else "📦 "
        print(f"{indentasi}{simbol}{self.nama}\n")
        
        for sub in self.sub_kategori:
            hasil += sub.dapatkan_tree_string(level + 1)
            return hasil

    def cari_node(self, target_nama):
        # Mencari node spesifik untuk menambahkan anak di bawahnya
        if self.nama.lower() == target_nama.lower():
            return self
            
        for sub in self.sub_kategori:
            hasil = sub.cari_node(target_nama)
            if hasil:
                return hasil
                
        return None

    def cari_jalur(self, target, path=""):
        # Mencari jalur lengkap (breadcrumb) seperti studi kasus sebelumnya
        jalur_saat_ini = path + " > " + self.nama if path else self.nama
        
        if self.nama.lower() == target.lower():
            return jalur_saat_ini
            
        for sub in self.sub_kategori:
            hasil = sub.cari_jalur(target, jalur_saat_ini)
            if hasil:
                return hasil
                
        return None

# ==========================================
# PROGRAM UTAMA (INTERAKTIF)
# ==========================================

st.set_page_config(page_title="Struktur Kategori", page_icon="+")

st.title("pembuat struktur kategori")
st.write("Aplikasi interaktif untuk mensimulasikan struktur data Tree.")

# Inisialisasi session state untuk menyimpan struktur Tree agar tidak hilang saat halaman di-refresh
if'root' not in st.session_state:
    st.session_state.root = None

#  jika root belum, tampilkan from pembuat root
if st.session_state.root is None:
    st.info("sistem belum memiliki kategori utama. silakan buat terlebih dahulu.")
    nama_root = st.text_input("Masukkan nama kategori utama (root) :", value="Toko Saya")

    if st.button("Buat Kategori Utama", type="primary"):
        st.session_state.root = KategoriNode(nama_root)
        st.rerun() #Refresh halaman

# jika root sudah ada, Tampilkan Menu Utama menggunakan Tabs
else:
    root = st.session_state.root

    # Mengganti menu cli dengan sistem Tab yang lebih modern
    tab1, tab2, tab3 = st.tabs(["Lihat struktur", "+ Tambah Sub-Kategori","cari jalur"])

    # TAB 1: Lihat Struktur
    with tab1:
        st.subheader("struktur Kategori saat ini") 
        tree_teks = root.dapatkan_tree_string()
        # menggunkan st.code agar format indentasi (spasi) tetap rapih
        st.code(tree_teks, language="text")

    # TAB 2: Tambah sub-Kategori
    with tab2:
        st.subheader("Tambah Cabang Baru")
        induk_nama = st.text_input("Nama Kategori induk tempat cabang ditambahkan:")
        anak_nama = st.text_input("Nama sub-kategori baru:")

        if st.button("tambah kategori"):
            if induk_nama and anak_nama:
                induk_node = root.cari_node(induk_nama)
                if induk_node:
                    induk_node.tambah_sub(KategoriNode(anak_nama))
                    st.success(f"Berhasil menambahkan '{anak_nama}' di belakang '{induk_node.nama}' !")

                else:
                    st.error(f"kategori '{induk_nama}' tidak ditemukan! pastikan ejaannya benar.")

            else:
                st.warning("Harap isi kedua kolom di atas.")

    # TAB 3 : Cari Jalur
    with tab3:
        st.subheader("Pencarian Breadcrumb")
        target_cari = st.text_input("Nama kategori yang ingin di cari jalurnya:")

        if st.button("cari jalur"):
            if target_cari:
                hasil = root.cari_jalur(target_cari)
                if hasil:
                    st.success("Ditemukan!")
                    st.info(f" ! Jalur: {hasil}")
                else:
                    st.error(f"kategori '{target_cari}' tidak ditemukan dalam sistem.")

            else:
                st.warning("Harap isi nama kategori yang dicari.")

# Tombol reset
st.divider()
if st.button("reset sitem / Mulai dari awal"):
    st.session_state.root = None
    st.rerun()
