import streamlit as st
from google import genai

# --- CONFIGURAÇÃO ---
# A chave já está segura nos 'Secrets' do Streamlit
CHAVE_API = st.secrets["GEMINI_API_KEY"]

try:
    client = genai.Client(api_key=CHAVE_API, http_options={'api_version': 'v1'})
    # Testamos a conexão com o modelo estável
    client.models.generate_content(model="gemini-1.5-flash", contents="oi")
    online = True
except:
    online = False

# --- MEMÓRIA DA SESSÃO ---
if "memoria" not in st.session_state:
    st.session_state.memoria = {}

# --- INTERFACE ---
st.set_page_config(page_title="Jéssica - Flavors Flight", page_icon="🤖")
st.title("🤖 Jéssica Cloud: Flavors Flight")
st.write(f"Status: {'✅ Online' if online else '❌ Erro de Chave'}")

with st.expander("📚 Clientes Memorizados"):
    st.write(list(st.session_state.memoria.keys()))

nome = st.text_input("👤 Nome da Companhia/Cliente:")
pedido = st.text_area("📋 Detalhes do Pedido:")

if st.button("🚀 Analisar e Memorizar"):
    if nome and pedido:
        with st.spinner('Jéssica está processando...'):
            # Buscamos o que já sabemos sobre esse cliente
            historico = st.session_state.memoria.get(nome, "Primeiro pedido.")
            
            prompt = f"Você é a Jéssica da Flavors Flight Catering. Analise o pedido de {nome}. Histórico: {historico}. Pedido Atual: {pedido}. Liste preferências, alertas e 3 perguntas técnicas."
            
            try:
                # TENTATIVA AUTOMÁTICA: Testamos os dois modelos principais
                try:
                    response = client.models.generate_content(model="gemini-1.5-flash", contents=prompt)
                except:
                    response = client.models.generate_content(model="gemini-3-flash-preview", contents=prompt)
                
                st.subheader("💡 Insights da Jéssica")
                st.markdown(response.text)
                
                # Salvamos na memória para a próxima vez
                st.session_state.memoria[nome] = response.text
                st.success("Análise salva com sucesso!")
                
            except Exception as e:
                st.error(f"Erro técnico: {e}")
    else:
        st.warning("Preencha todos os campos.")
