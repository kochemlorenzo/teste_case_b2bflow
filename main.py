import os
import requests
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

supabase = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_ANON_KEY"))

ZAPI_URL = f"https://api.z-api.io/instances/{os.environ.get('ZAPI_INSTANCE_ID')}/token/{os.environ.get('ZAPI_TOKEN')}/send-text"
ZAPI_HEADERS = {
    "Client-Token": os.environ.get("ZAPI_CLIENT_TOKEN"),
    "Content-Type": "application/json",
}

contatos = (
    supabase.table("cadastro").select("*").eq("enviado", False).limit(3).execute().data
)
 
if not contatos:
    print("Nenhum contato pendente de envio.")
 
for contato in contatos:
    mensagem = f"Olá, {contato['nome']} tudo bem com você?"
    payload = {"phone": contato["telefone"], "message": mensagem}
 
    try:
        resp = requests.post(ZAPI_URL, json=payload, headers=ZAPI_HEADERS, timeout=10)
        resp.raise_for_status()
        print(f"Enviado para {contato['nome']} ({contato['telefone']})")
        supabase.table("cadastro").update({"enviado": True}).eq("id", contato["id"]).execute()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao enviar para {contato['nome']}: {e}")
