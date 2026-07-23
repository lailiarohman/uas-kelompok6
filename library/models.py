from django.db import models


class Buku(models.Model):
    kode_buku = models.CharField(max_length=20, unique=True)
    judul = models.CharField(max_length=200)
    penulis = models.CharField(max_length=100)
    penerbit = models.CharField(max_length=100)
    tahun_terbit = models.PositiveIntegerField()
    kategori = models.CharField(max_length=100)
    stok = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.judul


class Anggota(models.Model):
    nim = models.CharField(max_length=20, unique=True)
    nama = models.CharField(max_length=100)
    prodi = models.CharField(max_length=100)
    fakultas = models.CharField(max_length=100)
    no_hp = models.CharField(max_length=15)
    alamat = models.TextField()

    def __str__(self):
        return self.nama


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