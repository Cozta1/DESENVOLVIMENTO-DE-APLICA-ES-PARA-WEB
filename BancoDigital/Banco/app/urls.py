from django import views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('registro/', views.registro, name='registro'),
    path('cadastrar-endereco/', views.cadastrar_endereco, name='cadastrar_endereco'),
    path('excluir_endereco/<int:endereco_id>/', views.excluir_endereco, name='excluir_endereco'),
    path('selecionar_agencia/', views.selecionar_agencia, name='selecionar_agencia'),
    path('login/', views.login_view, name='login'),
    path('sucesso/', views.sucesso, name='sucesso'),
    path('logout/', views.logout_view, name='logout'),
    path('conta/', views.conta_view, name='conta'),
    path('perfil/', views.perfil, name='perfil'),
    path('solicitar_cartao/', views.solicitar_cartao, name='solicitar_cartao'),
    path('transacao/', views.transacao_view, name='transacao'),
    
]