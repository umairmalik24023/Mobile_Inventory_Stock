import html
from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout


def home_view(request):
    return render(request, 'index.html')


def admin_view(request):
    user = request.user
    if user.is_authenticated and user.is_superuser:
        return render(request, 'admin.html')
    return render(request, 'error.html', status=403)


def about_view(request):
    return render(request, 'about.html')


def forms_view(request):
    return render(request, 'forms.html')






def logout_view(request):
    """Log out current user and redirect to home page."""
    auth_logout(request)
    return redirect('home')
