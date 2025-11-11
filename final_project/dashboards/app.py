"""
Dashboard Interactivo - Análisis de Deserción Educativa
Proyecto: ITM - Análisis de Datos 2025-2

Autor: Sistema de Análisis de Datos
Descripción: Dashboard interactivo con múltiples páginas para análisis de deserción
"""

import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime

# Configuración
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
    suppress_callback_exceptions=True
)

app.title = "Dashboard de Deserción Educativa"

# =====================================================================
# CARGA DE DATOS
# =====================================================================

def cargar_datos():
    """Carga todos los datos necesarios para el dashboard"""
    try:
        # Datos procesados
        df_academica = pd.read_csv('../data/processed/desercion_academica_clean.csv')
        df_no_academica = pd.read_csv('../data/processed/desercion_no_academica_clean.csv')
        df_sena = pd.read_csv('../data/processed/desercion_sena_clean.csv')

        # Datos de BI
        fact_desercion = pd.read_csv('../data/bi/fact_desercion.csv')
        dim_estudiante = pd.read_csv('../data/bi/dim_estudiante.csv')
        dim_tiempo = pd.read_csv('../data/bi/dim_tiempo.csv')
        kpis = pd.read_csv('../data/bi/kpis_principales.csv')

        # Modelo ML
        modelo = None
        scaler = None
        if os.path.exists('../src/models/modelo_desercion.pkl'):
            modelo = joblib.load('../src/models/modelo_desercion.pkl')
            scaler = joblib.load('../src/models/scaler.pkl')

        return {
            'academica': df_academica,
            'no_academica': df_no_academica,
            'sena': df_sena,
            'fact': fact_desercion,
            'dim_estudiante': dim_estudiante,
            'dim_tiempo': dim_tiempo,
            'kpis': kpis,
            'modelo': modelo,
            'scaler': scaler
        }
    except Exception as e:
        print(f"Error cargando datos: {e}")
        return None

# Cargar datos al iniciar
datos = cargar_datos()

# =====================================================================
# FUNCIONES AUXILIARES
# =====================================================================

def combinar_datasets(datasets_seleccionados):
    """Combina los datasets seleccionados"""
    if datos is None:
        return None

    dfs = []
    for dataset in datasets_seleccionados:
        if dataset == 'academica' and 'academica' in datos:
            df_temp = datos['academica'].copy()
            df_temp['dataset_origen'] = 'Académica'
            dfs.append(df_temp)
        elif dataset == 'no_academica' and 'no_academica' in datos:
            df_temp = datos['no_academica'].copy()
            df_temp['dataset_origen'] = 'No Académica UPTC'
            dfs.append(df_temp)
        elif dataset == 'sena' and 'sena' in datos:
            df_temp = datos['sena'].copy()
            df_temp['dataset_origen'] = 'SENA'
            dfs.append(df_temp)

    if not dfs:
        return None

    # Concatenar datasets
    df_combinado = pd.concat(dfs, ignore_index=True)
    return df_combinado

def crear_kpi_card(titulo, valor, icono, color="primary"):
    """Crea una tarjeta de KPI"""
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                html.I(className=f"fas {icono} fa-2x", style={'color': f'var(--bs-{color})'}),
                html.H3(valor, className="mt-2 mb-0"),
                html.P(titulo, className="text-muted mb-0")
            ], className="text-center")
        ])
    ], className="shadow-sm mb-4")

def calcular_kpis_principales(df):
    """Calcula KPIs principales del dataset"""
    total = len(df)

    kpis_dict = {
        'total_desertores': f"{total:,}",
        'edad_promedio': f"{df['edad'].mean():.1f} años" if 'edad' in df.columns else "N/A",
        'genero_mayor': df['genero'].mode()[0] if 'genero' in df.columns else "N/A",
        'facultad_critica': df['nombre_facultad'].value_counts().index[0][:30] + "..." if 'nombre_facultad' in df.columns else "N/A"
    }

    return kpis_dict

# =====================================================================
# LAYOUT PRINCIPAL
# =====================================================================

# Header
header = dbc.Navbar(
    dbc.Container([
        html.A(
            dbc.Row([
                dbc.Col(html.I(className="fas fa-graduation-cap fa-2x", style={'color': 'white'})),
                dbc.Col(dbc.NavbarBrand("Dashboard de Deserción Educativa", className="ms-2")),
            ], align="center", className="g-0"),
            href="/",
            style={"textDecoration": "none"}
        ),
        dbc.NavbarToggler(id="navbar-toggler"),
        dbc.Collapse(
            dbc.Nav([
                dbc.NavItem(dbc.NavLink("Inicio", href="/")),
                dbc.NavItem(dbc.NavLink("Análisis", href="/analisis")),
                dbc.NavItem(dbc.NavLink("Predictor", href="/predictor")),
            ], className="ms-auto", navbar=True),
            id="navbar-collapse",
            navbar=True
        ),
    ], fluid=True),
    color="primary",
    dark=True,
    className="mb-4"
)

# Tabs para navegación
tabs = dbc.Tabs([
    dbc.Tab(label="📊 Overview", tab_id="tab-overview"),
    dbc.Tab(label="👥 Demográfico", tab_id="tab-demografico"),
    dbc.Tab(label="🎓 Académico", tab_id="tab-academico"),
    dbc.Tab(label="📈 Métricas & KPIs", tab_id="tab-metricas"),
    dbc.Tab(label="🤖 Predictor ML", tab_id="tab-predictor"),
], id="tabs", active_tab="tab-overview", className="mb-3")

# Selector de datasets
dataset_selector = dbc.Card([
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.I(className="fas fa-database me-2"),
                    html.Strong("Seleccionar Datasets:"),
                ], className="mb-2")
            ], md=12),
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Checklist(
                    options=[
                        {"label": " Deserción Académica (3,372 registros)", "value": "academica"},
                        {"label": " Deserción No Académica UPTC (1,009 registros)", "value": "no_academica"},
                        {"label": " Deserción SENA (47,862 registros)", "value": "sena"},
                    ],
                    value=["academica"],  # Por defecto solo académica
                    id="dataset-selector",
                    inline=True,
                    switch=True,
                )
            ], md=12),
        ]),
        dbc.Row([
            dbc.Col([
                html.Div(id="dataset-info", className="mt-2 small text-muted")
            ], md=12)
        ])
    ])
], className="mb-3")

# Layout principal
app.layout = html.Div([
    header,
    dbc.Container([
        dataset_selector,
        tabs,
        html.Div(id="tab-content")
    ], fluid=True)
])

# =====================================================================
# TAB: OVERVIEW
# =====================================================================

def crear_tab_overview():
    """Crea el contenido de la pestaña Overview"""

    if datos is None:
        return html.Div("Error cargando datos")

    df = datos['academica']
    kpis_dict = calcular_kpis_principales(df)

    # KPIs principales
    kpis_row = dbc.Row([
        dbc.Col(crear_kpi_card("Total Desertores", kpis_dict['total_desertores'], "fa-users", "danger"), md=3),
        dbc.Col(crear_kpi_card("Edad Promedio", kpis_dict['edad_promedio'], "fa-birthday-cake", "info"), md=3),
        dbc.Col(crear_kpi_card("Género Predominante", kpis_dict['genero_mayor'], "fa-venus-mars", "warning"), md=3),
        dbc.Col(crear_kpi_card("Facultad Crítica", kpis_dict['facultad_critica'], "fa-university", "success"), md=3),
    ])

    # Gráficos principales - 3 columnas
    graficos_row1 = dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Evolución Temporal de Deserción"),
                dbc.CardBody([
                    dcc.Graph(id='graph-temporal-overview')
                ])
            ])
        ], xs=12, sm=12, md=4, className="mb-3 mb-md-0"),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Distribución por Género"),
                dbc.CardBody([
                    dcc.Graph(id='graph-genero-overview')
                ])
            ])
        ], xs=12, sm=12, md=4, className="mb-3 mb-md-0"),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Deserción por Modalidad"),
                dbc.CardBody([
                    dcc.Graph(id='graph-modalidad-overview')
                ])
            ])
        ], xs=12, sm=12, md=4),
    ], className="mb-4")

    graficos_row2 = dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Top 10 Facultades con Mayor Deserción"),
                dbc.CardBody([
                    dcc.Graph(id='graph-facultades-overview')
                ])
            ])
        ], xs=12, sm=12, md=4, className="mb-3 mb-md-0"),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Distribución por Dataset"),
                dbc.CardBody([
                    dcc.Graph(id='graph-dataset-overview')
                ])
            ])
        ], xs=12, sm=12, md=4, className="mb-3 mb-md-0"),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Deserción por Estrato"),
                dbc.CardBody([
                    dcc.Graph(id='graph-estrato-overview')
                ])
            ])
        ], xs=12, sm=12, md=4),
    ], className="mb-4")

    return html.Div([
        html.H2("Resumen Ejecutivo", className="mb-4"),
        kpis_row,
        html.Hr(),
        graficos_row1,
        graficos_row2
    ])

# =====================================================================
# TAB: DEMOGRÁFICO
# =====================================================================

def crear_tab_demografico():
    """Crea el contenido de la pestaña Demográfico"""

    return html.Div([
        html.H2("Análisis Demográfico", className="mb-4"),

        # Filtros
        dbc.Row([
            dbc.Col([
                html.Label("Género:"),
                dcc.Dropdown(
                    id='filter-genero',
                    options=[{'label': 'Todos', 'value': 'all'}],
                    value='all',
                    clearable=False
                )
            ], md=3),
            dbc.Col([
                html.Label("Grupo de Edad:"),
                dcc.Dropdown(
                    id='filter-edad',
                    options=[{'label': 'Todos', 'value': 'all'}],
                    value='all',
                    clearable=False
                )
            ], md=3),
            dbc.Col([
                html.Label("Estrato:"),
                dcc.Dropdown(
                    id='filter-estrato',
                    options=[{'label': 'Todos', 'value': 'all'}],
                    value='all',
                    clearable=False
                )
            ], md=3),
        ], className="mb-4"),

        # Gráficos demográficos - 3 columnas
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Distribución de Edad"),
                    dbc.CardBody([
                        dcc.Graph(id='graph-edad-dist')
                    ])
                ])
            ], xs=12, sm=12, md=4, className="mb-3 mb-md-0"),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Deserción por Estrato Socioeconómico"),
                    dbc.CardBody([
                        dcc.Graph(id='graph-estrato-dist')
                    ])
                ])
            ], xs=12, sm=12, md=4, className="mb-3 mb-md-0"),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Distribución por Género"),
                    dbc.CardBody([
                        dcc.Graph(id='graph-genero-demografico')
                    ])
                ])
            ], xs=12, sm=12, md=4),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Edad vs Modalidad"),
                    dbc.CardBody([
                        dcc.Graph(id='graph-edad-modalidad')
                    ])
                ])
            ], xs=12, sm=12, md=12),
        ])
    ])

# =====================================================================
# TAB: ACADÉMICO
# =====================================================================

def crear_tab_academico():
    """Crea el contenido de la pestaña Académico"""

    return html.Div([
        html.H2("Análisis Académico", className="mb-4"),

        # Filtros académicos
        dbc.Row([
            dbc.Col([
                html.Label("Facultad:"),
                dcc.Dropdown(
                    id='filter-facultad',
                    options=[{'label': 'Todas', 'value': 'all'}],
                    value='all',
                    clearable=False
                )
            ], md=4),
            dbc.Col([
                html.Label("Modalidad:"),
                dcc.Dropdown(
                    id='filter-modalidad',
                    options=[{'label': 'Todas', 'value': 'all'}],
                    value='all',
                    clearable=False
                )
            ], md=4),
            dbc.Col([
                html.Label("Jornada:"),
                dcc.Dropdown(
                    id='filter-jornada',
                    options=[{'label': 'Todas', 'value': 'all'}],
                    value='all',
                    clearable=False
                )
            ], md=4),
        ], className="mb-4"),

        # Gráficos académicos - 3 columnas
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Distribución por Jornada"),
                    dbc.CardBody([
                        dcc.Graph(id='graph-jornada-pie')
                    ])
                ])
            ], xs=12, sm=12, md=4, className="mb-3 mb-md-0"),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Modalidades"),
                    dbc.CardBody([
                        dcc.Graph(id='graph-modalidad-academico')
                    ])
                ])
            ], xs=12, sm=12, md=4, className="mb-3 mb-md-0"),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Distribución por Dataset"),
                    dbc.CardBody([
                        dcc.Graph(id='graph-dataset-academico')
                    ])
                ])
            ], xs=12, sm=12, md=4),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Deserción por Facultad (Top 10)"),
                    dbc.CardBody([
                        dcc.Graph(id='graph-facultad-analisis')
                    ])
                ])
            ], xs=12, sm=12, md=6, className="mb-3 mb-md-0"),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Género por Facultad (Top 5)"),
                    dbc.CardBody([
                        dcc.Graph(id='graph-genero-facultad')
                    ])
                ])
            ], xs=12, sm=12, md=6),
        ])
    ])

# =====================================================================
# TAB: MÉTRICAS & KPIs
# =====================================================================

def crear_tab_metricas():
    """Crea el contenido de la pestaña Métricas y KPIs"""

    if datos is None:
        return html.Div("Error cargando datos")

    df = datos['academica']
    kpis_data = datos['kpis']

    # Calcular métricas de calidad de datos
    total_registros = len(df)
    total_columnas = len(df.columns)

    # Completitud por columna
    completitud = {}
    for col in df.columns:
        no_nulos = df[col].notna().sum()
        completitud[col] = (no_nulos / total_registros) * 100

    # KPIs principales del BI
    kpis_bi = {}
    if not kpis_data.empty:
        for _, row in kpis_data.iterrows():
            kpis_bi[row['KPI']] = row['Valor']

    # Estadísticas descriptivas
    edad_stats = df['edad'].describe() if 'edad' in df.columns else None

    return html.Div([
        html.H2("Métricas, KPIs y Calidad de Datos", className="mb-4"),

        # Sección 1: KPIs del Diseño BI
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="fas fa-chart-line me-2"),
                        "KPIs Principales del Sistema BI"
                    ], className="bg-primary text-white"),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.I(className="fas fa-users fa-3x text-danger mb-3"),
                                    html.H2(f"{kpis_bi.get('Total Desertores', 0):,.0f}", className="mb-0"),
                                    html.P("Total Desertores", className="text-muted")
                                ], className="text-center")
                            ], md=3),
                            dbc.Col([
                                html.Div([
                                    html.I(className="fas fa-exclamation-triangle fa-3x text-warning mb-3"),
                                    html.H2(f"{kpis_bi.get('% Alto Riesgo', 0):.2f}%", className="mb-0"),
                                    html.P("Estudiantes Alto Riesgo", className="text-muted")
                                ], className="text-center")
                            ], md=3),
                            dbc.Col([
                                html.Div([
                                    html.I(className="fas fa-chart-bar fa-3x text-info mb-3"),
                                    html.H2(f"{kpis_bi.get('Score Promedio Riesgo', 0):.2f}", className="mb-0"),
                                    html.P("Score Promedio de Riesgo", className="text-muted")
                                ], className="text-center")
                            ], md=3),
                            dbc.Col([
                                html.Div([
                                    html.I(className="fas fa-user-shield fa-3x text-success mb-3"),
                                    html.H2(f"{kpis_bi.get('Estudiantes Alto Riesgo', 0):,.0f}", className="mb-0"),
                                    html.P("Requieren Intervención", className="text-muted")
                                ], className="text-center")
                            ], md=3),
                        ])
                    ])
                ], className="shadow mb-4")
            ], md=12)
        ]),

        # Sección 2: Calidad de Datos
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="fas fa-database me-2"),
                        "Calidad de los Datos"
                    ], className="bg-success text-white"),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.H4("📋 Resumen General"),
                                    html.Hr(),
                                    html.P([html.Strong("Total de Registros: "), f"{total_registros:,}"]),
                                    html.P([html.Strong("Total de Columnas: "), f"{total_columnas}"]),
                                    html.P([html.Strong("Periodo Analizado: "),
                                           f"{df['periodo_año'].min():.0f} - {df['periodo_año'].max():.0f}"
                                           if 'periodo_año' in df.columns else "N/A"]),
                                    html.P([html.Strong("Instituciones: "),
                                           f"{df['institucion'].nunique()}"
                                           if 'institucion' in df.columns else "N/A"]),
                                ])
                            ], md=6),
                            dbc.Col([
                                html.Div([
                                    html.H4("📊 Completitud Promedio"),
                                    html.Hr(),
                                    dcc.Graph(id='graph-completitud-metricas', config={'displayModeBar': False})
                                ])
                            ], md=6),
                        ])
                    ])
                ], className="shadow mb-4")
            ], md=12)
        ]),

        # Sección 3: Estadísticas Descriptivas
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="fas fa-calculator me-2"),
                        "Estadísticas Descriptivas - Edad"
                    ], className="bg-info text-white"),
                    dbc.CardBody([
                        html.Div(id='stats-edad-table')
                    ])
                ], className="shadow mb-4")
            ], md=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="fas fa-table me-2"),
                        "Distribución por Variables Clave"
                    ], className="bg-warning text-white"),
                    dbc.CardBody([
                        html.Div(id='stats-variables-table')
                    ])
                ], className="shadow mb-4")
            ], md=6),
        ]),

        # Sección 4: Top Facultades y Programas
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="fas fa-university me-2"),
                        "Top 10 Facultades con Mayor Deserción"
                    ]),
                    dbc.CardBody([
                        html.Div(id='table-top-facultades')
                    ])
                ], className="shadow mb-4")
            ], md=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.I(className="fas fa-graduation-cap me-2"),
                        "Distribución por Modalidad y Jornada"
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='graph-modalidad-jornada-metricas')
                    ])
                ], className="shadow mb-4")
            ], md=6),
        ]),
    ])

# =====================================================================
# TAB: PREDICTOR ML
# =====================================================================

def crear_tab_predictor():
    """Crea el contenido de la pestaña Predictor ML"""

    return html.Div([
        html.H2("Predictor de Riesgo de Deserción", className="mb-4"),

        dbc.Alert([
            html.I(className="fas fa-info-circle me-2"),
            "Ingrese las características del estudiante para predecir su riesgo de deserción"
        ], color="info"),

        dbc.Row([
            # Formulario de entrada
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Datos del Estudiante"),
                    dbc.CardBody([
                        html.Div([
                            html.Label("Edad:"),
                            dcc.Input(
                                id='input-edad',
                                type='number',
                                min=16,
                                max=60,
                                value=20,
                                className='form-control mb-3'
                            ),

                            html.Label("Género:"),
                            dcc.Dropdown(
                                id='input-genero',
                                options=[
                                    {'label': 'Masculino', 'value': 'M'},
                                    {'label': 'Femenino', 'value': 'F'}
                                ],
                                value='M',
                                clearable=False,
                                className='mb-3'
                            ),

                            html.Label("Estrato Socioeconómico:"),
                            dcc.Slider(
                                id='input-estrato',
                                min=1,
                                max=6,
                                step=1,
                                value=3,
                                marks={i: str(i) for i in range(1, 7)},
                                className='mb-4'
                            ),

                            html.Label("Modalidad:"),
                            dcc.Dropdown(
                                id='input-modalidad',
                                options=[
                                    {'label': 'Presencial', 'value': 'PRESENCIAL'},
                                    {'label': 'Virtual', 'value': 'VIRTUAL'},
                                    {'label': 'Distancia', 'value': 'DISTANCIA'}
                                ],
                                value='PRESENCIAL',
                                clearable=False,
                                className='mb-3'
                            ),

                            html.Label("Jornada:"),
                            dcc.Dropdown(
                                id='input-jornada',
                                options=[
                                    {'label': 'Diurna', 'value': 'DIURNA'},
                                    {'label': 'Nocturna', 'value': 'NOCTURNA'},
                                    {'label': 'Extendida', 'value': 'EXTENDIDA'}
                                ],
                                value='DIURNA',
                                clearable=False,
                                className='mb-3'
                            ),

                            dbc.Button(
                                "Predecir Riesgo",
                                id='btn-predecir',
                                color="primary",
                                size="lg",
                                className="w-100 mt-3"
                            )
                        ])
                    ])
                ])
            ], md=4),

            # Resultado de predicción
            dbc.Col([
                html.Div(id='prediccion-resultado')
            ], md=8),
        ])
    ])

# =====================================================================
# CALLBACKS
# =====================================================================

# Callback para mostrar información de datasets seleccionados
@app.callback(
    Output('dataset-info', 'children'),
    Input('dataset-selector', 'value')
)
def actualizar_info_datasets(datasets_seleccionados):
    """Muestra información de los datasets seleccionados"""
    if not datasets_seleccionados:
        return html.Span("⚠️ Seleccione al menos un dataset", className="text-warning")

    df = combinar_datasets(datasets_seleccionados)
    if df is None:
        return html.Span("❌ Error cargando datasets", className="text-danger")

    total = len(df)
    datasets_nombres = []
    if 'academica' in datasets_seleccionados:
        datasets_nombres.append("Académica")
    if 'no_academica' in datasets_seleccionados:
        datasets_nombres.append("No Académica UPTC")
    if 'sena' in datasets_seleccionados:
        datasets_nombres.append("SENA")

    return html.Span([
        html.I(className="fas fa-check-circle text-success me-2"),
        f"Datasets cargados: {', '.join(datasets_nombres)} • Total: {total:,} registros"
    ])

@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "active_tab")
)
def render_tab_content(active_tab):
    """Renderiza el contenido de la pestaña activa"""
    if active_tab == "tab-overview":
        return crear_tab_overview()
    elif active_tab == "tab-demografico":
        return crear_tab_demografico()
    elif active_tab == "tab-academico":
        return crear_tab_academico()
    elif active_tab == "tab-metricas":
        return crear_tab_metricas()
    elif active_tab == "tab-predictor":
        return crear_tab_predictor()
    return html.Div("Seleccione una pestaña")

# Callbacks para gráficos de Overview
@app.callback(
    Output('graph-temporal-overview', 'figure'),
    [Input('tabs', 'active_tab'),
     Input('dataset-selector', 'value')]
)
def update_temporal_graph(tab, datasets_seleccionados):
    if datos is None or tab != 'tab-overview':
        return {}

    df = combinar_datasets(datasets_seleccionados)
    if df is None:
        return {}
    if 'periodo_año' not in df.columns:
        return {}

    temporal = df.groupby('periodo_año').size().reset_index(name='count')

    fig = px.line(
        temporal,
        x='periodo_año',
        y='count',
        markers=True,
        title="",
        labels={'periodo_año': 'Año', 'count': 'Número de Desertores'}
    )
    fig.update_traces(line_color='#e74c3c', line_width=3)
    fig.update_layout(template='plotly_white')

    return fig

@app.callback(
    Output('graph-genero-overview', 'figure'),
    [Input('tabs', 'active_tab'),
     Input('dataset-selector', 'value')]
)
def update_genero_graph(tab, datasets_seleccionados):
    if datos is None or tab != 'tab-overview':
        return {}

    df = combinar_datasets(datasets_seleccionados)
    if df is None:
        return {}
    if 'genero' not in df.columns:
        return {}

    genero_counts = df['genero'].value_counts()

    fig = go.Figure(data=[go.Pie(
        labels=genero_counts.index,
        values=genero_counts.values,
        hole=0.4,
        marker_colors=['#3498db', '#e74c3c']
    )])
    fig.update_layout(template='plotly_white')

    return fig

@app.callback(
    Output('graph-facultades-overview', 'figure'),
    [Input('tabs', 'active_tab'),
     Input('dataset-selector', 'value')]
)
def update_facultades_graph(tab, datasets_seleccionados):
    if datos is None or tab != 'tab-overview':
        return {}

    df = combinar_datasets(datasets_seleccionados)
    if df is None:
        return {}
    if 'nombre_facultad' not in df.columns:
        return {}

    top10 = df['nombre_facultad'].value_counts().head(10)

    fig = go.Figure(data=[go.Bar(
        y=[str(x)[:40] + '...' if len(str(x)) > 40 else str(x) for x in top10.index],
        x=top10.values,
        orientation='h',
        marker_color='steelblue'
    )])
    fig.update_layout(
        template='plotly_white',
        xaxis_title='Número de Desertores',
        yaxis_title='',
        height=400
    )

    return fig

@app.callback(
    Output('graph-modalidad-overview', 'figure'),
    [Input('tabs', 'active_tab'),
     Input('dataset-selector', 'value')]
)
def update_modalidad_graph(tab, datasets_seleccionados):
    if datos is None or tab != 'tab-overview':
        return {}

    df = combinar_datasets(datasets_seleccionados)
    if df is None:
        return {}
    if 'modalidad' not in df.columns:
        return {}

    modalidad_counts = df['modalidad'].value_counts()

    fig = px.bar(
        x=modalidad_counts.index,
        y=modalidad_counts.values,
        labels={'x': 'Modalidad', 'y': 'Cantidad'},
        color=modalidad_counts.index,
        color_discrete_map={
            'PRESENCIAL': '#2ecc71',
            'VIRTUAL': '#e74c3c',
            'DISTANCIA': '#3498db'
        }
    )
    fig.update_layout(template='plotly_white', showlegend=False)

    return fig

@app.callback(
    Output('graph-dataset-overview', 'figure'),
    [Input('tabs', 'active_tab'),
     Input('dataset-selector', 'value')]
)
def update_dataset_graph(tab, datasets_seleccionados):
    if datos is None or tab != 'tab-overview' or not datasets_seleccionados:
        return {}

    df = combinar_datasets(datasets_seleccionados)
    if df is None or 'dataset_origen' not in df.columns:
        return {}

    dataset_counts = df['dataset_origen'].value_counts()

    fig = go.Figure(data=[go.Pie(
        labels=dataset_counts.index,
        values=dataset_counts.values,
        hole=0.4,
        marker_colors=['#3498db', '#e74c3c', '#2ecc71']
    )])
    fig.update_layout(template='plotly_white')

    return fig

@app.callback(
    Output('graph-estrato-overview', 'figure'),
    [Input('tabs', 'active_tab'),
     Input('dataset-selector', 'value')]
)
def update_estrato_overview_graph(tab, datasets_seleccionados):
    if datos is None or tab != 'tab-overview':
        return {}

    df = combinar_datasets(datasets_seleccionados)
    if df is None or 'estrato' not in df.columns:
        return {}

    # Filtrar solo valores numéricos
    df_temp = df.copy()
    df_temp['estrato_num'] = pd.to_numeric(df_temp['estrato'], errors='coerce')
    df_temp = df_temp[df_temp['estrato_num'].notna()]

    estrato_counts = df_temp['estrato_num'].value_counts().sort_index()

    fig = px.bar(
        x=[f'Estrato {int(e)}' for e in estrato_counts.index],
        y=estrato_counts.values,
        labels={'x': 'Estrato', 'y': 'Cantidad'},
        color=estrato_counts.values,
        color_continuous_scale='Blues'
    )
    fig.update_layout(template='plotly_white', showlegend=False)

    return fig

# =====================================================================
# CALLBACKS PARA TAB MÉTRICAS & KPIs
# =====================================================================

@app.callback(
    Output('graph-completitud-metricas', 'figure'),
    [Input('tabs', 'active_tab'),
     Input('dataset-selector', 'value')]
)
def actualizar_grafico_completitud(tab, datasets_seleccionados):
    """Actualiza el gráfico de completitud de datos"""
    if datos is None or tab != 'tab-metricas':
        return {}

    df = combinar_datasets(datasets_seleccionados)
    if df is None:
        return {}

    # Calcular completitud por columna
    completitud_data = []
    for col in df.columns:
        porcentaje = (df[col].notna().sum() / len(df)) * 100
        completitud_data.append({
            'Columna': col,
            'Completitud': porcentaje
        })

    df_completitud = pd.DataFrame(completitud_data)
    completitud_promedio = df_completitud['Completitud'].mean()

    # Crear gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=completitud_promedio,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Completitud Promedio (%)", 'font': {'size': 20}},
        delta={'reference': 100, 'increasing': {'color': "green"}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 50], 'color': '#ffcccc'},
                {'range': [50, 75], 'color': '#fff4cc'},
                {'range': [75, 90], 'color': '#d4edda'},
                {'range': [90, 100], 'color': '#c3e6cb'}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 95}}))

    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=40, b=20)
    )

    return fig

@app.callback(
    Output('stats-edad-table', 'children'),
    [Input('tabs', 'active_tab'),
     Input('dataset-selector', 'value')]
)
def actualizar_stats_edad(tab, datasets_seleccionados):
    """Actualiza la tabla de estadísticas de edad"""
    if datos is None or tab != 'tab-metricas':
        return html.Div()

    df = combinar_datasets(datasets_seleccionados)
    if df is None:
        return html.Div()

    if 'edad' not in df.columns:
        return html.Div("No hay datos de edad disponibles")

    stats = df['edad'].describe()

    table_data = [
        html.Tr([html.Td(html.Strong("Media")), html.Td(f"{stats['mean']:.2f} años")]),
        html.Tr([html.Td(html.Strong("Mediana")), html.Td(f"{stats['50%']:.2f} años")]),
        html.Tr([html.Td(html.Strong("Desviación Estándar")), html.Td(f"{stats['std']:.2f}")]),
        html.Tr([html.Td(html.Strong("Mínimo")), html.Td(f"{stats['min']:.0f} años")]),
        html.Tr([html.Td(html.Strong("Máximo")), html.Td(f"{stats['max']:.0f} años")]),
        html.Tr([html.Td(html.Strong("Q1 (25%)")), html.Td(f"{stats['25%']:.2f} años")]),
        html.Tr([html.Td(html.Strong("Q3 (75%)")), html.Td(f"{stats['75%']:.2f} años")]),
    ]

    return dbc.Table(
        html.Tbody(table_data),
        bordered=True,
        striped=True,
        hover=True,
        responsive=True
    )

@app.callback(
    Output('stats-variables-table', 'children'),
    [Input('tabs', 'active_tab'),
     Input('dataset-selector', 'value')]
)
def actualizar_stats_variables(tab, datasets_seleccionados):
    """Actualiza la tabla de distribución por variables"""
    if datos is None or tab != 'tab-metricas':
        return html.Div()

    df = combinar_datasets(datasets_seleccionados)
    if df is None:
        return html.Div()

    table_rows = []

    # Género
    if 'genero' in df.columns:
        genero_counts = df['genero'].value_counts()
        genero_str = ", ".join([f"{k}: {v:,}" for k, v in genero_counts.items()])
        table_rows.append(html.Tr([html.Td(html.Strong("Género")), html.Td(genero_str)]))

    # Modalidad
    if 'modalidad' in df.columns:
        modalidad_counts = df['modalidad'].value_counts()
        modalidad_str = ", ".join([f"{k}: {v:,}" for k, v in modalidad_counts.items()])
        table_rows.append(html.Tr([html.Td(html.Strong("Modalidad")), html.Td(modalidad_str)]))

    # Jornada
    if 'jornada' in df.columns:
        jornada_counts = df['jornada'].value_counts().head(3)
        jornada_str = ", ".join([f"{k}: {v:,}" for k, v in jornada_counts.items()])
        table_rows.append(html.Tr([html.Td(html.Strong("Jornada (Top 3)")), html.Td(jornada_str)]))

    # Estrato
    if 'estrato' in df.columns:
        estrato_counts = df['estrato'].value_counts().head(3)
        estrato_str = ", ".join([f"{k}: {v:,}" for k, v in estrato_counts.items()])
        table_rows.append(html.Tr([html.Td(html.Strong("Estrato (Top 3)")), html.Td(estrato_str)]))

    return dbc.Table(
        html.Tbody(table_rows),
        bordered=True,
        striped=True,
        hover=True,
        responsive=True
    )

@app.callback(
    Output('table-top-facultades', 'children'),
    [Input('tabs', 'active_tab'),
     Input('dataset-selector', 'value')]
)
def actualizar_tabla_facultades(tab, datasets_seleccionados):
    """Actualiza la tabla de top facultades"""
    if datos is None or tab != 'tab-metricas':
        return html.Div()

    df = combinar_datasets(datasets_seleccionados)
    if df is None:
        return html.Div()

    if 'nombre_facultad' not in df.columns:
        return html.Div("No hay datos de facultades disponibles")

    top_facultades = df['nombre_facultad'].value_counts().head(10).reset_index()
    top_facultades.columns = ['Facultad', 'Cantidad']

    # Crear tabla
    table_header = [
        html.Thead(html.Tr([
            html.Th("#"),
            html.Th("Facultad"),
            html.Th("Desertores", className="text-end")
        ]))
    ]

    rows = []
    for idx, row in top_facultades.iterrows():
        facultad_nombre = str(row['Facultad'])[:60] + '...' if len(str(row['Facultad'])) > 60 else str(row['Facultad'])
        rows.append(html.Tr([
            html.Td(f"{idx + 1}"),
            html.Td(facultad_nombre),
            html.Td(f"{row['Cantidad']:,}", className="text-end")
        ]))

    table_body = [html.Tbody(rows)]

    return dbc.Table(
        table_header + table_body,
        bordered=True,
        striped=True,
        hover=True,
        responsive=True,
        size='sm'
    )

@app.callback(
    Output('graph-modalidad-jornada-metricas', 'figure'),
    [Input('tabs', 'active_tab'),
     Input('dataset-selector', 'value')]
)
def actualizar_grafico_modalidad_jornada(tab, datasets_seleccionados):
    """Actualiza el gráfico de modalidad vs jornada"""
    if datos is None or tab != 'tab-metricas':
        return {}

    df = combinar_datasets(datasets_seleccionados)
    if df is None:
        return {}

    if 'modalidad' not in df.columns or 'jornada' not in df.columns:
        return {}

    # Crear tabla cruzada
    cross_tab = pd.crosstab(df['modalidad'], df['jornada'])

    fig = go.Figure()

    for jornada in cross_tab.columns:
        fig.add_trace(go.Bar(
            name=str(jornada)[:20],
            x=cross_tab.index,
            y=cross_tab[jornada],
            text=cross_tab[jornada],
            textposition='auto',
        ))

    fig.update_layout(
        barmode='group',
        template='plotly_white',
        xaxis_title='Modalidad',
        yaxis_title='Cantidad de Desertores',
        legend_title='Jornada',
        height=400
    )

    return fig

# =====================================================================
# CALLBACKS PARA TAB DEMOGRÁFICO
# =====================================================================

# Callback para poblar los filtros demográficos
@app.callback(
    [
        Output('filter-genero', 'options'),
        Output('filter-edad', 'options'),
        Output('filter-estrato', 'options')
    ],
    [Input('tabs', 'active_tab'),
     Input('dataset-selector', 'value')]
)
def actualizar_filtros_demografico(tab, datasets_seleccionados):
    """Actualiza las opciones de los filtros demográficos"""
    if datos is None or tab != 'tab-demografico':
        default_options = [{'label': 'Todos', 'value': 'all'}]
        return default_options, default_options, default_options

    df = combinar_datasets(datasets_seleccionados)
    if df is None:
        default_options = [{'label': 'Todos', 'value': 'all'}]
        return default_options, default_options, default_options

    # Opciones de género
    genero_opts = [{'label': 'Todos', 'value': 'all'}]
    if 'genero' in df.columns:
        genero_opts.extend([
            {'label': g, 'value': g} for g in df['genero'].dropna().unique()
        ])

    # Opciones de edad (por rangos)
    edad_opts = [{'label': 'Todos', 'value': 'all'}]
    if 'edad' in df.columns:
        edad_opts.extend([
            {'label': '16-20 años', 'value': '16-20'},
            {'label': '21-25 años', 'value': '21-25'},
            {'label': '26-30 años', 'value': '26-30'},
            {'label': '31+ años', 'value': '31+'}
        ])

    # Opciones de estrato
    estrato_opts = [{'label': 'Todos', 'value': 'all'}]
    if 'estrato' in df.columns:
        # Filtrar solo valores numéricos válidos
        estratos = df['estrato'].dropna().unique()
        estratos_numericos = []
        for e in estratos:
            try:
                estratos_numericos.append(int(float(e)))
            except (ValueError, TypeError):
                pass  # Ignorar valores no numéricos como 'SIN INFORMACION'

        estratos_numericos = sorted(set(estratos_numericos))
        estrato_opts.extend([
            {'label': f'Estrato {e}', 'value': str(e)} for e in estratos_numericos
        ])

    return genero_opts, edad_opts, estrato_opts

# Callback para nuevo gráfico de género en demográfico
@app.callback(
    Output('graph-genero-demografico', 'figure'),
    [Input('tabs', 'active_tab'),
     Input('dataset-selector', 'value'),
     Input('filter-edad', 'value'),
     Input('filter-estrato', 'value')]
)
def actualizar_grafico_genero_demografico(tab, datasets_seleccionados, edad_rango, estrato):
    if datos is None or tab != 'tab-demografico':
        return {}

    df = combinar_datasets(datasets_seleccionados)
    if df is None or 'genero' not in df.columns:
        return {}

    genero_counts = df['genero'].value_counts()

    fig = go.Figure(data=[go.Pie(
        labels=genero_counts.index,
        values=genero_counts.values,
        hole=0.3,
        marker_colors=['#3498db', '#e74c3c']
    )])
    fig.update_layout(template='plotly_white')

    return fig

# Callback para gráfico de distribución de edad
@app.callback(
    Output('graph-edad-dist', 'figure'),
    [
        Input('tabs', 'active_tab'),
        Input('dataset-selector', 'value'),
        Input('filter-genero', 'value'),
        Input('filter-estrato', 'value')
    ]
)
def actualizar_grafico_edad(tab, datasets_seleccionados, genero, estrato):
    """Actualiza el gráfico de distribución de edad"""
    if datos is None or tab != 'tab-demografico':
        return {}

    df = combinar_datasets(datasets_seleccionados)
    if df is None:
        return {}

    df = df.copy()

    if 'edad' not in df.columns:
        return {}

    # Aplicar filtros
    if genero != 'all' and 'genero' in df.columns:
        df = df[df['genero'] == genero]

    if estrato != 'all' and 'estrato' in df.columns:
        # Convertir estrato a numérico y filtrar
        try:
            estrato_val = int(estrato)
            df = df[pd.to_numeric(df['estrato'], errors='coerce') == estrato_val]
        except (ValueError, TypeError):
            pass  # Si no se puede convertir, no filtrar

    # Crear histograma
    fig = px.histogram(
        df,
        x='edad',
        nbins=30,
        title="",
        labels={'edad': 'Edad', 'count': 'Frecuencia'},
        color_discrete_sequence=['#3498db']
    )

    fig.update_layout(
        template='plotly_white',
        showlegend=False,
        xaxis_title='Edad',
        yaxis_title='Número de Estudiantes'
    )

    return fig

# Callback para gráfico de estratos
@app.callback(
    Output('graph-estrato-dist', 'figure'),
    [
        Input('tabs', 'active_tab'),
        Input('dataset-selector', 'value'),
        Input('filter-genero', 'value'),
        Input('filter-edad', 'value')
    ]
)
def actualizar_grafico_estrato(tab, datasets_seleccionados, genero, edad_rango):
    """Actualiza el gráfico de deserción por estrato"""
    if datos is None or tab != 'tab-demografico':
        return {}

    df = combinar_datasets(datasets_seleccionados)
    if df is None:
        return {}

    df = df.copy()

    if 'estrato' not in df.columns:
        return {}

    # Aplicar filtros
    if genero != 'all' and 'genero' in df.columns:
        df = df[df['genero'] == genero]

    if edad_rango != 'all' and 'edad' in df.columns:
        if edad_rango == '16-20':
            df = df[(df['edad'] >= 16) & (df['edad'] <= 20)]
        elif edad_rango == '21-25':
            df = df[(df['edad'] >= 21) & (df['edad'] <= 25)]
        elif edad_rango == '26-30':
            df = df[(df['edad'] >= 26) & (df['edad'] <= 30)]
        elif edad_rango == '31+':
            df = df[df['edad'] >= 31]

    # Contar por estrato (solo valores numéricos)
    df_estrato = df.copy()
    df_estrato['estrato_num'] = pd.to_numeric(df_estrato['estrato'], errors='coerce')
    df_estrato = df_estrato[df_estrato['estrato_num'].notna()]

    estrato_counts = df_estrato['estrato_num'].value_counts().sort_index()

    fig = px.bar(
        x=[f'Estrato {int(e)}' for e in estrato_counts.index],
        y=estrato_counts.values,
        title="",
        labels={'x': 'Estrato Socioeconómico', 'y': 'Número de Desertores'},
        color=estrato_counts.values,
        color_continuous_scale='Reds'
    )

    fig.update_layout(
        template='plotly_white',
        showlegend=False,
        xaxis_title='Estrato Socioeconómico',
        yaxis_title='Número de Desertores'
    )

    return fig

# Callback para gráfico edad vs modalidad
@app.callback(
    Output('graph-edad-modalidad', 'figure'),
    [
        Input('tabs', 'active_tab'),
        Input('dataset-selector', 'value'),
        Input('filter-genero', 'value'),
        Input('filter-estrato', 'value')
    ]
)
def actualizar_grafico_edad_modalidad(tab, datasets_seleccionados, genero, estrato):
    """Actualiza el gráfico de edad vs modalidad"""
    if datos is None or tab != 'tab-demografico':
        return {}

    df = combinar_datasets(datasets_seleccionados)
    if df is None:
        return {}

    df = df.copy()

    if 'edad' not in df.columns or 'modalidad' not in df.columns:
        return {}

    # Aplicar filtros
    if genero != 'all' and 'genero' in df.columns:
        df = df[df['genero'] == genero]

    if estrato != 'all' and 'estrato' in df.columns:
        # Convertir estrato a numérico y filtrar
        try:
            estrato_val = int(estrato)
            df = df[pd.to_numeric(df['estrato'], errors='coerce') == estrato_val]
        except (ValueError, TypeError):
            pass  # Si no se puede convertir, no filtrar

    # Crear box plot
    fig = px.box(
        df,
        x='modalidad',
        y='edad',
        title="",
        labels={'modalidad': 'Modalidad', 'edad': 'Edad'},
        color='modalidad',
        color_discrete_map={
            'PRESENCIAL': '#2ecc71',
            'VIRTUAL': '#e74c3c',
            'DISTANCIA': '#3498db'
        }
    )

    fig.update_layout(
        template='plotly_white',
        showlegend=False,
        xaxis_title='Modalidad',
        yaxis_title='Edad'
    )

    return fig

# =====================================================================
# CALLBACKS PARA TAB ACADÉMICO
# =====================================================================

# Callback para poblar los filtros académicos
@app.callback(
    [
        Output('filter-facultad', 'options'),
        Output('filter-modalidad', 'options'),
        Output('filter-jornada', 'options')
    ],
    [Input('tabs', 'active_tab'),
     Input('dataset-selector', 'value')]
)
def actualizar_filtros_academico(tab, datasets_seleccionados):
    """Actualiza las opciones de los filtros académicos"""
    if datos is None or tab != 'tab-academico':
        default_options = [{'label': 'Todas', 'value': 'all'}]
        return default_options, default_options, default_options

    df = combinar_datasets(datasets_seleccionados)
    if df is None:
        default_options = [{'label': 'Todas', 'value': 'all'}]
        return default_options, default_options, default_options

    # Opciones de facultad
    facultad_opts = [{'label': 'Todas', 'value': 'all'}]
    if 'nombre_facultad' in df.columns:
        facultades = df['nombre_facultad'].dropna().unique()
        facultad_opts.extend([
            {'label': str(f)[:50] + '...' if len(str(f)) > 50 else str(f), 'value': f}
            for f in sorted(facultades)
        ])

    # Opciones de modalidad
    modalidad_opts = [{'label': 'Todas', 'value': 'all'}]
    if 'modalidad' in df.columns:
        modalidades = df['modalidad'].dropna().unique()
        modalidad_opts.extend([
            {'label': m, 'value': m} for m in sorted(modalidades)
        ])

    # Opciones de jornada
    jornada_opts = [{'label': 'Todas', 'value': 'all'}]
    if 'jornada' in df.columns:
        jornadas = df['jornada'].dropna().unique()
        jornada_opts.extend([
            {'label': j, 'value': j} for j in sorted(jornadas)
        ])

    return facultad_opts, modalidad_opts, jornada_opts

# Callback para gráfico de deserción por facultad
@app.callback(
    Output('graph-facultad-analisis', 'figure'),
    [
        Input('tabs', 'active_tab'),
        Input('dataset-selector', 'value'),
        Input('filter-modalidad', 'value'),
        Input('filter-jornada', 'value')
    ]
)
def actualizar_grafico_facultad(tab, datasets_seleccionados, modalidad, jornada):
    """Actualiza el gráfico de deserción por facultad"""
    if datos is None or tab != 'tab-academico':
        return {}

    df = combinar_datasets(datasets_seleccionados)
    if df is None:
        return {}

    df = df.copy()

    if 'nombre_facultad' not in df.columns:
        return {}

    # Aplicar filtros
    if modalidad != 'all' and 'modalidad' in df.columns:
        df = df[df['modalidad'] == modalidad]

    if jornada != 'all' and 'jornada' in df.columns:
        df = df[df['jornada'] == jornada]

    # Top 10 facultades
    top_facultades = df['nombre_facultad'].value_counts().head(10)

    fig = go.Figure(data=[go.Bar(
        y=[str(x)[:50] + '...' if len(str(x)) > 50 else str(x) for x in top_facultades.index],
        x=top_facultades.values,
        orientation='h',
        marker_color='#e74c3c',
        text=top_facultades.values,
        textposition='outside'
    )])

    fig.update_layout(
        template='plotly_white',
        xaxis_title='Número de Desertores',
        yaxis_title='',
        height=500,
        margin=dict(l=200)
    )

    return fig

# Callback para gráfico pie de jornada
@app.callback(
    Output('graph-jornada-pie', 'figure'),
    [
        Input('tabs', 'active_tab'),
        Input('dataset-selector', 'value'),
        Input('filter-facultad', 'value'),
        Input('filter-modalidad', 'value')
    ]
)
def actualizar_grafico_jornada(tab, datasets_seleccionados, facultad, modalidad):
    """Actualiza el gráfico de distribución por jornada"""
    if datos is None or tab != 'tab-academico':
        return {}

    df = combinar_datasets(datasets_seleccionados)
    if df is None:
        return {}

    df = df.copy()

    if 'jornada' not in df.columns:
        return {}

    # Aplicar filtros
    if facultad != 'all' and 'nombre_facultad' in df.columns:
        df = df[df['nombre_facultad'] == facultad]

    if modalidad != 'all' and 'modalidad' in df.columns:
        df = df[df['modalidad'] == modalidad]

    # Contar por jornada
    jornada_counts = df['jornada'].value_counts()

    fig = go.Figure(data=[go.Pie(
        labels=jornada_counts.index,
        values=jornada_counts.values,
        hole=0.4,
        marker_colors=['#3498db', '#e74c3c', '#2ecc71']
    )])

    fig.update_layout(template='plotly_white')

    return fig

# Callback para gráfico género por facultad
@app.callback(
    Output('graph-genero-facultad', 'figure'),
    [
        Input('tabs', 'active_tab'),
        Input('dataset-selector', 'value'),
        Input('filter-modalidad', 'value'),
        Input('filter-jornada', 'value')
    ]
)
def actualizar_grafico_genero_facultad(tab, datasets_seleccionados, modalidad, jornada):
    """Actualiza el gráfico de género por facultad (Top 5)"""
    if datos is None or tab != 'tab-academico':
        return {}

    df = combinar_datasets(datasets_seleccionados)
    if df is None:
        return {}

    df = df.copy()

    if 'nombre_facultad' not in df.columns or 'genero' not in df.columns:
        return {}

    # Aplicar filtros
    if modalidad != 'all' and 'modalidad' in df.columns:
        df = df[df['modalidad'] == modalidad]

    if jornada != 'all' and 'jornada' in df.columns:
        df = df[df['jornada'] == jornada]

    # Top 5 facultades
    top5_facultades = df['nombre_facultad'].value_counts().head(5).index
    df_top5 = df[df['nombre_facultad'].isin(top5_facultades)]

    # Contar por facultad y género
    cross_tab = pd.crosstab(df_top5['nombre_facultad'], df_top5['genero'])

    fig = go.Figure()

    for genero in cross_tab.columns:
        fig.add_trace(go.Bar(
            name=genero,
            x=[str(x)[:40] + '...' if len(str(x)) > 40 else str(x) for x in cross_tab.index],
            y=cross_tab[genero],
            text=cross_tab[genero],
            textposition='auto'
        ))

    fig.update_layout(
        template='plotly_white',
        barmode='group',
        xaxis_title='Facultad',
        yaxis_title='Número de Desertores',
        legend_title='Género',
        height=400
    )

    return fig

# Callback para gráfico de modalidades en académico
@app.callback(
    Output('graph-modalidad-academico', 'figure'),
    [Input('tabs', 'active_tab'),
     Input('dataset-selector', 'value'),
     Input('filter-facultad', 'value'),
     Input('filter-jornada', 'value')]
)
def actualizar_grafico_modalidad_academico(tab, datasets_seleccionados, facultad, jornada):
    if datos is None or tab != 'tab-academico':
        return {}

    df = combinar_datasets(datasets_seleccionados)
    if df is None or 'modalidad' not in df.columns:
        return {}

    # Aplicar filtros
    if facultad != 'all' and 'nombre_facultad' in df.columns:
        df = df[df['nombre_facultad'] == facultad]

    if jornada != 'all' and 'jornada' in df.columns:
        df = df[df['jornada'] == jornada]

    modalidad_counts = df['modalidad'].value_counts()

    fig = go.Figure(data=[go.Pie(
        labels=modalidad_counts.index,
        values=modalidad_counts.values,
        hole=0.4
    )])
    fig.update_layout(template='plotly_white')

    return fig

# Callback para gráfico de dataset en académico
@app.callback(
    Output('graph-dataset-academico', 'figure'),
    [Input('tabs', 'active_tab'),
     Input('dataset-selector', 'value'),
     Input('filter-facultad', 'value'),
     Input('filter-modalidad', 'value'),
     Input('filter-jornada', 'value')]
)
def actualizar_grafico_dataset_academico(tab, datasets_seleccionados, facultad, modalidad, jornada):
    if datos is None or tab != 'tab-academico':
        return {}

    df = combinar_datasets(datasets_seleccionados)
    if df is None or 'dataset_origen' not in df.columns:
        return {}

    dataset_counts = df['dataset_origen'].value_counts()

    fig = px.bar(
        x=dataset_counts.index,
        y=dataset_counts.values,
        labels={'x': 'Dataset', 'y': 'Cantidad'},
        color=dataset_counts.index
    )
    fig.update_layout(template='plotly_white', showlegend=False)

    return fig

# =====================================================================
# CALLBACK PARA PREDICCIÓN
# =====================================================================

# Callback para predicción
@app.callback(
    Output('prediccion-resultado', 'children'),
    Input('btn-predecir', 'n_clicks'),
    [
        Input('input-edad', 'value'),
        Input('input-genero', 'value'),
        Input('input-estrato', 'value'),
        Input('input-modalidad', 'value'),
        Input('input-jornada', 'value')
    ]
)
def realizar_prediccion(n_clicks, edad, genero, estrato, modalidad, jornada):
    if n_clicks is None or n_clicks == 0:
        return dbc.Alert("Haga clic en 'Predecir Riesgo' para obtener el resultado", color="secondary")

    # Calcular score simple (sin modelo real por ahora)
    score = 0
    if estrato <= 2:
        score += 30
    if modalidad in ['VIRTUAL', 'DISTANCIA']:
        score += 25
    if edad < 18 or edad > 30:
        score += 20
    if jornada == 'NOCTURNA':
        score += 15
    if genero == 'M':
        score += 5

    probabilidad = min(score, 100) / 100

    # Determinar nivel
    if probabilidad < 0.3:
        nivel = "BAJO"
        color = "success"
        icono = "fa-check-circle"
    elif probabilidad < 0.5:
        nivel = "MEDIO"
        color = "warning"
        icono = "fa-exclamation-triangle"
    elif probabilidad < 0.7:
        nivel = "ALTO"
        color = "danger"
        icono = "fa-exclamation-circle"
    else:
        nivel = "CRÍTICO"
        color = "danger"
        icono = "fa-times-circle"

    return dbc.Card([
        dbc.CardHeader([
            html.I(className=f"fas {icono} me-2"),
            f"Resultado de la Predicción"
        ]),
        dbc.CardBody([
            html.Div([
                html.H1(f"{probabilidad*100:.1f}%", className=f"text-{color}"),
                html.H4(f"Riesgo {nivel}", className="mb-4"),

                dbc.Progress(
                    value=probabilidad*100,
                    color=color,
                    className="mb-4",
                    style={'height': '30px'}
                ),

                html.H5("Factores Evaluados:", className="mt-4"),
                dbc.ListGroup([
                    dbc.ListGroupItem([
                        html.Strong("Edad: "),
                        f"{edad} años ",
                        dbc.Badge("✓ Normal" if 18 <= edad <= 30 else "⚠ Fuera de rango", color="success" if 18 <= edad <= 30 else "warning")
                    ]),
                    dbc.ListGroupItem([
                        html.Strong("Estrato: "),
                        f"{estrato} ",
                        dbc.Badge("✓ Medio/Alto" if estrato > 2 else "⚠ Bajo", color="success" if estrato > 2 else "warning")
                    ]),
                    dbc.ListGroupItem([
                        html.Strong("Modalidad: "),
                        f"{modalidad} ",
                        dbc.Badge("✓ Presencial" if modalidad == 'PRESENCIAL' else "⚠ A distancia", color="success" if modalidad == 'PRESENCIAL' else "warning")
                    ]),
                    dbc.ListGroupItem([
                        html.Strong("Jornada: "),
                        f"{jornada} ",
                        dbc.Badge("✓ Diurna/Extendida" if jornada != 'NOCTURNA' else "⚠ Nocturna", color="success" if jornada != 'NOCTURNA' else "warning")
                    ]),
                ]),

                html.Hr(),

                dbc.Alert([
                    html.H6("Recomendaciones:", className="alert-heading"),
                    html.Ul([
                        html.Li("Asignar consejero académico") if probabilidad > 0.5 else None,
                        html.Li("Inscribir en programa de tutorías") if probabilidad > 0.3 else None,
                        html.Li("Evaluar apoyo socioeconómico") if estrato <= 2 else None,
                        html.Li("Seguimiento mensual") if probabilidad > 0.7 else None,
                    ])
                ], color=color)
            ], className="text-center")
        ])
    ], className="shadow")

# =====================================================================
# EJECUTAR APLICACIÓN
# =====================================================================

if __name__ == '__main__':
    print("="*70)
    print("DASHBOARD DE DESERCIÓN EDUCATIVA")
    print("="*70)
    print("\nIniciando servidor...")
    print("URL: http://127.0.0.1:8050")
    print("\nPresione Ctrl+C para detener el servidor\n")
    print("="*70)

    app.run(debug=True, host='127.0.0.1', port=8050)
