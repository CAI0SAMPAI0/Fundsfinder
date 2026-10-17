from rest_framework import serializers
from .models import FundoImobiliario
from .services import buscar_cotacao


class FundoImobiliarioSerializer(serializers.ModelSerializer):
    preco_mercado = serializers.SerializerMethodField()

    class Meta:
        model = FundoImobiliario  # define qual modelo esse serializer deve serializar.
        fields = [
            "id",
            "codigo",
            "setor",
            "dividend_yield_medio_12m",
            "vacancia_financeira",
            "vacancia_fisica",
            "quantidade_ativos",
            "preco_mercado",
        ]  # define os campos que serão serializados.

    def get_preco_mercado(self, obj):
        dados = buscar_cotacao(obj.codigo)
        return dados.get("regularMarketPrice") if dados else None
