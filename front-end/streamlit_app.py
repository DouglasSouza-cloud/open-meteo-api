import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

GEOCODING_URL = os.getenv(
    "database_url_geocoding",
    "https://geocoding-api.open-meteo.com/v1/search"
)
FORECAST_URL = os.getenv(
    "database_url",
    "https://api.open-meteo.com/v1/forecast"
)

st.set_page_config(
    page_title="ClimaAgora | Previsão do tempo",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
    --bg: #08111f;
    --panel: rgba(18, 32, 53, .82);
    --panel-2: rgba(25, 43, 68, .72);
    --line: rgba(148, 180, 220, .15);
    --muted: #9aacc4;
    --text: #edf5ff;
    --cyan: #63d5e8;
}
.stApp {
    background:
      radial-gradient(ellipse at 12% 0%, rgba(31, 115, 151, .25), transparent 34%),
      radial-gradient(ellipse at 90% 10%, rgba(74, 89, 170, .20), transparent 30%),
      var(--bg);
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
}
.block-container { max-width: 1180px; padding-top: 2.2rem; padding-bottom: 3rem; }
h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; color: var(--text) !important; }
p, label, span { color: var(--text); }
.brand { color: var(--cyan); font-weight: 800; letter-spacing: .16em; font-size: .78rem; }
.hero-title { font-family: 'Space Grotesk', sans-serif; font-size: clamp(2.2rem, 5vw, 3.7rem); font-weight: 700; line-height: 1.05; margin: .45rem 0 .55rem; }
.hero-sub { color: var(--muted); font-size: 1.04rem; margin-bottom: 1.6rem; }
.panel {
    background: linear-gradient(145deg, rgba(24, 43, 68, .92), rgba(13, 27, 46, .92));
    border: 1px solid var(--line); border-radius: 22px; padding: 1.35rem 1.5rem;
    box-shadow: 0 18px 55px rgba(0,0,0,.16);
}
.current-temp { font-family: 'Space Grotesk', sans-serif; font-size: clamp(3.5rem, 7vw, 5.5rem); font-weight: 700; line-height: 1; letter-spacing: -.07em; }
.condition { color: #c1d2e7; font-size: 1.05rem; margin-top: .55rem; }
.weather-icon { font-size: 4.2rem; line-height: 1; }
.eyebrow { color: var(--muted); font-size: .75rem; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; }
.metric {
    background: rgba(255,255,255,.045); border: 1px solid var(--line);
    border-radius: 16px; padding: 1rem 1.1rem; min-height: 112px;
}
.metric-label { color: var(--muted); font-size: .82rem; }
.metric-value { color: var(--text); font-family: 'Space Grotesk', sans-serif; font-size: 1.55rem; font-weight: 700; margin-top: .35rem; }
.forecast-card {
    background: rgba(255,255,255,.045); border: 1px solid var(--line);
    border-radius: 16px; padding: 1rem .65rem; text-align: center; min-height: 150px;
}
.forecast-day { color: #c4d4e8; font-size: .82rem; font-weight: 600; }
.forecast-icon { font-size: 1.8rem; margin: .45rem 0; }
.forecast-temp { font-weight: 700; font-size: 1.05rem; }
.forecast-low { color: var(--muted); font-size: .85rem; margin-left: .35rem; }
div[data-testid="stTextInput"] input {
    background: rgba(255,255,255,.07); color: white; border: 1px solid var(--line);
    border-radius: 12px; min-height: 3rem;
}
div[data-testid="stButton"] button {
    background: linear-gradient(100deg, #54c8dd, #7c9cf5); color: #071321;
    border: 0; border-radius: 12px; min-height: 3rem; font-weight: 800;
}
div[data-testid="stButton"] button:hover { color: #071321; border: 0; filter: brightness(1.08); }
div[data-testid="stAlert"] { border-radius: 14px; }
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


def weather_description(code: int):
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
        56: ("Garoa congelante fraca", "🌧️"),
        57: ("Garoa congelante intensa", "🌧️"),
        61: ("Chuva fraca", "🌦️"),
        63: ("Chuva moderada", "🌧️"),
        65: ("Chuva forte", "🌧️"),
        66: ("Chuva congelante fraca", "🌧️"),
        67: ("Chuva congelante forte", "🌧️"),
        71: ("Neve fraca", "🌨️"),
        73: ("Neve moderada", "🌨️"),
        75: ("Neve forte", "❄️"),
        77: ("Grãos de neve", "🌨️"),
        80: ("Pancadas de chuva fracas", "🌦️"),
        81: ("Pancadas de chuva moderadas", "🌧️"),
        82: ("Pancadas de chuva fortes", "⛈️"),
        85: ("Pancadas de neve fracas", "🌨️"),
        86: ("Pancadas de neve fortes", "❄️"),
        95: ("Trovoada", "⛈️"),
        96: ("Trovoada com granizo fraco", "⛈️"),
        99: ("Trovoada com granizo forte", "⛈️"),
    }
    return descriptions.get(int(code), ("Condição não identificada", "🌡️"))


def get_city(city_name: str):
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


def get_weather(latitude: float, longitude: float):
    response = requests.get(
        FORECAST_URL,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": (
                "temperature_2m,relative_humidity_2m,"
                "apparent_temperature,wind_speed_10m,weather_code"
            ),
            "daily": (
                "weather_code,temperature_2m_max,temperature_2m_min,"
                "precipitation_probability_max"
            ),
            "forecast_days": 5,
            "timezone": "auto"
        },
        timeout=15
    )
    response.raise_for_status()
    return response.json()


def format_date(date_string: str):
    from datetime import datetime
    date = datetime.strptime(date_string, "%Y-%m-%d")
    weekdays = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]
    return weekdays[date.weekday()].capitalize()


st.markdown('<div class="brand">CLIMAAGORA&nbsp; / &nbsp;OPEN-METEO</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">O tempo, do seu jeito.</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Consulte as condições atuais e a previsão dos próximos dias em qualquer cidade.</div>', unsafe_allow_html=True)

with st.container():
    col_input, col_button = st.columns([4, 1])
    with col_input:
        city_input = st.text_input(
            "Cidade",
            placeholder="Digite uma cidade (ex.: Joinville, Curitiba, São Paulo)",
            label_visibility="collapsed"
        )
    with col_button:
        search = st.button("Consultar clima", use_container_width=True)

if search:
    if not city_input.strip():
        st.warning("Digite o nome de uma cidade para continuar.")
    else:
        try:
            with st.spinner("Localizando cidade e consultando o clima..."):
                cities = get_city(city_input.strip())

                if not cities:
                    st.session_state.pop("weather_result", None)
                    st.error("Não encontramos essa cidade. Confira a escrita e tente novamente.")
                else:
                    st.session_state["city_options"] = cities
                    st.session_state["searched_city"] = city_input.strip()
                    st.session_state.pop("weather_result", None)
        except requests.RequestException as error:
            st.error(f"Não foi possível consultar a API de localização. Detalhes: {error}")

if "city_options" in st.session_state and st.session_state.city_options:
    options = st.session_state.city_options
    labels = [
        f"{item['name']} — {item.get('admin1', 'Região não informada')}, {item.get('country', 'País não informado')}"
        for item in options
    ]
    selected_label = st.selectbox("Selecione a localização correta", labels)
    selected_index = labels.index(selected_label)
    selected_city = options[selected_index]

    if st.button("Ver previsão desta cidade", use_container_width=True):
        try:
            with st.spinner("Buscando a previsão..."):
                weather_data = get_weather(
                    selected_city["latitude"],
                    selected_city["longitude"]
                )
                st.session_state["weather_result"] = {
                    "city": selected_city,
                    "weather": weather_data
                }
        except requests.RequestException as error:
            st.error(f"Não foi possível consultar a previsão. Detalhes: {error}")

if "weather_result" in st.session_state:
    result = st.session_state.weather_result
    city = result["city"]
    weather = result["weather"]
    current = weather["current"]
    daily = weather["daily"]

    description, icon = weather_description(current["weather_code"])
    city_name = city["name"]
    region = city.get("admin1", "")
    country = city.get("country", "")

    st.markdown("---")
    left, right = st.columns([1.35, 1])
    with left:
        st.markdown(f"""
        <div class="panel">
          <div class="eyebrow">CLIMA AGORA · {weather.get('timezone', '')}</div>
          <div style="display:flex; align-items:center; justify-content:space-between; gap:1rem; margin-top:1rem;">
            <div>
              <div style="font-size:1.55rem;font-weight:700;">{city_name}</div>
              <div style="color:#9aacc4;">{region}{', ' if region else ''}{country}</div>
              <div class="current-temp" style="margin-top:1rem;">{round(current['temperature_2m'])}°</div>
              <div class="condition">{description}</div>
            </div>
            <div class="weather-icon">{icon}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel" style="height:100%;"><div class="eyebrow">RESUMO</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="margin-top:1.15rem;color:#9aacc4;font-size:.9rem;">Sensação térmica</div>
        <div style="font-family:'Space Grotesk';font-size:2rem;font-weight:700;">{round(current['apparent_temperature'])}°C</div>
        <div style="margin-top:1rem;color:#9aacc4;font-size:.9rem;">Atualizado em</div>
        <div style="font-weight:600;">{current['time'].replace('T', ' ')}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Condições atuais")
    m1, m2, m3 = st.columns(3)
    metrics = [
        (m1, "💧", "Umidade relativa", f"{current['relative_humidity_2m']}%"),
        (m2, "🌬️", "Velocidade do vento", f"{current['wind_speed_10m']} km/h"),
        (m3, "🌡️", "Sensação térmica", f"{current['apparent_temperature']}°C"),
    ]
    for column, emoji, label, value in metrics:
        with column:
            st.markdown(f"""
            <div class="metric">
              <div style="font-size:1.35rem;">{emoji}</div>
              <div class="metric-label">{label}</div>
              <div class="metric-value">{value}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Próximos 5 dias")
    forecast_columns = st.columns(5)
    for index, column in enumerate(forecast_columns):
        day_description, day_icon = weather_description(daily["weather_code"][index])
        day_name = "Hoje" if index == 0 else format_date(daily["time"][index])
        rain = daily["precipitation_probability_max"][index]
        rain_text = f"💧 {rain}%" if rain is not None else ""
        with column:
            st.markdown(f"""
            <div class="forecast-card">
              <div class="forecast-day">{day_name}</div>
              <div class="forecast-icon">{day_icon}</div>
              <div class="forecast-temp">{round(daily['temperature_2m_max'][index])}° <span class="forecast-low">{round(daily['temperature_2m_min'][index])}°</span></div>
              <div style="font-size:.72rem;color:#9aacc4;margin-top:.4rem;">{day_description}</div>
              <div style="font-size:.75rem;color:#63d5e8;margin-top:.5rem;">{rain_text}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("Ver dados brutos recebidos da API (JSON)"):
        st.json(weather)

st.markdown("""
<div style="text-align:center;color:#71849e;font-size:.8rem;margin-top:3rem;">
  Dados meteorológicos fornecidos por <a href="https://open-meteo.com/" target="_blank">Open-Meteo</a>
  · Projeto educacional de consumo de APIs REST
</div>
""", unsafe_allow_html=True)
