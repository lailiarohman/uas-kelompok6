from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('registrasi/',views.registrasi,name='registrasi'),
    path('logout/', views.logout_view, name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard-anggota/', views.dashboard_anggota, name='dashboard_anggota'),
    path('dashboard-kepala/', views.dashboard_kepala, name='dashboard_kepala'),

    # CRUD Buku
    path('buku/', views.buku, name='buku'),
    path('buku/tambah/', views.tambah_buku, name='tambah_buku'),
    path('buku/edit/<int:id>/', views.edit_buku, name='edit_buku'),
    path('buku/hapus/<int:id>/', views.hapus_buku, name='hapus_buku'),

    # CRUD Anggota
    path('anggota/', views.anggota, name='anggota'),
    path('anggota/tambah/', views.tambah_anggota, name='tambah_anggota'),
    path('anggota/edit/<int:id>/', views.edit_anggota, name='edit_anggota'),
    path('anggota/hapus/<int:id>/', views.hapus_anggota, name='hapus_anggota'),

    # CRUD Peminjaman
    path('peminjaman/', views.peminjaman, name='peminjaman'),
    path('peminjaman/tambah/', views.tambah_peminjaman, name='tambah_peminjaman'),
    path('peminjaman/edit/<int:id>/', views.edit_peminjaman, name='edit_peminjaman'),
    path('peminjaman/hapus/<int:id>/', views.hapus_peminjaman, name='hapus_peminjaman'),

    # CRUD Pengembalian
    path('pengembalian/', views.pengembalian, name='pengembalian'),
    path('pengembalian/tambah/<int:id>/',views.tambah_pengembalian,name='tambah_pengembalian'),
    path('pengembalian/edit/<int:id>/', views.edit_pengembalian, name='edit_pengembalian'),
    path('pengembalian/hapus/<int:id>/', views.hapus_pengembalian, name='hapus_pengembalian'),
      
    # Laporan
    path('laporan/', views.laporan, name='laporan'),
    
    path('katalog/', views.katalog_buku, name='katalog_buku'),
    
    path('riwayat-peminjaman/',views.riwayat_peminjaman,name='riwayat_peminjaman'),
    
    path('profil/',views.profil_anggota,name='profil_anggota'),
 
    path('data-peminjaman-kepala/',views.data_peminjaman_kepala,name='data_peminjaman_kepala'),
    path('histori-jabatan/', views.histori_jabatan, name='histori_jabatan'),
    path(
    'verifikasi-anggota/',
    views.verifikasi_anggota,
    name='verifikasi_anggota'
),

path(
    'setujui-anggota/<int:id>/',
    views.setujui_anggota,
    name='setujui_anggota'
),
]