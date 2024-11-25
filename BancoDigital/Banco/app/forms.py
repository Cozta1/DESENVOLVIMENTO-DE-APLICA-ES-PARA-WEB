from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Cliente
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from .models import Endereco

class ClienteUserCreationForm(UserCreationForm):
    class Meta:
        model = Cliente
        fields = ('username', 'email', 'first_name', 'last_name', 'CPF', 'telefone', 'foto')
        
    def clean_CPF(self):
        cpf = self.cleaned_data.get('CPF')
        if Cliente.objects.filter(CPF=cpf).exists():
            raise forms.ValidationError('CPF já cadastrado.')
        return cpf


class ClienteLoginForm(forms.Form):
    CPF = forms.CharField(max_length=11, label='CPF', widget=forms.TextInput(attrs={'placeholder': 'Digite seu CPF'}))
    password = forms.CharField(widget=forms.PasswordInput(), label='Senha')

    def clean_CPF(self):
        cpf = self.cleaned_data.get('CPF')
        try:
            # Verificar se o CPF existe na base de dados
            cliente = Cliente.objects.get(CPF=cpf)
        except Cliente.DoesNotExist:
            raise forms.ValidationError('CPF não encontrado.')
        return cpf

    def clean(self):
        cleaned_data = super().clean()
        cpf = cleaned_data.get("CPF")
        password = cleaned_data.get("password")

        if cpf and password:
            # Tentando autenticar com o CPF e senha
            user = authenticate(username=cpf, password=password)
            if user is None:
                raise forms.ValidationError('Credenciais inválidas. Tente novamente.')
        return cleaned_data
    
    # forms.py


class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = ['cep', 'rua', 'bairro', 'cidade', 'estado', 'numero', 'complemento']

        widgets = {
            'cep': forms.TextInput(attrs={'placeholder': 'Digite o CEP'}),
            'rua': forms.TextInput(attrs={'placeholder': 'Digite a rua'}),
            'bairro': forms.TextInput(attrs={'placeholder': 'Digite o bairro'}),
            'cidade': forms.TextInput(attrs={'placeholder': 'Digite a cidade'}),
            'estado': forms.Select(attrs={'placeholder': 'Escolha o estado'}),
            'numero': forms.TextInput(attrs={'placeholder': 'Digite o número'}),
            'complemento': forms.TextInput(attrs={'placeholder': 'Complemento (opcional)'}),
        }
