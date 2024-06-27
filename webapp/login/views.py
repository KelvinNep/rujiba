from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.urls import reverse

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            # Redirect to the previous page or dashboard if 'next' is not present
            next_page = request.POST.get('next', request.GET.get('next', reverse('dashboard')))
            return redirect(next_page)
        else:
            # Set a flag to indicate login failure
            login_failed = True
            # Capture the 'next' parameter from the GET request
            next_page = request.GET.get('next', '')
            return render(request, 'login.html', {'next': next_page, 'login_failed': login_failed})
    else:
        # Capture the 'next' parameter from the GET request
        next_page = request.GET.get('next', '')
        return render(request, 'login.html', {'next': next_page})
