import pandas as pd
import requests
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

# 🟢 Debug para verificar se a variável está carregada
print("🔍 Verificando variável GOOGLE_CREDENTIALS...")

# Carregar credenciais do Google Sheets do Secret do GitHub
credenciais_json = os.getenv("GOOGLE_CREDENTIALS")
if not credenciais_json:
    raise ValueError("❌ ERRO: A variável GOOGLE_CREDENTIALS não foi encontrada!")

print("✅ Variável GOOGLE_CREDENTIALS encontrada!")

# Converter o JSON string para dicionário
credenciais_dict = json.loads(credenciais_json)

# 🔹 Configurar escopo e autenticar
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credenciais = ServiceAccountCredentials.from_json_keyfile_dict(credenciais_dict, scope)
cliente = gspread.authorize(credenciais)

# 🔹 Abrir planilha no Google Sheets
spreadsheet = cliente.open_by_url("https://docs.google.com/spreadsheets/d/1aiaG9InWCYqbb7KP7QG6s7ixCSmdMWuKAdjIeimpQcg/edit")
sheet = spreadsheet.worksheet("AbaFluxo")  # Nome da aba no Google Sheets

# 🔹 Obter dados do site
url = "https://www.dadosdemercado.com.br/fluxo"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# 🔹 Converter tabela para DataFrame
tabela_html = soup.find("table")
df = pd.read_html(str(tabela_html))[0]

# 🔹 Atualizar planilha do Google Sheets
sheet.clear()
sheet.update([df.columns.values.tolist()] + df.values.tolist())

print("✅ Planilha atualizada com sucesso!")
