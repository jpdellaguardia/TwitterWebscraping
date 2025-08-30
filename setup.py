#!/usr/bin/env python3
"""
Script de configuração para instalar dependências e ChromeDriver
"""
import subprocess
import sys
import os

def setup_venv():
    """Cria ambiente virtual e instala dependências"""
    # Cria ambiente virtual
    subprocess.check_call([sys.executable, "-m", "venv", "venv"])
    
    # Determina o caminho do pip no venv
    pip_path = "venv/bin/pip" if os.name != 'nt' else "venv\\Scripts\\pip.exe"
    python_path = "venv/bin/python" if os.name != 'nt' else "venv\\Scripts\\python.exe"
    
    # Instala dependências no venv
    subprocess.check_call([pip_path, "install", "-r", "requirements.txt"])
    
    return python_path

if __name__ == "__main__":
    print("Criando ambiente virtual...")
    python_path = setup_venv()
    
    print("Configuração concluída!")
    print("\nPara usar o scraper:")
    print("1. Edite o arquivo example_usage.py com suas credenciais")
    print(f"2. Execute: {python_path} example_usage.py")
    print("\nOu ative o ambiente virtual:")
    if os.name != 'nt':
        print("source venv/bin/activate")
    else:
        print("venv\\Scripts\\activate")
    print("python example_usage.py")