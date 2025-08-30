#!/bin/bash
# Script para executar o sistema de captura de comentários

echo "Configurando ambiente..."
python3 setup.py

echo -e "\nAtivando ambiente virtual..."
source venv/bin/activate

echo -e "\nExecutando captura de comentários..."
python example_usage.py