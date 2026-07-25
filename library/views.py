from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from django.db.models import Q

from .models import Buku, Anggota, Peminjaman, Pengembalian, HistoriJabatan
from .forms import (
    BukuForm,
    AnggotaForm,
    PeminjamanForm,
    PengembalianForm,
    RegistrasiAnggotaForm,
)


def home(request):
    return redirect('login')


# ==========================
# LOGIN
# ==========================
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            if user.groups.filter(name='Anggota').exists():
                anggota = Anggota.objects.get(user=user)

                if anggota.status != 'Disetujui':
                    return render(
                        request,
                        'library/login.html',
                        {
                            'error': 'Akun Anda masih menunggu persetujuan Admin.'
                        }
                    )

            login(request, user)

            if user.groups.filter(name='Admin').exists():
                return redirect('dashboard')

            elif user.groups.filter(name='Kepala').exists():
                return redirect('dashboard_kepala')

            elif user.groups.filter(name='Anggota').exists():
                return redirect('dashboard_anggota')

            else:
                messages.error(request, "Role pengguna belum diatur.")
                logout(request)
                return redirect('login')

        else:
            return render(
                request,
                'library/login.html',
                {
                    'error': 'Username atau Password salah!'
                }
            )

    return render(request, 'library/login.html')


# ==========================
# LOGOUT
# ==========================
def logout_view(request):
    logout(request)
    return redirect('login')


# ==========================
# DASHBOARD ADMIN
# ==========================
@login_required(login_url='login')
def dashboard(request):
    total_buku = Buku.objects.count()
    total_anggota = Anggota.objects.count()
    buku_dipinjam = Peminjaman.objects.filter(
        status="Dipinjam"
    ).count()
    buku_dikembalikan = Peminjaman.objects.filter(
        status="Dikembalikan"
    ).count()
    peminjaman_terbaru = Peminjaman.objects.all().order_by('-id')[:5]

    context = {
        'total_buku': total_buku,
        'total_anggota': total_anggota,
        'buku_dipinjam': buku_dipinjam,
        'buku_dikembalikan': buku_dikembalikan,
        'peminjaman_terbaru': peminjaman_terbaru,
    }

    return render(
        request,
        'library/dashboard.html',
        context
    )


# ==========================
# DASHBOARD ANGGOTA
# ==========================
@login_required(login_url='login')
def dashboard_anggota(request):
    try:
        anggota = Anggota.objects.get(user=request.user)
    except Anggota.DoesNotExist:
        return redirect('login')

    buku_dipinjam = Peminjaman.objects.filter(
        anggota=anggota,
        status='Dipinjam'
    )

    total_dipinjam = buku_dipinjam.count()

    total_riwayat = Peminjaman.objects.filter(
        anggota=anggota
    ).count()

    total_kembali = Peminjaman.objects.filter(
        anggota=anggota,
        status='Dikembalikan'
    ).count()

    buku_terbaru = Buku.objects.order_by('-id')[:5]

    context = {
        'anggota': anggota,
        'total_dipinjam': total_dipinjam,
        'total_riwayat': total_riwayat,
        'total_kembali': total_kembali,
        'belum_kembali': total_dipinjam,
        'buku_dipinjam': buku_dipinjam,
        'buku_terbaru': buku_terbaru,
    }

    return render(request, 'library/dashboard_anggota.html', context)


# ==========================
# DASHBOARD KEPALA
# ==========================
@login_required(login_url='login')
def dashboard_kepala(request):
    if not request.user.groups.filter(name='Kepala').exists():
        return redirect('login')

    total_buku = Buku.objects.count()
    total_anggota = Anggota.objects.count()
    total_peminjaman = Peminjaman.objects.count()
    total_pengembalian = Peminjaman.objects.filter(
        status='Dikembalikan'
    ).count()

    peminjaman_terbaru = Peminjaman.objects.order_by(
        '-tanggal_pinjam'
    )[:5]

    context = {
        'total_buku': total_buku,
        'total_anggota': total_anggota,
        'total_peminjaman': total_peminjaman,
        'total_pengembalian': total_pengembalian,
        'peminjaman_terbaru': peminjaman_terbaru,
    }

    return render(
        request,
        'library/dashboard_kepala.html',
        context
    )


# ==========================
# CRUD ANGGOTA (List)
# ==========================
@login_required(login_url='login')
def anggota(request):
    data_anggota = Anggota.objects.all().order_by('nim')

    return render(
        request,
        'library/anggota/index.html',
        {
            'anggota': data_anggota
        }
    )


# ==========================
# CRUD BUKU
# ==========================
@login_required(login_url='login')
def buku(request):
    data_buku = Buku.objects.all().order_by('kode_buku')

    context = {
        'buku': data_buku
    }

    return render(request, 'library/buku/index.html', context)


@login_required(login_url='login')
def tambah_buku(request):
    if request.method == 'POST':
        form = BukuForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Data buku berhasil ditambahkan.')
            return redirect('buku')

    else:
        form = BukuForm()

    context = {
        'form': form
    }

    return render(request, 'library/buku/tambah.html', context)


@login_required(login_url='login')
def edit_buku(request, id):
    buku = Buku.objects.get(id=id)

    if request.method == "POST":
        form = BukuForm(request.POST, instance=buku)

        if form.is_valid():
            form.save()
            messages.success(request, 'Data buku berhasil diubah.')
            return redirect('buku')

    else:
        form = BukuForm(instance=buku)

    return render(
        request,
        'library/buku/edit.html',
        {
            'form': form
        }
    )


@login_required(login_url='login')
def hapus_buku(request, id):
    buku = Buku.objects.get(id=id)
    buku.delete()
    messages.success(request, 'Data buku berhasil dihapus.')
    return redirect('buku')


# ==========================
# CRUD ANGGOLA (Tambah/Edit/Hapus)
# ==========================
@login_required(login_url='login')
def tambah_anggota(request):
    if request.method == "POST":
        form = AnggotaForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Data anggota berhasil ditambahkan.")
            return redirect('anggota')

    else:
        form = AnggotaForm()

    return render(
        request,
        'library/anggota/tambah.html',
        {
            'form': form
        }
    )


@login_required(login_url='login')
def edit_anggota(request, id):
    anggota = Anggota.objects.get(id=id)

    if request.method == "POST":
        form = AnggotaForm(
            request.POST,
            instance=anggota
        )

        if form.is_valid():
            form.save()
            messages.success(request, "Data anggota berhasil diubah.")
            return redirect('anggota')

    else:
        form = AnggotaForm(instance=anggota)

    return render(
        request,
        'library/anggota/edit.html',
        {
            'form': form
        }
    )


@login_required(login_url='login')
def hapus_anggota(request, id):
    anggota = Anggota.objects.get(id=id)

    if request.method == "POST":
        anggota.delete()
        messages.success(request, "Data anggota berhasil dihapus.")
        return redirect('anggota')

    return render(request, 'library/anggota/hapus.html', {
        'anggota': anggota
    })


# ==========================
# CRUD PEMINJAMAN
# ==========================
@login_required(login_url='login')
def peminjaman(request):
    data = Peminjaman.objects.all().order_by('-tanggal_pinjam')

    context = {
        'peminjaman': data
    }

    return render(request, 'library/peminjaman/index.html', context)


@login_required(login_url='login')
def tambah_peminjaman(request):
    if request.method == "POST":
        form = PeminjamanForm(request.POST)

        if form.is_valid():
            pinjam = form.save(commit=False)
            buku = pinjam.buku

            if buku.stok > 0:
                buku.stok -= 1
                buku.save()
                pinjam.save()
                messages.success(
                    request,
                    "Peminjaman berhasil ditambahkan."
                )
                return redirect('peminjaman')

            else:
                messages.error(
                    request,
                    "Stok buku habis."
                )

    else:
        form = PeminjamanForm()

    return render(
        request,
        'library/peminjaman/tambah.html',
        {
            'form': form
        }
    )


@login_required(login_url='login')
def edit_peminjaman(request, id):
    pinjam = Peminjaman.objects.get(id=id)

    if request.method == "POST":
        form = PeminjamanForm(
            request.POST,
            instance=pinjam
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Data peminjaman berhasil diubah."
            )
            return redirect('peminjaman')

    else:
        form = PeminjamanForm(instance=pinjam)

    return render(
        request,
        'library/peminjaman/edit.html',
        {
            'form': form
        }
    )


@login_required(login_url='login')
def hapus_peminjaman(request, id):
    pinjam = Peminjaman.objects.get(id=id)

    # Kembalikan stok buku
    buku = pinjam.buku
    buku.stok += 1
    buku.save()

    pinjam.delete()

    messages.success(
        request,
        "Data peminjaman berhasil dihapus."
    )

    return redirect('peminjaman')


# ==========================
# CRUD PENGEMBALIAN
# ==========================
@login_required(login_url='login')
def pengembalian(request):
    data = Peminjaman.objects.filter(
        status="Dipinjam"
    )

    return render(
        request,
        'library/pengembalian.html',
        {
            'peminjaman': data
        }
    )


@login_required(login_url='login')
def tambah_pengembalian(request, id):
    peminjaman = Peminjaman.objects.get(id=id)

    if request.method == 'POST':
        form = PengembalianForm(request.POST)

        if form.is_valid():
            pengembalian = form.save(commit=False)
            pengembalian.peminjaman = peminjaman
            pengembalian.save()

            # ubah status peminjaman
            peminjaman.status = "Dikembalikan"
            peminjaman.save()

            # tambah stok buku
            buku = peminjaman.buku
            buku.stok += 1
            buku.save()

            messages.success(
                request,
                "Buku berhasil dikembalikan"
            )

            return redirect('pengembalian')

    else:
        form = PengembalianForm(
            initial={
                'peminjaman': peminjaman
            }
        )

    return render(
        request,
        'library/tambah_pengembalian.html',
        {
            'form': form,
            'peminjaman': peminjaman
        }
    )


@login_required(login_url='login')
def edit_pengembalian(request, id):
    data = Pengembalian.objects.get(id=id)

    if request.method == 'POST':
        form = PengembalianForm(
            request.POST,
            instance=data
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Data pengembalian berhasil diperbarui"
            )
            return redirect('pengembalian')

    else:
        form = PengembalianForm(instance=data)

    return render(
        request,
        'library/edit_pengembalian.html',
        {
            'form': form
        }
    )


@login_required(login_url='login')
def hapus_pengembalian(request, id):
    data = Pengembalian.objects.get(id=id)
    data.delete()

    messages.success(
        request,
        "Data pengembalian berhasil dihapus"
    )

    return redirect('pengembalian')


# ==========================
# LAPORAN
# ==========================
@login_required(login_url='login')
def laporan(request):
    buku = Buku.objects.count()
    anggota = Anggota.objects.count()
    peminjaman = Peminjaman.objects.count()
    pengembalian = Pengembalian.objects.count()

    context = {
        'jumlah_buku': buku,
        'jumlah_anggota': anggota,
        'jumlah_peminjaman': peminjaman,
        'jumlah_pengembalian': pengembalian,
        'data_peminjaman': Peminjaman.objects.all(),
        'data_pengembalian': Pengembalian.objects.all(),
    }

    return render(request, 'library/laporan.html', context)


# ==========================
# KATALOG BUKU
# ==========================
@login_required(login_url='login')
def katalog_buku(request):
    cari = request.GET.get('cari', '')
    data_buku = Buku.objects.all()

    if cari:
        data_buku = data_buku.filter(
            Q(judul__icontains=cari) |
            Q(penulis__icontains=cari) |
            Q(kategori__icontains=cari)
        )

    return render(
        request,
        'library/katalog_buku.html',
        {
            'data_buku': data_buku,
            'cari': cari
        }
    )


# ==========================
# RIWAYAT PEMINJAMAN
# ==========================
@login_required(login_url='login')
def riwayat_peminjaman(request):
    anggota = Anggota.objects.get(user=request.user)
    data = Peminjaman.objects.filter(anggota=anggota)

    return render(
        request,
        'library/riwayat_peminjaman.html',
        {
            'data': data
        }
    )


# ==========================
# PROFIL ANGGOTA
# ==========================
@login_required(login_url='login')
def profil_anggota(request):
    anggota = Anggota.objects.get(user=request.user)

    return render(
        request,
        'library/profil_anggota.html',
        {
            'anggota': anggota
        }
    )


# ==========================
# DATA PEMINJAMAN KEPALA
# ==========================
@login_required(login_url='login')
def data_peminjaman_kepala(request):
    data = Peminjaman.objects.select_related(
        'anggota',
        'buku'
    ).all().order_by('-tanggal_pinjam')

    return render(
        request,
        'library/data_peminjaman_kepala.html',
        {
            'data': data
        }
    )


# ==========================
# HISTORI JABATAN
# ==========================
@login_required(login_url='login')
def histori_jabatan(request):
    data = HistoriJabatan.objects.all()

    return render(
        request,
        'library/histori_jabatan.html',
        {'data': data}
    )


# ==========================
# REGISTRASI ANGGOTA
# ==========================
def registrasi(request):
    if request.method == 'POST':
        form = RegistrasiAnggotaForm(request.POST)

        if form.is_valid():
            user = form.save()

            # Masukkan ke grup Anggota
            group = Group.objects.get(name='Anggota')
            user.groups.add(group)

            # Simpan data anggota dengan status Menunggu
            Anggota.objects.create(
                user=user,
                nama=form.cleaned_data['nama'],
                nim=form.cleaned_data['nim'],
                prodi=form.cleaned_data['prodi'],
                fakultas=form.cleaned_data['fakultas'],
                no_hp=form.cleaned_data['no_hp'],
                alamat=form.cleaned_data['alamat'],
                status='Menunggu',
            )

            messages.success(
                request,
                'Pendaftaran berhasil. Silakan login.'
            )

            return redirect('login')

    else:
        form = RegistrasiAnggotaForm()

    return render(
        request,
        'library/registrasi.html',
        {
            'form': form
        }
    )


# ==========================
# VERIFIKASI ANGGOTA
# ==========================
@login_required(login_url='login')
def verifikasi_anggota(request):
    anggota = Anggota.objects.filter(status='Menunggu')

    return render(
        request,
        'library/verifikasi_anggota.html',
        {
            'anggota': anggota
        }
    )


@login_required(login_url='login')
def setujui_anggota(request, id):
    anggota = Anggota.objects.get(id=id)
    anggota.status = 'Disetujui'
    anggota.save()

    messages.success(
        request,
        'Anggota berhasil disetujui.'
    )

    return redirect('verifikasi_anggota')
