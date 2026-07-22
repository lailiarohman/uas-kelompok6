from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


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
    return render(request, 'library/dashboard.html')


def logout_view(request):
    logout(request)
    return redirect('login')