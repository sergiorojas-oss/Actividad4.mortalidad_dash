
## Introducción del proyecto
El proyecto busca ofrecer una herramienta visual para analizar la mortalidad en Colombia, facilitando la interpretación de datos demográficos mediante mapas interactivos. Se desarrolló como parte del curso Aplicaciones 1 de la Universidad de La Salle, bajo la guía del docente Cristian Duney Bermúdez Quintero.

## Objetivo
El objetivo principal del proyecto es desarrollar e implementar una aplicación web interactiva en Dash que centralice y exponga visualmente los registros de defunción en Colombia durante el año 2019. El tablero busca transformar datos tabulares complejos en herramientas de diagnóstico visual mediante un mapa coroplético basado en GeoJSON y componentes dinámicos de filtrado lateral. Con esto, se pretende que el usuario pueda identificar geográficamente las zonas de mayor impacto, clasificar las causas principales de muerte y descubrir patrones demográficos clave (según edad, género y códigos Divipola) bajo un entorno analítico con diseño corporativo y profesional.

## Estructura del proyecto
La organización del repositorio está diseñada de forma modular, conteniendo de manera exacta los siguientes archivos y carpetas necesarios para la ejecución de la aplicación:

    ├── data/
    │   ├── Anexo1.NoFetal2019_CE_15-03-2021.csv  # Dataset con registros de mortalidad general
    │   ├── Anexo2.CodigosDeMuerte_CE_15-03.csv   # Diccionario y codificación de causas de muerte
    │   ├── Divipola_CE_.xlsx                    # Codificación de la División Político-Administrativa
    │   └── colombia.zip                         # Archivos de capas geográficas (GeoJSON/Shapefiles)
    ├── app.py                                    # Código principal de la aplicación (Interfaz y Callbacks)
    ├── Procfile                                  # Configuración del proceso de ejecución para la PaaS
    ├── requirements.txt                          # Librerías y dependencias necesarias de Python
    ├── runtime.txt                               # Especificación de la versión de Python del servidor
    └── README.md                                 # Documentación general del proyecto (este archivo)

## Requisitos
Para el correcto funcionamiento de la aplicación, tanto en un entorno local como en el servidor de despliegue, el sistema se basa en los siguientes componentes core de software:
* **Python 3.9+** (o la versión específica definida en el archivo `runtime.txt`): Entorno de ejecución para interpretar la lógica del proyecto.
* **dash**: Framework principal utilizado para orquestar la interfaz de usuario web y conectar los componentes interactivos con la lógica del servidor (callbacks).
* **plotly**: Biblioteca encargada de renderizar el mapa coroplético dinámico y los gráficos estadísticos basados en datos geoespaciales.
* **pandas**: Librería fundamental para realizar la carga, limpieza, cruce de datos (entre los anexos de mortalidad y Divipola) y estructuración de los dataframes.
* **openpyxl**: Requerido por Pandas para poder leer correctamente el archivo de Excel de la división político-administrativa (`Divipola_CE_.xlsx`).
* **gunicorn**: Servidor HTTP WSGI para entornos Unix, estrictamente necesario para que la plataforma PaaS (Render) pueda ejecutar la aplicación en producción a través del `Procfile`.

## Despliegue
La aplicación ha sido desplegada con éxito en una Plataforma como Servicio (PaaS) como Render. Los pasos seguidos para el despliegue fueron:
1. Vinculación del repositorio público de GitHub a la plataforma de despliegue.
2. Configuración del comando de construcción (Build Command): `pip install -r requirements.txt`.
3. Configuración del comando de inicio (Start Command) mediante Gunicorn: `gunicorn app:server`.
4. Ejecución y puesta en marcha del enlace público y funcional para la revisión.

## Software
Las herramientas y tecnologías clave utilizadas para el desarrollo de esta aplicación fueron:
* **Lenguaje de Programación:** Python
* **Framework Web:** Dash
* **Visualización Dinámica:** Plotly
* **Procesamiento de Datos:** Pandas
* **Formatos de Datos Geográficos:** GeoJSON

## Instalación
Para clonar este repositorio y ejecutar la aplicación de forma local en tu máquina, sigue estos pasos:

1. **Clonar el repositorio y acceder a la carpeta:**
   ```bash
   git clone https://github.com/sergiorojasord/colombia-mortalidad-dash.git
   cd colombia-mortalidad-dash

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt


3. **Ejecutar la aplicación localmente:**
   ```bash
      python app.py


## Visualizaciones con explicaciones de los resultados

### 1. Mapa: Distribución total de muertes por departamento (2019)

* **Descripción del Gráfico:** Se presenta un mapa de dispersión geoespacial interactivo sobre la cartografía de Colombia. Cada punto o zona representa un departamento del país, donde la escala cromática de intensidad (gradiente de rojo) y el tamaño del marcador reflejan proporcionalmente el volumen total de muertes registradas durante el año 2019. El gráfico permite al usuario realizar acercamientos (zoom) e interactuar dinámicamente para auditar los valores específicos de cada región.
* **Hallazgos Principales:** El análisis visual expone una correlación directa entre la densidad demográfica de las principales áreas metropolitanas y la concentración del número de decesos. Se destacan de forma crítica tres núcleos con la mayor frecuencia de registros históricos: Bogotá D.C. (superando los 35k casos), seguido por los nodos regionales de Antioquia (Medellín) y Valle del Cauca (Cali). Este comportamiento demográfico valida la necesidad de un filtrado lateral en el tablero para aislar factores específicos en las regiones con menor tasa de densidad.
   <img width="1902" height="598" alt="image" src="https://github.com/user-attachments/assets/63daf58a-e6c7-4522-8486-98c3bf4f90e8" />

### 2. Gráfico de líneas: Total de muertes por mes (2019)

* **Descripción del Gráfico:** Se presenta un gráfico de líneas continuo que mapea la evolución temporal de la mortalidad en Colombia a lo largo de los 12 meses del año 2019. El eje horizontal ($X$) representa la secuencia cronológica mensual, mientras que el eje vertical ($Y$) cuantifica el volumen total de decesos registrados. Los puntos de inflexión interactivos detallan los valores absolutos en cada periodo evaluado.
* **Hallazgos Principales:** La curva de distribución temporal expone una fluctuación cíclica con dinámicas muy marcadas. Se identifica una caída abrupta y drástica en el mes de febrero, donde los registros tocan el punto mínimo del año (aproximadamente 18k decesos). Posteriormente, se observa un crecimiento sostenido que genera picos de alta frecuencia en los meses de enero, julio y, de manera crítica, en diciembre, superando en este último la barrera de los 21k registros. Estos insights estacionales son clave para que los analistas y usuarios del tablero identifiquen periodos de alta demanda o alertas epidemiológicas cíclicas en el sistema de salud.

<img width="1861" height="540" alt="image" src="https://github.com/user-attachments/assets/a07b1c1b-d34b-423d-8af5-10fff81b3322" />

### 3. Gráfico de barras: 5 ciudades más violentas (Homicidios) (2019)

* **Descripción del Gráfico:** Se presenta un gráfico de barras categórico que ordena y compara el impacto de la mortalidad por causas externas específicas (homicidios) a nivel municipal. El eje horizontal ($X$) identifica los códigos de los municipios evaluados según la clasificación oficial, mientras que el eje vertical ($Y$) cuantifica la frecuencia absoluta del total de homicidios registrados durante el año 2019.
* **Hallazgos Principales:** El gráfico revela una asimetría crítica y una alta concentración de la violencia urbana en el país. Se destaca de forma contundente el primer nodo municipal (código 0, correspondiente a la capital del país o nodo principal de agregación), el cual despunta exponencialmente al registrar una cifra superior a los 5,000 homicidios en el periodo. En contraste, los demás municipios clasificados en el top muestran cifras significativamente menores que no logran superar la barrera de los 500 casos. Este hallazgo interactivo evidencia la disparidad en las problemáticas de seguridad ciudadana y justifica el uso de herramientas analíticas para focalizar estrategias de intervención social y orden público.

<img width="1877" height="553" alt="image" src="https://github.com/user-attachments/assets/da357b68-89f6-4ce2-9b63-ab9077509cd3" />

### 4. Gráfico circular: 10 ciudades con menor mortalidad (2019)

* **Descripción del Gráfico:** Se presenta un gráfico circular (o de sectores) que distribuye porcentualmente la participación de los 10 municipios con menor registro absoluto de decesos en el país durante 2019. Cada sector representa un municipio identificado por su código oficial, y el tamaño de la rebanada expone su peso relativo respecto al total acumulado de este grupo de baja frecuencia.
* **Hallazgos Principales:** El análisis de la torta revela una distribución fragmentada donde un único nodo municipal (código 420) abarca la quinta parte del total del grupo con un 20%, seguido muy de cerca por dos sectores estables del 15% (códigos 705 y 884). El 50% restante se atomiza de forma equitativa en porciones menores de entre el 10% y el 5%. Estos insights interactivos son de alto valor epidemiológico, ya que permiten visibilizar los territorios con menor densidad de eventos fatales, sirviendo como línea base para investigar factores protectores de salud o posibles subregistros de información en zonas periféricas.
<img width="1863" height="597" alt="image" src="https://github.com/user-attachments/assets/540c5c6f-1b37-48b5-bb4f-61b994ab2c88" />

### 5. Gráfico de barras: Principales 10 causas de muerte en Colombia (2019)

* **Descripción del Gráfico:** Se presenta un gráfico de barras categórico que identifica y clasifica en orden descendente las 10 principales causas de mortalidad en el territorio nacional durante 2019. El eje horizontal ($X$) detalla los códigos internacionales de diagnóstico médico oficiales (CIE-10), mientras que el eje vertical ($Y$) mide la frecuencia absoluta de decesos vinculados a cada patología o evento fatal.
* **Hallazgos Principales:** El tablero expone una prevalencia epidemiológica contundente asociada al código `I219` (Infarto agudo de miocardio, sin otra especificación), el cual lidera de forma aislada y crítica las estadísticas al superar la barrera de los 35,000 fallecimientos en el año. Las causas subsecuentes, representadas por patologías respiratorias crónicas y neoplásicas (como `J449`, `J440` o `C169`), muestran un comportamiento homogéneo y significativamente menor, promediando rangos entre los 3,000 y 7,000 casos. Este hallazgo interactivo es crucial dentro del tablero, ya que visibiliza de inmediato que las enfermedades isquémicas del corazón constituyen la principal prioridad e impacto para el sistema de salud pública del país.
<img width="1866" height="586" alt="image" src="https://github.com/user-attachments/assets/cd6ac56e-21ee-41c5-be7b-9a4511eb5c45" />

### 6. Gráfico de barras horizontales: 10 municipios con mayor número de muertes (2019)

* **Descripción del Gráfico:** Se presenta un gráfico de barras horizontales que clasifica y compara los 10 municipios de Colombia con el mayor registro absoluto de decesos durante el año 2019. El eje vertical ($Y$) identifica los códigos de la División Político-Administrativa (Divipola) de cada municipio, ordenados de forma descendente, mientras que el eje horizontal ($X$) mide la frecuencia total de fallecimientos acumulados.
* **Hallazgos Principales:** El análisis confirma una alta concentración espacial de la mortalidad en los principales centros urbanos y económicos del país. El nodo municipal correspondiente al código `11001` (Bogotá D.C.) encabeza la lista de manera masiva y aislada, superando los 35,000 registros. Detrás se ubican los códigos `05001` (Medellín) y `76001` (Cali), con frecuencias que oscilan entre los 15,000 y 18,000 casos. El resto de los municipios del top (como Barranquilla, Bucaramanga o Cúcuta) presentan un comportamiento homogéneo por debajo de los 10,000 decesos. Este comportamiento resalta cómo la escala demográfica de las capitales define el volumen global de la base de datos, justificando la inclusión de herramientas de normalización o tasas por cada 100,000 habitantes en fases avanzadas del tablero.
* 
<img width="1888" height="567" alt="image" src="https://github.com/user-attachments/assets/c5b49803-e020-4a0b-a53d-7438ef0a28d9" />

### 7. Gráfico de barras: Distribución de la mortalidad por género (2019)

* **Descripción del Gráfico:** Se presenta un gráfico de barras categórico y comparativo que ilustra la distribución total de fallecimientos en Colombia durante el año 2019, segmentado según el género biológico registrado de los individuos. El eje horizontal ($X$) divide la muestra en las categorías correspondientes, mientras que el eje vertical ($Y$) cuantifica de manera absoluta el volumen total de decesos.
* **Hallazgos Principales:** Los datos reflejan una marcada brecha epidemiológica basada en el género, registrándose una mayor incidencia de mortalidad en la población masculina. El grupo de hombres lidera las estadísticas con una cifra aproximada de 135,000 registros fatales, en comparación con el grupo de mujeres, que se sitúa cerca de los 105,000 casos. Esta diferencia de aproximadamente 30,000 registros pone de manifiesto la necesidad de estudiar factores de riesgo diferenciales dentro del tablero, tales como la exposición a causas externas (violencia, accidentes) o patologías crónicas de mayor prevalencia en varones para el periodo evaluado.

<img width="1863" height="546" alt="image" src="https://github.com/user-attachments/assets/f444185e-253b-4336-822a-1365f924d931" />



