# Proyecto Semestral - Análisis de Datos

Este proyecto corresponde al análisis de datos en el marco de un trabajo semestral.  

---


## Link Exposición

https://drive.google.com/file/d/1HwkkhHc6MA-NMBu-9Fp-71YygDNk-U1V/view?usp=sharing

## 1. Clonar repositorio

```bash
git clone https://github.com/fajurife12/Analisis_de_datos.git
cd Analisis_de_datos
```
## 2. Entorno virtual y creación de dependencias
windows
```bash
python -m venv venv-data-2
venv-data-2\Scripts\activate
pip install -r requirements.txt
```

linux o mac
```bash
python -m venv venv-data-2
source venv-data-2/bin/activate
pip install -r requirements.txt
```


# Link Exposición

https://drive.google.com/file/d/1HwkkhHc6MA-NMBu-9Fp-71YygDNk-U1V/view?usp=sharing

# EDA
Construcción de hipotesis inciales


## “La edad influye significativamente en la probabilidad de fallecimiento por COVID-19”
Justificación: Es conocido que los adultos mayores tienen mayor riesgo.

## “Existe una relación entre el departamento de residencia y la tasa de letalidad”
Justificación: Diferentes regiones pueden tener distintos niveles de acceso a salud, lo que afecta la supervivencia.

## “El tiempo entre la fecha de inicio de síntomas y la fecha de diagnóstico influye en la probabilidad de recuperación”
Justificación: Un diagnóstico temprano podría asociarse a mejores resultados clínicos.

## “El sexo biológico está relacionado con diferencias en la tasa de recuperación”
Justificación: Estudios previos sugieren diferencias en la respuesta inmunológica por sexo.

## “La pertenencia étnica muestra disparidades en el acceso a diagnóstico temprano”
Justificación: Grupos étnicos minoritarios podrían tener menores tasas de fecha de diagnóstico registrada.

## “La estacionalidad (mes del año) afecta la cantidad de casos reportados”
Justificación: Los picos de contagio suelen relacionarse con épocas de mayor movilidad o condiciones climáticas.


# Insights principales

## Evolución temporal clara de la pandemia
Al agrupar por Año-Mes en variables como fecha de diagnóstico, inicio de síntomas y reporte web, se observa un crecimiento inicial en 2020, picos hacia mediados de 2021 y una disminución hacia 2023.
Los gráficos de tendencia muestran olas claras de contagio que coinciden con lo esperado epidemiológicamente.

## Edad y diagnóstico
La edad promedio de diagnóstico varía a lo largo del tiempo, con picos en meses donde se concentraron contagios en adultos mayores.
El análisis multivariado muestra que la edad es un factor determinante en el estado de los pacientes (recuperado, fallecido).


## Sexo y estado clínico
Aunque la distribución por sexo está relativamente equilibrada, los hombres muestran una mayor proporción de casos graves y muertes en comparación con las mujeres.

## Relaciones multivariadas
Los análisis de dispersión y correlaciones muestran que:
La variable Edad está asociada a una mayor probabilidad de fallecimiento.
El tiempo entre inicio de síntomas y diagnóstico varía bastante, lo que podría reflejar diferencias en acceso al sistema de salud según región.
Existen diferencias en patrones de contagio según el tipo de contagio (importado vs comunitario).

## Geografía y contagios
Los departamentos con mayor población (ej. Bogotá, Antioquia, Valle) concentran la mayoría de los casos, pero en la fase exploratoria también se evidencian picos locales en municipios más pequeños, probablemente asociados a brotes localizados.s