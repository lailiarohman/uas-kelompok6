from django.db import models
from django.contrib.auth.models import User

class Buku(models.Model):
    kode_buku = models.CharField(max_length=20, unique=True)
    judul = models.CharField(max_length=200)
    penulis = models.CharField(max_length=100)
    penerbit = models.CharField(max_length=100)
    tahun_terbit = models.PositiveIntegerField()
    kategori = models.CharField(max_length=100)

    isbn = models.CharField(max_length=20, blank=True)

    lokasi_rak = models.CharField(
        max_length=50,
        default="Rak A1"
    )

    kondisi = models.CharField(
        max_length=20,
        choices=[
            ('Baik', 'Baik'),
            ('Rusak', 'Rusak'),
        ],
        default='Baik'
    )

    stok = models.PositiveIntegerField(default=0)
    def __str__(self):
        return f"{self.kode_buku} - {self.judul}"

class Anggota(models.Model):

    STATUS = (
        ('Menunggu', 'Menunggu'),
        ('Disetujui', 'Disetujui'),
        ('Ditolak', 'Ditolak'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    nim = models.CharField(max_length=20)
    nama = models.CharField(max_length=100)
    prodi = models.CharField(max_length=100)
    fakultas = models.CharField(max_length=100)
    no_hp = models.CharField(max_length=20)
    alamat = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='Menunggu'
    )

    def __str__(self):
        return f"{self.nama} ({self.nim})"


class Peminjaman(models.Model):
    STATUS = (
        ('Dipinjam', 'Dipinjam'),
        ('Dikembalikan', 'Dikembalikan'),
    )

    anggota = models.ForeignKey(Anggota, on_delete=models.CASCADE)
    buku = models.ForeignKey(Buku, on_delete=models.CASCADE)
    tanggal_pinjam = models.DateField()
    tanggal_kembali = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS, default='Dipinjam')

    def __str__(self):
        return f"{self.anggota.nama} - {self.buku.judul}"
    
class Pengembalian(models.Model):
    peminjaman = models.OneToOneField(
        Peminjaman,
        on_delete=models.CASCADE
    )

    tanggal_pengembalian = models.DateField()

    kondisi_buku = models.CharField(
        max_length=20,
        choices=[
            ('Baik', 'Baik'),
            ('Rusak', 'Rusak'),
        ]
    )

    denda = models.IntegerField(default=0)

    def __str__(self):
        return self.peminjaman.anggota.nama
    
class HistoriJabatan(models.Model):
    nama_kepala = models.CharField(max_length=100)
    jabatan = models.CharField(
        max_length=100,
        default="Kepala Perpustakaan"
    )
    tanggal_mulai = models.DateField()
    tanggal_selesai = models.DateField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.nama_kepala