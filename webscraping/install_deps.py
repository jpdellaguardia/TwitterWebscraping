#!/usr/bin/env python3
"""
Script para instalar dependências na venv webscraping
"""
import subprocess
import sys

def install_requirements():
    """Instala as dependências necessárias"""
    packages = [
        "selenium==4.15.2",
        "webdriver-manager==4.0.1"
    ]
    
    for package in packages:
        print(f"Instalando {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

if __name__ == "__main__":
    print("Instalando dependências na venv webscraping...")
    install_requirements()
    print("Dependências instaladas com sucesso!")
    print("\nPara usar o scraper:")
    print("1. Edite example_usage.py com suas credenciais")
    print("2. Execute: python example_usage.py")