import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px
import json
import os

# ---------- CARGA DE DATOS ----------
ruta_nofetal = "data/Anexo1.NoFetal2019_CE_15-03-23.xlsx"
ruta_codigos = "data/Anexo2.CodigosDeMuerte_CE_15-03-23.xlsx"
ruta_divipola = "data/Divipola_CE_.xlsx"
ruta_geojson = "data/colombia.geojson"

# Cargamos el archivo principal de mortalidad
df_mortalidad = pd.read_excel(ruta_nofetal)

# Cargamos los archivos secundarios de forma segura. 
# Si el servidor no los encuentra o se queda sin RAM, no romperán la app.
try:
    df_codigos = pd.read_excel(ruta_codigos)
except Exception:
    df_codigos = pd.DataFrame()

try:
    df_divipola = pd.read_excel(ruta_divipola)
except Exception:
    df_divipola = pd.DataFrame()


    
# ---------- GRAFICO 2: LÍNEAS ----------
df_lineas = df_mortalidad.groupby("MES").size().reset_index(name="total_muertes")
fig_lineas = px.line(
    df_lineas,
    x="MES",
    y="total_muertes",
    markers=True,
    title="Total de muertes por mes (2019)"
)

# ---------- GRAFICO 3: HOMICIDIOS ----------
df_homicidios = df_mortalidad[df_mortalidad["MANERA_MUERTE"] == "Homicidio"]
df_violencia = (
    df_homicidios.groupby("COD_MUNICIPIO")
    .size()
    .reset_index(name="total_homicidios")
    .sort_values("total_homicidios", ascending=False)
    .head(5)
)
fig_violencia = px.bar(
    df_violencia,
    x="COD_MUNICIPIO",
    y="total_homicidios",
    title="Top 5 ciudades más violentas (Homicidios)"
)

# ---------- GRAFICO 4: CIRCULAR ----------
df_municipios = (
    df_mortalidad.groupby("COD_MUNICIPIO")
    .size()
    .reset_index(name="total_muertes")
    .sort_values("total_muertes")
    .head(10)
)
fig_menor_mortalidad = px.pie(
    df_municipios,
    names="COD_MUNICIPIO",
    values="total_muertes",
    title="10 ciudades con menor mortalidad (2019)"
)

# ---------- GRAFICO 5: TABLA DE CAUSAS ----------
df_causas = (
    df_mortalidad.groupby("COD_MUERTE")
    .size()
    .reset_index(name="total_muertes")
    .sort_values("total_muertes", ascending=False)
    .head(10)
)
fig_causas = px.bar(
    df_causas,
    x="COD_MUERTE",
    y="total_muertes",
    title="Top 10 causas de muerte (2019)"
)

# ---------- GRAFICO 6: SEXO ----------
df_sexo = (
    df_mortalidad.groupby(["COD_DEPARTAMENTO", "SEXO"])
    .size()
    .reset_index(name="total_muertes")
)
fig_sexo = px.bar(
    df_sexo,
    x="COD_DEPARTAMENTO",
    y="total_muertes",
    color="SEXO",
    barmode="stack",
    title="Muertes por departamento según sexo"
)

# ---------- GRAFICO 7: HISTOGRAMA EDADES ----------
df_edades = (
    df_mortalidad.groupby("GRUPO_EDAD1")
    .size()
    .reset_index(name="total_muertes")
    .sort_values("GRUPO_EDAD1")
)
fig_edades = px.bar(
    df_edades,
    x="GRUPO_EDAD1",
    y="total_muertes",
    title="Distribución de muertes por grupos de edad (2019)"
)

# ---------- APP ----------
app = Dash(__name__)
server = app.server

app.layout = html.Div(
    style={"margin": "20px"},
    children=[

        html.H1("Actividad 4 – Análisis de Mortalidad en Colombia (2019)",
                style={"textAlign": "center", "fontWeight": "bold"}),

        html.H3("Maestría en Inteligencia Artificial – Universidad de La Salle",
                style={"textAlign": "center"}),

        html.H4("Estudiante: Sergio Andrés Rojas Ordoñez",
                style={"textAlign": "center", "marginBottom": "30px"}),

        # 1. MAPA (Se eliminaron los asteriscos internos de los encabezados)
        html.H2("1. Mapa: Distribución total de muertes por departamento (2019)",
                style={"fontWeight": "bold"}),
        dcc.Graph(figure=fig_mapa_geo),

        # 2. LÍNEAS
        html.H2("2. Gráfico de líneas: Total de muertes por mes (2019)",
                style={"fontWeight": "bold"}),
        dcc.Graph(figure=fig_lineas),

        # 3. VIOLENCIA
        html.H2("3. Gráfico de barras: 5 ciudades más violentas (Homicidios)",
                style={"fontWeight": "bold"}),
        dcc.Graph(figure=fig_violencia),

        # 4. CIRCULAR
        html.H2("4. Gráfico circular: 10 ciudades con menor mortalidad (2019)",
                style={"fontWeight": "bold"}),
        dcc.Graph(figure=fig_menor_mortalidad),

        # 5. TABLA DE CAUSAS
        html.H2("5. Tabla: Principales 10 causas de muerte en Colombia (2019)",
                style={"fontWeight": "bold"}),
        dcc.Graph(figure=fig_causas),

        # 6. SEXO
        html.H2("6. Gráfico de barras apiladas: Muertes por sexo y departamento",
                style={"fontWeight": "bold"}),
        dcc.Graph(figure=fig_sexo),

        # 7. HISTOGRAMA
        html.H2("7. Histograma: Distribución de muertes por grupos de edad (GRUPO_EDAD1)",
                style={"fontWeight": "bold"}),
        dcc.Graph(figure=fig_edades),
    ]
)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run(host="0.0.0.0", port=port)