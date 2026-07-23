from django import forms
from .models import Buku, Anggota, Peminjaman, Pengembalian


class BukuForm(forms.ModelForm):
    class Meta:
        model = Buku
        fields = [
            'kode_buku',
            'judul',
            'penulis',
            'penerbit',
            'tahun_terbit',
            'kategori',
            'stok'
        ]

        widgets = {
            'kode_buku': forms.TextInput(attrs={'class': 'form-control'}),
            'judul': forms.TextInput(attrs={'class': 'form-control'}),
            'penulis': forms.TextInput(attrs={'class': 'form-control'}),
            'penerbit': forms.TextInput(attrs={'class': 'form-control'}),
            'tahun_terbit': forms.NumberInput(attrs={'class': 'form-control'}),
            'kategori': forms.TextInput(attrs={'class': 'form-control'}),
            'stok': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class AnggotaForm(forms.ModelForm):
    class Meta:
        model = Anggota
        fields = [
            'nim',
            'nama',
            'prodi',
            'fakultas',
            'no_hp',
            'alamat'
        ]

        widgets = {
            'nim': forms.TextInput(attrs={'class': 'form-control'}),
            'nama': forms.TextInput(attrs={'class': 'form-control'}),
            'prodi': forms.TextInput(attrs={'class': 'form-control'}),
            'fakultas': forms.TextInput(attrs={'class': 'form-control'}),
            'no_hp': forms.TextInput(attrs={'class': 'form-control'}),
            'alamat': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }
        
class PeminjamanForm(forms.ModelForm):
    class Meta:
        model = Peminjaman
        fields = [
            'anggota',
            'buku',
            'tanggal_pinjam',
            'tanggal_kembali',
            'status'
        ]

        widgets = {
            'anggota': forms.Select(attrs={'class': 'form-control'}),
            'buku': forms.Select(attrs={'class': 'form-control'}),
            'tanggal_pinjam': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'tanggal_kembali': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
        
class PengembalianForm(forms.ModelForm):
    class Meta:
        model = Pengembalian
        exclude = ['peminjaman']

        widgets = {
            'tanggal_pengembalian': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'kondisi_buku': forms.Select(attrs={
                'class': 'form-control'
            }),
            'denda': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
        }