"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import include, path

from . import views

# Textos del panel de administración
admin.site.site_header = 'InvenLote'
admin.site.site_title = 'InvenLote'
admin.site.index_title = 'Panel de inventario multialmacén'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('almacenes/', include('almacenes.urls')),
    path('ubicaciones/', include('ubicaciones.urls')),
    path('categorias/', include('categorias.urls')),
    path('articulos/', include('articulos.urls')),
    path('lotes/', include('lotes.urls')),
    path('movimientos/', include('movimientos.urls')),
]
