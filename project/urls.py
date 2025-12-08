from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from financas import views as financas_views
from financas.views import custom_logout, custom_login


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='financas/login.html'), name='login'),
    #path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/register/', financas_views.register, name='register'),
    path('financas/', include('financas.urls', namespace='financas')),
    path('', RedirectView.as_view(pattern_name='financas:dashboard', permanent=False)),
    path('logout/', custom_logout, name='logout'),
    #path('login/', custom_login, name='login'),
    
    # Recuperação de senha
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='financas/password_reset.html'
         ),
         name='password_reset'),

    path('password-reset-enviado/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='financas/password_reset_done.html'
         ),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='financas/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),

    path('reset/sucesso/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='financas/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]

