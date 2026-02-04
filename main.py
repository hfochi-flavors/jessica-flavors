import streamlit as st
from google import genai
import json
import os

# --- CONFIGURAÇÃO ---
CHAVE_API = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=CHAVE_API, http_options={'api_version': 'v1'})

# --- SISTEMA DE MEMÓRIA (Dicionário de Preferências) ---
# Na nuvem, usaremos o st.session_state para manter a memória durante o uso
if "memoria_flavors" not in st.session_state:
    st.session_state.memoria_flavors = {}

def carregar_contexto(cliente):
    return st.session_state.memoria_flavors.get(cliente, "Primeiro pedido deste cliente.")

def salvar_contexto(cliente, insights):
    st.session_state.memoria_flavors[cliente] = insights

# --- INTERFACE ---
st.set_page_config(page_title="Jéssica - Flavors Flight", page_icon="🤖")
st.title("🤖 Jéssica Cloud: Inteligência de Pedidos")
st.write("Status: ✅ Online e com Memória Ativa")

with st.expander("📚 Ver Clientes na Memória"):
    st.write(list(st.session_state.memoria_flavors.keys()))

nome_cliente = st.text_input("👤 Nome da Companhia/Cliente:", placeholder="Ex: Latam Airlines")
detalhes_pedido = st.text_area("📋 Detalhes do Pedido:", height=150)

if st.button("🚀 Analisar e Memorizar"):
    if nome_cliente and detalhes_pedido:
        with st.spinner('Acessando histórico e analisando...'):
            contexto_antigo = carregar_contexto(nome_cliente)
            
            prompt = f"""
            Você é a Jéssica, IA da Flavors Flight Catering.
            Analise o pedido para: {nome_cliente}
            
            O que já sabemos sobre eles: {contexto_antigo}
            
            Novo Pedido: {detalhes_pedido}
            
            Responda em português:
            1. RESUMO: O que foi pedido agora?
            2. PREFERÊNCIAS: Identifique padrões ou exigências recorrentes.
            3. ALERTAS: Se houver mudança brusca no padrão, avise.
            4. PERGUNTAS: 3 perguntas técnicas para o time de produção.
            """
            
            try:
                response = client.models.generate_content(model="gemini-1.5-flash", contents=prompt)
                
                # Exibição
                st.markdown("---")
                st.subheader(f"💡 Insights para {nome_cliente}")
                st.markdown(response.text)
                
                # Salva os novos insights na memória para a próxima consulta
                salvar_contexto(nome_cliente, response.text)
                st.success(f"A memória de {nome_cliente} foi atualizada!")
                
            except Exception as e:
                st.error(f"Erro na análise: {e}")
    else:
        st.warning("Preencha o nome do cliente e o pedido.")
