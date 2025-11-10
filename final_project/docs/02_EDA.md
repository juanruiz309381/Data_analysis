# Fase 2: EDA - Análisis Exploratorio de Datos

## Objetivos de la Fase
1. Comprender la distribución de las variables
2. Identificar patrones y tendencias en la deserción
3. Detectar correlaciones entre variables
4. Identificar outliers y anomalías
5. Generar hipótesis para el modelo predictivo

## 1. Análisis Univariado

### 1.1 Variables Numéricas
- **Edad**: Distribución, media, mediana, desviación estándar
- **Número de estudiantes**: Por programa, facultad, periodo
- **Tasa de deserción**: Estadísticas descriptivas

#### Visualizaciones
- Histogramas de distribuciones
- Box plots para detectar outliers
- Gráficos de densidad

### 1.2 Variables Categóricas
- **Género**: Distribución y frecuencias
- **Estrato**: Niveles socioeconómicos
- **Modalidad**: Presencial, virtual, distancia
- **Jornada**: Diurna, nocturna, extendida
- **Facultad/Programa**: Top programas con deserción

#### Visualizaciones
- Gráficos de barras
- Gráficos de pastel
- Tablas de frecuencia

## 2. Análisis Bivariado

### 2.1 Deserción por Variables Demográficas
- Deserción vs Género
- Deserción vs Estrato socioeconómico
- Deserción vs Edad
- Deserción vs Origen geográfico

### 2.2 Deserción por Variables Académicas
- Deserción vs Facultad
- Deserción vs Programa
- Deserción vs Nivel académico (pregrado/posgrado)
- Deserción vs Modalidad de estudio
- Deserción vs Jornada

### 2.3 Deserción por Variables Temporales
- Tendencias por periodo
- Estacionalidad (semestres)
- Evolución temporal

## 3. Análisis Multivariado

### 3.1 Matriz de Correlación
- Correlaciones entre variables numéricas
- Identificación de multicolinealidad
- Heatmap de correlaciones

### 3.2 Análisis de Componentes Principales (PCA)
- Reducción de dimensionalidad
- Identificación de componentes principales
- Visualización en 2D/3D

### 3.3 Análisis de Clustering
- Segmentación de perfiles de desertores
- K-means clustering
- Dendrogramas jerárquicos

## 4. Patrones y Tendencias Identificadas

### 4.1 Hallazgos Principales
*(Se completará durante la ejecución)*

#### Por Facultad
- Facultades con mayor tasa de deserción
- Comparación entre facultades

#### Por Programa
- Programas críticos
- Nivel académico (pregrado vs posgrado)

#### Por Modalidad
- Presencial vs Virtual vs Distancia
- Impacto de la modalidad

#### Temporal
- Tendencias por semestre
- Periodos críticos

### 4.2 Factores de Riesgo Identificados
1. **Alto riesgo**:
2. **Riesgo medio**:
3. **Bajo riesgo**:

## 5. Análisis de Valores Faltantes

### Estrategia de Imputación
- Variables con >50% faltantes: Análisis especial
- Variables con <50% faltantes: Imputación según distribución
- Variables categóricas: Moda o categoría "Sin información"
- Variables numéricas: Media, mediana o modelo predictivo

## 6. Detección de Outliers

### Métodos Aplicados
- IQR (Rango Intercuartílico)
- Z-Score
- Isolation Forest

### Tratamiento
- Análisis de causa
- Decisión: mantener, transformar o eliminar

## 7. Insights para Business Intelligence

### KPIs Identificados
1. **Tasa Global de Deserción**: %
2. **Deserción por Facultad**: Top 5
3. **Deserción por Modalidad**: Comparativo
4. **Evolución Temporal**: Tendencia
5. **Perfil del Desertor**: Características

### Segmentaciones Relevantes
- Por nivel socioeconómico
- Por ubicación geográfica
- Por tipo de programa
- Por jornada de estudio

## 8. Hipótesis Generadas

### Para Modelo Predictivo
1. **H1**: El estrato socioeconómico es un predictor significativo
2. **H2**: La modalidad virtual tiene mayor deserción
3. **H3**: Estudiantes de primer semestre tienen mayor riesgo
4. **H4**: Género influye en la tasa de deserción
5. **H5**: Programas de educación tienen menor deserción

## 9. Visualizaciones Clave

### Dashboard Preview
1. **Mapa de calor** de deserción por facultad y periodo
2. **Gráfico de líneas** de tendencia temporal
3. **Gráfico de barras apiladas** por modalidad y género
4. **Sunburst chart** de jerarquía facultad-programa
5. **Box plots comparativos** de edad por nivel académico

## 10. Preparación para Modelado

### Feature Engineering Identificado
- Categorización de edad en grupos
- Binning de estrato socioeconómico
- One-hot encoding de variables categóricas
- Scaling de variables numéricas

### Variables Candidatas para el Modelo
**Top Features**:
1. Modalidad
2. Estrato
3. Facultad
4. Edad
5. Género
6. Jornada
7. Nivel académico
8. Periodo
9. Sede
10. Origen geográfico

## 11. Código de Referencia

**Notebook**: `notebooks/02_EDA.ipynb`

**Scripts**:
- `src/data/eda_utils.py`: Funciones de análisis
- `src/visualization/plots.py`: Funciones de visualización

## 12. Conclusiones del EDA

### Principales Descubrimientos
*(Se completará con hallazgos específicos)*

### Implicaciones
- Para el diseño del dashboard
- Para la selección de features en ML
- Para las recomendaciones de negocio

## 13. Próximos Pasos

- ✓ Datos explorados y entendidos
- → Diseñar modelo dimensional de BI
- → Crear dashboard interactivo
- → Desarrollar modelo predictivo

---

**Responsable**: Analítica de Datos - Prof. Daniel Nieto
**Estado**: En Desarrollo
**Última actualización**: Noviembre 2025
