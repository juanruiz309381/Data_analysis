# Proyecto de Análisis de Datos: Deserción Educativa en Colombia

## Descripción del Proyecto
Este proyecto analiza la deserción educativa en instituciones de educación superior y formación profesional en Colombia, utilizando datos de la Universidad Pedagógica y Tecnológica de Colombia (UPTC) y el Servicio Nacional de Aprendizaje (SENA).

## Objetivo
Desarrollar una solución analítica completa que incluya:
- Análisis exploratorio de datos sobre deserción educativa
- Identificación de factores de riesgo
- Construcción de un modelo predictivo
- Dashboard interactivo de Business Intelligence
- Recomendaciones para reducir la deserción

## Estructura del Proyecto

```
final_project/
├── datasets/              # Datos originales (raw)
├── data/
│   ├── raw/              # Datos sin procesar
│   ├── interim/          # Datos en transformación
│   └── processed/        # Datos procesados y limpios
├── notebooks/            # Jupyter notebooks por fase
│   ├── 01_ETL.ipynb
│   ├── 02_EDA.ipynb
│   ├── 03_BI_Design.ipynb
│   ├── 04_Dashboard.ipynb
│   └── 05_ML_Model.ipynb
├── src/                  # Código fuente modular
│   ├── data/            # Scripts de procesamiento de datos
│   ├── models/          # Scripts de modelos ML
│   └── visualization/   # Scripts de visualización
├── dashboards/          # Dashboards de BI
├── reports/             # Reportes y análisis
│   └── figures/         # Gráficos generados
└── docs/                # Documentación del proyecto
```

## Datasets Utilizados

### 1. Deserción No Académica UPTC
- **Fuente**: datos.gov.co
- **Registros**: 1,595
- **Características**: 7 columnas
- **Descripción**: Deserción no académica de programas de pregrado y posgrado

### 2. Deserción Académica Pregrado y Posgrado UPTC
- **Fuente**: datos.gov.co
- **Registros**: 3,372
- **Características**: 13 columnas
- **Descripción**: Deserción académica con información demográfica detallada

### 3. Deserción Formación Profesional Integral SENA
- **Fuente**: datos.gov.co
- **Registros**: 42,100+
- **Características**: 15 columnas
- **Descripción**: Conteos de cupos desertados en programas SENA

## Fases del Proyecto

### Fase 1: ETL (Extracción, Transformación y Carga)
- Carga de datasets
- Limpieza inicial
- Integración de fuentes de datos
- Documentación: [docs/01_ETL.md](docs/01_ETL.md)

### Fase 2: Análisis Exploratorio de Datos (EDA)
- Análisis estadístico descriptivo
- Visualización de distribuciones
- Identificación de correlaciones
- Detección de outliers y valores atípicos
- Documentación: [docs/02_EDA.md](docs/02_EDA.md)

### Fase 3: Diseño de Modelo de Datos para BI
- Definición de dimensiones y métricas
- Diseño de modelo estrella/copo de nieve
- Reglas de negocio
- Documentación: [docs/03_BI_Design.md](docs/03_BI_Design.md)

### Fase 4: Dashboard Interactivo
- Visualizaciones clave
- KPIs de deserción
- Filtros interactivos
- Documentación: [docs/04_Dashboard.md](docs/04_Dashboard.md)

### Fase 5: Modelo Predictivo de Machine Learning
- Selección de características
- Entrenamiento de modelos
- Evaluación y comparación
- Optimización
- Documentación: [docs/05_ML_Model.md](docs/05_ML_Model.md)

### Fase 6: Conclusiones y Recomendaciones
- Hallazgos principales
- Insights de negocio
- Recomendaciones accionables
- Documentación: [docs/06_Conclusiones.md](docs/06_Conclusiones.md)

## Tecnologías Utilizadas

- **Python 3.x**: Lenguaje principal
- **Pandas**: Manipulación de datos
- **NumPy**: Computación numérica
- **Matplotlib/Seaborn**: Visualización
- **Plotly**: Visualizaciones interactivas
- **Scikit-learn**: Machine Learning
- **Jupyter Notebook**: Desarrollo interactivo
- **Power BI / Tableau / Plotly Dash**: Dashboard de BI

## Instalación

```bash
# Crear ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt
```

## Ejecución

```bash
# Iniciar Jupyter Notebook
jupyter notebook

# Ejecutar notebooks en orden:
# 01_ETL.ipynb → 02_EDA.ipynb → 03_BI_Design.ipynb → 04_Dashboard.ipynb → 05_ML_Model.ipynb
```

## Autores
- Proyecto desarrollado para las asignaturas:
  - Inteligencia de Negocios (Prof. Carlos Jaramillo, Gustavo Macias)
  - Analítica de Datos (Prof. Daniel Nieto)
  - Aprendizaje Computacional (Prof. July Galeano)

## Institución
Instituto Tecnológico Metropolitano (ITM)
Programa: Análisis de Datos
Semestre: 2025-2

## Licencia
Este proyecto es de uso académico
