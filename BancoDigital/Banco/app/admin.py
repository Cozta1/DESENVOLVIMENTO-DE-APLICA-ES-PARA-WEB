# Register your models here.
from django import forms
from django.contrib import admin

from .models import Cliente, Agencia, Conta, Transacao, Cartao, Endereco, Notificacao



class EnderecoInline(admin.TabularInline):
    model = Endereco
    extra = 1  # Número de formulários em branco para adicionar novos endereços

# Admin para Endereco
class EnderecoAdmin(admin.ModelAdmin):
    # Atualizando list_display para corresponder aos campos do modelo
    list_display = ('rua', 'bairro', 'cidade', 'cliente')  # Alterado 'logradouro' para 'rua'
    search_fields = ('rua', 'bairro', 'cliente__nome')  # Permitindo buscar pelo nome do cliente
    list_filter = ('cliente',)  # Filtrando por cliente

# Admin para Cliente
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'listar_enderecos', 'foto', 'last_login', 'is_active', 'is_staff')
    search_fields = ('nome', 'email', 'CPF')
    list_filter = ('is_active', 'is_staff')
    
    # Inline para adicionar endereços no formulário de cliente
    inlines = [EnderecoInline]
    
    # Definindo os campos no formulário de edição
    fieldsets = (
        (None, {
            'fields': ('nome', 'email', 'telefone', 'CPF', 'foto')
        }),
        ('Segurança', {
            'fields': ('senha', 'is_active', 'is_staff', 'last_login')
        }),
    )
    readonly_fields = ('last_login',)  # 'last_login' deve ser somente leitura

    # Sobrescreve o método get_form para ocultar o campo 'senha' se o cliente já existir
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:  # Se for um cliente já existente, escondemos o campo 'senha' no formulário
            form.base_fields['senha'].widget = forms.HiddenInput()
        return form

# Registro dos modelos no admin
# Verifique se o modelo já foi registrado antes de registrar novamente
try:
    admin.site.unregister(Endereco)
except admin.sites.NotRegistered:
    pass

# Registrando o modelo Endereco e Cliente no admin
admin.site.register(Endereco, EnderecoAdmin)
admin.site.register(Cliente, ClienteAdmin)




    
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
    list_filter = ('tipoTransacao', 'status')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('conta', 'contaDestino')  # Otimizar as consultas para evitar N+1

@admin.register(Cartao)
class CartaoAdmin(admin.ModelAdmin):
    list_display = ('numeroCartao', 'bandeira', 'cvv', 'dataExpiracao', 'conta')
    list_filter = ('bandeira', 'conta')


@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ('conta', 'mensagem', 'dataHora')



