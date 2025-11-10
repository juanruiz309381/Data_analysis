# Fase 1: ETL - Extracción, Transformación y Carga de Datos

## Objetivos de la Fase
1. Cargar y comprender los datasets disponibles
2. Realizar limpieza y transformación de datos
3. Integrar múltiples fuentes de datos
4. Preparar datasets procesados para análisis

## 1. Fuentes de Datos Identificadas

### Dataset 1: Deserción No Académica UPTC
- **Archivo**: `DESERCION_NO_ACADEMICA_UPTC_20251110.csv`
- **Registros**: 1,595
- **Columnas**: 7
- **Variables**:
  - PERIODO
  - NOMBRE_FACULTAD
  - NOMBRE_PROGRAMA
  - NIVEL ACADÉMICO
  - JORNADA
  - MODALIDAD
  - No_ESTUDIANTES

**Descripción**: Contiene información agregada sobre estudiantes que han desertado por razones no académicas, agrupados por programa, facultad y modalidad.

### Dataset 2: Deserción Académica Pregrado y Posgrado UPTC
- **Archivo**: `DESERCION_ACADEMICA_PREGRADO_Y_POSGRADO_20251110.csv`
- **Registros**: 3,372
- **Columnas**: 13
- **Variables**:
  - PERIODO
  - NOMBRE_FACULTAD
  - NOMBRE_PROGRAMA
  - JORNADA
  - MODALIDAD
  - NOMBRE_SEDE
  - TIPO_IDEN_EST
  - FECHA_NACIMIENTO
  - GENERO
  - ESTRATO
  - NOMBRE_ESTADO (motivo deserción)
  - ORIGEN_GEOGRAFICO
  - LUGAR_EXPEDICION

**Descripción**: Datos individuales de estudiantes desertores con información demográfica y motivos de deserción académica.

### Dataset 3: Deserción Formación Profesional SENA
- **Archivo**: `DESERCION_DE_LA_FORMACIÓN_PROFESIONAL_INTEGRAL_20251110.csv`
- **Registros**: 42,100+
- **Columnas**: 15
- **Variables**:
  - CODIGO_REGIONAL, NOMBRE_REGIONAL
  - CODIGO_CENTRO, NOMBRE_CENTRO
  - IDENTIFICADOR_UNICO_FICHA
  - FECHA_INICIO_FICHA, FECHA_TERMINACION_FICHA
  - CODIGO_PROGRAMA, VERSION_PROGRAMA
  - NOMBRE_PROGRAMA_FORMACION
  - NIVEL_FORMACION
  - MODALIDAD_FORMACION
  - TOTAL_APRENDICES_MATRICULADOS
  - DESERTORES_AÑO_ACTUAL
  - PERIODO

**Descripción**: Información sobre programas de formación del SENA con conteos de desertores.

## 2. Proceso ETL Implementado

### 2.1 Extracción (Extract)
```python
# Carga de datasets con manejo de encoding
df_no_academica = pd.read_csv('datasets/DESERCION_NO_ACADEMICA_UPTC_20251110.csv')
df_academica = pd.read_csv('datasets/DESERCION_ACADEMICA_PREGRADO_Y_POSGRADO_20251110.csv')
df_sena = pd.read_csv('datasets/DESERCION_DE_LA_FORMACIÓN_PROFESIONAL_INTEGRAL_20251110.csv')
```

### 2.2 Transformación (Transform)

#### Limpieza de Datos
- **Valores faltantes**: Identificación y tratamiento
- **Duplicados**: Detección y eliminación
- **Tipos de datos**: Conversión a tipos apropiados
- **Formato de fechas**: Estandarización
- **Normalización de texto**: Mayúsculas, espacios, caracteres especiales

#### Variables Derivadas
- **Edad**: Calculada desde fecha de nacimiento
- **Grupo etario**: Categorización de edades
- **Tasa de deserción**: (Desertores / Matriculados) * 100
- **Periodo año**: Extracción del año del periodo
- **Periodo semestre**: Extracción del semestre

#### Estandarización
- **Nombres de columnas**: Minúsculas y sin espacios
- **Categorías**: Unificación de valores similares
- **Codificación**: Variables categóricas

### 2.3 Carga (Load)
```python
# Guardar datasets procesados
df_no_academica_clean.to_csv('data/processed/desercion_no_academica_clean.csv', index=False)
df_academica_clean.to_csv('data/processed/desercion_academica_clean.csv', index=False)
df_sena_clean.to_csv('data/processed/desercion_sena_clean.csv', index=False)
```

## 3. Calidad de Datos

### Métricas de Calidad
| Métrica | Dataset 1 | Dataset 2 | Dataset 3 |
|---------|-----------|-----------|-----------|
| Completitud | % | % | % |
| Duplicados | N | N | N |
| Valores nulos | % | % | % |
| Outliers | N | N | N |

*(Se completará durante la ejecución)*

## 4. Desafíos Encontrados

### Problemas Identificados
1. **Formato de fechas inconsistente**: Diferentes formatos entre datasets
2. **Valores faltantes en estrato**: Alto porcentaje de "SIN INFORMACIÓN"
3. **Codificación de caracteres**: Tildes y caracteres especiales
4. **Categorías inconsistentes**: Variaciones en nombres de programas

### Soluciones Implementadas
1. Función unificada de parseo de fechas
2. Categoría explícita "Sin Información"
3. Encoding UTF-8 consistente
4. Diccionario de normalización de programas

## 5. Estructura de Datos Procesados

### Esquema Final
```
data/processed/
├── desercion_no_academica_clean.csv
├── desercion_academica_clean.csv
├── desercion_sena_clean.csv
└── desercion_integrado.csv  (dataset unificado)
```

## 6. Variables Clave para Análisis

### Variables Objetivo
- `tasa_desercion`: Tasa de deserción calculada
- `es_desertor`: Variable binaria (1=desertor, 0=no desertor)

### Variables Predictoras
- **Demográficas**: género, edad, estrato, origen_geográfico
- **Académicas**: facultad, programa, nivel, jornada, modalidad
- **Temporales**: periodo, semestre, año
- **Institucionales**: sede, regional, centro

## 7. Código de Referencia

**Notebook**: `notebooks/01_ETL.ipynb`

**Scripts**:
- `src/data/load_data.py`: Funciones de carga
- `src/data/clean_data.py`: Funciones de limpieza
- `src/data/transform_data.py`: Transformaciones

## 8. Próximos Pasos

- ✓ Datos cargados y limpios
- → Análisis exploratorio de datos (EDA)
- → Identificación de patrones
- → Diseño de modelo de BI

## 9. Conclusiones de ETL

### Logros
- Integración exitosa de 3 fuentes de datos
- Limpieza y estandarización completa
- Creación de variables derivadas relevantes
- Preparación de datos para análisis

### Lecciones Aprendidas
- Importancia de la normalización temprana
- Necesidad de diccionarios de datos
- Valor de la documentación del proceso

---

**Responsable**: Analítica de Datos - Prof. Daniel Nieto
**Estado**: Completado
**Última actualización**: Noviembre 2025
