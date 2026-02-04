import streamlit as st
from google import genai

# Configuração Segura
CHAVE_API = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=CHAVE_API, http_options={'api_version': 'v1'})

# Sistema de Memória Simples
if "memoria" not in st.session_state:
    st.session_state.memoria = {}

st.set_page_config(page_title="Jéssica - Flavors Flight")
st.title("🤖 Jéssica Cloud: Flavors Flight")
st.write("Status: ✅ Online e com Memória Ativa")

with st.expander("📚 Ver Clientes na Memória"):
    st.write(list(st.session_state.memoria.keys()))

nome = st.text_input("👤 Nome da Companhia/Cliente:")
pedido = st.text_area("📋 Detalhes do Pedido:")

if st.button("🚀 Analisar e Memorizar"):
    if nome and pedido:
        with st.spinner('Acessando inteligência...'):
            historico = st.session_state.memoria.get(nome, "Primeiro pedido.")
            
            prompt = f"Você é a Jéssica da Flavors Flight. Analise o pedido de {nome}. Histórico: {historico}. Pedido Atual: {pedido}. Liste preferências, alertas e 3 perguntas técnicas."
            
            try:
                # Usando o modelo exato que funcionou no seu Playground
                response = client.models.generate_content(model="models/gemini-3-flash-preview", contents=prompt)
                
                st.subheader("💡 Insights")
                st.markdown(response.text)
                
                # Salva na memória da sessão
                st.session_state.memoria[nome] = response.text
                st.success("Análise concluída!")
            except Exception as e:
                st.error(f"Erro técnico: {e}")
    else:
        st.warning("Preencha os campos.")
