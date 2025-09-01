import pandas as pd 
import os

df = pd.read_csv('comentarios_mauro_davi6.csv')
df = df.drop_duplicates(subset=['comentario'])
df = pd.drop_columns(['posturl'])

df.to_csv('comentarios_mauro_davi6_limpo.csv', index=False)
pasta_destino = "/home/aquila/unifor/comentarios_tratados"
os.mkdir(pasta_destino, exist_ok=True)

caminho_arquivo = os.path.join(pasta_destino, "comentarios_mauro_davi6_limpo.csv")
df.to_csv(caminho_arquivo, index=False, encoding="utf-8-sig")
print(f"Arquivo salvo em: {caminho_arquivo}")