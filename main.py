import streamlit as st
import google.generativeai as genai

# --- CONFIGURAÇÃO ---
try:
    CHAVE = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=CHAVE)
    # Usamos o caminho completo para garantir que o erro 404 suma
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    status_msg = "✅ Jéssica Cloud: Online"
    online = True
except Exception as e:
    status_msg = f"❌ Erro: {e}"
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
        with st.spinner('Jéssica analisando...'):
            hist = st.session_state.memoria.get(nome, "Primeiro contato.")
            prompt = f"Você é a Jéssica da Flavors Flight. Analise o pedido de {nome}. Histórico: {hist}. Pedido: {pedido}."
            
            try:
                # Aqui está a correção do modelo
                response = model.generate_content(prompt)
                st.markdown("---")
                st.markdown(response.text)
                st.session_state.memoria[nome] = response.text
                st.success("Análise concluída!")
            except Exception as e:
                st.error(f"Erro na análise: {e}")
    else:
        st.warning("Verifique os campos ou a conexão.")
