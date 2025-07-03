import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Página de Contrato", layout="wide")
st.title("Página de Contrato")
st.markdown("## Datos de Contratación Pública en Ecuador 2025")

# Fuente de datos
st.markdown("## Fuente de datos")
st.markdown("[Ver datos en sitio oficial](https://datosabiertos.compraspublicas.gob.ec/PLATAFORMA/procedimientos?local=1&year=2025&page=1)")


# Sidebar de navegación
st.sidebar.title("Filtros")

años = [str(a) for a in range(2015, 2026)]
provincias = ["Todos", "AZUAY", "BOLÍVAR", "CAÑAR", "CARCHI", "CHIMBORAZO", "COTOPAXI", "EL ORO",
    "ESMERALDAS", "GALÁPAGOS", "GUAYAS", "IMBABURA", "LOJA", "LOS RÍOS",
    "MANABÍ", "MORONA SANTIAGO", "NAPO", "ORELLANA", "PASTAZA", "PICHINCHA",
    "SANTA ELENA", "SANTO DOMINGO DE LOS TSÁCHILAS", "SUCUMBÍOS", "TUNGURAHUA",
    "ZAMORA CHINCHIPE"]

tipos_contratacion = [
    "Todos", "Subasta Inversa Electrónica", "Menor Cuantía", "Cotización",
    "Contratacion directa", "Licitación", "Catálogo electrónico", "Bienes y Servicios únicos"
]

anio_seleccionado = st.selectbox("Seleccione el año", años)
provincia_seleccionada = st.selectbox("Seleccione la provincia", provincias)
tipo_contratacion_seleccionado = st.selectbox("Seleccione el tipo de contratación", tipos_contratacion)
palabra_clave = st.sidebar.text_input("Filtrar por palabra clave en descripción")

# Mostrar filtros
st.markdown("### Filtros seleccionados")
st.write(f"Año: {anio_seleccionado}")
st.write(f"Provincia: {provincia_seleccionada}")
st.write(f"Tipo de contratación: {tipo_contratacion_seleccionado}")
datos_cargados=st.button("datos")
# Mostrar tabla
if datos_cargados:
    # Simulación de columnas para fines de ejemplo
    

# Paso 1: Obtener datos de la API 
    parametros = {
            "year": anio_seleccionado,
            "province": provincia_seleccionada if provincia_seleccionada != "Todos" else None,
            "type": tipo_contratacion_seleccionado if tipo_contratacion_seleccionado != "Todos" else None,
            "keyword": palabra_clave
        }
    st.write(parametros)
    url = "https://datosabiertos.compraspublicas.gob.ec/PLATAFORMA/api/get_analysis?local=1&year={year}&province={province}&type={type}&keyword={keyword}".format(
        year=anio_seleccionado,
        province=provincia_seleccionada if provincia_seleccionada != "Todos" else "",
        type=tipo_contratacion_seleccionado if tipo_contratacion_seleccionado != "Todos" else "",
        keyword=palabra_clave
    )
    response = requests.get(url)
    

    if response.status_code == 200:
        data = response.json()
        df_filtrado = pd.DataFrame(data)
        st.dataframe(df_filtrado.head())  # Mostrar las primeras filas del DataFrame
        st.success("Datos obtenidos de la API exitosamente.")
        # Gráfica
        st.markdown("### Gráfica de Procedimientos por Año")
        df_anio = df_filtrado["month"].value_counts().sort_index()
        plt.figure(figsize=(10, 5))
        plt.plot(df_anio.index, df_anio.values, marker='o')
        plt.title("Número de Procedimientos por mes")
        plt.xlabel("mes")
        plt.ylabel("Número de Procedimientos")
        st.pyplot(plt)
    else:
        st.error("Error al consumir la API")
        
