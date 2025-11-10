#!/bin/bash

# Script para ejecutar el Dashboard de Deserción Educativa
# Autor: Sistema de Análisis de Datos
# Fecha: Noviembre 2025

echo "======================================================================"
echo "         DASHBOARD DE DESERCIÓN EDUCATIVA - ITM 2025-2"
echo "======================================================================"
echo ""

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar si estamos en el directorio correcto
if [ ! -f "app.py" ]; then
    echo -e "${RED}Error: No se encontró app.py${NC}"
    echo "Por favor ejecute este script desde el directorio 'dashboards/'"
    exit 1
fi

# Verificar si el ambiente virtual está activado
if [ -z "$VIRTUAL_ENV" ]; then
    echo -e "${YELLOW}Advertencia: Ambiente virtual no activado${NC}"
    echo "Activando ambiente virtual..."

    # Buscar el ambiente virtual
    if [ -d "../venv_final_project" ]; then
        source ../venv_final_project/bin/activate
        echo -e "${GREEN}✓ Ambiente virtual activado${NC}"
    elif [ -d "../venv" ]; then
        source ../venv/bin/activate
        echo -e "${GREEN}✓ Ambiente virtual activado${NC}"
    else
        echo -e "${RED}Error: No se encontró el ambiente virtual${NC}"
        echo "Por favor cree el ambiente virtual primero:"
        echo "  cd .."
        echo "  python3 -m venv venv_final_project"
        echo "  source venv_final_project/bin/activate"
        echo "  pip install -r requirements.txt"
        exit 1
    fi
fi

# Verificar que los datos procesados existen
echo ""
echo "Verificando datos..."
if [ ! -d "../data/processed" ] || [ -z "$(ls -A ../data/processed)" ]; then
    echo -e "${RED}Error: No se encontraron datos procesados${NC}"
    echo "Por favor ejecute primero los notebooks de ETL:"
    echo "  1. notebooks/01_ETL.ipynb"
    echo "  2. notebooks/03_BI_Design.ipynb"
    exit 1
fi
echo -e "${GREEN}✓ Datos encontrados${NC}"

# Verificar dependencias
echo ""
echo "Verificando dependencias de Python..."
python3 -c "import dash" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}Instalando dependencias faltantes...${NC}"
    pip install dash dash-bootstrap-components plotly pandas joblib
fi
echo -e "${GREEN}✓ Dependencias instaladas${NC}"

# Ejecutar la aplicación
echo ""
echo "======================================================================"
echo -e "${GREEN}✓ Iniciando Dashboard...${NC}"
echo "======================================================================"
echo ""
echo -e "${BLUE}URL del Dashboard:${NC} http://127.0.0.1:8050"
echo ""
echo -e "${YELLOW}Presione Ctrl+C para detener el servidor${NC}"
echo ""
echo "======================================================================"
echo ""

# Esperar 2 segundos y abrir el navegador
sleep 2
if command -v xdg-open > /dev/null; then
    xdg-open http://127.0.0.1:8050 &
elif command -v open > /dev/null; then
    open http://127.0.0.1:8050 &
fi

# Ejecutar la aplicación
python3 app.py
