from django.urls import path
from . import views

app_name = 'financas'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('transacoes/', views.lista_transacoes, name='lista_transacoes'),
    path('transacoes/novo/', views.criar_transacao, name='criar_transacao'),
    path('transacoes/<int:pk>/editar/', views.editar_transacao, name='editar_transacao'),
    path('transacoes/<int:pk>/excluir/', views.excluir_transacao, name='excluir_transacao'),
    path('relatorio/', views.relatorio_mensal, name='relatorio_mensal'),
    path('relatorio/pdf/', views.gerar_pdf_relatorio, name='relatorio_pdf'),
]
