import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px
import os

# ---------- CARGA DE DATOS ----------
ruta_nofetal = "data/Anexo1.NoFetal2019_CE_15-03-23.xlsx"
ruta_codigos = "data/Anexo2.CodigosDeMuerte_CE_15-03-23.xlsx"
ruta_divipola = "data/Divipola_CE_.xlsx"

# Cargamos el archivo principal de mortalidad
df_mortalidad = pd.read_excel(ruta_nofetal)

# Archivos secundarios limpios con try/except
try:
    df_codigos = pd.read_excel(ruta_codigos)
except Exception:
    df_codigos = pd.DataFrame()

try:
    df_divipola = pd.read_excel(ruta_divipola)
except Exception:
    df_divipola = pd.DataFrame()

# ---------- DICCIONARIO SEGURO DE COORDENADAS POR DEPARTAMENTO ----------
coordenadas_colombia = {
    11: {"lat": 4.6097, "lon": -74.0817, "nombre": "Bogotá D.C."},
    5:  {"lat": 6.2442, "lon": -75.5812, "nombre": "Antioquia"},
    76: {"lat": 3.4516, "lon": -76.5320, "nombre": "Valle del Cauca"},
    8:  {"lat": 10.9685, "lon": -74.7813, "nombre": "Atlántico"},
    13: {"lat": 10.3910, "lon": -75.4794, "nombre": "Bolívar"},
    15: {"lat": 5.5353, "lon": -73.3678, "nombre": "Boyacá"},
    17: {"lat": 5.0689, "lon": -75.5174, "nombre": "Caldas"},
    18: {"lat": 1.6144, "lon": -75.6062, "nombre": "Caquetá"},
    19: {"lat": 2.4419, "lon": -76.6063, "nombre": "Cauca"},
    20: {"lat": 10.4631, "lon": -73.2532, "nombre": "Cesar"},
    23: {"lat": 8.7479, "lon": -75.8814, "nombre": "Córdoba"},
    25: {"lat": 4.7110, "lon": -74.2400, "nombre": "Cundinamarca"},
    27: {"lat": 5.6923, "lon": -76.6582, "nombre": "Chocó"},
    41: {"lat": 2.9273, "lon": -75.2819, "nombre": "Huila"},
    44: {"lat": 11.5444, "lon": -72.9069, "nombre": "La Guajira"},
    47: {"lat": 11.2404, "lon": -74.1990, "nombre": "Magdalena"},
    50: {"lat": 4.1420, "lon": -73.6266, "nombre": "Meta"},
    52: {"lat": 1.2136, "lon": -77.2811, "nombre": "Nariño"},
    54: {"lat": 7.8939, "lon": -72.5078, "nombre": "Norte de Santander"},
    63: {"lat": 4.5339, "lon": -75.6811, "nombre": "Quindío"},
    66: {"lat": 4.8133, "lon": -75.6961, "nombre": "Risaralda"},
    68: {"lat": 7.1254, "lon": -73.1198, "nombre": "Santander"},
    70: {"lat": 9.3047, "lon": -75.3978, "nombre": "Sucre"},
    73: {"lat": 4.4389, "lon": -75.2322, "nombre": "Tolima"},
    81: {"lat": 7.0840, "lon": -70.7451, "nombre": "Arauca"},
    85: {"lat": 5.3378, "lon": -72.3959, "nombre": "Casanare"},
    86: {"lat": 1.1494, "lon": -76.6461, "nombre": "Putumayo"},
    88: {"lat": 12.5833, "lon": -81.7000, "nombre": "San Andrés y Providencia"},
    91: {"lat": -4.2153, "lon": -69.9441, "nombre": "Amazonas"},
    94: {"lat": 3.8653, "lon": -67.9239, "nombre": "Guainía"},
    95: {"lat": 2.5744, "lon": -72.6425, "nombre": "Guaviare"},
    97: {"lat": 1.1984, "lon": -70.1733, "nombre": "Vaupés"},
    99: {"lat": 6.1857, "lon": -67.4856, "nombre": "Vichada"}
}

# ---------- GRAFICO 1: MAPA DE DENSIDAD (SCATTER MAPBOX) ----------
df_mapa = df_mortalidad.groupby("COD_DEPARTAMENTO").size().reset_index(name="total_muertes")

# Limpieza numérica estándar
df_mapa["COD_DEPARTAMENTO"] = pd.to_numeric(df_mapa["COD_DEPARTAMENTO"], errors='coerce').fillna(0).astype(int)

# Cruzamos las coordenadas usando el diccionario
df_mapa["lat"] = df_mapa["COD_DEPARTAMENTO"].map(lambda x: coordenadas_colombia.get(x, {}).get("lat", None))
df_mapa["lon"] = df_mapa["COD_DEPARTAMENTO"].map(lambda x: coordenadas_colombia.get(x, {}).get("lon", None))
df_mapa["DEPARTAMENTO"] = df_mapa["COD_DEPARTAMENTO"].map(lambda x: coordenadas_colombia.get(x, {}).get("nombre", "Desconocido"))

# Quitamos filas que no tengan coordenadas válidas
df_mapa = df_mapa.dropna(subset=["lat", "lon"])

# Generamos el mapa interactivo de burbujas rojas
fig_mapa_geo = px.scatter_mapbox(
    df_mapa,
    lat="lat",
    lon="lon",
    size="total_muertes",
    color="total_muertes",
    color_continuous_scale="Reds",
    hover_name="DEPARTAMENTO",
    hover_data={"total_muertes": True, "lat": False, "lon": False},
    mapbox_style="open-street-map",
    zoom=4.4,
    center={"lat": 4.570868, "lon": -74.297333},
    title="Distribución Geográfica de la Mortalidad en Colombia (2019)"
)
fig_mapa_geo.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0})

# ---------- GRAFICO 2: LÍNEAS ----------
df_lineas = df_mortalidad.groupby("MES").size().reset_index(name="total_muertes")
fig_lineas = px.line(
    df_lineas,
    x="MES",
    y="total_muertes",
    markers=True,
    title="Total de muertes por mes (2019)",
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
    title="Top 5 ciudades más violentas (Homicidios)",
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
    title="10 ciudades con menor mortalidad (2019)",
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
    title="Top 10 causas de muerte (2019)",
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
    title="Muertes por departamento según sexo",
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
    title="Distribución de muertes por grupos de edad (2019)",
)

# ---------- APP ----------
app = Dash(__name__)
server = app.server

app.layout = html.Div(
    style={"margin": "20px"},
    children=[
        html.H1(
            "Actividad 4 – Análisis de Mortalidad en Colombia (2019)",
            style={"textAlign": "center", "fontWeight": "bold"},
        ),
        html.H3(
            "Maestría en Inteligencia Artificial – Universidad de La Salle",
            style={"textAlign": "center"},
        ),
        html.H4(
            "Estudiante: Sergio Andrés Rojas Ordoñez",
            style={"textAlign": "center", "marginBottom": "30px"},
        ),

        # 1. MAPA
        html.H2(
            "1. Mapa: Distribución total de muertes por departamento (2019)",
            style={"fontWeight": "bold"},
        ),
        dcc.Graph(figure=fig_mapa_geo),

        # 2. LÍNEAS
        html.H2(
            "2. Gráfico de líneas: Total de muertes por mes (2019)",
            style={"fontWeight": "bold"},
        ),
        dcc.Graph(figure=fig_lineas),

        # 3. VIOLENCIA
        html.H2(
            "3. Gráfico de barras: 5 ciudades más violentas (Homicidios)",
            style={"fontWeight": "bold"},
        ),
        dcc.Graph(figure=fig_violencia),

        # 4. CIRCULAR
        html.H2(
            "4. Gráfico circular: 10 ciudades con menor mortalidad (2019)",
            style={"fontWeight": "bold"},
        ),
        dcc.Graph(figure=fig_menor_mortalidad),

        # 5. TABLA DE CAUSAS
        html.H2(
            "5. Tabla: Principales 10 causas de muerte en Colombia (2019)",
            style={"fontWeight": "bold"},
        ),
        dcc.Graph(figure=fig_causas),

        # 6. SEXO
        html.H2(
            "6. Gráfico de barras apiladas: Muertes por sexo y departamento",
            style={"fontWeight": "bold"},
        ),
        dcc.Graph(figure=fig_sexo),

        # 7. HISTOGRAMA
        html.H2(
            "7. Histograma: Distribución de muertes por grupos de edad (GRUPO_EDAD1)",
            style={"fontWeight": "bold"},
        ),
        dcc.Graph(figure=fig_edades),
    ],
)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run(host="0.0.0.0", port=port)