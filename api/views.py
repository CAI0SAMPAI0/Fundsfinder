from rest_framework import viewsets, permissions
from .models import FundoImobiliario
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import FundoImobiliarioSerializer


class FundoImobiliarioViewSet(viewsets.ModelViewSet):
    # queryset: configura o queryset base para ser utilizado pela API. Ele é utilizado na ação de listar, por exemplo.
    queryset = FundoImobiliario.objects.all()
    serializer_class = FundoImobiliarioSerializer  # configura os dados a serem enviados e utilizados pela API.
    permission_classes = [
        permissions.IsAuthenticated
    ]  # configura as permissões para a API.
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]  # configura os filtros para a API.
    ordering_fields = [
        "dividend_yield_medio_12m",
        "setor",
        "vacancia_financeira",
        "vacancia_fisica",
        "quantidade_ativos",
    ]  # ordena os resultados da API.
    filterset_fields = ["codigo", "setor"]
    search_fields = ["codigo", "setor"]
