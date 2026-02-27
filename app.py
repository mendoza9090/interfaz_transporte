import streamlit as st
import requests
import pandas as pd

API_URL = "https://laapi-transporte.onrender.com/routes"

st.title("Transporte Público - Interfaz")


st.header("Rutas disponibles")
try:
    response = requests.get(API_URL)
    if response.status_code == 200:
        rutas = response.json()
        if rutas:
            df = pd.DataFrame(rutas)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No hay rutas registradas.")
    else:
        st.error("No se pudieron obtener las rutas")
except Exception as e:
    st.error(f"Error al conectar con la API: {e}")


st.header("Buscar ruta")
busqueda = st.text_input("Nombre de la ruta")
if busqueda:
    filtradas = [r for r in rutas if busqueda.lower() in r['name'].lower()]
    if filtradas:
        for r in filtradas:
            st.subheader(r['name'])
            st.write("Paradas:", ", ".join(r['stops']))
    else:
        st.warning("No se encontraron rutas con ese nombre.")


st.header("Agregar nueva ruta")
nombre = st.text_input("Nombre de la nueva ruta")
paradas = st.text_input("Paradas (separadas por coma)")

if st.button("Registrar ruta"):
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
        st.warning("Completa todos los campos antes de registrar.")
