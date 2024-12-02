from django import views
from django.urls import path
from . import views
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language

urlpatterns = [
    path('', views.home, name='home'),
    path('registro/', views.registro, name='registro'),
    path('cadastrar-endereco/', views.cadastrar_endereco, name='cadastrar_endereco'),
    path('excluir_endereco/<int:endereco_id>/', views.excluir_endereco, name='excluir_endereco'),
    path('selecionar_agencia/', views.selecionar_agencia, name='selecionar_agencia'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('conta/', views.conta_view, name='conta'),
    path('perfil/', views.perfil, name='perfil'),
    path('solicitar_cartao/', views.solicitar_cartao, name='solicitar_cartao'),
    path('transacao/', views.realizar_transacao_view, name='transacao'),
    path('i18n/setlang/', set_language, name='set_language'),
    
]