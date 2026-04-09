import streamlit as st
import requests
import time

API_URL = "http://127.0.0.1:8001/latest"

st.set_page_config(page_title="Hydronyx Dashboard", layout="wide")

st.title("🌊 Hydronyx Real-Time Monitoring System")

placeholder = st.empty()

while True:
    try:
        res = requests.get(API_URL, timeout=5)

        if res.status_code == 200:
            data = res.json()

            if isinstance(data, list) and len(data) > 0:
                d = data[0]

                water = d.get("water_level", "N/A")
                temp = d.get("temperature", "N/A")
                humidity = d.get("humidity", "N/A")
                rain = d.get("rain", 0)
                lat = d.get("lat", "N/A")
                lon = d.get("lon", "N/A")

                with placeholder.container():
                    col1, col2, col3 = st.columns(3)

                    col1.metric("💧 Water Level", water)
                    col2.metric("🌡 Temperature (°C)", temp)
                    col3.metric("💦 Humidity (%)", humidity)

                    st.write("📍 Location:", lat, lon)
                    st.write("🌧 Rain:", rain)

            else:
                st.warning("No data yet...")

        else:
            st.error(f"Backend error: {res.status_code}")

    except Exception as e:
        st.error(f"Backend not responding: {e}")

    time.sleep(3)