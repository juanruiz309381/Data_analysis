# Guía de Ejecución del Proyecto

## Bienvenido al Proyecto de Análisis de Deserción Educativa

Esta guía te llevará paso a paso para ejecutar el proyecto completo.

## 📋 Pre-requisitos

### Software Necesario
- **Python 3.8+**: [Descargar](https://www.python.org/downloads/)
- **Jupyter Notebook**: Se instalará con las dependencias
- **Git**: Para control de versiones
- **Editor de código**: VS Code, PyCharm, o similar

### Conocimientos Recomendados
- Python básico/intermedio
- Pandas y NumPy
- Conceptos de Machine Learning
- Estadística descriptiva

## 🚀 Pasos para Iniciar

### Paso 1: Configurar el Ambiente

#### 1.1 Crear Ambiente Virtual
```bash
# Navegar al directorio del proyecto
cd "/home/david/Documentos/estudios/2025-2 ITM/analisis_de_datos/final_project"

# Crear ambiente virtual
python3 -m venv venv

# Activar ambiente virtual
# En Linux/Mac:
source venv/bin/activate

# En Windows:
venv\Scripts\activate
```

#### 1.2 Instalar Dependencias
```bash
# Instalar todas las librerías necesarias
pip install --upgrade pip
pip install -r requirements.txt

# Verificar instalación
python -c "import pandas; import sklearn; import plotly; print('✓ Instalación exitosa')"
```

### Paso 2: Verificar Datos

#### 2.1 Revisar Datasets
```bash
# Listar archivos de datos
ls -lh datasets/

# Debería mostrar:
# DESERCION_NO_ACADEMICA_UPTC_20251110.csv
# DESERCION_ACADEMICA_PREGRADO_Y_POSGRADO_20251110.csv
# DESERCION_DE_LA_FORMACIÓN_PROFESIONAL_INTEGRAL_20251110.csv
```

#### 2.2 Exploración Rápida
```bash
# Ver primeras líneas de un dataset
head -5 datasets/DESERCION_NO_ACADEMICA_UPTC_20251110.csv
```

### Paso 3: Ejecutar los Notebooks

**IMPORTANTE**: Los notebooks deben ejecutarse en orden secuencial.

#### 3.1 Abrir Jupyter
```bash
# Iniciar Jupyter Notebook
jupyter notebook

# Se abrirá en el navegador en: http://localhost:8888
```

#### 3.2 Orden de Ejecución

##### Notebook 1: ETL (Extracción, Transformación y Carga)
```
📓 notebooks/01_ETL.ipynb

Objetivo: Cargar, limpiar y preparar los datos

Tiempo estimado: 15-20 minutos

Qué hace:
- Carga los 3 datasets
- Limpia valores faltantes y duplicados
- Estandariza formatos
- Crea variables derivadas
- Guarda datos procesados en data/processed/

Resultado esperado:
- 3 archivos CSV limpios
- Reporte de calidad de datos
```

##### Notebook 2: EDA (Análisis Exploratorio)
```
📓 notebooks/02_EDA.ipynb

Objetivo: Explorar y entender los datos

Tiempo estimado: 30-40 minutos

Qué hace:
- Estadísticas descriptivas
- Visualizaciones de distribuciones
- Análisis de correlaciones
- Identificación de patrones
- Detección de outliers

Resultado esperado:
- 15+ gráficos guardados en reports/figures/
- Insights documentados
- Hipótesis para el modelo
```

##### Notebook 3: Diseño BI
```
📓 notebooks/03_BI_Design.ipynb

Objetivo: Diseñar modelo dimensional

Tiempo estimado: 20-30 minutos

Qué hace:
- Define dimensiones y hechos
- Crea tablas del modelo estrella
- Calcula KPIs
- Prepara datos para dashboard

Resultado esperado:
- Modelo estrella implementado
- Datos listos para BI
```

##### Notebook 4: Dashboard
```
📓 notebooks/04_Dashboard.ipynb

Objetivo: Crear dashboard interactivo

Tiempo estimado: 40-50 minutos

Qué hace:
- Crea visualizaciones con Plotly
- Implementa filtros interactivos
- Desarrolla aplicación Dash
- Genera reportes visuales

Resultado esperado:
- Aplicación web del dashboard
- URL: http://localhost:8050
```

##### Notebook 5: Modelo ML
```
📓 notebooks/05_ML_Model.ipynb

Objetivo: Construir modelo predictivo

Tiempo estimado: 45-60 minutos

Qué hace:
- Prepara features para ML
- Entrena múltiples modelos
- Optimiza hiperparámetros
- Evalúa y compara resultados
- Guarda mejor modelo

Resultado esperado:
- Modelo entrenado (.pkl)
- Reporte de métricas
- Feature importance
- Interpretabilidad (SHAP)
```

### Paso 4: Ejecutar el Dashboard

```bash
# Desde el directorio del proyecto
cd dashboards

# Ejecutar aplicación Dash
python app.py

# Abrir navegador en: http://localhost:8050
```

**Características del Dashboard**:
- 5 páginas interactivas
- Filtros dinámicos
- KPIs en tiempo real
- Gráficos exportables
- Datos descargables

### Paso 5: Usar el Modelo Predictivo

#### 5.1 Predicción Individual
```python
# Cargar modelo
import joblib
model = joblib.load('src/models/desercion_model.pkl')

# Preparar datos de un estudiante
estudiante = {
    'edad': 20,
    'genero': 'M',
    'estrato': 2,
    'modalidad': 'PRESENCIAL',
    'facultad': 'INGENIERIA',
    # ... más features
}

# Predecir
probabilidad = model.predict_proba(estudiante)[0, 1]
print(f"Probabilidad de deserción: {probabilidad:.2%}")
```

#### 5.2 Predicción en Lote
```python
# Cargar estudiantes desde CSV
estudiantes_df = pd.read_csv('data/estudiantes_nuevos.csv')

# Predecir para todos
probabilidades = model.predict_proba(estudiantes_df)[:, 1]
estudiantes_df['riesgo_desercion'] = probabilidades

# Exportar
estudiantes_df.to_csv('reports/estudiantes_con_riesgo.csv', index=False)
```

## 📊 Interpretación de Resultados

### Métricas del Modelo

#### Accuracy (Precisión Global)
```
Accuracy = (TP + TN) / (TP + TN + FP + FN)

Interpretación:
> 90% : Excelente
80-90% : Muy bueno ✓
70-80% : Bueno
< 70%  : Necesita mejora
```

#### Precision (Precisión Positiva)
```
Precision = TP / (TP + FP)

Interpretación:
De los estudiantes que el modelo predice como desertores,
¿qué porcentaje realmente lo es?

> 80% : Muy confiable
> 70% : Confiable ✓
< 70% : Muchos falsos positivos
```

#### Recall (Sensibilidad)
```
Recall = TP / (TP + FN)

Interpretación:
De todos los estudiantes que realmente desertan,
¿qué porcentaje el modelo logra detectar?

> 80% : Muy bueno
> 70% : Bueno ✓
< 70% : Se escapan muchos desertores
```

#### F1-Score
```
F1 = 2 * (Precision * Recall) / (Precision + Recall)

Interpretación:
Balance entre precisión y recall

> 0.85 : Excelente
> 0.75 : Muy bueno ✓
> 0.65 : Bueno
< 0.65 : Necesita mejora
```

### Niveles de Riesgo

```
🟢 Bajo Riesgo:    Probabilidad < 30%
    → Seguimiento normal

🟡 Riesgo Medio:   Probabilidad 30-60%
    → Monitoreo periódico
    → Tutorías preventivas

🔴 Riesgo Alto:    Probabilidad 60-80%
    → Intervención inmediata
    → Asignación de consejero
    → Seguimiento semanal

🚨 Riesgo Crítico: Probabilidad > 80%
    → Intervención urgente
    → Plan personalizado
    → Apoyo institucional integral
```

## 🔧 Resolución de Problemas

### Problema: Error al instalar dependencias
```bash
# Solución 1: Actualizar pip
pip install --upgrade pip setuptools wheel

# Solución 2: Instalar dependencias problemáticas por separado
pip install numpy pandas matplotlib
pip install scikit-learn
pip install plotly dash
```

### Problema: Jupyter no inicia
```bash
# Verificar que esté instalado
pip install jupyter

# Lanzar con parámetros específicos
jupyter notebook --ip=127.0.0.1 --port=8888
```

### Problema: El dashboard no carga
```bash
# Verificar que todos los datos estén procesados
ls data/processed/

# Verificar logs de la aplicación
python dashboards/app.py 2>&1 | tee dashboard.log
```

### Problema: Modelo da errores de predicción
```bash
# Verificar que el modelo esté entrenado
ls -lh src/models/desercion_model.pkl

# Re-entrenar si es necesario
cd notebooks
jupyter nbconvert --execute 05_ML_Model.ipynb
```

## 📈 Mejores Prácticas

### Durante el Análisis

1. **Ejecuta las celdas en orden**: No saltes celdas
2. **Lee los comentarios**: Cada celda está documentada
3. **Guarda frecuentemente**: Ctrl+S o Cmd+S
4. **Revisa las salidas**: Valida que los resultados tengan sentido

### Al Modificar el Código

1. **Crea una copia**: Antes de modificar notebooks
2. **Comenta tus cambios**: Explica qué y por qué
3. **Prueba incrementalmente**: No hagas muchos cambios a la vez
4. **Versiona con Git**: Commit regularmente

```bash
# Ejemplo de versionado
git add .
git commit -m "Añadí análisis de nueva variable X"
git push
```

### Al Presentar Resultados

1. **Exporta visualizaciones**: Guarda gráficos en alta resolución
2. **Documenta hallazgos**: Actualiza los .md en docs/
3. **Prepara datasets**: Ten los datos listos para mostrar
4. **Practica la demo**: Ensaya mostrando el dashboard

## 📚 Recursos Adicionales

### Documentación
- **Pandas**: https://pandas.pydata.org/docs/
- **Scikit-learn**: https://scikit-learn.org/stable/
- **Plotly**: https://plotly.com/python/
- **Dash**: https://dash.plotly.com/

### Tutoriales
- **Machine Learning**: [Curso de Andrew Ng](https://www.coursera.org/learn/machine-learning)
- **Pandas**: [10 Minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html)
- **Visualización**: [Plotly Tutorials](https://plotly.com/python/plotly-fundamentals/)

### Comunidades
- **Stack Overflow**: Para preguntas técnicas
- **Kaggle**: Para aprender de otros proyectos
- **GitHub**: Para ver código de referencia

## 🎯 Checklist de Entrega

### Entregables Técnicos
- [ ] 5 notebooks ejecutados completamente
- [ ] Todos los datos procesados en data/processed/
- [ ] Dashboard funcional y accesible
- [ ] Modelo entrenado guardado (.pkl)
- [ ] Scripts en src/ documentados

### Documentación
- [ ] README.md actualizado
- [ ] Docs de cada fase completados (01-06)
- [ ] Comentarios en código
- [ ] requirements.txt actualizado

### Visualizaciones
- [ ] Figuras exportadas en reports/figures/
- [ ] Dashboard con 15+ visualizaciones
- [ ] Gráficos de alta calidad para presentación

### Análisis
- [ ] Reporte de calidad de datos
- [ ] Estadísticas descriptivas completas
- [ ] Matriz de correlación
- [ ] Feature importance del modelo
- [ ] Métricas de evaluación

### Presentación
- [ ] Slides preparados
- [ ] Demo del dashboard ensayada
- [ ] Hallazgos principales identificados
- [ ] Recomendaciones concretas

## 💡 Consejos Finales

### Para el Éxito del Proyecto

1. **Gestiona bien tu tiempo**
   - ETL: 15% del tiempo
   - EDA: 30% del tiempo
   - BI: 20% del tiempo
   - ML: 25% del tiempo
   - Documentación: 10% del tiempo

2. **No te quedes atascado**
   - Si algo no funciona por >30 min, pide ayuda
   - Usa Stack Overflow y ChatGPT
   - Consulta con profesores

3. **Documenta mientras trabajas**
   - No dejes la documentación para el final
   - Toma notas de hallazgos interesantes
   - Exporta gráficos importantes inmediatamente

4. **Valida tus resultados**
   - ¿Los números tienen sentido?
   - ¿Los gráficos cuentan una historia?
   - ¿Las métricas del modelo son realistas?

5. **Piensa en el negocio**
   - No solo técnica, también impacto
   - ¿Cómo se usarían estas recomendaciones?
   - ¿Qué valor aporta a la institución?

### Para la Presentación

1. **Cuenta una historia**
   - Inicio: Problema de la deserción
   - Desarrollo: Análisis y hallazgos
   - Final: Solución y recomendaciones

2. **Usa visualizaciones efectivas**
   - 1 gráfico = 1 mensaje
   - Colores consistentes
   - Tamaños de fuente legibles

3. **Prepara para preguntas**
   - ¿Por qué elegiste ese modelo?
   - ¿Cómo manejaste el desbalanceo?
   - ¿Cuál es el impacto esperado?
   - ¿Qué limitaciones tiene el análisis?

4. **Demuestra expertise**
   - Conoce tus números
   - Explica decisiones técnicas
   - Muestra código clave (no todo)

## 🎓 ¡Éxito en tu Proyecto!

Este proyecto te permitirá:
- ✅ Demostrar habilidades en todo el pipeline de datos
- ✅ Crear un portafolio impresionante
- ✅ Generar impacto social real
- ✅ Sobresalir en la evaluación

**Recuerda**: La deserción educativa es un problema real que afecta a miles de estudiantes. Tu trabajo puede hacer la diferencia.

---

**¿Preguntas?**
- Revisa la documentación en docs/
- Consulta con profesores
- Busca en Stack Overflow
- ¡No te rindas!

**¡Manos a la obra!** 🚀
