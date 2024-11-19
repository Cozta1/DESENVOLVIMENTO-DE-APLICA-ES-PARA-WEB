from django import forms
from .models import Cliente, Endereco

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password


class ClienteForm(forms.ModelForm):
    senha = forms.CharField(
        widget=forms.PasswordInput, label="Senha", min_length=8
    )
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

        # Verifica se as senhas coincidem
        if senha != senha_confirmacao:
            raise forms.ValidationError("As senhas não coincidem.")
        
        # Se a senha for fornecida, criptografa a senha
        if senha:
            self.instance.set_password(senha)  # Criptografando a senha antes de salvar
        
        return cleaned_data



    
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

from django import forms

class LoginForm(forms.Form):
    cpf = forms.CharField(
        label="CPF",
        max_length=11,  # CPF tem exatamente 11 caracteres numéricos
        min_length=11,  # CPF não pode ter menos que 11 caracteres
        widget=forms.TextInput(attrs={'placeholder': 'Digite seu CPF'})
    )
    senha = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Digite sua senha', 'id': 'id_senha'}),
        label="Senha"
    )

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        
        # Verifica se o CPF possui exatamente 11 caracteres
        if len(cpf) != 11:
            raise ValidationError("O CPF deve ter exatamente 11 caracteres.")
        
        # Verifique se o CPF é numérico
        if not cpf.isdigit():
            raise ValidationError("O CPF deve conter apenas números.")
        
        return cpf

    def clean(self):
        cleaned_data = super().clean()
        cpf = cleaned_data.get("cpf")
        senha = cleaned_data.get("senha")

        # Verifica se o CPF e a senha são válidos
        if cpf and senha:
            cliente = authenticate(cpf=cpf, senha=senha)
            if not cliente:
                raise forms.ValidationError("CPF ou Senha inválidos.")
        return cleaned_data

    
    
    
    
class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = ['cep', 'rua', 'bairro', 'cidade', 'estado', 'numero', 'complemento']
