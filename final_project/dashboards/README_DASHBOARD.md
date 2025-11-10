# 📊 Dashboard Interactivo de Deserción Educativa

## Descripción

Dashboard web interactivo desarrollado con **Plotly Dash** para análisis y visualización de datos de deserción educativa en Colombia (UPTC y SENA).

---

## 🎯 Características

### ✨ Páginas del Dashboard

#### 1. **📊 Overview** - Resumen Ejecutivo
- KPIs principales en tiempo real
- Evolución temporal de la deserción
- Distribución por género
- Top 10 facultades con mayor deserción
- Deserción por modalidad

#### 2. **👥 Análisis Demográfico**
- Filtros interactivos (género, edad, estrato)
- Distribución de edad de desertores
- Análisis por estrato socioeconómico
- Relación edad vs modalidad
- Gráficos dinámicos

#### 3. **🎓 Análisis Académico**
- Filtros por facultad, modalidad y jornada
- Deserción por facultad
- Distribución por jornada
- Análisis género por facultad
- Visualizaciones comparativas

#### 4. **🤖 Predictor ML** - Machine Learning
- Formulario interactivo de entrada
- Predicción de riesgo en tiempo real
- Cálculo de score de riesgo (0-100%)
- Clasificación: Bajo, Medio, Alto, Crítico
- Recomendaciones personalizadas
- Visualización de factores de riesgo

---

## 🚀 Cómo Ejecutar

### Opción 1: Script Automático (Recomendado)

```bash
cd dashboards
./run_dashboard.sh
```

El script hará todo automáticamente:
- ✅ Verificará el ambiente virtual
- ✅ Instalará dependencias faltantes
- ✅ Verificará que los datos existan
- ✅ Abrirá el dashboard en el navegador
- ✅ Iniciará el servidor

### Opción 2: Manual

```bash
# 1. Activar ambiente virtual
cd "/home/david/Documentos/estudios/2025-2 ITM/analisis_de_datos/final_project"
source venv/bin/activate

# 2. Instalar dependencias (si no están instaladas)
pip install dash dash-bootstrap-components plotly pandas joblib

# 3. Ejecutar dashboard
cd dashboards
python3 app.py

# 4. Abrir navegador en: http://127.0.0.1:8050
```

---

## 📋 Requisitos Previos

### Datos Necesarios

El dashboard requiere que los notebooks **01_ETL.ipynb** y **03_BI_Design.ipynb** hayan sido ejecutados previamente para generar:

```
data/
├── processed/
│   ├── desercion_academica_clean.csv
│   ├── desercion_no_academica_clean.csv
│   └── desercion_sena_clean.csv
└── bi/
    ├── fact_desercion.csv
    ├── dim_estudiante.csv
    ├── dim_tiempo.csv
    └── kpis_principales.csv
```

### Dependencias Python

- `dash >= 2.11.0`
- `dash-bootstrap-components >= 1.4.0`
- `plotly >= 5.14.0`
- `pandas >= 2.0.0`
- `joblib >= 1.3.0`

---

## 🎨 Interfaz del Dashboard

### Navegación

El dashboard utiliza **pestañas** (tabs) para navegar entre páginas:
- Click en cada pestaña para cambiar de vista
- Los datos se cargan dinámicamente
- Filtros se aplican en tiempo real

### Interactividad

#### Filtros
- **Dropdowns**: Selección de categorías
- **Sliders**: Valores numéricos (estrato)
- **Inputs**: Entrada de datos (edad)

#### Gráficos
- **Hover**: Información detallada al pasar el mouse
- **Zoom**: Click y arrastra para hacer zoom
- **Pan**: Shift + arrastra para mover
- **Reset**: Doble click para resetear vista
- **Export**: Botón cámara para descargar gráfico

---

## 🤖 Uso del Predictor de Riesgo

### Paso 1: Ingresar Datos
En la pestaña "🤖 Predictor ML":
1. **Edad**: Ingresa la edad del estudiante (16-60 años)
2. **Género**: Selecciona Masculino o Femenino
3. **Estrato**: Mueve el slider (1-6)
4. **Modalidad**: Presencial, Virtual o Distancia
5. **Jornada**: Diurna, Nocturna o Extendida

### Paso 2: Predecir
Click en el botón **"Predecir Riesgo"**

### Paso 3: Interpretar Resultado
El sistema mostrará:
- **Probabilidad de deserción** (0-100%)
- **Nivel de riesgo** (Bajo/Medio/Alto/Crítico)
- **Barra de progreso** visual
- **Factores evaluados** con badges
- **Recomendaciones** personalizadas

### Ejemplo de Interpretación

```
Probabilidad: 65%
Nivel: ALTO

Factores:
✓ Edad: 22 años - Normal
⚠ Estrato: 2 - Bajo
⚠ Modalidad: VIRTUAL - A distancia
✓ Jornada: DIURNA - Diurna/Extendida

Recomendaciones:
• Asignar consejero académico
• Inscribir en programa de tutorías
• Evaluar apoyo socioeconómico
```

---

## 📊 KPIs Principales

El dashboard calcula y muestra:

| KPI | Descripción | Fuente |
|-----|-------------|--------|
| **Total Desertores** | Cantidad total de estudiantes que han desertado | Dataset Académico |
| **Edad Promedio** | Edad promedio de los desertores | Cálculo en tiempo real |
| **Género Predominante** | Género con mayor tasa de deserción | Análisis demográfico |
| **Facultad Crítica** | Facultad con más desertores | Top 1 del ranking |

---

## 🎨 Personalización

### Modificar Colores

Edita `dashboards/assets/styles.css`:

```css
:root {
    --primary-color: #2c3e50;     /* Color principal */
    --danger-color: #e74c3c;       /* Color de alerta */
    --success-color: #27ae60;      /* Color éxito */
}
```

### Añadir Nuevas Visualizaciones

Edita `dashboards/app.py`:

```python
@app.callback(
    Output('nuevo-grafico', 'figure'),
    Input('filtro', 'value')
)
def actualizar_nuevo_grafico(filtro_valor):
    # Tu código aquí
    fig = px.bar(...)
    return fig
```

---

## 🐛 Solución de Problemas

### Error: "No se encontraron datos procesados"

**Solución**: Ejecuta primero los notebooks de ETL y BI:
```bash
jupyter notebook
# Ejecutar: 01_ETL.ipynb → 03_BI_Design.ipynb
```

### Error: "ModuleNotFoundError: No module named 'dash'"

**Solución**: Instala las dependencias:
```bash
pip install dash dash-bootstrap-components plotly
```

### Error: "Puerto 8050 ya en uso"

**Solución 1**: Mata el proceso existente:
```bash
lsof -ti:8050 | xargs kill -9
```

**Solución 2**: Cambia el puerto en `app.py`:
```python
app.run_server(debug=True, port=8051)  # Usar otro puerto
```

### El Dashboard carga pero no muestra datos

**Solución**: Verifica que las rutas de los archivos sean correctas:
```python
# En app.py, función cargar_datos()
df_academica = pd.read_csv('../data/processed/desercion_academica_clean.csv')
# Verifica que el path relativo sea correcto desde dashboards/
```

---

## 📈 Próximas Mejoras

Ideas para extender el dashboard:

- [ ] Integración con base de datos real
- [ ] Exportación de reportes en PDF
- [ ] Comparación de múltiples estudiantes
- [ ] Análisis predictivo avanzado con SHAP
- [ ] Mapa geográfico interactivo de Colombia
- [ ] Dashboard de administración de usuarios
- [ ] API REST para integraciones
- [ ] Modo oscuro
- [ ] Multi-idioma (español/inglés)
- [ ] Notificaciones en tiempo real

---

## 📞 Soporte

### Archivos de Referencia
- **Código fuente**: `dashboards/app.py`
- **Estilos**: `dashboards/assets/styles.css`
- **Script de ejecución**: `dashboards/run_dashboard.sh`

### Documentación
- **Dash**: https://dash.plotly.com/
- **Plotly**: https://plotly.com/python/
- **Bootstrap**: https://dash-bootstrap-components.opensource.faculty.ai/

---

## 🎓 Créditos

**Proyecto**: Análisis de Deserción Educativa en Colombia
**Institución**: Instituto Tecnológico Metropolitano (ITM)
**Programa**: Análisis de Datos 2025-2
**Cursos**: Inteligencia de Negocios, Analítica de Datos, Aprendizaje Computacional

**Profesores**:
- Inteligencia de Negocios: Carlos Jaramillo, Gustavo Macias
- Analítica de Datos: Daniel Nieto
- Aprendizaje Computacional: July Galeano

---

## 📝 Licencia

Este proyecto es de uso académico.

---

**Fecha**: Noviembre 2025
**Versión**: 1.0
**Estado**: ✅ Funcional
