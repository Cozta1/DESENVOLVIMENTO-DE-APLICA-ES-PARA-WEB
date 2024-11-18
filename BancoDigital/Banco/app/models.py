import uuid
import requests
from django.db.models import Sum
from django.db import models
from stdimage.models import StdImageField
from django.utils.translation import gettext_lazy as _
import random
from datetime import date, timedelta

from django.contrib.auth.hashers import make_password

def get_file_path(_instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return filename

# Models


class Endereco(models.Model):
    ESTADO_CHOICES = [
        ('AC', 'AC'), ('AL', 'AL'), ('AP', 'AP'), ('AM', 'AM'), ('BA', 'BA'),
        ('CE', 'CE'), ('DF', 'DF'), ('ES', 'ES'), ('GO', 'GO'), ('MA', 'MA'),
        ('MT', 'MT'), ('MS', 'MS'), ('MG', 'MG'), ('PA', 'PA'), ('PB', 'PB'),
        ('PR', 'PR'), ('PE', 'PE'), ('PI', 'PI'), ('RJ', 'RJ'), ('RN', 'RN'),
        ('RS', 'RS'), ('RO', 'RO'), ('RR', 'RR'), ('SC', 'SC'), ('SP', 'SP'),
        ('SE', 'SE'), ('TO', 'TO'),
    ]
    
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE, related_name='enderecos', null=True, blank=True)
    cep = models.CharField(_('CEP'), max_length=8)
    rua = models.CharField(_('Rua'), max_length=100)
    bairro = models.CharField(_('Bairro'), max_length=50)
    cidade = models.CharField(_('Cidade'), max_length=50)
    estado = models.CharField(_('Estado'), max_length=2, choices=ESTADO_CHOICES)
    numero = models.CharField(_('Número'), max_length=10)
    complemento = models.CharField(_('Complemento'), max_length=50, null=True, blank=True)
    
    class Meta:
        verbose_name = _('Endereço')
        verbose_name_plural = _('Endereços')

    def __str__(self):
        return f'{self.bairro} - {self.rua} - {self.numero}'
    
    
    ###################################################################################
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from stdimage.models import StdImageField
from django.utils.translation import gettext_lazy as _
    
class ClienteManager(BaseUserManager):
    def create_user(self, CPF, nome, email, telefone, senha, **extra_fields):
        if not CPF:
            raise ValueError("O CPF deve ser fornecido")
        cliente = self.model(CPF=CPF, nome=nome, email=email, telefone=telefone, **extra_fields)
        cliente.set_password(senha)  # Criptografar a senha
        cliente.save(using=self._db)
        return cliente

    def create_superuser(self, CPF, nome, email, telefone, senha, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(CPF, nome, email, telefone, senha, **extra_fields)

class Cliente(AbstractBaseUser):
    CPF = models.CharField(_('CPF'), max_length=11, unique=True, primary_key=True)
    nome = models.CharField(_('Nome'), max_length=100, null=False, blank=False)
    email = models.EmailField(_('E-Mail'), unique=True, null=False, blank=False, default='')
    telefone = models.CharField(_('Telefone'), max_length=11, unique=True, null=False, blank=False, default='')
    senha = models.CharField(_('Senha'), max_length=255)
    last_login = models.DateTimeField(_('Último login'), auto_now=True)
    dataCadastro = models.DateTimeField(auto_now_add=True)
    foto = StdImageField(_('Foto'), null=True, blank=True, upload_to='clientes/', variations={'thumb': {'width': 480, 'height': 480, 'crop': True}})

    # Campos de autenticação e controle de permissão
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Métodos necessários para autenticação do Django
    USERNAME_FIELD = 'CPF'  # Campo para login
    REQUIRED_FIELDS = ['nome', 'email', 'telefone']  # Campos obrigatórios no cadastro

    objects = ClienteManager()

    def __str__(self):
        return self.nome

    def set_password(self, raw_password):
        """Método para criptografar a senha"""
        self.senha = make_password(raw_password)

    def check_password(self, raw_password):
        """Método para verificar a senha"""
        return check_password(raw_password, self.senha)

    class Meta:
        verbose_name = _('Cliente')
        verbose_name_plural = _('Clientes')

    def listar_enderecos(self):
        return ", ".join(str(endereco) for endereco in self.enderecos.all())
    listar_enderecos.short_description = 'Endereços'
    

# class Cliente(models.Model):
#     CPF = models.CharField(_('CPF'), max_length=11, unique=True, primary_key=True)
#     nome = models.CharField(_('Nome'), max_length=100, null=False, blank=False)
#     email = models.EmailField(_('E-Mail'), unique=True, null=False, blank=False, default='')
#     telefone = models.CharField(_('Telefone'), max_length=11, unique=True, null=False, blank=False, default='')
#     senha = models.CharField(_('Senha'), max_length=25)
#     dataCadastro = models.DateTimeField(auto_now_add=True)
#     foto = StdImageField(_('Foto'), null=True, blank=True, upload_to=get_file_path, variations={'thumb': {'width': 480, 'height': 480, 'crop': True}})

#     class Meta:
#         verbose_name = _('Cliente')
#         verbose_name_plural = _('Clientes')

#     def __str__(self):
#         return self.nome

#     def listar_enderecos(self):
#         return ", ".join(str(endereco) for endereco in self.enderecos.all())
#     listar_enderecos.short_description = 'Endereços' 
    
    
#     def set_password(self, raw_password):
#         """Método para criptografar a senha"""
#         self.senha = make_password(raw_password)

#     def check_password(self, raw_password):
#         """Método para verificar a senha"""
#         from django.contrib.auth.hashers import check_password
#         return check_password(raw_password, self.senha)


###################################################################################


class Agencia(models.Model):
    nomeagencia = models.CharField(_('Nome da Agência'), max_length=100)
    numeroagencia = models.AutoField(primary_key=True, unique=True, editable=False)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Agência')
        verbose_name_plural = _('Agências')

    def __str__(self):
        return self.nomeagencia


###################################################################################

class Conta(models.Model):
    numeroConta = models.AutoField(_('Número da Conta'), primary_key=True, unique=True, editable=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    agencia = models.ForeignKey(Agencia, on_delete=models.CASCADE)
    dataAbertura = models.DateField(_('Data de Abertura'), auto_now_add=True)

    class Meta:
        verbose_name = _('Transação')
        verbose_name_plural = _('Transações')

    def __str__(self):
        return f'Transação {self.numeroTransacao}: {self.tipoTransacao} de {self.valor}'

    @property
    def saldo(self):
        total_creditos = self.transacoes.filter(
            tipoTransacao__in=['deposito'],
            status='concluida',
            contaDestino=self
        ).aggregate(Sum('valor'))['valor__sum'] or 0

        total_debitos = self.transacoes.filter(
            tipoTransacao__in=['saque'],
            status='concluida',
            conta=self
        ).aggregate(Sum('valor'))['valor__sum'] or 0

        return total_creditos - total_debitos

    def depositar(self, valor):
        if valor <= 0:
            raise ValueError("O valor do depósito deve ser positivo.")

    def sacar(self, valor):
        if valor <= 0:
            raise ValueError("O valor do saque deve ser positivo.")
        if self.saldo < valor:
            raise ValueError("Saldo insuficiente para realizar o saque.")

    def transferir(self, contaDestino, valor):
        if valor <= 0:
            raise ValueError("O valor da transferência deve ser positivo.")
        if self.saldo < valor:
            raise ValueError("Saldo insuficiente para realizar a transferência.")
        self.sacar(valor)
        contaDestino.depositar(valor)

    class Meta:
        verbose_name = _('Conta')
        verbose_name_plural = _('Contas')

    def __str__(self):
        return f'{self.cliente.nome} - {self.saldo}'


###################################################################################


class Transacao(models.Model):
    numeroTransacao = models.AutoField(_('Número da Transação'), primary_key=True)
    conta = models.ForeignKey(Conta, on_delete=models.CASCADE, related_name='transacoes')
    contaDestino = models.ForeignKey(Conta, on_delete=models.CASCADE, related_name='transacoes_destino', null=True, blank=False)
    valor = models.DecimalField(_('Valor'), max_digits=10, decimal_places=2)
    tipoTransacao = models.CharField(_('Tipo de Transação'), max_length=50, choices=[
        ('deposito', 'Depósito'),
        ('saque', 'Saque'),
        ('transferencia', 'Transferência')
    ])
    status = models.CharField(_('Status'), max_length=20, default='pendente', editable=False)
    dataHora = models.DateTimeField(_('Data e Hora da Transação'), auto_now_add=True, null=True)

    

    def save(self, *args, **kwargs):
        if self.tipoTransacao == 'saque':
            self.conta.sacar(self.valor)
            self.status = 'concluida'
            super().save(*args, **kwargs)
            Notificacao.objects.create(
                conta=self.conta,
                mensagem=f"Saque no valor de: R$:{self.valor} de {self.contaDestino} realizado com sucesso para transferência.")
            
        else:
            if self.tipoTransacao == 'deposito':
                self.conta.depositar(self.valor)
                self.status = 'concluida'
                super().save(*args, **kwargs)
                
                Notificacao.objects.create(
                    conta=self.conta,
                    mensagem=f"Depósito no valor de: R$:{self.valor} de {self.contaDestino} realizado com sucesso.")
                
            else:
                if self.tipoTransacao == 'transferencia' and self.contaDestino:
                    saque = Transacao(
                        conta=self.conta,
                        contaDestino=self.conta,
                        valor=self.valor,
                        tipoTransacao='saque',
                        status='concluida',
                        dataHora=self.dataHora,)
                    saque.save()

                    deposito = Transacao(
                        conta=self.contaDestino,
                        contaDestino=self.contaDestino,
                        valor=self.valor,
                        tipoTransacao='deposito',
                        status='concluida',
                        dataHora=self.dataHora,)
                    deposito.save()

                    self.status = 'concluida'

            super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Transação')
        verbose_name_plural = _('Transações')

    def __str__(self):
        return f'Transação {self.numeroTransacao}: {self.tipoTransacao} de {self.valor}'


###################################################################################


class Cartao(models.Model):
    BANDEIRAS = [
        ('visa', 'Visa'),
        ('elo', 'Elo'),
        ('mastercard', 'MasterCard'),
    ]

    numeroCartao = models.BigIntegerField(_('Numero do Cartão'), unique=True, blank=True, editable=False)
    conta = models.ForeignKey(Conta, on_delete=models.CASCADE)
    bandeira = models.CharField(_('Bandeira'), max_length=20, choices=BANDEIRAS, default='visa')
    dataExpiracao = models.DateField(_('Data de Expiração'), blank=True, editable=False)
    cvv = models.IntegerField(_('CVV'), blank=True, editable=False)

    class Meta:
        verbose_name = _('Cartão')
        verbose_name_plural = _('Cartões')

    def save(self, *args, **kwargs):
        if not self.numeroCartao:
            self.numeroCartao = self.gerar_numero_cartao()
        if not self.cvv:
            self.cvv = random.randint(100, 999)
        if not self.dataExpiracao:
            self.dataExpiracao = date.today() + timedelta(days=365*4)

        super().save(*args, **kwargs)

    def gerar_numero_cartao(self):
        if self.bandeira == 'visa':
            prefix = '4'
        else:
            if self.bandeira == 'mastercard':
                prefix = '5'
            else:
                if self.bandeira == 'elo':
                    prefix = '6'
                else:
                    raise ValueError("Bandeira do cartão inválida")

        numero = prefix + ''.join([str(random.randint(0, 9)) for _ in range(15)])
        return int(numero)

    def __str__(self):
        return f'{self.conta.cliente.nome} - {self.bandeira}'


##########################################################################################


class Notificacao(models.Model):
    conta = models.ForeignKey(Conta, on_delete=models.CASCADE, related_name='notificacoes')
    mensagem = models.TextField(_('Mensagem'))
    dataHora = models.DateTimeField(_('Data e Hora'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Notificação')
        verbose_name_plural = _('Notificações')