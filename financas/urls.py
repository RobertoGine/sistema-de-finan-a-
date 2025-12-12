from django.urls import path
from . import views

#teste envio de email
#from django.urls import path
#from .views import teste_email


app_name = 'financas'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('transacoes/', views.lista_transacoes, name='lista_transacoes'),
    path('transacoes/novo/', views.criar_transacao, name='criar_transacao'),
    path('transacoes/<int:pk>/editar/', views.editar_transacao, name='editar_transacao'),
    path('transacoes/<int:pk>/excluir/', views.excluir_transacao, name='excluir_transacao'),
    path('relatorio/', views.relatorio_mensal, name='relatorio_mensal'),
    path('relatorio/pdf/', views.gerar_pdf_relatorio, name='relatorio_pdf'),
    #lembrete contas a pagar
    path("contas/", views.listar_contas, name="listar_contas"),
    path("contas/nova/", views.cadastrar_conta, name="cadastrar_conta"),
    path("contas/<int:pk>/editar/", views.editar_conta, name="editar_conta"),
    path("contas/<int:pk>/excluir/", views.excluir_conta, name="excluir_conta"),
    
    #path("teste-email/", teste_email, name="teste_email"),
]
