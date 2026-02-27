import streamlit as st
import requests

API_URL = "https://laapi-transporte.onrender.com/routes"

st.title("Transporte Público - Rutas")

st.header("Rutas disponibles")
try:
    response = requests.get(API_URL)
    if response.status_code == 200:
        rutas = response.json()
        for r in rutas:
            st.write(f"{r['name']} → Paradas: {', '.join(r['stops'])}")
    else:
        st.error("No se pudieron obtener las rutas")
except Exception as e:
    st.error(f"Error al conectar con la API: {e}")

st.header("Agregar nueva ruta")
nombre = st.text_input("Nombre de la ruta")
paradas = st.text_input("Paradas (separadas por coma)")

if st.button("Registrar ruta"):
    payload = {"name": nombre, "stops": paradas.split(",")}
    try:
        post_response = requests.post(API_URL, json=payload)
        if post_response.status_code == 200:
            st.success(f"Ruta registrada: {post_response.json()['data']['name']}")
        else:
            st.error("Error al registrar la ruta")
    except Exception as e:
        st.error(f"Error al conectar con la API: {e}")
