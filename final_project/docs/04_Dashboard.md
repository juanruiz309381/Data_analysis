# Fase 4: Dashboard Interactivo de Business Intelligence

## Objetivos de la Fase
1. Implementar dashboard interactivo basado en el diseño
2. Crear visualizaciones efectivas y claras
3. Permitir exploración interactiva de datos
4. Facilitar toma de decisiones basada en datos

## 1. Herramientas Utilizadas

### Opción 1: Plotly Dash (Python)
**Ventajas**:
- Integración nativa con Python
- Control total sobre visualizaciones
- Despliegue web sencillo
- Código abierto

### Opción 2: Power BI
**Ventajas**:
- Interfaz drag-and-drop
- Amplia variedad de visualizaciones
- Integración con Microsoft
- Publicación en la nube

### Opción 3: Tableau
**Ventajas**:
- Visualizaciones avanzadas
- Excelente rendimiento
- Storytelling visual

## 2. Arquitectura del Dashboard

### 2.1 Estructura de Archivos
```
dashboards/
├── app.py                          # Aplicación principal Dash
├── assets/
│   ├── styles.css                  # Estilos personalizados
│   └── logo.png                    # Logo institucional
├── components/
│   ├── filters.py                  # Componentes de filtros
│   ├── kpi_cards.py               # Tarjetas de KPIs
│   ├── charts.py                  # Gráficos reutilizables
│   └── tables.py                  # Tablas interactivas
├── data/
│   └── dashboard_data.pkl         # Datos pre-procesados
└── utils/
    ├── data_loader.py             # Carga de datos
    └── metrics.py                 # Cálculo de métricas
```

## 3. Páginas del Dashboard

### 3.1 Página Principal: Resumen Ejecutivo

#### KPI Cards (Top)
```
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│ Tasa Deserción  │ Total Desertores│ Tasa Retención  │ Tendencia       │
│    16.5%        │     5,832       │     83.5%       │  ↓ -2.3%       │
│    ▼ vs prev    │   YTD 2024      │    ▲ vs prev    │  vs anterior   │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘
```

#### Visualizaciones Principales
1. **Gráfico de Líneas**: Evolución temporal de la tasa de deserción
   - Eje X: Periodo (semestre/año)
   - Eje Y: Tasa de deserción (%)
   - Líneas: Por modalidad o facultad

2. **Gráfico de Barras Horizontales**: Top 10 Programas con Mayor Deserción
   - Ordenado descendente
   - Color coding por umbral (verde/amarillo/rojo)

3. **Mapa de Colombia**: Distribución Geográfica
   - Coloreado por tasa de deserción regional
   - Tooltips con información detallada

4. **Donut Chart**: Distribución por Tipo de Deserción
   - Académica vs No Académica
   - Porcentajes y cantidades

### 3.2 Página 2: Análisis Demográfico

#### Visualizaciones
1. **Pirámide Poblacional**: Edad y Género
   - Lado izquierdo: Masculino
   - Lado derecho: Femenino
   - Grupos de edad: 16-20, 21-25, 26-30, 31+

2. **Stacked Bar Chart**: Deserción por Estrato
   - Barras apiladas: Desertores vs Activos
   - Porcentaje de deserción sobre cada barra

3. **Treemap**: Origen Geográfico
   - Jerarquía: Región → Departamento → Ciudad
   - Tamaño: Número de desertores
   - Color: Tasa de deserción

4. **Heatmap**: Cruce Género vs Estrato
   - Intensidad de color por tasa de deserción

### 3.3 Página 3: Análisis Académico

#### Visualizaciones
1. **Sunburst Chart**: Jerarquía Académica
   - Centro: Total
   - Anillo 1: Facultades
   - Anillo 2: Programas
   - Anillo 3: Modalidades

2. **Heatmap**: Facultad vs Periodo
   - Filas: Facultades
   - Columnas: Periodos
   - Color: Tasa de deserción

3. **Bubble Chart**: Matrícula vs Deserción
   - Eje X: Total matriculados
   - Eje Y: Total desertores
   - Tamaño burbuja: Tasa de deserción
   - Color: Nivel académico

4. **Bar Chart**: Comparativa por Modalidad
   - Presencial vs Virtual vs Distancia
   - Métricas: Tasa deserción, total estudiantes

### 3.4 Página 4: Análisis de Riesgo

#### Visualizaciones
1. **Scatter Plot**: Análisis de Factores de Riesgo
   - Múltiples factores en ejes
   - Puntos coloreados por nivel de riesgo

2. **Gauge Charts**: Niveles de Riesgo Actual
   - Estudiantes en Alto Riesgo
   - Estudiantes en Riesgo Medio
   - Estudiantes en Bajo Riesgo

3. **Tabla Interactiva**: Top 100 Estudiantes en Riesgo
   - Columnas: ID, Programa, Factores, Score
   - Ordenable y filtrable
   - Exportable a Excel

4. **Sankey Diagram**: Flujo de Estudiantes
   - Desde ingreso hasta deserción/graduación
   - Identificación de puntos críticos

### 3.5 Página 5: Tendencias y Predicción

#### Visualizaciones
1. **Time Series**: Tendencias Históricas
   - Múltiples series temporales
   - Detección de estacionalidad
   - Tendencia ajustada

2. **Forecast Chart**: Predicción Próximos 4 Semestres
   - Intervalo de confianza
   - Escenarios: optimista, base, pesimista

3. **Seasonal Decomposition**: Análisis de Estacionalidad
   - Componente de tendencia
   - Componente estacional
   - Componente residual

4. **Comparative Bar**: Año sobre Año (YoY)
   - Comparación entre años
   - Crecimiento/Decrecimiento

## 4. Interactividad

### 4.1 Filtros Globales
```python
# Panel de filtros lateral
- Selector de Año: [2020, 2021, 2022, 2023, 2024]
- Selector de Semestre: [1, 2, Ambos]
- Dropdown Facultad: Multiselección
- Dropdown Programa: Multiselección
- Radio Button Modalidad: [Todas, Presencial, Virtual, Distancia]
- Slider Estrato: [1-6]
- Checkbox Género: [M, F]
```

### 4.2 Interacciones Entre Gráficos
- **Click en gráfico**: Filtra otros gráficos
- **Hover**: Muestra tooltips detallados
- **Zoom**: Permite acercar en gráficos temporales
- **Brush selection**: Selección de rangos

### 4.3 Acciones Especiales
- **Exportar datos**: Descarga en CSV/Excel
- **Exportar gráfico**: Descarga en PNG/SVG
- **Compartir vista**: URL con filtros aplicados
- **Refresh datos**: Actualizar desde fuente

## 5. Diseño Visual

### 5.1 Paleta de Colores
```css
/* Colores principales */
--primary-color: #1f77b4;      /* Azul institucional */
--success-color: #2ca02c;      /* Verde (baja deserción) */
--warning-color: #ff7f0e;      /* Naranja (media deserción) */
--danger-color: #d62728;       /* Rojo (alta deserción) */
--info-color: #17becf;         /* Cyan (información) */

/* Colores secundarios */
--background: #f8f9fa;
--card-bg: #ffffff;
--text-primary: #212529;
--text-secondary: #6c757d;
```

### 5.2 Layout Responsivo
- **Desktop**: Grid de 12 columnas
- **Tablet**: Grid de 6 columnas
- **Mobile**: Grid de 4 columnas (stack)

### 5.3 Tipografía
- **Títulos**: Roboto Bold, 24px
- **Subtítulos**: Roboto Medium, 18px
- **Cuerpo**: Roboto Regular, 14px
- **Números**: Roboto Mono

## 6. Código de Implementación

### 6.1 Estructura Principal (Dash)
```python
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go

app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("Dashboard de Deserción Educativa"),
        html.P("Análisis Integral - UPTC & SENA")
    ], className='header'),

    # Filters
    html.Div([
        # Filtros globales
    ], className='filters'),

    # KPIs
    html.Div([
        # Tarjetas de KPIs
    ], className='kpi-container'),

    # Charts
    html.Div([
        # Gráficos principales
    ], className='charts-container')
])

# Callbacks
@app.callback(
    Output('main-chart', 'figure'),
    [Input('filter-year', 'value'),
     Input('filter-semester', 'value')]
)
def update_chart(year, semester):
    # Lógica de actualización
    pass

if __name__ == '__main__':
    app.run_server(debug=True)
```

## 7. Performance y Optimización

### 7.1 Estrategias
- **Data caching**: Caché de datos procesados
- **Lazy loading**: Carga diferida de gráficos
- **Aggregation**: Pre-agregación de métricas
- **Sampling**: Muestreo para grandes volúmenes

### 7.2 Benchmarks
- Tiempo de carga inicial: <3 segundos
- Tiempo de respuesta a filtros: <500ms
- Máximo datos renderizados: 100,000 puntos

## 8. Testing y Validación

### 8.1 Tests Funcionales
- ✓ Todos los filtros funcionan correctamente
- ✓ Gráficos se actualizan con filtros
- ✓ Exportación de datos funciona
- ✓ Responsive en diferentes dispositivos

### 8.2 Tests de Datos
- ✓ Validación de cálculos de KPIs
- ✓ Consistencia con datos originales
- ✓ Manejo de valores nulos

## 9. Documentación de Usuario

### 9.1 Manual de Usuario
- Guía de navegación
- Explicación de cada visualización
- Interpretación de métricas
- Casos de uso comunes

### 9.2 FAQ
**Q: ¿Cómo exporto los datos?**
A: Click en el botón "Exportar" en la esquina superior derecha.

**Q: ¿Con qué frecuencia se actualizan los datos?**
A: Los datos se actualizan semestralmente.

## 10. Despliegue

### 10.1 Opciones de Hosting
- **Local**: Ejecución en máquina local
- **Heroku**: Despliegue en la nube (gratis tier)
- **AWS**: EC2 o Elastic Beanstalk
- **Docker**: Containerización

### 10.2 Instrucciones de Despliegue
```bash
# Opción 1: Local
python dashboards/app.py

# Opción 2: Docker
docker build -t desercion-dashboard .
docker run -p 8050:8050 desercion-dashboard

# Opción 3: Heroku
heroku create desercion-dashboard
git push heroku main
```

## 11. Código de Referencia

**Notebook**: `notebooks/04_Dashboard.ipynb`

**Scripts**:
- `dashboards/app.py`: Aplicación principal
- `dashboards/components/`: Componentes reutilizables
- `dashboards/utils/`: Utilidades

## 12. Próximos Pasos

- ✓ Dashboard implementado y funcional
- → Desarrollar modelo predictivo de ML
- → Integrar predicciones en dashboard

---

**Responsable**: Inteligencia de Negocios - Prof. Carlos Jaramillo, Gustavo Macias
**Estado**: Implementación
**Última actualización**: Noviembre 2025
