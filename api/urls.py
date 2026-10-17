from rest_framework.routers import DefaultRouter
from .views import FundoImobiliarioViewSet

app_name = "api"  # epecifica o nome das URLConfs

router = DefaultRouter(
    trailing_slash=False
)  # cria um router padrão e configura o trailing_slash para False para evitar erros de URL.
router.register(
    r"fundos", FundoImobiliarioViewSet
)  # registra o FundoImobiliarioViewSet com o nome 'fundos'

urlpatterns = router.urls  # retorna as URLs do router.
