# 📚 SIMPEL
## Sistem Informasi Manajemen Perpustakaan Elektronik

SIMPEL merupakan aplikasi berbasis web yang dikembangkan menggunakan framework Django untuk membantu proses pengelolaan perpustakaan secara terkomputerisasi. Aplikasi ini memiliki tiga hak akses, yaitu Petugas, Anggota, dan Kepala Perpustakaan sehingga setiap pengguna memiliki fitur sesuai dengan tugas dan wewenangnya.

---

# ✨ Fitur Aplikasi

## 👨‍💼 Petugas

- Login
- Dashboard
- Kelola Data Buku
- Kelola Data Anggota
- Kelola Data Peminjaman
- Kelola Data Pengembalian
- Laporan
- Logout

---

## 👨‍🎓 Anggota

- Login
- Dashboard
- Melihat Katalog Buku
- Pencarian Buku
- Melihat Riwayat Peminjaman
- Melihat Profil
- Logout

---

## 👨‍💼 Kepala Perpustakaan

- Login
- Dashboard Statistik
- Monitoring Data Peminjaman
- Melihat Histori Jabatan
- Logout

---

# 🛠️ Teknologi yang Digunakan

- Python 3.13
- Django 6
- SQLite3
- Bootstrap 5
- HTML5
- CSS3
- JavaScript

---

# 📂 Struktur Project

```
SIMPEL
│
├── library/
├── perpustakaan/
├── static/
├── media/
├── templates/
├── db.sqlite3
├── manage.py
└── README.md
```

---

# ⚙️ Cara Menjalankan Project

## 1. Clone Repository

```bash
git clone https://github.com/lailia-rahman/uas-kelompok6.git
```

## 2. Masuk ke Folder Project

```bash
cd uas-kelompok6
```

## 3. Aktifkan Virtual Environment

Windows

```bash
env\Scripts\activate
```

## 4. Install Dependency

```bash
pip install -r requirements.txt
```

## 5. Jalankan Migrasi

```bash
python manage.py migrate
```

## 6. Jalankan Server

```bash
python manage.py runserver
```

Buka browser:

```
http://127.0.0.1:8000
```

---

# 👥 Hak Akses

| Hak Akses | Fitur |
|------------|--------------------------------|
| Petugas | Mengelola seluruh data perpustakaan |
| Anggota | Melihat katalog dan riwayat peminjaman |
| Kepala Perpustakaan | Monitoring dan melihat laporan |

---

# 📸 Tampilan Sistem

### Dashboard Petugas

*(Tambahkan Screenshot)*

---

### Dashboard Anggota

*(Tambahkan Screenshot)*

---

### Dashboard Kepala Perpustakaan

*(Tambahkan Screenshot)*

---

# 👨‍💻 Pengembang

**Nama :** Lailia Rohmatul Ula, Rohimatul Munibah

**Program Studi :** S1 Teknik Informatika

**Universitas :** Universitas Nurul Jadid

**Tahun :** 2026

---

# 📄 Lisensi

Project ini dibuat untuk memenuhi tugas UAS Mata Kuliah Web Programming Universitas Nurul Jadid.