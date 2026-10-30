import streamlit as st
import requests
import pandas as pd
import altair as alt
import textwrap
import html

from datetime import datetime


# ==========================================
# CONFIGURAÇÕES
# ==========================================

st.set_page_config(
    page_title="ClimaAgora | Weather Dashboard",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


# ==========================================
# FUNÇÃO DE RENDERIZAÇÃO HTML
# ==========================================

def render_html(content):
    """Renderiza HTML diretamente, sem passar pelo parser Markdown."""
    st.html(textwrap.dedent(content).strip())


# ==========================================
# ESTILIZAÇÃO
# ==========================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
    --background: #090a19;
    --sidebar: #11112b;
    --card: #191934;
    --purple: #8275ff;
    --cyan: #65d5e8;
    --text: #f4f4ff;
    --muted: #999bbd;
}

.stApp {
    background:
        radial-gradient(ellipse at 80% 0%, #202044 0%, transparent 40%),
        var(--background);
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
}

header[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stToolbar"] {
    visibility: hidden;
    height: 0;
}

.block-container {
    max-width: 1500px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: var(--text) !important;
}

p, label {
    color: var(--text);
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: #11112b;
    border-right: 1px solid rgba(255,255,255,.06);
}

section[data-testid="stSidebar"] > div {
    padding-top: 2rem;
}

.sidebar-logo {
    font-family: 'Space Grotesk';
    font-size: 1.5rem;
    font-weight: 700;
    color: white;
    margin-bottom: 2rem;
}

.sidebar-logo span {
    color: var(--purple);
}

section[data-testid="stSidebar"] .stRadio label {
    color: #c7c8e0 !important;
}

/* INPUT */

div[data-testid="stTextInput"] input {
    background: #252545 !important;
    color: #ffffff !important;
    border: 1px solid #45456d !important;
    border-radius: 12px !important;
    min-height: 45px;
    caret-color: white;
}

div[data-testid="stTextInput"] input::placeholder {
    color: #aaaaca !important;
    opacity: 1;
}

/* BOTÕES */

div[data-testid="stButton"] button,
div[data-testid="stFormSubmitButton"] button {
    background: linear-gradient(110deg, #7767ef, #a17aff);
    color: white !important;
    border: none;
    border-radius: 11px;
    min-height: 43px;
    font-weight: 700;
    transition: .2s;
}

div[data-testid="stButton"] button:hover,
div[data-testid="stFormSubmitButton"] button:hover {
    filter: brightness(1.2);
    transform: translateY(-1px);
}

/* SELECTBOX */

div[data-baseweb="select"] > div {
    background: #252545;
    border-color: #45456d;
    color: white;
    border-radius: 10px;
}

div[data-baseweb="popover"] {
    color: #17172d;
}

/* CABEÇALHO */

.welcome {
    color: var(--purple);
    font-size: .8rem;
    font-weight: 800;
    letter-spacing: .16em;
}

.main-title {
    font-family: 'Space Grotesk';
    font-size: 2.2rem;
    font-weight: 700;
    margin: .2rem 0;
}

.subtitle {
    color: var(--muted);
    font-size: .9rem;
    margin-bottom: 1.5rem;
}

/* CARDS */

.weather-card {
    background: linear-gradient(145deg, #1c1c3b, #15152e);
    border: 1px solid rgba(255,255,255,.07);
    border-radius: 18px;
    padding: 22px;
    height: 100%;
    box-shadow: 0 12px 35px rgba(0,0,0,.12);
}

.card-label {
    color: #a5a5c6;
    font-size: .78rem;
    font-weight: 600;
    letter-spacing: .08em;
    text-transform: uppercase;
}

.temperature {
    font-family: 'Space Grotesk';
    font-size: 4.5rem;
    font-weight: 700;
    line-height: 1.1;
}

.weather-icon {
    font-size: 4.5rem;
}

.city-name {
    font-size: 1.25rem;
    font-weight: 700;
    margin-top: 10px;
}

.muted {
    color: var(--muted);
    font-size: .85rem;
}

.metric-card {
    background: #191934;
    border: 1px solid rgba(255,255,255,.06);
    border-radius: 16px;
    padding: 18px;
    min-height: 125px;
}

.metric-icon {
    font-size: 1.4rem;
}

.metric-name {
    color: #aaaaca;
    font-size: .8rem;
    margin-top: 9px;
}

.metric-value {
    font-family: 'Space Grotesk';
    font-size: 1.55rem;
    font-weight: 700;
    margin-top: 3px;
}

/* PREVISÃO */

.forecast-card {
    background: #191934;
    border: 1px solid rgba(255,255,255,.06);
    border-radius: 14px;
    padding: 15px 8px;
    text-align: center;
    min-height: 155px;
    height: 100%;
}

.forecast-day {
    font-size: .8rem;
    color: #b9b9d4;
    font-weight: 600;
}

.forecast-icon {
    font-size: 2rem;
    margin: 12px 0;
}

.forecast-temp {
    font-weight: 700;
    font-size: 1rem;
}

.forecast-low {
    color: #999bbd;
    font-size: .8rem;
    margin-left: 5px;
}

.forecast-rain {
    color: var(--cyan);
    font-size: .72rem;
    margin-top: 8px;
}

/* GRÁFICOS */

div[data-testid="stVegaLiteChart"] {
    background: #191934;
    border: 1px solid rgba(255,255,255,.06);
    border-radius: 14px;
    padding: 10px;
}

/* OUTROS */

hr {
    border-color: rgba(255,255,255,.08);
}

footer {
    visibility: hidden;
}

#MainMenu {
    visibility: hidden;
}

@media(max-width: 768px) {
    .main-title {
        font-size: 1.7rem;
    }

    .temperature {
        font-size: 3.5rem;
    }
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# DESCRIÇÃO DO CLIMA
# ==========================================

def weather_description(code):

    descriptions = {
        0: ("Céu limpo", "☀️"),
        1: ("Predominantemente limpo", "🌤️"),
        2: ("Parcialmente nublado", "⛅"),
        3: ("Nublado", "☁️"),
        45: ("Neblina", "🌫️"),
        48: ("Neblina com geada", "🌫️"),
        51: ("Garoa fraca", "🌦️"),
        53: ("Garoa moderada", "🌦️"),
        55: ("Garoa intensa", "🌧️"),
        56: ("Garoa congelante", "🌧️"),
        57: ("Garoa congelante", "🌧️"),
        61: ("Chuva fraca", "🌦️"),
        63: ("Chuva moderada", "🌧️"),
        65: ("Chuva forte", "🌧️"),
        66: ("Chuva congelante", "🌧️"),
        67: ("Chuva congelante", "🌧️"),
        71: ("Neve fraca", "🌨️"),
        73: ("Neve moderada", "🌨️"),
        75: ("Neve forte", "❄️"),
        77: ("Grãos de neve", "🌨️"),
        80: ("Pancadas fracas", "🌦️"),
        81: ("Pancadas moderadas", "🌧️"),
        82: ("Pancadas fortes", "⛈️"),
        85: ("Neve fraca", "🌨️"),
        86: ("Neve forte", "❄️"),
        95: ("Trovoada", "⛈️"),
        96: ("Trovoada com granizo", "⛈️"),
        99: ("Trovoada forte", "⛈️")
    }

    return descriptions.get(
        int(code),
        ("Condição desconhecida", "🌡️")
    )


# ==========================================
# CONSUMO DAS APIS
# ==========================================

def get_city(city_name):

    response = requests.get(
        GEOCODING_URL,
        params={
            "name": city_name,
            "count": 10,
            "language": "pt",
            "format": "json"
        },
        timeout=15
    )

    response.raise_for_status()

    return response.json().get("results", [])


def get_weather(latitude, longitude):

    response = requests.get(
        FORECAST_URL,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": (
                "temperature_2m,"
                "relative_humidity_2m,"
                "apparent_temperature,"
                "wind_speed_10m,"
                "weather_code"
            ),
            "hourly": (
                "temperature_2m,"
                "precipitation_probability,"
                "weather_code,"
                "wind_speed_10m"
            ),
            "daily": (
                "weather_code,"
                "temperature_2m_max,"
                "temperature_2m_min,"
                "precipitation_probability_max"
            ),
            "forecast_days": 5,
            "timezone": "auto"
        },
        timeout=15
    )

    response.raise_for_status()

    return response.json()


# ==========================================
# FORMATAÇÃO
# ==========================================

def format_date(date_string):

    date = datetime.strptime(
        date_string,
        "%Y-%m-%d"
    )

    weekdays = [
        "Segunda",
        "Terça",
        "Quarta",
        "Quinta",
        "Sexta",
        "Sábado",
        "Domingo"
    ]

    return weekdays[date.weekday()]


def get_hourly_indices(hourly, current_time):

    hours = [
        datetime.fromisoformat(hour)
        for hour in hourly["time"]
    ]

    end_of_day = current_time.replace(
        hour=23,
        minute=59,
        second=59,
        microsecond=0
    )

    indices = [
        i for i, hour in enumerate(hours)
        if current_time <= hour <= end_of_day
    ]

    return hours, indices[:12]


def create_chart(data, x_column, y_column, color, chart_type="line"):

    if chart_type == "bar":
        mark = alt.Chart(data).mark_bar(
            color=color,
            cornerRadiusTopLeft=5,
            cornerRadiusTopRight=5
        )
    elif chart_type == "area":
        mark = alt.Chart(data).mark_area(
            color=color,
            opacity=0.35,
            line={"color": color}
        )
    else:
        mark = alt.Chart(data).mark_line(
            color=color,
            strokeWidth=3,
            point=alt.OverlayMarkDef(
                filled=True,
                size=55,
                color=color
            )
        )

    chart = (
        mark.encode(
            x=alt.X(
                f"{x_column}:N",
                title=None,
                axis=alt.Axis(
                    labelColor="#aaaaca",
                    titleColor="#aaaaca",
                    grid=False,
                    labelAngle=0
                )
            ),
            y=alt.Y(
                f"{y_column}:Q",
                title=None,
                axis=alt.Axis(
                    labelColor="#aaaaca",
                    titleColor="#aaaaca",
                    gridColor="#30304d"
                )
            ),
            tooltip=[x_column, y_column]
        )
        .properties(
            height=220,
            background="#191934"
        )
        .configure_view(
            strokeOpacity=0
        )
        .configure_axis(
            domainColor="#45456d",
            tickColor="#45456d"
        )
    )

    return chart


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    render_html("""
        <div class="sidebar-logo">
            CLIMA<span>AGORA</span>
        </div>
    """)

    st.caption("MENU PRINCIPAL")

    page = st.radio(
        "Navegação",
        ["Dashboard", "Gráficos", "Sobre"],
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.markdown("### 🌎 Open-Meteo")

    render_html("""
        <p class="muted">
            Informações meteorológicas e previsão
            para os próximos dias.
        </p>
    """)

    st.markdown("---")

    render_html("""
        <p class="muted">
            ClimaAgora · Projeto educacional
        </p>
    """)


# ==========================================
# CABEÇALHO
# ==========================================

render_html("""
    <div class="welcome">
        WEATHER DASHBOARD / OPEN-METEO
    </div>

    <div class="main-title">
        Olá! Como está o tempo?
    </div>

    <div class="subtitle">
        Acompanhe as condições meteorológicas da sua cidade.
    </div>
""")


# ==========================================
# PESQUISA DE CIDADE
# ==========================================

with st.form("city_search"):

    col_search, col_button = st.columns([4, 1])

    with col_search:

        city_input = st.text_input(
            "Cidade",
            placeholder="🔍 Pesquise uma cidade...",
            label_visibility="collapsed"
        )

    with col_button:

        search = st.form_submit_button(
            "Pesquisar",
            use_container_width=True
        )


if search:

    if not city_input.strip():

        st.warning("Digite o nome de uma cidade.")

    else:

        try:

            with st.spinner("Localizando cidade..."):

                cities = get_city(city_input.strip())

                if cities:

                    st.session_state["city_options"] = cities

                    st.session_state.pop(
                        "weather_result",
                        None
                    )

                else:

                    st.session_state.pop(
                        "city_options",
                        None
                    )

                    st.session_state.pop(
                        "weather_result",
                        None
                    )

                    st.error("Nenhuma cidade encontrada.")

        except requests.RequestException:

            st.error(
                "Não foi possível localizar a cidade. "
                "Verifique sua conexão e tente novamente."
            )


# ==========================================
# SELEÇÃO DA LOCALIZAÇÃO
# ==========================================

if "city_options" in st.session_state:

    options = st.session_state.city_options

    labels = [
        f"{item['name']} — {item.get('admin1', '')}, "
        f"{item.get('country', '')}"
        for item in options
    ]

    selected = st.selectbox(
        "Selecione a localização",
        labels
    )

    selected_city = options[labels.index(selected)]

    if st.button(
        "Consultar previsão",
        use_container_width=True
    ):

        try:

            with st.spinner("Consultando condições meteorológicas..."):

                weather = get_weather(
                    selected_city["latitude"],
                    selected_city["longitude"]
                )

                st.session_state["weather_result"] = {
                    "city": selected_city,
                    "weather": weather
                }

        except requests.RequestException:

            st.error(
                "Não foi possível consultar a previsão. "
                "Tente novamente."
            )


# ==========================================
# RODAPÉ
# ==========================================

def footer():

    render_html("""
        <div style="
            text-align:center;
            color:#77799f;
            font-size:.8rem;
            margin-top:3rem;
            padding:20px;
            border-top:1px solid rgba(255,255,255,.07);
        ">
            Dados meteorológicos fornecidos por
            <a href="https://open-meteo.com/"
               target="_blank"
               style="color:#8275ff;text-decoration:none;">
               Open-Meteo
            </a>
            <br>
            ClimaAgora · Desenvolvido com Python e Streamlit
        </div>
    """)


# ==========================================
# DASHBOARD
# ==========================================

if "weather_result" in st.session_state:

    result = st.session_state.weather_result

    city = result["city"]
    weather = result["weather"]

    current = weather["current"]
    hourly = weather["hourly"]
    daily = weather["daily"]

    description, icon = weather_description(
        current["weather_code"]
    )

    city_name = html.escape(city["name"])
    country = html.escape(city.get("country", ""))
    region = html.escape(city.get("admin1", ""))

    current_time = datetime.fromisoformat(
        current["time"]
    )

    hours, indices = get_hourly_indices(
        hourly,
        current_time
    )

    st.markdown("---")

    # ======================================
    # PÁGINA DASHBOARD
    # ======================================

    if page == "Dashboard":

        st.markdown("### 📍 Localização atual")

        left, right = st.columns([1.15, 1])

        # CARD PRINCIPAL

        with left:

            render_html(f"""
                <div class="weather-card">

                    <div class="card-label">
                        CONDIÇÕES ATUAIS
                    </div>

                    <div style="
                        display:flex;
                        align-items:center;
                        justify-content:space-between;
                        margin-top:15px;
                    ">

                        <div>

                            <div class="temperature">
                                {round(current['temperature_2m'])}°
                            </div>

                            <div style="
                                font-size:1rem;
                                color:#c4c4df;
                            ">
                                {description}
                            </div>

                        </div>

                        <div class="weather-icon">
                            {icon}
                        </div>

                    </div>

                    <div class="city-name">
                        {city_name}
                    </div>

                    <div class="muted">
                        {region}, {country}
                    </div>

                    <hr>

                    <div class="muted">
                        Sensação térmica:
                        {round(current['apparent_temperature'])}°C
                    </div>

                    <div class="muted">
                        Horário local:
                        {current['time'].replace('T', ' ')}
                    </div>

                </div>
            """)

        # GRÁFICO PRINCIPAL

        with right:

            render_html("""
                <div class="weather-card"
                     style="padding-bottom:5px;">

                    <div class="card-label">
                        TEMPERATURA AO LONGO DO DIA
                    </div>

                </div>
            """)

            if indices:

                chart_data = pd.DataFrame({
                    "Horário": [
                        hours[i].strftime("%H:%M")
                        for i in indices
                    ],
                    "Temperatura": [
                        hourly["temperature_2m"][i]
                        for i in indices
                    ]
                })

                chart = create_chart(
                    chart_data,
                    "Horário",
                    "Temperatura",
                    "#8275ff"
                )

                st.altair_chart(
                    chart,
                    use_container_width=True
                )

            else:

                st.info("Não há dados horários disponíveis.")

        # MÉTRICAS

        st.markdown("### Condições meteorológicas")

        m1, m2, m3 = st.columns(3)

        metrics = [
            (
                m1,
                "💨",
                "Vento",
                f"{current['wind_speed_10m']} km/h"
            ),
            (
                m2,
                "💧",
                "Umidade",
                f"{current['relative_humidity_2m']}%"
            ),
            (
                m3,
                "🌡️",
                "Sensação térmica",
                f"{current['apparent_temperature']}°C"
            )
        ]

        for column, emoji, name, value in metrics:

            with column:

                render_html(f"""
                    <div class="metric-card">

                        <div class="metric-icon">
                            {emoji}
                        </div>

                        <div class="metric-name">
                            {name}
                        </div>

                        <div class="metric-value">
                            {value}
                        </div>

                    </div>
                """)

        # PREVISÃO DOS PRÓXIMOS DIAS

        st.markdown("### 📅 Previsão dos próximos dias")

        forecast_columns = st.columns(5)

        for index, column in enumerate(forecast_columns):

            day_description, day_icon = weather_description(
                daily["weather_code"][index]
            )

            day_name = (
                "Hoje"
                if index == 0
                else format_date(daily["time"][index])
            )

            rain = daily["precipitation_probability_max"][index]

            rain_text = (
                f"💧 {rain}%"
                if rain is not None
                else "Sem dados"
            )

            with column:

                render_html(f"""
                    <div class="forecast-card">

                        <div class="forecast-day">
                            {day_name}
                        </div>

                        <div class="forecast-icon">
                            {day_icon}
                        </div>

                        <div class="forecast-temp">
                            {round(daily['temperature_2m_max'][index])}°

                            <span class="forecast-low">
                                {round(daily['temperature_2m_min'][index])}°
                            </span>
                        </div>

                        <div class="muted"
                             style="margin-top:7px;">
                            {day_description}
                        </div>

                        <div class="forecast-rain">
                            {rain_text}
                        </div>

                    </div>
                """)

        # JSON

        with st.expander("🔍 Visualizar JSON recebido da API"):

            st.json(weather)

    # ======================================
    # PÁGINA GRÁFICOS
    # ======================================

    elif page == "Gráficos":

        st.markdown("## 📊 Análise meteorológica")

        if indices:

            temperature_data = pd.DataFrame({
                "Horário": [
                    hours[i].strftime("%H:%M")
                    for i in indices
                ],
                "Temperatura": [
                    hourly["temperature_2m"][i]
                    for i in indices
                ]
            })

            rain_data = pd.DataFrame({
                "Horário": [
                    hours[i].strftime("%H:%M")
                    for i in indices
                ],
                "Probabilidade": [
                    hourly["precipitation_probability"][i]
                    for i in indices
                ]
            })

            wind_data = pd.DataFrame({
                "Horário": [
                    hours[i].strftime("%H:%M")
                    for i in indices
                ],
                "Vento": [
                    hourly["wind_speed_10m"][i]
                    for i in indices
                ]
            })

            st.markdown("### 🌡️ Temperatura por horário")

            st.altair_chart(
                create_chart(
                    temperature_data,
                    "Horário",
                    "Temperatura",
                    "#8275ff"
                ),
                use_container_width=True
            )

            st.markdown("### 🌧️ Probabilidade de chuva")

            st.altair_chart(
                create_chart(
                    rain_data,
                    "Horário",
                    "Probabilidade",
                    "#65d5e8",
                    "area"
                ),
                use_container_width=True
            )

            st.markdown("### 🌬️ Velocidade do vento")

            st.altair_chart(
                create_chart(
                    wind_data,
                    "Horário",
                    "Vento",
                    "#a17aff",
                    "bar"
                ),
                use_container_width=True
            )

        else:

            st.info("Não existem dados horários disponíveis.")

    # ======================================
    # PÁGINA SOBRE
    # ======================================

    elif page == "Sobre":

        st.markdown("## 🌤️ Sobre o ClimaAgora")

        render_html("""
            <div class="weather-card">

                <h2>ClimaAgora</h2>

                <p class="muted">
                    Uma aplicação desenvolvida para demonstrar
                    o consumo de APIs REST utilizando Python
                    e Streamlit.
                </p>

                <hr>

                <h3>Funcionalidades</h3>

                <p>
                    🌎 Pesquisa de cidades através de coordenadas geográficas.
                </p>

                <p>
                    🌡️ Consulta das condições meteorológicas atuais.
                </p>

                <p>
                    📅 Previsão para os próximos cinco dias.
                </p>

                <p>
                    📊 Gráficos de temperatura, vento e chuva.
                </p>

                <p>
                    💧 Informações de umidade e sensação térmica.
                </p>

                <hr>

                <h3>Tecnologias utilizadas</h3>

                <p>
                    Python · Streamlit · Requests · Pandas · Altair · Open-Meteo API
                </p>

                <hr>

                <p class="muted">
                    Projeto educacional de consumo de APIs REST.
                </p>

            </div>
        """)

else:

    # ======================================
    # TELA INICIAL
    # ======================================

    render_html("""
        <div class="weather-card"
             style="text-align:center;padding:55px 20px;">

            <div style="font-size:4rem;">
                🌤️
            </div>

            <h2>Bem-vindo ao ClimaAgora</h2>

            <p class="muted">
                Pesquise uma cidade para descobrir
                as condições meteorológicas.
            </p>

            <p style="color:#8275ff;font-weight:600;">
                Sua previsão do tempo em um só lugar.
            </p>

        </div>
    """)


# ==========================================
# RODAPÉ
# ==========================================

footer()
