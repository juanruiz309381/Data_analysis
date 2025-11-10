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
    dbc.Tab(label="🤖 Predictor ML", tab_id="tab-predictor"),
], id="tabs", active_tab="tab-overview", className="mb-3")

# Layout principal
app.layout = html.Div([
    header,
    dbc.Container([
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

    # Gráficos principales
    graficos_row1 = dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Evolución Temporal de Deserción"),
                dbc.CardBody([
                    dcc.Graph(id='graph-temporal-overview')
                ])
            ])
        ], md=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Distribución por Género"),
                dbc.CardBody([
                    dcc.Graph(id='graph-genero-overview')
                ])
            ])
        ], md=6),
    ], className="mb-4")

    graficos_row2 = dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Top 10 Facultades con Mayor Deserción"),
                dbc.CardBody([
                    dcc.Graph(id='graph-facultades-overview')
                ])
            ])
        ], md=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Deserción por Modalidad"),
                dbc.CardBody([
                    dcc.Graph(id='graph-modalidad-overview')
                ])
            ])
        ], md=6),
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

        # Gráficos demográficos
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Distribución de Edad"),
                    dbc.CardBody([
                        dcc.Graph(id='graph-edad-dist')
                    ])
                ])
            ], md=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Deserción por Estrato Socioeconómico"),
                    dbc.CardBody([
                        dcc.Graph(id='graph-estrato-dist')
                    ])
                ])
            ], md=6),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Edad vs Modalidad"),
                    dbc.CardBody([
                        dcc.Graph(id='graph-edad-modalidad')
                    ])
                ])
            ], md=12),
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

        # Gráficos académicos
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Deserción por Facultad"),
                    dbc.CardBody([
                        dcc.Graph(id='graph-facultad-analisis')
                    ])
                ])
            ], md=8),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Distribución por Jornada"),
                    dbc.CardBody([
                        dcc.Graph(id='graph-jornada-pie')
                    ])
                ])
            ], md=4),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Género por Facultad (Top 5)"),
                    dbc.CardBody([
                        dcc.Graph(id='graph-genero-facultad')
                    ])
                ])
            ], md=12),
        ])
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
    elif active_tab == "tab-predictor":
        return crear_tab_predictor()
    return html.Div("Seleccione una pestaña")

# Callbacks para gráficos de Overview
@app.callback(
    Output('graph-temporal-overview', 'figure'),
    Input('tabs', 'active_tab')
)
def update_temporal_graph(tab):
    if datos is None or tab != 'tab-overview':
        return {}

    df = datos['academica']
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
    Input('tabs', 'active_tab')
)
def update_genero_graph(tab):
    if datos is None or tab != 'tab-overview':
        return {}

    df = datos['academica']
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
    Input('tabs', 'active_tab')
)
def update_facultades_graph(tab):
    if datos is None or tab != 'tab-overview':
        return {}

    df = datos['academica']
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
    Input('tabs', 'active_tab')
)
def update_modalidad_graph(tab):
    if datos is None or tab != 'tab-overview':
        return {}

    df = datos['academica']
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
    Input('tabs', 'active_tab')
)
def actualizar_filtros_demografico(tab):
    """Actualiza las opciones de los filtros demográficos"""
    if datos is None or tab != 'tab-demografico':
        default_options = [{'label': 'Todos', 'value': 'all'}]
        return default_options, default_options, default_options

    df = datos['academica']

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
        estratos = sorted(df['estrato'].dropna().unique())
        estrato_opts.extend([
            {'label': f'Estrato {int(e)}', 'value': str(int(e))} for e in estratos
        ])

    return genero_opts, edad_opts, estrato_opts

# Callback para gráfico de distribución de edad
@app.callback(
    Output('graph-edad-dist', 'figure'),
    [
        Input('tabs', 'active_tab'),
        Input('filter-genero', 'value'),
        Input('filter-estrato', 'value')
    ]
)
def actualizar_grafico_edad(tab, genero, estrato):
    """Actualiza el gráfico de distribución de edad"""
    if datos is None or tab != 'tab-demografico':
        return {}

    df = datos['academica'].copy()

    if 'edad' not in df.columns:
        return {}

    # Aplicar filtros
    if genero != 'all' and 'genero' in df.columns:
        df = df[df['genero'] == genero]

    if estrato != 'all' and 'estrato' in df.columns:
        df = df[df['estrato'] == int(estrato)]

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
        Input('filter-genero', 'value'),
        Input('filter-edad', 'value')
    ]
)
def actualizar_grafico_estrato(tab, genero, edad_rango):
    """Actualiza el gráfico de deserción por estrato"""
    if datos is None or tab != 'tab-demografico':
        return {}

    df = datos['academica'].copy()

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

    # Contar por estrato
    estrato_counts = df['estrato'].value_counts().sort_index()

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
        Input('filter-genero', 'value'),
        Input('filter-estrato', 'value')
    ]
)
def actualizar_grafico_edad_modalidad(tab, genero, estrato):
    """Actualiza el gráfico de edad vs modalidad"""
    if datos is None or tab != 'tab-demografico':
        return {}

    df = datos['academica'].copy()

    if 'edad' not in df.columns or 'modalidad' not in df.columns:
        return {}

    # Aplicar filtros
    if genero != 'all' and 'genero' in df.columns:
        df = df[df['genero'] == genero]

    if estrato != 'all' and 'estrato' in df.columns:
        df = df[df['estrato'] == int(estrato)]

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
    Input('tabs', 'active_tab')
)
def actualizar_filtros_academico(tab):
    """Actualiza las opciones de los filtros académicos"""
    if datos is None or tab != 'tab-academico':
        default_options = [{'label': 'Todas', 'value': 'all'}]
        return default_options, default_options, default_options

    df = datos['academica']

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
        Input('filter-modalidad', 'value'),
        Input('filter-jornada', 'value')
    ]
)
def actualizar_grafico_facultad(tab, modalidad, jornada):
    """Actualiza el gráfico de deserción por facultad"""
    if datos is None or tab != 'tab-academico':
        return {}

    df = datos['academica'].copy()

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
        Input('filter-facultad', 'value'),
        Input('filter-modalidad', 'value')
    ]
)
def actualizar_grafico_jornada(tab, facultad, modalidad):
    """Actualiza el gráfico de distribución por jornada"""
    if datos is None or tab != 'tab-academico':
        return {}

    df = datos['academica'].copy()

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
        Input('filter-modalidad', 'value'),
        Input('filter-jornada', 'value')
    ]
)
def actualizar_grafico_genero_facultad(tab, modalidad, jornada):
    """Actualiza el gráfico de género por facultad (Top 5)"""
    if datos is None or tab != 'tab-academico':
        return {}

    df = datos['academica'].copy()

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
