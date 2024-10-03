from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Cliente, Agencia, Conta, Transacao, Cartao, Endereco


@admin.register(Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    list_display = ('cep', 'rua', 'bairro', 'cidade', 'estado', 'numero', 'complemento')
    
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('CPF', 'nome', 'email', 'telefone','endereco', 'dataCadastro', 'foto')

@admin.register(Agencia)
class AgenciaAdmin(admin.ModelAdmin):
    list_display = ('nomeagencia', 'numeroagencia', 'endereco')

@admin.register(Conta)
class ContaAdmin(admin.ModelAdmin):
    list_display = ('numeroConta', 'cliente', 'agencia', 'saldo', 'dataAbertura')
    
    def saldo(self, obj):
        return obj.saldo

    saldo.short_description = 'Saldo Atual'
    
@admin.register(Transacao)
class TransacaoAdmin(admin.ModelAdmin):
    list_display = ('numeroTransacao', 'conta', 'tipoTransacao', 'valor', 'dataHora', 'status', 'contaDestino')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('conta', 'contaDestino')  # Otimizar as consultas para evitar N+1

@admin.register(Cartao)
class CartaoAdmin(admin.ModelAdmin):
    list_display = ('numeroCartao', 'bandeira', 'cvv', 'dataExpiracao', 'conta')


# @admin.register(Notificacao)
# class NotificacaoAdmin(admin.ModelAdmin):
#     list_display = ('conta', 'mensagem', 'dataEnvio')



