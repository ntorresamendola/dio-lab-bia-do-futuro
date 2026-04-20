from pathlib import Path, PurePath
import pandas as pd
import json
from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st


########### CARREGAR DADOS ###########

 
perfil_investidor_caminho = PurePath(Path.cwd().parents[0]) / "data" / "perfil_investidor.json"
historico_atendimento_caminho = PurePath(Path.cwd().parents[0]) / "data" / "historico_atendimento.csv"
produtos_financeiros_caminho = PurePath(Path.cwd().parents[0]) / "data" / "produtos_financeiros.json"
transacoes_caminho = PurePath(Path.cwd().parents[0]) / "data" / "transacoes.csv"

with open(perfil_investidor_caminho, 'r', encoding='utf-8') as f:
    perfil = json.load(f)

with open(produtos_financeiros_caminho, 'r', encoding='utf-8') as f:
    produtos = json.load(f)

transacoes = pd.read_csv(transacoes_caminho)
historico = pd.read_csv(historico_atendimento_caminho)


########### MONTAR CONTEXTO ###########

contexto = f"""
CLIENTE: {perfil['nome']}, {perfil['idade']} anos, perfil {perfil['perfil_investidor']}
OBJETIVO: {perfil['objetivo_principal']}
PATRIMÔNIO: R$ {perfil['patrimonio_total']} | RESERVA: R$ {perfil['reserva_emergencia_atual']}

TRANSAÇÕES RECENTES:
{transacoes.to_string(index=False)}

ATENDIMENTOS ANTERIORES:
{historico.to_string(index=False)}

PRODUTOS DISPONÍVEIS:
{json.dumps(produtos, indent=2, ensure_ascii=False)}
"""

########### SYSTEM PROMPT ###########

SYSTEM_PROMPT = """
Ensinar conceitos de finanças pessoais de forma simples, usando os dados do cliente como exemplos práticos.

REGRAS:

1. Nunca recomende investimentos específicos - apenas explique como funcionam.
2. Use os dados fornecidos para dar exemplos personalizados.
3. Linguagem simples, como se explicasse para um amigo.
4. Se não souber algo, admita: "Não tenho essa informação, mas posso explicar..."
5. Sempre pergunte se o cliente entendeu.
6. Jamais responda a perguntas fora do tema de finanças pessoais. Quando ocorrer, responda lembrando o seu papel de educador financeiro.
7 - Responda de forma sucinta e direta.
"""
########### CARREGAR CHAVE DA API DO CHAT GPT E INICIAR CLIENTE ###########

load_dotenv()
client = OpenAI()

########### CHAMAR A API DO CHATGPT ###########

def perguntar(msg):
    prompt = f"""
    {SYSTEM_PROMPT}

    CONTEXTO DO CLIENTE:
    {contexto}

    Pergunta: {msg}
    """
    response = client.responses.create(
        model="gpt-5.4",
        input=prompt
    )
    
    return response.output_text

########### INTERFACE ###########

st.title("🎓 Elo, Seu Educador Financeiro")

if pergunta := st.chat_input("Sua dúvida sobre finanças..."):
    st.chat_message("user").write(pergunta)
    with st.spinner("..."):
        st.chat_message("assistant").write(perguntar(pergunta))
