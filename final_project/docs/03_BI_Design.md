# Fase 3: Diseño de Modelo de Datos para Business Intelligence

## Objetivos de la Fase
1. Definir reglas de negocio aplicables a los datos
2. Diseñar un modelo dimensional (estrella/copo de nieve)
3. Identificar dimensiones y tablas de hechos
4. Definir métricas y KPIs clave
5. Preparar estructura para el dashboard

## 1. Reglas de Negocio Definidas

### 1.1 Deserción
**Definición**: Un estudiante se considera desertor cuando abandona sus estudios antes de completar el programa académico.

**Tipos de Deserción**:
- **Deserción Académica**: Por rendimiento académico insuficiente
- **Deserción No Académica**: Por razones económicas, personales, de salud, etc.

**Periodo de Análisis**: Semestral (Primer Semestre, Segundo Semestre)

### 1.2 Tasa de Deserción
**Fórmula**:
```
Tasa de Deserción (%) = (Número de Desertores / Total Matriculados) × 100
```

**Umbrales de Alertas**:
- 🟢 **Baja**: < 10%
- 🟡 **Media**: 10% - 20%
- 🔴 **Alta**: > 20%
- 🚨 **Crítica**: > 30%

### 1.3 Periodo Académico
- **Año Académico**: Compuesto por dos semestres
- **Semestre 1**: Enero - Junio
- **Semestre 2**: Julio - Diciembre

### 1.4 Nivel de Riesgo del Estudiante
**Clasificación basada en características**:
- **Alto Riesgo**: 3+ factores de riesgo
- **Medio Riesgo**: 1-2 factores de riesgo
- **Bajo Riesgo**: 0 factores de riesgo

**Factores de Riesgo Identificados**:
1. Estrato 1-2
2. Modalidad virtual/distancia
3. Primera matrícula
4. Edad >25 años o <18 años
5. Trabaja durante estudios

## 2. Modelo Dimensional - Esquema Estrella

### 2.1 Tabla de Hechos (Fact Table)

#### `FACT_DESERCION`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_hecho | INT (PK) | Identificador único |
| id_tiempo | INT (FK) | Clave de dimensión tiempo |
| id_estudiante | INT (FK) | Clave de dimensión estudiante |
| id_programa | INT (FK) | Clave de dimensión programa |
| id_sede | INT (FK) | Clave de dimensión sede |
| id_motivo | INT (FK) | Clave de dimensión motivo |
| es_desertor | BOOLEAN | 1=Desertor, 0=Activo |
| tipo_desercion | VARCHAR | Académica/No Académica |
| cantidad_estudiantes | INT | Conteo de estudiantes |
| matriculados | INT | Total matriculados |
| desertores | INT | Total desertores |
| tasa_desercion | DECIMAL | % de deserción |

### 2.2 Dimensiones

#### `DIM_TIEMPO`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_tiempo | INT (PK) | Clave primaria |
| periodo | VARCHAR | Ej: "PRIMER SEMESTRE 2020" |
| año | INT | 2020, 2021, 2022... |
| semestre | INT | 1, 2 |
| trimestre | INT | 1, 2, 3, 4 |
| nombre_mes | VARCHAR | Enero, Febrero... |
| numero_mes | INT | 1-12 |

#### `DIM_ESTUDIANTE`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_estudiante | INT (PK) | Clave primaria |
| tipo_identificacion | VARCHAR | CC, TI, CE |
| edad | INT | Edad del estudiante |
| grupo_edad | VARCHAR | 16-20, 21-25, 26-30, >30 |
| genero | VARCHAR | M, F |
| estrato | VARCHAR | 1, 2, 3, 4, 5, 6 |
| grupo_estrato | VARCHAR | Bajo (1-2), Medio (3-4), Alto (5-6) |
| origen_geografico | VARCHAR | Ciudad de origen |
| departamento | VARCHAR | Departamento |
| region | VARCHAR | Región de Colombia |

#### `DIM_PROGRAMA`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_programa | INT (PK) | Clave primaria |
| codigo_programa | VARCHAR | Código institucional |
| nombre_programa | VARCHAR | Nombre completo |
| nivel_academico | VARCHAR | Pregrado, Posgrado, Técnico, Tecnólogo |
| facultad | VARCHAR | Nombre de la facultad |
| area_conocimiento | VARCHAR | Ingeniería, Ciencias, Educación... |
| modalidad | VARCHAR | Presencial, Virtual, Distancia |
| jornada | VARCHAR | Diurna, Nocturna, Extendida |

#### `DIM_SEDE`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_sede | INT (PK) | Clave primaria |
| nombre_sede | VARCHAR | Tunja, Duitama, Sogamoso... |
| tipo_sede | VARCHAR | Principal, Seccional |
| ciudad | VARCHAR | Ciudad |
| departamento | VARCHAR | Departamento |
| codigo_regional | VARCHAR | Para datos SENA |
| nombre_regional | VARCHAR | Para datos SENA |
| codigo_centro | VARCHAR | Para datos SENA |
| nombre_centro | VARCHAR | Para datos SENA |

#### `DIM_MOTIVO_DESERCION`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_motivo | INT (PK) | Clave primaria |
| codigo_motivo | VARCHAR | Código del motivo |
| nombre_estado | VARCHAR | Descripción del motivo |
| categoria | VARCHAR | Académica, Económica, Personal, Salud |
| es_academico | BOOLEAN | 1=Académico, 0=No académico |
| nivel_gravedad | VARCHAR | Bajo, Medio, Alto |

## 3. KPIs y Métricas Definidas

### 3.1 KPIs Principales

#### 1. Tasa Global de Deserción
```sql
Tasa Global = (Total Desertores / Total Matriculados) × 100
```

#### 2. Tasa de Deserción por Periodo
```sql
Tasa Periodo = (Desertores en Periodo / Matriculados en Periodo) × 100
```

#### 3. Tasa de Retención
```sql
Retención = 100 - Tasa de Deserción
```

#### 4. Estudiantes en Riesgo
```sql
En Riesgo = COUNT(estudiantes con score_riesgo > umbral)
```

#### 5. Top Programas con Deserción
```sql
SELECT programa, COUNT(*) as desertores
ORDER BY desertores DESC
LIMIT 10
```

### 3.2 Métricas Secundarias

- **Deserción por Género**: Comparativa M vs F
- **Deserción por Estrato**: Distribución 1-6
- **Deserción por Modalidad**: Presencial vs Virtual vs Distancia
- **Deserción por Facultad**: Ranking de facultades
- **Tendencia Temporal**: Evolución semestral
- **Distribución Geográfica**: Mapa de calor
- **Tiempo Promedio a Deserción**: Semestres hasta desertar

### 3.3 Métricas Calculadas (DAX/MDX)

```dax
// Tasa de Deserción
Tasa_Desercion =
DIVIDE(
    SUM(FACT_DESERCION[desertores]),
    SUM(FACT_DESERCION[matriculados]),
    0
) * 100

// Tasa de Retención
Tasa_Retencion = 100 - [Tasa_Desercion]

// Variación Periodo Anterior
Var_Periodo =
[Tasa_Desercion] -
CALCULATE(
    [Tasa_Desercion],
    PREVIOUSPERIOD(DIM_TIEMPO[Periodo])
)

// Ranking de Programas
Ranking_Programa =
RANKX(
    ALL(DIM_PROGRAMA[nombre_programa]),
    [Tasa_Desercion],
    ,
    DESC
)
```

## 4. Estructura del Dashboard

### 4.1 Página 1: Overview Ejecutivo

**Componentes**:
- KPI Cards: Tasa global, Total desertores, Tendencia
- Gráfico de líneas: Evolución temporal
- Gráfico de barras: Top 10 programas
- Mapa geográfico: Distribución regional

### 4.2 Página 2: Análisis Demográfico

**Componentes**:
- Pirámide poblacional: Edad y género
- Gráfico de barras: Deserción por estrato
- Treemap: Origen geográfico
- Tabla dinámica: Cruce de variables

### 4.3 Página 3: Análisis Académico

**Componentes**:
- Sunburst: Facultad → Programa → Modalidad
- Heatmap: Facultad vs Periodo
- Gráfico de burbujas: Matriculados vs Desertores vs Tasa
- Filtros: Nivel académico, Jornada

### 4.4 Página 4: Análisis de Riesgo

**Componentes**:
- Scatter plot: Factores de riesgo
- Gauge charts: Niveles de riesgo
- Tabla: Estudiantes de alto riesgo
- Recomendaciones automáticas

### 4.5 Página 5: Tendencias y Predicción

**Componentes**:
- Serie temporal: Tendencias históricas
- Forecast: Predicción de próximos semestres
- Análisis de estacionalidad
- Comparativa año sobre año

## 5. Filtros Globales del Dashboard

**Slicers Principales**:
- 📅 Periodo (año, semestre)
- 🏫 Facultad
- 📚 Programa
- 🏛️ Sede
- 👤 Género
- 💰 Estrato
- 📖 Modalidad
- 🕐 Jornada
- 📍 Región

## 6. Código de Referencia

**Notebook**: `notebooks/03_BI_Design.ipynb`

**Scripts**:
- `src/data/create_star_schema.py`: Creación del modelo estrella
- `src/data/load_dimensions.py`: Carga de dimensiones
- `src/data/load_facts.py`: Carga de hechos

## 7. Próximos Pasos

- ✓ Modelo dimensional diseñado
- ✓ KPIs definidos
- → Implementar dashboard en herramienta BI
- → Crear visualizaciones interactivas

---

**Responsable**: Inteligencia de Negocios - Prof. Carlos Jaramillo, Gustavo Macias
**Estado**: Diseño Completado
**Última actualización**: Noviembre 2025
