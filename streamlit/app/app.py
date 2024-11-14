import streamlit as st
import requests
import datetime
import pandas as pd
import time
import numpy as np



url = "https://api.open-meteo.com/v1/forecast"

'''
params = {
    "latitude": -22.8833,
    "longitude": -43.1036,
    "current": "precipitation",
    "hourly": "temperature_2m",
    "timezone": "America/Sao_Paulo",
    "past_days": 92,
    "forecast_days": 14
}
'''

municipios_brasil = {
    "São Paulo": {"latitude": -23.5505, "longitude": -46.6333},
    "Rio de Janeiro": {"latitude": -22.9083, "longitude": -43.1728},
    "Brasília": {"latitude": -15.7801, "longitude": -47.9292},
    "Fortaleza": {"latitude": -3.7197, "longitude": -38.5222},
    "Salvador": {"latitude": -12.9704, "longitude": -38.5011}
}


st.title("Streamlit/app/app.py")

selected_option = st.selectbox("Selecione uma opção", municipios_brasil.keys(), index=None, placeholder="Please Select The City...")
if selected_option:
    st.write("You selected:", selected_option)
    #st.write(f"Voce Digitou Latitude {municipios_brasil[selected_option]["latitude"]} e Longitude {municipios_brasil[selected_option]["longitude"]}")
    st.write(f"Você Digitou Latitude {municipios_brasil[selected_option]['latitude']} e Longitude {municipios_brasil[selected_option]['longitude']}")
    lat = municipios_brasil[selected_option]['latitude']
    lon = municipios_brasil[selected_option]['longitude']

    params = {
    "latitude": lat,
    "longitude": lon,
    "current": "precipitation",
    "hourly": "temperature_2m",
    "timezone": "America/Sao_Paulo",
    "past_days": 92,
    "forecast_days": 14
}
    st.header("Loading")
    with st.spinner("Aguarde ..."):
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            #display(data)  # Imprime o JSON da resposta
            #display(data.keys())
            #print(f"Coordinates {data['latitude']}°N {data['longitude']}°E")
            #print(f"Elevation {data['latitude']} m asl")
            #print(f"Timezone {data['timezone']} GMT{data['timezone_abbreviation']}")
            df = pd.DataFrame(data['hourly'])
            df["data_datetime"] = [datetime.datetime.strptime(x, "%Y-%m-%dT%H:%M") for x in data['hourly']['time'] ]
        else:
            print(f"Erro na requisição: {response.status_code}")


        progress_bar = st.sidebar.progress(0)
        status_text = st.sidebar.empty()
        last_rows = df[["temperature_2m"]][:1]
        chart = st.line_chart(last_rows)

        for i in range(1, 101):
            new_rows = df[["temperature_2m"]][i-1:i]
            status_text.text(f"{i}% complete")
            chart.add_rows(new_rows)
            progress_bar.progress(i)
            last_rows = new_rows
            time.sleep(0.05)

        progress_bar.empty()

        # Streamlit widgets automatically run the script from top to bottom. Since
        # this button is not connected to any other logic, it just causes a plain
        # rerun.
        st.button("Rerun")
        st.success("Carregamento Finalizado")

else:
    st.write("You selected:", selected_option)


    