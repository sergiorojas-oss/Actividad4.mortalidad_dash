import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px
import os

# ---------- CARGA DE DATOS ----------
ruta_nofetal = "data/Anexo1.NoFetal2019_CE_15-03-23.xlsx"
ruta_codigos = "data/Anexo2.CodigosDeMuerte_CE_15-03-23.xlsx"
ruta_divipola = "data/Divipola_CE_.xlsx"

df_mortalidad = pd.read_excel(ruta_nofetal)

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

# ---------- PALETA CORPORATIVA ----------
COLOR_FONDO = "#F1F5F9"
COLOR_TEXTO = "#0F172A"
COLOR_SUBTITULO = "#334155"
COLOR_TARJETA = "#FFFFFF"
COLOR_BORDE = "#E2E8F0"

# ---------- ESTILOS CORPORATIVOS ----------
estilo_tarjeta = {
    "backgroundColor": COLOR_TARJETA,
    "borderRadius": "12px",
    "boxShadow": "0 2px 8px rgba(0,0,0,0.06)",
    "padding": "28px",
    "marginBottom": "28px",
    "border": f"1px solid {COLOR_BORDE}"
}

estilo_titulo_grafico = {
    "fontSize": "18px",
    "color": COLOR_TEXTO,
    "fontWeight": "600",
    "marginBottom": "18px",
    "fontFamily": "Segoe UI, sans-serif"
}

estilo_subtitulo = {
    "fontSize": "14px",
    "color": COLOR_SUBTITULO,
    "fontWeight": "400",
    "marginTop": "4px",
    "fontFamily": "Segoe UI, sans-serif"
}

estilo_encabezado = {
    "textAlign": "center",
    "marginBottom": "40px",
    "paddingBottom": "25px",
    "borderBottom": f"2px solid {COLOR_BORDE}"
}

# ---------- GENERACIÓN DE GRÁFICOS ----------

# 1. MAPA
df_mapa = df_mortalidad.groupby("COD_DEPARTAMENTO").size().reset_index(name="total_muertes")
df_mapa["COD_DEPARTAMENTO"] = pd.to_numeric(df_mapa["COD_DEPARTAMENTO"], errors='coerce').fillna(0).astype(int)
df_mapa["lat"] = df_mapa["COD_DEPARTAMENTO"].map(lambda x: coordenadas_colombia.get(x, {}).get("lat", None))
df_mapa["lon"] = df_mapa["COD_DEPARTAMENTO"].map(lambda x: coordenadas_colombia.get(x, {}).get("lon", None))
df_mapa["DEPARTAMENTO"] = df_mapa["COD_DEPARTAMENTO"].map(lambda x: coordenadas_colombia.get(x, {}).get("nombre", "Desconocido"))
df_mapa = df_mapa.dropna(subset=["lat", "lon"])

fig_mapa_geo = px.scatter_mapbox(
    df_mapa, lat="lat", lon="lon", size="total_muertes", color="total_muertes",
    color_continuous_scale="Reds", hover_name="DEPARTAMENTO",
    hover_data={"total_muertes": True, "lat": False, "lon": False},
    mapbox_style="open-street-map", zoom=4.3, center={"lat": 4.570868, "lon": -74.297333}
)
fig_mapa_geo.update_layout(template="plotly_white", margin={"r":0,"t":10,"l":0,"b":0})

# 2. LÍNEAS
df_lineas = df_mortalidad.groupby("MES").size().reset_index(name="total_muertes")
fig_lineas = px.line(
    df_lineas, x="MES", y="total_muertes", markers=True,
    labels={"MES": "Mes", "total_muertes": "Casos"},
    color_discrete_sequence=["#2563EB"]
)
fig_lineas.update_layout(template="plotly_white", margin={"t":20,"b":20})

# 3. HOMICIDIOS
df_homicidios = df_mortalidad[df_mortalidad["MANERA_MUERTE"] == "Homicidio"]
df_violencia = df_homicidios.groupby("COD_MUNICIPIO").size().reset_index(name="total_homicidios").sort_values("total_homicidios", ascending=False).head(5)
fig_violencia = px.bar(
    df_violencia, x="COD_MUNICIPIO", y="total_homicidios",
    labels={"COD_MUNICIPIO": "Municipio", "total_homicidios": "Casos"},
    color_discrete_sequence=["#0F172A"]
)
fig_violencia.update_layout(template="plotly_white", margin={"t":20,"b":20})

# 4. CIRCULAR
df_municipios = df_mortalidad.groupby("COD_MUNICIPIO").size().reset_index(name="total_muertes").sort_values("total_muertes").head(10)
fig_menor_mortalidad = px.pie(
    df_municipios, names="COD_MUNICIPIO", values="total_muertes",
    color_discrete_sequence=px.colors.sequential.Slate
)
fig_menor_mortalidad.update_layout(template="plotly_white", margin={"t":20,"b":20})

# 5. TABLA DE CAUSAS
df_causas = df_mortalidad.groupby("COD_MUERTE").size().reset_index(name="total_muertes").sort_values("total_muertes", ascending=False).head(10)
fig_causas = px.bar(
    df_causas, x="COD_MUERTE", y="total_muertes",
    labels={"COD_MUERTE": "Causa", "total_muertes": "Casos"},
    color_discrete_sequence=["#DC2626"]
)
fig_causas.update_layout(template="plotly_white", margin={"t":20,"b":20})

# 6. SEXO
df_sexo = df_mortalidad.groupby(["COD_DEPARTAMENTO", "SEXO"]).size().reset_index(name="total_muertes")
fig_sexo = px.bar(
    df_sexo, x="COD_DEPARTAMENTO", y="total_muertes", color="SEXO", barmode="stack",
    color_discrete_map={"Masculino": "#1e3a8a", "Femenino": "#ec4899", "Indeterminado": "#94a3b8"},
    labels={"COD_DEPARTAMENTO": "Departamento", "total_muertes": "Casos"}
)
fig_sexo.update_layout(template="plotly_white", margin={"t":20,"b":20})

# 7. HISTOGRAMA EDADES
df_edades = df_mortalidad.groupby("GRUPO_EDAD1").size().reset_index(name="total_muertes").sort_values("GRUPO_EDAD1")
fig_edades = px.bar(
    df_edades, x="GRUPO_EDAD1", y="total_muertes",
    labels={"GRUPO_EDAD1": "Grupo de Edad", "total_muertes": "Casos"},
    color_discrete_sequence=["#475569"]
)
fig_edades.update_layout(template="plotly_white", margin={"t":20,"b":20})

# ---------- UI CORPORATIVA ----------
app = Dash(__name__)
server = app.server

app.layout = html.Div(
    style={"backgroundColor": COLOR_FONDO, "fontFamily": "Segoe UI, sans-serif", "padding": "40px 20px"},
    children=[

        # ENCABEZADO CORPORATIVO
        html.Div(
            style=estilo_encabezado,
            children=[
                html.H1("Actividad 4 – Análisis de Mortalidad en Colombia (2019)",
                        style={"color": COLOR_TEXTO, "fontWeight": "700", "fontSize": "34px", "margin": "0"}),
                html.Div("Maestría en Inteligencia Artificial – Universidad de La Salle",
                         style=estilo_subtitulo),
                html.Div("Estudiante: Sergio Andrés Rojas Ordoñez",
                         style=estilo_subtitulo)
            ]
        ),

        # MAPA
        html.Div(style=estilo_tarjeta, children=[
            html.Div("1. Distribución Geográfica de la Mortalidad en Colombia (2019)", style=estilo_titulo_grafico),
            dcc.Graph(figure=fig_mapa_geo, style={"height": "480px"})
        ]),

        # REJILLA DE 2 COLUMNAS
        html.Div(
            style={"display": "grid", "gridTemplateColumns": "repeat(auto-fit, minmax(48%, 1fr))", "gap": "24px"},
            children=[

                html.Div(style=estilo_tarjeta, children=[
                    html.Div("2. Total de muertes por mes (2019)", style=estilo_titulo_grafico),
                    dcc.Graph(figure=fig_lineas)
                ]),

                html.Div(style=estilo_tarjeta, children=[
                    html.Div("3. Top 5 ciudades más violentas (Homicidios)", style=estilo_titulo_grafico),
                    dcc.Graph(figure=fig_violencia)
                ]),

                html.Div(style=estilo_tarjeta, children=[
                    html.Div("4. 10 ciudades con menor mortalidad (2019)", style=estilo_titulo_grafico),
                    dcc.Graph(figure=fig_menor_mortalidad)
                ]),

                html.Div(style=estilo_tarjeta, children=[
                    html.Div("5. Top 10 causas de muerte en Colombia (2019)", style=estilo_titulo_grafico),
                    dcc.Graph(figure=fig_causas)
                ]),

                html.Div(style=estilo_tarjeta, children=[
                    html.Div("6. Muertes por sexo y departamento", style=estilo_titulo_grafico),
                    dcc.Graph(figure=fig_sexo)
                ]),

                html.Div(style=estilo_tarjeta, children=[
                    html.Div("7. Distribución de muertes por grupos de edad (GRUPO_EDAD1)", style=estilo_titulo_grafico),
                    dcc.Graph(figure=fig_edades)
                ]),
            ]
        )
    ]
)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run(host="0.0.0.0", port=port)
