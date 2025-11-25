"""
URL configuration for mydjangoapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views




urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin site
    path('admin.html', views.admin_view, name='admin_dashboard_legacy'),  # direct .html URL to custom dashboard
    path('dashboard/', views.admin_view, name='admin_dashboard'),
    path('dashboard/', include('dashboard.urls')),
    path('logout/', views.logout_view, name='logout'),

    # Friendly and .html routes
    path('about.html', views.about_view, name='about_legacy'),
    path('about/', views.about_view, name='about'),
    path('forms.html', views.forms_view, name='forms_legacy'),
    path('forms/', views.forms_view, name='forms'),

    path('', views.home_view, name='home'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    # Serve assets directory
    from django.conf.urls.static import static
    urlpatterns += static('/assets/', document_root=settings.BASE_DIR / 'assets')


