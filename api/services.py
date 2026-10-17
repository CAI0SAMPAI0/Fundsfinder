import requests
import json
from django.core.cache import cache
from dotenv import load_dotenv
import os

load_dotenv()

URL_COTACAO = os.getenv("URL_COTACAO")


def buscar_cotacao(codigo: str) -> dict | None:
    chave_cache = f"cotacao_{codigo.upper()}"
    dados_em_cache = cache.get(chave_cache)
    if dados_em_cache is not None:
        return dados_em_cache  # retorna os dados em cache se existirem sem ficar buscando novamente.
    url = f"{URL_COTACAO}/{codigo.strip().upper()}.SA"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=5)
    if response.status_code == 200:
        dados = response.json()
        resultados = dados.get("chart", {}).get("result")
        if resultados:
            cotacao = resultados[0].get("meta")
            cache.set(chave_cache, cotacao, timeout=60 * 60 * 24)
            return cotacao
    return None
