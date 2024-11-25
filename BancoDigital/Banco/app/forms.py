from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Cliente
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate


class ClienteUserCreationForm(UserCreationForm):
    class Meta:
        model = Cliente
        fields = ('username', 'email', 'first_name', 'last_name', 'CPF', 'telefone', 'foto')


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