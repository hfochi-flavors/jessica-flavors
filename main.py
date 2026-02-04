import streamlit as st
import google.generativeai as genai
from google.api_core import exceptions

# 1. Configuração Robusta
try:
    CHAVE = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=CHAVE)
    
    # Forçamos o uso do modelo estável 1.5 Flash
    # Este modelo substitui o gemini-pro e o 3-flash-preview nas APIs estáveis
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    status_msg = "✅ Jéssica Cloud: Conectada"
    online = True
except Exception as e:
    status_msg = f"❌ Erro na Inicialização: {e}"
    online = False

st.set_page_config(page_title="Jéssica - Flavors Flight", page_icon="🤖")
st.title("🤖 Jéssica: Inteligência de Pedidos")
st.caption("Sistema Flavors Flight Catering")

st.info(status_msg)

# Memória Temporária (enquanto a aba estiver aberta)
if "memoria" not in st.session_state:
    st.session_state.memoria = {}

nome = st.text_input("👤 Companhia Aérea:")
pedido = st.text_area("📋 Detalhes do Pedido:", height=150)

if st.button("🚀 Analisar com a Jéssica"):
    if online and nome and pedido:
        with st.spinner('Acessando servidores do Google...'):
            hist = st.session_state.memoria.get(nome, "Primeiro pedido.")
            prompt = f"Você é a Jéssica da Flavors Flight. Analise o pedido de {nome}. Histórico: {hist}. Pedido: {pedido}."
            
            try:
                # Chamada direta e simplificada
                response = model.generate_content(prompt)
                
                st.markdown("---")
                st.subheader(f"💡 Resultado para {nome}")
                st.markdown(response.text)
                
                # Guarda na memória
                st.session_state.memoria[nome] = response.text
                st.success("Análise memorizada nesta sessão.")
                
            except exceptions.NotFound:
                st.error("Erro 404: O modelo não foi encontrado nesta região. Tentando alternativa...")
                # Tenta um modelo de backup caso o 1.5 Flash falhe
                model_backup = genai.GenerativeModel('gemini-1.5-flash-8b')
                response = model_backup.generate_content(prompt)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Erro técnico: {e}")
    else:
        st.warning("Preencha os dados e verifique a conexão.")
