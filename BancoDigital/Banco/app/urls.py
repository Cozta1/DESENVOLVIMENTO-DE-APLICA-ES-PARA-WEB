from django.urls import path
from .views import IndexView, TesteView, ContatoView, SobreView, listar_contas  # Importe listar_contas aqui
from . import views

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('teste/', TesteView.as_view(), name='teste'),  # Adicione barra '/' ao final dos paths para manter o padrão
    path('sobre/', SobreView.as_view(), name='sobre'),
    path('contato/', ContatoView.as_view(), name='contato'),
    path('api/contas/', listar_contas, name='listar_contas'),
    path('registrar/', views.registrar, name='registrar'),
    path('login/', views.logar, name='login'),
    path('logout/', views.deslogar, name='logout'),# Use a função listar_contas diretamente
]
