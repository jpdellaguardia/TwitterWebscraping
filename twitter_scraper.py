from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import json
import csv

class TwitterScraper:
    def __init__(self, headless=True):
        self.options = Options()
        if headless:
            self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--disable-gpu')
        
        self.driver = webdriver.Chrome(options=self.options)
        self.wait = WebDriverWait(self.driver, 10)
    
    def login(self, username, password):
        """Login no Twitter/X"""
        try:
            print("Acessando página de login...")
            self.driver.get("https://twitter.com/login")
            time.sleep(5)
            
            # Username
            print(f"Inserindo username: {username}")
            username_input = self.wait.until(EC.presence_of_element_located((By.NAME, "text")))
            username_input.clear()
            username_input.send_keys(username)
            time.sleep(2)
            
            next_button = self.driver.find_element(By.XPATH, "//span[text()='Avançar'] | //span[text()='Next']")
            next_button.click()
            time.sleep(3)
            
            # Password
            print("Inserindo senha...")
            password_input = self.wait.until(EC.presence_of_element_located((By.NAME, "password")))
            password_input.clear()
            password_input.send_keys(password)
            time.sleep(2)
            
            login_button = self.driver.find_element(By.XPATH, "//span[text()='Entrar'] | //span[text()='Log in']")
            login_button.click()
            
            print("Aguardando login...")
            time.sleep(10)
            
            # Verifica se o login foi bem-sucedido
            current_url = self.driver.current_url
            if "home" in current_url or "twitter.com" in current_url:
                print("Login realizado com sucesso!")
            else:
                print(f"Possível erro no login. URL atual: {current_url}")
                
        except Exception as e:
            print(f"Erro durante o login: {e}")
            print("Pressione Enter para continuar mesmo assim...")
            input()
    
    def get_posts(self, profile_url, max_posts=30):
        """Captura URLs das últimas postagens"""
        print(f"Acessando perfil: {profile_url}")
        self.driver.get(profile_url)
        time.sleep(5)
        
        posts = set()  # Usar set para evitar duplicatas
        scroll_attempts = 0
        max_scrolls = 10
        
        while len(posts) < max_posts and scroll_attempts < max_scrolls:
            # Busca por links de tweets do perfil específico
            tweet_links = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/status/')]")
            print(f"Encontrados {len(tweet_links)} links na página")
            
            for link in tweet_links:
                href = link.get_attribute('href')
                # Filtra apenas posts do usuário específico
                if '/status/' in href and profile_url.split('/')[-1] in href:
                    # Remove parâmetros extras da URL
                    clean_href = href.split('?')[0].split('/analytics')[0]
                    posts.add(clean_href)
                    print(f"Post encontrado: {clean_href}")
                    if len(posts) >= max_posts:
                        break
            
            print(f"Total de posts únicos: {len(posts)}")
            
            # Scroll para carregar mais posts
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            scroll_attempts += 1
        
        return list(posts)[:max_posts]
    
    def get_comments(self, post_url):
        """Captura comentários de uma postagem específica"""
        print(f"Capturando comentários de: {post_url}")
        
        # Remove /analytics da URL se existir
        clean_url = post_url.replace('/analytics', '')
        self.driver.get(clean_url)
        time.sleep(5)
        
        comments = []
        
        # Scroll para carregar comentários
        for i in range(3):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            print(f"Scroll {i+1}/3")
        
        # Busca especificamente por replies/comentários
        # Usa seletor mais específico para comentários reais
        comment_containers = self.driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")
        print(f"Containers de tweet encontrados: {len(comment_containers)}")
        
        original_post_found = False
        
        for container in comment_containers:
            try:
                # Verifica se é o post original
                links = container.find_elements(By.XPATH, ".//a[contains(@href, '/status/')]")
                is_original = any(clean_url.split('/')[-1] in link.get_attribute('href') for link in links)
                
                if is_original and not original_post_found:
                    original_post_found = True
                    print("Post original encontrado, pulando...")
                    continue
                
                # Se não é o post original, é um comentário
                if original_post_found and len(comments) < 10:
                    text_elements = container.find_elements(By.XPATH, ".//div[@data-testid='tweetText']")
                    for text_element in text_elements:
                        if len(comments) >= 10:
                            break
                        comment_text = text_element.text.strip()
                        if comment_text and comment_text not in comments:
                            comments.append(comment_text)
                            print(f"Comentário {len(comments)}: {comment_text[:50]}...")
                            
            except Exception as e:
                print(f"Erro ao processar container: {e}")
                continue
        
        print(f"Total de comentários capturados: {len(comments)} (limitado a 10)")
        return comments[:10]
    
    def scrape_portal(self, portal_username, username, password, output_file="comments.csv"):
        """Função principal para capturar comentários"""
        try:
            print("=== INICIANDO CAPTURA DE COMENTÁRIOS ===")
            
            # Login
            self.login(username, password)
            
            # URL do perfil
            profile_url = f"https://twitter.com/{portal_username}"
            
            # Captura posts
            print("\n=== CAPTURANDO POSTS ===")
            posts = self.get_posts(profile_url)
            print(f"\nEncontrados {len(posts)} posts")
            
            if not posts:
                print("ERRO: Nenhum post encontrado!")
                print("Verifique se o perfil existe e está público.")
                input("Pressione Enter para fechar...")
                return
            
            # Captura comentários
            print("\n=== CAPTURANDO COMENTÁRIOS ===")
            all_comments = []
            for i, post_url in enumerate(posts, 1):
                print(f"\nProcessando post {i}/{len(posts)}")
                comments = self.get_comments(post_url)
                
                for comment in comments:
                    all_comments.append({
                        'post_url': post_url,
                        'comment': comment
                    })
                
                time.sleep(2)  # Evita rate limiting
            
            # Salva em CSV
            print(f"\n=== SALVANDO RESULTADOS ===")
            with open(output_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=['post_url', 'comment'])
                writer.writeheader()
                writer.writerows(all_comments)
            
            print(f"\n✅ SUCESSO! Capturados {len(all_comments)} comentários")
            print(f"📁 Arquivo salvo: {output_file}")
            
        except Exception as e:
            print(f"\n❌ ERRO: {e}")
            import traceback
            traceback.print_exc()
        finally:
            print("\nPressione Enter para fechar o navegador...")
            input()
            self.driver.quit()

if __name__ == "__main__":
    # Configurações
    PORTAL_USERNAME = "nome_do_portal"  # Substitua pelo username do portal
    YOUR_USERNAME = "seu_usuario"       # Seu username do Twitter
    YOUR_PASSWORD = "sua_senha"         # Sua senha do Twitter
    
    scraper = TwitterScraper(headless=False)  # headless=True para executar sem interface
    scraper.scrape_portal(PORTAL_USERNAME, YOUR_USERNAME, YOUR_PASSWORD)