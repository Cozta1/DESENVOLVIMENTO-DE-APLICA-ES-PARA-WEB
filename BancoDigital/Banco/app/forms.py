from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    senha_confirmacao = forms.CharField(
        widget=forms.PasswordInput, label="Confirmar Senha"
    )

    class Meta:
        model = Cliente
        fields = ['CPF', 'nome', 'email', 'telefone', 'senha', 'senha_confirmacao', 'foto']
        widgets = {
            'senha': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get('senha')
        senha_confirmacao = cleaned_data.get('senha_confirmacao')

        if senha != senha_confirmacao:
            raise forms.ValidationError("As senhas não coincidem.")
        
        if senha:
            self.instance.set_password(senha)  # Criptografando a senha antes de salvar
        
        return cleaned_data

    
    
from django import forms
from .models import Cliente
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password

class LoginForm(forms.Form):
    CPF = forms.CharField(max_length=11)
    senha = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        CPF = cleaned_data.get('CPF')
        senha = cleaned_data.get('senha')

        cliente = Cliente.objects.filter(CPF=CPF).first()
        if cliente and not check_password(senha, cliente.senha):
            raise forms.ValidationError('CPF ou senha inválidos')
        return cleaned_data

