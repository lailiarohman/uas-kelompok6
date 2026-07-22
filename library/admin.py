from django.contrib import admin
from .models import Buku, Anggota, Peminjaman

admin.site.register(Buku)
admin.site.register(Anggota)
admin.site.register(Peminjaman)