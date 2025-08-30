#!/usr/bin/env python3
"""
Exemplo de uso do TwitterScraper
"""
from twitter_scraper import TwitterScraper

def main():
    # Configurações
    PORTAL_USERNAME = "LulaOficial"       # Perfil do Lula
    YOUR_USERNAME = "luizsdg"             # Seu username do Twitter
    YOUR_PASSWORD = "DGinfo01"            # Sua senha do Twitter
    
    # Cria o scraper
    scraper = TwitterScraper(headless=False)  # headless=True para executar sem interface gráfica
    
    # Executa a captura
    scraper.scrape_portal(
        portal_username=PORTAL_USERNAME,
        username=YOUR_USERNAME,
        password=YOUR_PASSWORD,
        output_file="comentarios_lula.csv"
    )

if __name__ == "__main__":
    main()