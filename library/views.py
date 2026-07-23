from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Buku, Anggota, Peminjaman, Pengembalian
from .forms import BukuForm, AnggotaForm, PeminjamanForm, PengembalianForm


def home(request):
    return redirect('login')


def login_view(request):

    # Jika sudah login, langsung ke dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')

    # Proses login
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        # Jika login gagal
        return render(
            request,
            'library/login.html',
            {
                'error': 'Username atau Password salah!'
            }
        )

    # Tampilkan halaman login
    return render(request, 'library/login.html')


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


def logout_view(request):
    logout(request)
    return redirect('login')


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
# CRUD ANGGOTA
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

            # Kurangi stok buku
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
    
@login_required
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
    
@login_required
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
    
@login_required
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
    
@login_required
def hapus_pengembalian(request, id):

    data = Pengembalian.objects.get(id=id)

    data.delete()

    messages.success(
        request,
        "Data pengembalian berhasil dihapus"
    )

    return redirect('pengembalian')

@login_required
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