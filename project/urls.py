from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from financas import views as financas_views
from financas.views import custom_login, custom_logout
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),

    # Rotas principais do app (somente UMA vez)
    path('', RedirectView.as_view(pattern_name='financas:dashboard', permanent=False)),

    # App financas com namespace
    path('financas/', include(('financas.urls', 'financas'), namespace='financas')),

    # Login / Logout personalizados
    path('login/', custom_login, name='login'),
    path('logout/', custom_logout, name='logout'),

    # Registrar usuários
    path('register/', financas_views.register, name='register'),
]
