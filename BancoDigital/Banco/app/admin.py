from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Cliente, Agencia, Conta, Transacao, Cartao, Notificacao, Extrato

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'CPF', 'email', 'dataCadastro')

@admin.register(Agencia)
class AgenciaAdmin(admin.ModelAdmin):
    list_display = ('nomeAgencia', 'endereco')

@admin.register(Conta)
class ContaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'agencia', 'tipoConta', 'saldo', 'dataAbertura')

@admin.register(Transacao)
class TransacaoAdmin(admin.ModelAdmin):
    list_display = ('conta', 'tipoTransacao', 'valor', 'dataHora', 'status')

@admin.register(Cartao)
class CartaoAdmin(admin.ModelAdmin):
    list_display = ('conta', 'dataExpiracao', 'cvv')

@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'tipoNotificacao', 'dataEnvio')

@admin.register(Extrato)
class ExtratoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'conta', 'acao', 'dataHora')
