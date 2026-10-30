import requests
import os 
from dotenv import load_dotenv

load_dotenv()

url_geocoding = os.getenv("database_url_geocoding")

# USUÁRIO ESCOLHE A CIDADE
cidade = input("Digite o nome da cidade: ")

params_geocoding = {
    "name": cidade,
    "count": 5,
    "language": "pt",
    "format": "json"
}

response_cidade = requests.get(
    url_geocoding,
    params=params_geocoding
)

if response_cidade.status_code == 200:

    dados_cidade = response_cidade.json()

    if dados_cidade.get("results"):

        # PEGA A PRIMEIRA CIDADE ENCONTRADA
        resultado = dados_cidade["results"][0]

        latitude = resultado["latitude"]
        longitude = resultado["longitude"]

        print("Cidade:", resultado["name"])
        print("País:", resultado.get("country"))

        # SEGUNDA API DE PREVISÃO DO TEMPO
        url_clima = os.getenv("database_url")
        
        params_clima = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,wind_speed_10m"
        }

        response_clima = requests.get(
            url_clima,
            params=params_clima
        )

        if response_clima.status_code == 200:

            dados = response_clima.json()

            print("\n--- PREVISÃO DO TEMPO ---")

            print("Temperatura:", dados["current"]["temperature_2m"], "°C")
            print("Umidade:", dados["current"]["relative_humidity_2m"], "%")
            print("Sensação térmica:", dados["current"]["apparent_temperature"], "°C")
            print("Vento:", dados["current"]["wind_speed_10m"], "km/h")

        else:
            print("Erro ao consultar o clima:", response_clima.status_code)

    else:
        print("Cidade não encontrada!")

else:
    print("Erro ao pesquisar cidade:", response_cidade.status_code)