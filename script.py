import os
import json
import pandas as pd
import requests
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 🟢 Criar o arquivo JSON com as credenciais corretamente formatadas
CREDENTIALS_PATH = "credentials.json"

if not os.path.exists(CREDENTIALS_PATH):
    credentials_json = os.getenv("GOOGLE_SHEETS_CREDENTIALS")

    if credentials_json:
        try:
            # 🔍 Teste: Exibir os primeiros 500 caracteres do JSON recebido
            print("🔍 JSON Recebido do GitHub Secrets:")
            print(credentials_json[:500])  

            # Converter JSON corretamente
            credentials_data = json.loads(credentials_json.strip())

            # Substituir `\\n` por `\n` para corrigir a private_key
            if "private_key" in credentials_data:
                credentials_data["private_key"] = credentials_data["private_key"].replace("\\n", "\n")

            # Salvar credenciais corrigidas no arquivo
            with open(CREDENTIALS_PATH, "w", encoding="utf-8") as f:
                json.dump(credentials_data, f, indent=4)

            print("✅ Credenciais JSON foram salvas corretamente!")
        except json.JSONDecodeError as e:
            print(f"❌ ERRO AO DECODIFICAR JSON: {e}")
            exit(1)

# 🟢 Configuração da API do Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credenciais = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_PATH, scope)
cliente = gspread.authorize(credenciais)

# 🟢 Abrir a planilha no Google Sheets (substitua pelo seu link)
spreadsheet = cliente.open_by_url("https://docs.google.com/spreadsheets/d/1aiaG9InWCYqbb7KP7QG6s7ixCSmdMWuKAdjIeimpQcg/edit?gid=0#gid=0")
sheet = spreadsheet.worksheet("AbaFluxo")  # 🔹 Certifique-se de que esse é o nome correto da aba

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
