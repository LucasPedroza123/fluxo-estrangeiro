import os
import json

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

            # Substituir `\\n` por `\n` na private_key
            if "private_key" in credentials_data:
                credentials_data["private_key"] = credentials_data["private_key"].replace("\\n", "\n")

            # Salvar credenciais corrigidas no arquivo
            with open(CREDENTIALS_PATH, "w", encoding="utf-8") as f:
                json.dump(credentials_data, f, indent=4)

            print("✅ Credenciais JSON foram salvas corretamente!")
        except json.JSONDecodeError as e:
            print(f"❌ ERRO AO DECODIFICAR JSON: {e}")
            exit(1)
