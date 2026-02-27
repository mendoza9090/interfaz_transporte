import streamlit as st
import requests
import pandas as pd

API_URL = "https://laapi-transporte.onrender.com/routes"


st.set_page_config(page_title="Transporte Público", layout="wide")


st.markdown(
    "<h1 style='text-align: center; color: #2C3E50;'>Sistema de Información de Transporte Público</h1>",
    unsafe_allow_html=True
)


st.subheader("Rutas registradas")
try:
    response = requests.get(API_URL)
    if response.status_code == 200:
        rutas = response.json()
        if rutas:
            # Crear tabla con columnas personalizadas
            df = pd.DataFrame(rutas)
            df["Número de paradas"] = df["stops"].apply(len)
            df = df[["name", "Número de paradas", "stops"]]
            df.rename(columns={"name": "Nombre de la ruta", "stops": "Paradas"}, inplace=True)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No hay rutas registradas.")
    else:
        st.error("No se pudieron obtener las rutas")
except Exception as e:
    st.error(f"Error al conectar con la API: {e}")

# Búsqueda de rutas
st.subheader("Buscar una ruta")
busqueda = st.text_input("Escribe el nombre de la ruta")
if busqueda:
    filtradas = [r for r in rutas if busqueda.lower() in r['name'].lower()]
    if filtradas:
        for r in filtradas:
            st.markdown(f"<h3 style='color:#2980B9;'>{r['name']}</h3>", unsafe_allow_html=True)
            st.write("Paradas:", ", ".join(r['stops']))
    else:
        st.warning("No se encontraron rutas con ese nombre.")

st.subheader("Registrar nueva ruta")
nombre = st.text_input("Nombre de la nueva ruta")
paradas = st.text_area("Paradas (separadas por coma)")

if st.button("Guardar ruta"):
    if nombre and paradas:
        payload = {"name": nombre, "stops": [p.strip() for p in paradas.split(",")]}
        try:
            post_response = requests.post(API_URL, json=payload)
            if post_response.status_code == 200:
                st.success(f"Ruta registrada: {post_response.json()['data']['name']}")
            else:
                st.error("Error al registrar la ruta")
        except Exception as e:
            st.error(f"Error al conectar con la API: {e}")
    else:
        st.warning("Completa todos los campos antes de guardar.")
