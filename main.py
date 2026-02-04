import streamlit as st
from google import genai

# Configuração de Segurança
try:
    CHAVE = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=CHAVE, http_options={'api_version': 'v1'})
    # Testamos o modelo mais estável disponível
    client.models.generate_content(model="gemini-1.5-flash-8b", contents="oi")
    status_msg = "✅ Jéssica Online e Pronta"
    online = True
except Exception as e:
    status_msg = f"❌ Aguardando Conexão: {e}"
    online = False

st.set_page_config(page_title="Jéssica - Flavors Flight", page_icon="🤖")
st.title("🤖 Jéssica: Inteligência de Pedidos")
st.caption("Flavors Flight Catering")

st.write(f"Status: **{status_msg}**")

# Memória da Sessão
if "memoria" not in st.session_state:
    st.session_state.memoria = {}

with st.sidebar:
    st.subheader("📚 Histórico")
    if st.button("Limpar Memória"):
        st.session_state.memoria = {}
        st.rerun()

nome = st.text_input("👤 Companhia Aérea:")
pedido = st.text_area("📋 Detalhes do Pedido:", height=150)

if st.button("🚀 Analisar Pedido"):
    if online and nome and pedido:
        with st.spinner('Analisando preferências...'):
            hist = st.session_state.memoria.get(nome, "Primeiro pedido.")
            prompt = f"Você é a Jéssica da Flavors Flight. Analise o pedido de {nome}. Histórico: {hist}. Pedido: {pedido}. Liste preferências, alertas e 3 perguntas."
            
            try:
                # Usando o modelo 8b, que é o 'coringa' para evitar erros 404
                response = client.models.generate_content(model="gemini-1.5-flash-8b", contents=prompt)
                st.markdown("---")
                st.subheader(f"💡 Insights para {nome}")
                st.markdown(response.text)
                st.session_state.memoria[nome] = response.text
            except Exception as e:
                st.error(f"Erro na nuvem: {e}")
    else:
        st.warning("Preencha os campos e verifique o status Online.")
