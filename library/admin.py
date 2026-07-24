from django.contrib import admin
from .models import (
    Buku,
    Anggota,
    Peminjaman,
    Pengembalian,
    HistoriJabatan,
)

admin.site.register(Buku)
admin.site.register(Anggota)
admin.site.register(Peminjaman)
admin.site.register(Pengembalian)
admin.site.register(HistoriJabatan)