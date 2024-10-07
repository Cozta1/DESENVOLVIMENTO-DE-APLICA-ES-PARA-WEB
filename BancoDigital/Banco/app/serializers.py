from rest_framework import serializers
from .models import Conta

class ContaSerializer(serializers.ModelSerializer):
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True)  # Adiciona o nome do cliente
    saldo = serializers.SerializerMethodField()  # Para retornar o saldo

    class Meta:
        model = Conta
        fields = ['numeroConta', 'dataAbertura', 'cliente_nome', 'saldo', 'agencia']

    def get_saldo(self, obj):
        return obj.saldo  # Retorna o saldo da conta
