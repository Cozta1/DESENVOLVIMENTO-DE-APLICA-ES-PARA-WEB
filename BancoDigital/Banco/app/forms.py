from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Cliente, Conta, Transacao
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from .models import Endereco
from django.utils.translation import gettext_lazy as _  # Importando a função de tradução


class ClienteUserCreationForm(UserCreationForm):
    class Meta:
        model = Cliente
        fields = ('username', 'CPF', 'first_name', 'last_name', 'email', 'telefone', 'foto')
        
    def clean_CPF(self):
        cpf = self.cleaned_data.get('CPF')
        if Cliente.objects.filter(CPF=cpf).exists():
            raise forms.ValidationError(_('CPF já cadastrado.'))  # Tradução
        return cpf


class ClienteLoginForm(forms.Form):
    CPF = forms.CharField(max_length=11, label=_('CPF'), widget=forms.TextInput(attrs={'placeholder': _('Digite seu CPF')}))  # Tradução
    password = forms.CharField(widget=forms.PasswordInput(), label=_('Senha'))  # Tradução

    def clean_CPF(self):
        cpf = self.cleaned_data.get('CPF')
        try:
            # Verificar se o CPF existe na base de dados
            cliente = Cliente.objects.get(CPF=cpf)
        except Cliente.DoesNotExist:
            raise forms.ValidationError(_('CPF não encontrado.'))  # Tradução
        return cpf

    def clean(self):
        cleaned_data = super().clean()
        cpf = cleaned_data.get("CPF")
        password = cleaned_data.get("password")

        if cpf and password:
            # Tentando autenticar com o CPF e senha
            user = authenticate(username=cpf, password=password)
            if user is None:
                raise forms.ValidationError(_('Credenciais inválidas. Tente novamente.'))  # Tradução
        return cleaned_data


class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = ['cep', 'rua', 'bairro', 'cidade', 'estado', 'numero', 'complemento']

        widgets = {
            'cep': forms.TextInput(attrs={'placeholder': _('Digite o CEP')}),  # Tradução
            'rua': forms.TextInput(attrs={'placeholder': _('Digite a rua')}),  # Tradução
            'bairro': forms.TextInput(attrs={'placeholder': _('Digite o bairro')}),  # Tradução
            'cidade': forms.TextInput(attrs={'placeholder': _('Digite a cidade')}),  # Tradução
            'estado': forms.Select(attrs={'placeholder': _('Escolha o estado')}),  # Tradução
            'numero': forms.TextInput(attrs={'placeholder': _('Digite o número')}),  # Tradução
            'complemento': forms.TextInput(attrs={'placeholder': _('Complemento (opcional)')}),  # Tradução
        }


class TransacaoForm(forms.ModelForm):
    class Meta:
        model = Transacao
        fields = ['conta', 'contaDestino', 'tipoTransacao', 'valor']

    def __init__(self, *args, **kwargs):
        cliente = kwargs.pop('cliente', None)  # Cliente logado
        tipo_transacao = kwargs.pop('tipo_transacao', None)  # Tipo de transação (Depósito, Saque ou Transferência)
        super().__init__(*args, **kwargs)

        # Filtra as contas do cliente para a conta de origem
        if cliente:
            self.fields['conta'].queryset = Conta.objects.filter(cliente=cliente)
        
        # Se for "Depósito" ou "Saque", mostra apenas a conta de origem para contaDestino
        if tipo_transacao in ['deposito', 'saque']:
            self.fields['contaDestino'].queryset = Conta.objects.filter(cliente=cliente)
        else:
            # Para "Transferência", permite escolher qualquer conta
            self.fields['contaDestino'].queryset = Conta.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        tipo_transacao = cleaned_data.get('tipoTransacao')
        conta_origem = cleaned_data.get('conta')
        conta_destino = cleaned_data.get('contaDestino')

        # Verifica se a contaDestino é diferente da contaOrigem em Depósito ou Saque
        if tipo_transacao in ['deposito', 'saque'] and conta_origem != conta_destino:
            self.add_error('contaDestino', _('A conta de destino deve ser a mesma que a conta de origem para Depósito ou Saque.'))  # Tradução

        # Verifica se contaDestino está presente para transferência
        if tipo_transacao == 'transferencia' and not conta_destino:
            self.add_error('contaDestino', _('A conta de destino é obrigatória para transferências.'))  # Tradução

        return cleaned_data
