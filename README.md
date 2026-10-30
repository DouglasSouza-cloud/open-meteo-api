# 🌤️ Open-Meteo API — Consulta de Clima

Aplicação em Python que consome as APIs da **Open-Meteo** para consultar informações meteorológicas a partir do nome de uma cidade informado pelo usuário.

O projeto utiliza duas APIs: a **Geocoding API**, que localiza a cidade e retorna suas coordenadas geográficas, e a **Forecast API**, que utiliza latitude e longitude para retornar as condições meteorológicas atuais.

## ✨ Funcionalidades

- Pesquisa de cidades pelo nome.
- Identificação do país da cidade encontrada.
- Obtenção de latitude e longitude por meio da Geocoding API.
- Consulta das condições meteorológicas atuais.
- Exibição de temperatura, umidade relativa, sensação térmica e velocidade do vento.
- Verificação do status HTTP das requisições e tratamento básico para cidades não encontradas.

## 🛠️ Tecnologias utilizadas

- **Python** — linguagem de programação.
- **Requests** — realização de requisições HTTP.
- **Python-dotenv** — leitura das configurações armazenadas no arquivo `.env`.
- **Open-Meteo** — serviço externo de dados meteorológicos.

## 🌐 APIs utilizadas

| API | Finalidade | Documentação |
|---|---|---|
| Geocoding API | Pesquisar a cidade e obter latitude e longitude | [Documentação](https://open-meteo.com/en/docs/geocoding-api) |
| Forecast API | Consultar as condições meteorológicas | [Documentação](https://open-meteo.com/en/docs) |

As APIs públicas utilizadas neste projeto não exigem API Key para o uso gratuito padrão.

## 📁 Estrutura do projeto

```text
open-meteo-api/
├── app.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

O arquivo `.env` deve existir localmente, mas não deve ser enviado ao GitHub.

## ⚙️ Configuração e execução

### 1. Clone o repositório

```bash
git clone URL_DO_REPOSITORIO
cd open-meteo-api
```

### 2. Crie e ative um ambiente virtual

```bash
python -m venv .venv
```

No Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

O projeto utiliza `requests` e `python-dotenv`.

### 4. Configure as variáveis de ambiente

Crie uma cópia de `.env.example` com o nome `.env` e configure as URLs dos endpoints:

```env
database_url=https://api.open-meteo.com/v1/forecast
database_url_geocoding=https://geocoding-api.open-meteo.com/v1/search
```

Essas variáveis guardam os endereços das APIs; não são credenciais nem API Keys.

### 5. Execute a aplicação

```bash
python app.py
```

Informe o nome da cidade quando solicitado. O programa pesquisará a localização e, em seguida, consultará os dados meteorológicos.

## 📊 Dados consultados

| Campo da API | Informação exibida |
|---|---|
| `temperature_2m` | Temperatura a 2 metros (°C) |
| `relative_humidity_2m` | Umidade relativa do ar (%) |
| `apparent_temperature` | Sensação térmica (°C) |
| `wind_speed_10m` | Velocidade do vento a 10 metros (km/h) |

## 🔄 Fluxo de funcionamento

```text
Usuário informa a cidade
          |
          v
Geocoding API (Open-Meteo)
          |
          v
Retorna latitude e longitude
          |
          v
Forecast API (Open-Meteo)
          |
          v
Retorna os dados meteorológicos em JSON
          |
          v
Python interpreta e exibe os resultados
```

## ⚠️ Observações e melhorias futuras

- Atualmente, o programa utiliza o primeiro resultado retornado pela pesquisa de cidades. Uma melhoria seria permitir que o usuário escolha entre cidades com nomes iguais.
- As requisições podem receber um timeout e tratamento de exceções para lidar com falhas de conexão.
- Também é possível ampliar a consulta para incluir previsão horária, previsão diária e outros indicadores meteorológicos.
- As unidades apresentadas dependem dos parâmetros e das unidades configuradas na requisição à API.

## 📚 Créditos

Dados meteorológicos fornecidos pela [Open-Meteo](https://open-meteo.com/).

Projeto desenvolvido para fins de estudo e prática de consumo de APIs REST com Python.
