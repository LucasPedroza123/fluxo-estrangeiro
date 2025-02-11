import pandas as pd
import requests
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import os

# 🟢 Criar o arquivo JSON com credenciais a partir do Secret (caso esteja rodando no GitHub Actions)
CREDENTIALS_PATH = "credentials.json"

if not os.path.exists(CREDENTIALS_PATH):
    with open(CREDENTIALS_PATH, "w") as cred_file:
        cred_file.write(os.getenv("GOOGLE_SHEETS_CREDENTIALS", ""))

# 🟢 Configuração da API do Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credenciais = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_PATH, scope)
cliente = gspread.authorize(credenciais)

# 🟢 Abrir a planilha no Google Sheets
spreadsheet = cliente.open_by_url("https://docs.google.com/spreadsheets/d/1aiaG9InWCYqbb7KP7QG6s7ixCSmdMWuKAdjIeimpQcg/edit?gid=0#gid=0")
sheet = spreadsheet.worksheet("AbaFluxo")  # Nome da aba no Google Sheets

# 🟢 URL do site para obter os dados
url = "https://www.dadosdemercado.com.br/fluxo"

# 🟢 Fazer a requisição HTTP para obter o HTML da página
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# 🟢 Encontrar a tabela de fluxo de mercado no site
tabela_html = soup.find("table")

# 🟢 Converter a tabela para um DataFrame do Pandas
import io
df = pd.read_html(io.StringIO(str(tabela_html)))[0]

# 🟢 Atualizar a planilha no Google Sheets
sheet.clear()  # Limpa os dados antigos
sheet.update([df.columns.values.tolist()] + df.values.tolist())  # Adiciona os novos dados

print("✅ Planilha do Google Sheets atualizada com sucesso!")
