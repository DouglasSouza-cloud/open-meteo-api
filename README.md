# 🌤️ ClimaAgora — Consulta e previsão do tempo

O **ClimaAgora** é uma aplicação desenvolvida em Python para consultar informações meteorológicas de cidades escolhidas pelo usuário. O projeto utiliza os serviços da **Open-Meteo** para localizar cidades e obter dados do clima, oferecendo duas formas de utilização: uma aplicação de terminal e uma interface visual construída com Streamlit.

---

## ✨ Funcionalidades

### Consulta pelo terminal
- Pesquisa de cidades pelo nome.
- Recuperação de país, latitude e longitude da localização encontrada.
- Consulta das condições meteorológicas atuais.
- Exibição de temperatura, umidade relativa, sensação térmica e velocidade do vento.

### Interface web com Streamlit
- Pesquisa de cidades e seleção entre resultados com nomes semelhantes.
- Dashboard com temperatura atual, condição climática e localização.
- Indicadores de umidade, vento e sensação térmica.
- Gráfico de temperatura ao longo do dia.
- Previsão diária para os próximos cinco dias, com temperaturas máximas e mínimas e probabilidade máxima de precipitação.
- Página de gráficos com temperatura, probabilidade de chuva e velocidade do vento.
- Página com informações sobre o projeto.
- Visualização do JSON retornado pela API.

## 🖥️ Tecnologias utilizadas

| Tecnologia | Utilização |
|---|---|
| Python | Linguagem principal do projeto |
| Requests | Requisições HTTP para as APIs |
| Streamlit | Construção da interface web |
| Pandas | Organização dos dados para os gráficos |
| Altair | Criação dos gráficos |
| python-dotenv | Leitura das configurações do arquivo `.env` na aplicação de terminal |
| Open-Meteo | Fornecimento dos dados de geolocalização e meteorologia |

## 🌐 APIs utilizadas

O projeto utiliza dois serviços da Open-Meteo:

| API | Finalidade | Documentação |
|---|---|---|
| Geocoding API | Pesquisa a cidade e retorna informações de localização, incluindo latitude e longitude | [Documentação](https://open-meteo.com/en/docs/geocoding-api) |
| Forecast API | Retorna condições atuais, dados horários e previsão diária | [Documentação](https://open-meteo.com/en/docs) |

As consultas utilizadas neste projeto não exigem uma API Key para o uso gratuito padrão da Open-Meteo. Consulte os [termos de uso](https://open-meteo.com/en/terms) para conhecer os limites e condições aplicáveis.

## 📁 Estrutura do projeto

```text
open-meteo-api/
├── app.py
├── front-end/
│   └── streamlit_app.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

- `app.py`: versão de terminal que pesquisa a cidade e consulta as condições atuais.
- `front-end/streamlit_app.py`: interface web com dashboard, gráficos e previsão diária.
- `.env.example`: modelo das variáveis de ambiente utilizadas pela aplicação de terminal.
- `.env`: arquivo local de configuração; não deve ser enviado ao GitHub.
- `requirements.txt`: dependências Python do projeto.

## ⚙️ Instalação

### 1. Clone o repositório

```bash
git clone URL_DO_REPOSITORIO
cd open-meteo-api
```

Substitua `URL_DO_REPOSITORIO` pelo endereço do seu repositório GitHub.

### 2. Crie um ambiente virtual

```bash
python -m venv .venv
```

Ative o ambiente virtual:

**Windows — PowerShell**
```powershell
.venv\Scripts\Activate.ps1
```

**Windows — Prompt de Comando**
```cmd
.venv\Scripts\activate.bat
```

**Linux / macOS**
```bash
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

## 🚀 Como executar

O projeto possui duas formas de execução.

### Opção 1 — Aplicação pelo terminal

Crie um arquivo `.env` na raiz do projeto, usando `.env.example` como referência:

```env
database_url=https://api.open-meteo.com/v1/forecast
database_url_geocoding=https://geocoding-api.open-meteo.com/v1/search
```

Depois execute:

```bash
python app.py
```

Informe o nome da cidade quando solicitado. O programa pesquisa a localização e utiliza as coordenadas retornadas para consultar o clima.

### Opção 2 — Interface web com Streamlit

Na raiz do projeto, execute:

```bash
streamlit run front-end/streamlit_app.py
```

O Streamlit abrirá a aplicação no navegador. Digite o nome de uma cidade, clique em **Pesquisar**, selecione a localização correta e clique em **Consultar previsão**.

> A interface Streamlit utiliza os endereços públicos dos endpoints da Open-Meteo definidos no próprio arquivo `front-end/streamlit_app.py`. O `.env` é utilizado pela versão de terminal (`app.py`).

## 🔄 Como funciona o consumo das APIs

O fluxo de consulta segue estas etapas:

```text
Usuário informa o nome da cidade
              |
              v
       Geocoding API
              |
              v
   Retorna dados da localização
   (nome, país, latitude e longitude)
              |
              v
        Forecast API
              |
              v
   Retorna os dados meteorológicos
              |
              v
 Python organiza os dados recebidos
              |
              v
 Terminal ou dashboard Streamlit
```

A Geocoding API transforma o nome da cidade em coordenadas geográficas. Em seguida, a Forecast API recebe latitude e longitude e retorna os dados meteorológicos correspondentes.

## 📊 Dados meteorológicos consultados

### Condições atuais

| Campo | Informação | Unidade |
|---|---|---|
| `temperature_2m` | Temperatura do ar a 2 metros | °C |
| `relative_humidity_2m` | Umidade relativa do ar | % |
| `apparent_temperature` | Sensação térmica | °C |
| `wind_speed_10m` | Velocidade do vento a 10 metros | km/h |
| `weather_code` | Código da condição meteorológica | Código WMO |

### Dados horários

A interface também consulta:

- `temperature_2m`: temperatura por horário.
- `precipitation_probability`: probabilidade de precipitação.
- `weather_code`: condição meteorológica por horário.
- `wind_speed_10m`: velocidade do vento por horário.

### Dados diários

A previsão diária utiliza:

- `weather_code`: condição meteorológica do dia.
- `temperature_2m_max`: temperatura máxima.
- `temperature_2m_min`: temperatura mínima.
- `precipitation_probability_max`: probabilidade máxima de precipitação.

A interface solicita uma previsão de cinco dias e utiliza o fuso horário local retornado pela API.

## 🧩 Exemplo de requisição

Exemplo simplificado de consulta à Forecast API com Python:

```python
import requests

url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": -26.3044,
    "longitude": -48.8487,
    "current": (
        "temperature_2m,"
        "relative_humidity_2m,"
        "apparent_temperature,"
        "wind_speed_10m"
    )
}

response = requests.get(url, params=params)
dados = response.json()

print(dados["current"]["temperature_2m"])
```

A resposta é recebida em JSON. Os valores são acessados pelas chaves correspondentes, como `dados["current"]["temperature_2m"]`.

## 🔐 Configurações e segurança

- O arquivo `.env` contém configurações locais e não deve ser versionado.
- O `.env.example` pode ser compartilhado, pois apresenta apenas os nomes das variáveis e os endpoints públicos.
- A Open-Meteo não exige uma chave de API para as consultas gratuitas utilizadas neste projeto.

## 📚 Créditos

- Dados meteorológicos: [Open-Meteo](https://open-meteo.com/)
- Documentação da Geocoding API: [open-meteo.com/en/docs/geocoding-api](https://open-meteo.com/en/docs/geocoding-api)
- Documentação da Forecast API: [open-meteo.com/en/docs](https://open-meteo.com/en/docs)

Projeto desenvolvido para fins educacionais, com o objetivo de praticar requisições HTTP, consumo de APIs REST, interpretação de JSON e desenvolvimento de interfaces com Python e Streamlit.
