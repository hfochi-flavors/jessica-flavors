import streamlit as st
import google.generativeai as genai

# Tenta carregar a chave do cofre (Secrets)
try:
    CHAVE = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=CHAVE)
    # Usamos o modelo 'gemini-1.5-flash', que é o mais rápido e estável
    model = genai.GenerativeModel('gemini-1.5-flash')
    # Teste de conexão
    model.generate_content("oi")
    status_msg = "✅ Jéssica Cloud: Online"
    online = True
except Exception as e:
    status_msg = f"❌ Erro de Conexão: {e}"
    online = False

st.set_page_config(page_title="Jéssica - Flavors Flight", page_icon="🤖")
st.title("🤖 Jéssica: Inteligência de Pedidos")
st.write(f"Status: **{status_msg}**")

# Memória da Sessão
if "memoria" not in st.session_state:
    st.session_state.memoria = {}

nome = st.text_input("👤 Companhia Aérea:")
pedido = st.text_area("📋 Detalhes do Pedido:", height=150)

if st.button("🚀 Analisar Pedido"):
    if online and nome and pedido:
        with st.spinner('Analisando...'):
            hist = st.session_state.memoria.get(nome, "Primeiro contato.")
            prompt = f"Você é a Jéssica da Flavors Flight. Analise o pedido de {nome}. Histórico: {hist}. Pedido: {pedido}."
            
            try:
                response = model.generate_content(prompt)
                st.markdown("---")
                st.markdown(response.text)
                # Salva na memória
                st.session_state.memoria[nome] = response.text
                st.success("Análise concluída!")
            except Exception as e:
                st.error(f"Erro na análise: {e}")
    else:
        st.warning("Verifique os campos ou a conexão.")
