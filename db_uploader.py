#!/usr/bin/env python3
"""
Script para enviar dados CSV limpos para PostgreSQL
"""
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import os
from datetime import datetime

class PostgreSQLUploader:
    def __init__(self, host='localhost', port=5432, database='twitter_data', 
                 username='postgres', password='password'):
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password
        self.engine = None
    
    def connect(self):
        """Conecta ao PostgreSQL"""
        try:
            connection_string = f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
            self.engine = create_engine(connection_string)
            print("✅ Conectado ao PostgreSQL")
            return True
        except Exception as e:
            print(f"❌ Erro na conexão: {e}")
            return False
    
    def create_table(self):
        """Cria tabela se não existir"""
        try:
            with self.engine.connect() as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS twitter_comments (
                        id SERIAL PRIMARY KEY,
                        post_url TEXT,
                        post_content TEXT,
                        comment TEXT,
                        profile_username VARCHAR(100),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                conn.commit()
            print("✅ Tabela criada/verificada")
            return True
        except Exception as e:
            print(f"❌ Erro ao criar tabela: {e}")
            return False
    
    def upload_csv(self, csv_file, table_name='twitter_comments'):
        """Envia CSV para PostgreSQL"""
        try:
            # Ler CSV
            df = pd.read_csv(csv_file, encoding='utf-8')
            print(f"📊 Lendo {len(df)} registros do CSV")
            
            # Extrair username do arquivo se não existir coluna
            if 'profile_username' not in df.columns:
                filename = os.path.basename(csv_file)
                username = filename.replace('comentarios_', '').replace('_limpo.csv', '')
                df['profile_username'] = username
            
            # Enviar para PostgreSQL
            df.to_sql(table_name, self.engine, if_exists='append', index=False)
            print(f"✅ {len(df)} registros enviados para {table_name}")
            return True
            
        except Exception as e:
            print(f"❌ Erro no upload: {e}")
            return False
    
    def get_stats(self, table_name='twitter_comments'):
        """Mostra estatísticas da tabela"""
        try:
            with self.engine.connect() as conn:
                # Total de registros
                result = conn.execute(f"SELECT COUNT(*) FROM {table_name}")
                total = result.fetchone()[0]
                
                # Por perfil
                result = conn.execute(f"""
                    SELECT profile_username, COUNT(*) as count 
                    FROM {table_name} 
                    GROUP BY profile_username 
                    ORDER BY count DESC
                """)
                profiles = result.fetchall()
                
                print(f"\n📈 Estatísticas da tabela {table_name}:")
                print(f"Total de registros: {total}")
                print("\nPor perfil:")
                for profile, count in profiles:
                    print(f"  {profile}: {count} registros")
                    
        except Exception as e:
            print(f"❌ Erro ao obter estatísticas: {e}")

def main():
    """Função principal"""
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python db_uploader.py <arquivo_csv> [host] [database] [username] [password]")
        print("Exemplo: python db_uploader.py comentarios_lula_limpo.csv")
        return
    
    csv_file = sys.argv[1]
    
    # Parâmetros opcionais
    host = sys.argv[2] if len(sys.argv) > 2 else 'localhost'
    database = sys.argv[3] if len(sys.argv) > 3 else 'twitter_data'
    username = sys.argv[4] if len(sys.argv) > 4 else 'postgres'
    password = sys.argv[5] if len(sys.argv) > 5 else 'password'
    
    if not os.path.exists(csv_file):
        print(f"❌ Arquivo não encontrado: {csv_file}")
        return
    
    # Executar upload
    uploader = PostgreSQLUploader(host, 5432, database, username, password)
    
    print("🔄 Iniciando upload para PostgreSQL...")
    
    if not uploader.connect():
        return
    
    if not uploader.create_table():
        return
    
    if uploader.upload_csv(csv_file):
        uploader.get_stats()
        print("\n✅ Upload concluído com sucesso!")
    else:
        print("\n❌ Falha no upload")

if __name__ == "__main__":
    main()