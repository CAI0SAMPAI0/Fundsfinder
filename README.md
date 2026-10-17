# FundsFinder API

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django" />
  <img src="https://img.shields.io/badge/Django_REST_Framework-A30000?style=for-the-badge&logo=django&logoColor=white" alt="DRF" />
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/Requests-2C5E8A?style=for-the-badge&logo=python&logoColor=white" alt="Requests" />
</p>

Uma API REST desenvolvida em Django REST Framework (DRF) para consulta, gestao e analise de Fundos Imobiliarios (FIIs) negociados na B3.

A API integra dados cadastrais no banco de dados com cotacoes de mercado em tempo real obtidas de servico financeiro externo, utilizando estrategia de cache em memoria para garantir alta performance e evitar requisicoes repetitivas a servicos de terceiros.

---

## Tecnologias e Bibliotecas

| Tecnologia | Descricao |
|---|---|
| Python | Linguagem base do projeto |
| Django | Framework web e ORM |
| Django REST Framework (DRF) | Toolkit para construcao de APIs REST com Browsable API |
| django-filter | Filtragem declarativa de consultas via parametros de URL |
| Requests | Cliente HTTP para consumo de APIs financeiras externas |
| python-dotenv | Gerenciamento de configuracoes via variaveis de ambiente (.env) |
| PostgreSQL / SQLite | Bancos de dados relacionais suportados |

---

## Configuracao do Ambiente (.env)

Crie um arquivo `.env` na raiz do projeto (no mesmo nivel de `manage.py`) com as seguintes variaveis:

```env
# URL base do servico externo de cotacoes
URL_COTACAO=https://query1.finance.yahoo.com/v8/finance/chart

# Exemplo para conexao com PostgreSQL (se aplicavel)
# DATABASE_URL=postgres://usuario:senha@localhost:5432/fundsfinder
```

O arquivo `.env` contem credenciais locais e nao deve ser versionado no Git.

---

## Instalacao e Execucao

### 1. Clonar o repositorio
```bash
git clone https://github.com/CAI0SAMPAI0/Fundsfinder.git
cd Fundsfinder
```

### 2. Criar e ativar o ambiente virtual
- No Windows:
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\activate
  ```
- No Linux / macOS:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 3. Instalar as dependencias
```bash
pip install -r requirements.txt
```

### 4. Executar as migracoes
```bash
python manage.py migrate
```

### 5. Carregar os dados iniciais dos fundos (Opcional)
Para popular o banco com os 25 fundos imobiliarios ja catalogados:
```bash
python manage.py loaddata fundos_fixtures.json
```

### 6. Criar um superusuario para autenticacao
Como os endpoints exigem autenticacao (`IsAuthenticated`), crie seu usuario:
```bash
python manage.py createsuperuser
```

### 7. Iniciar o servidor
```bash
python manage.py runserver
```

A API estara disponivel em: `http://127.0.0.1:8000/`

---

## Como Usar a API

### Autenticacao na Browsable API
Acesse pelo navegador:
- `http://127.0.0.1:8000/api-auth/login/`

Efetue o login com as credenciais cadastradas no `createsuperuser`.

### Endpoints

A rota principal da API e: `/api/v1/fundos`

| Metodo | Rota | Descricao |
|---|---|---|
| GET | `/api/v1/fundos` | Lista todos os fundos com cotacao atual de mercado |
| POST | `/api/v1/fundos` | Cadastra um novo fundo imobiliario |
| GET | `/api/v1/fundos/<id>` | Detalhes de um fundo especifico |
| PUT / PATCH | `/api/v1/fundos/<id>` | Atualiza dados do fundo |
| DELETE | `/api/v1/fundos/<id>` | Remove o fundo do banco |

### Filtros, Buscas e Ordenacao

- Filtrar por setor:
  ```http
  GET /api/v1/fundos?setor=logistica
  ```
  *(Opcoes de setor: `hospital`, `hotel`, `hibrido`, `lajes_corporativas`, `logistica`, `residencial`, `titulos_valores_mobiliarios`, `outros`)*

- Buscar por termo (Codigo ou Setor):
  ```http
  GET /api/v1/fundos?search=MXRF11
  ```

- Ordenar resultados:
  ```http
  GET /api/v1/fundos?ordering=-dividend_yield_medio_12m
  ```

---

## Exemplo de Resposta JSON

```json
{
  "id": "161aaef3-a2e3-438d-ae5e-9fba1a88be00",
  "codigo": "MXRF11",
  "setor": "titulos_valores_mobiliarios",
  "dividend_yield_medio_12m": "12.10",
  "vacancia_financeira": "0.00",
  "vacancia_fisica": "0.00",
  "quantidade_ativos": 0,
  "preco_mercado": 9.34
}
```

---

## Arquitetura de Cache
Para otimizar o tempo de resposta nas listagens e respeitar os limites de requisicao de servicos externos:
- As cotacoes sao armazenadas no cache em memoria do Django (`django.core.cache`) com expiracao de 24 horas (`60 * 60 * 24` segundos).
- Na primeira consulta, a cotacao e obtida externamente; nas chamadas seguintes, o valor e recuperado instantaneamente da memoria.
