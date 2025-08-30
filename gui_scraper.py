#!/usr/bin/env python3
"""
Interface gráfica para o TwitterScraper
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
from twitter_scraper import TwitterScraper
import os

class TwitterScraperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Twitter Scraper - Captura de Comentários")
        self.root.geometry("500x400")
        
        # Variáveis
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.profile_var = tk.StringVar()
        self.max_posts_var = tk.IntVar(value=30)
        self.max_comments_var = tk.IntVar(value=10)
        self.headless_var = tk.BooleanVar(value=False)
        
        self.create_widgets()
    
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        title_label = ttk.Label(main_frame, text="Twitter Scraper", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Credenciais
        ttk.Label(main_frame, text="Usuário Twitter:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.username_var, width=30).grid(row=1, column=1, pady=5)
        
        ttk.Label(main_frame, text="Senha:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.password_var, show="*", width=30).grid(row=2, column=1, pady=5)
        
        # Perfil alvo
        ttk.Label(main_frame, text="Perfil alvo:").grid(row=3, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.profile_var, width=30).grid(row=3, column=1, pady=5)
        
        # Configurações
        ttk.Label(main_frame, text="Máximo de posts:").grid(row=4, column=0, sticky=tk.W, pady=5)
        ttk.Spinbox(main_frame, from_=1, to=100, textvariable=self.max_posts_var, width=28).grid(row=4, column=1, pady=5)
        
        ttk.Label(main_frame, text="Comentários por post:").grid(row=5, column=0, sticky=tk.W, pady=5)
        ttk.Spinbox(main_frame, from_=1, to=50, textvariable=self.max_comments_var, width=28).grid(row=5, column=1, pady=5)
        
        # Opções
        ttk.Checkbutton(main_frame, text="Executar sem interface (headless)", 
                       variable=self.headless_var).grid(row=6, column=0, columnspan=2, pady=10)
        
        # Botões
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Iniciar Captura", 
                  command=self.start_scraping).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Limpar", 
                  command=self.clear_fields).pack(side=tk.LEFT, padx=5)
        
        # Área de status
        self.status_text = tk.Text(main_frame, height=8, width=60)
        self.status_text.grid(row=8, column=0, columnspan=2, pady=10)
        
        # Scrollbar para o texto
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.status_text.yview)
        scrollbar.grid(row=8, column=2, sticky="ns")
        self.status_text.configure(yscrollcommand=scrollbar.set)
        
        # Exemplos
        examples_frame = ttk.LabelFrame(main_frame, text="Exemplos de perfis", padding="5")
        examples_frame.grid(row=9, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        ttk.Button(examples_frame, text="LulaOficial", 
                  command=lambda: self.profile_var.set("LulaOficial")).pack(side=tk.LEFT, padx=2)
        ttk.Button(examples_frame, text="jairbolsonaro", 
                  command=lambda: self.profile_var.set("jairbolsonaro")).pack(side=tk.LEFT, padx=2)
        ttk.Button(examples_frame, text="jonesmanoel_PE", 
                  command=lambda: self.profile_var.set("jonesmanoel_PE")).pack(side=tk.LEFT, padx=2)
    
    def log_message(self, message):
        """Adiciona mensagem ao log"""
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)
        self.root.update()
    
    def clear_fields(self):
        """Limpa todos os campos"""
        self.username_var.set("")
        self.password_var.set("")
        self.profile_var.set("")
        self.status_text.delete(1.0, tk.END)
    
    def validate_inputs(self):
        """Valida os campos de entrada"""
        if not self.username_var.get():
            messagebox.showerror("Erro", "Digite seu usuário do Twitter")
            return False
        if not self.password_var.get():
            messagebox.showerror("Erro", "Digite sua senha")
            return False
        if not self.profile_var.get():
            messagebox.showerror("Erro", "Digite o perfil alvo")
            return False
        return True
    
    def start_scraping(self):
        """Inicia o processo de captura em thread separada"""
        if not self.validate_inputs():
            return
        
        # Desabilita o botão durante a execução
        for widget in self.root.winfo_children():
            self.disable_widget(widget)
        
        # Inicia thread
        thread = threading.Thread(target=self.run_scraper)
        thread.daemon = True
        thread.start()
    
    def disable_widget(self, widget):
        """Desabilita widgets recursivamente"""
        try:
            widget.configure(state='disabled')
        except:
            pass
        for child in widget.winfo_children():
            self.disable_widget(child)
    
    def enable_widget(self, widget):
        """Habilita widgets recursivamente"""
        try:
            widget.configure(state='normal')
        except:
            pass
        for child in widget.winfo_children():
            self.enable_widget(child)
    
    def run_scraper(self):
        """Executa o scraper"""
        try:
            self.log_message("=== INICIANDO CAPTURA ===")
            
            # Cria o scraper
            scraper = TwitterScraper(headless=self.headless_var.get())
            
            # Modifica o scraper para usar nossos parâmetros
            scraper.max_comments = self.max_comments_var.get()
            
            # Arquivo de saída
            output_file = f"comentarios_{self.profile_var.get()}.csv"
            
            self.log_message(f"Perfil: @{self.profile_var.get()}")
            self.log_message(f"Posts: {self.max_posts_var.get()}")
            self.log_message(f"Comentários por post: {self.max_comments_var.get()}")
            self.log_message(f"Arquivo: {output_file}")
            
            # Executa captura
            scraper.scrape_portal_gui(
                portal_username=self.profile_var.get(),
                username=self.username_var.get(),
                password=self.password_var.get(),
                max_posts=self.max_posts_var.get(),
                max_comments=self.max_comments_var.get(),
                output_file=output_file,
                log_callback=self.log_message
            )
            
            self.log_message(f"✅ CONCLUÍDO! Arquivo salvo: {output_file}")
            messagebox.showinfo("Sucesso", f"Captura concluída!\nArquivo: {output_file}")
            
        except Exception as e:
            self.log_message(f"❌ ERRO: {str(e)}")
            messagebox.showerror("Erro", f"Erro durante a captura:\n{str(e)}")
        finally:
            # Reabilita interface
            for widget in self.root.winfo_children():
                self.enable_widget(widget)

def main():
    root = tk.Tk()
    app = TwitterScraperGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()