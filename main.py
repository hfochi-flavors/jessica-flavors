import streamlit as st
from google import genai

# Forçamos a leitura direta do segredo
try:
    CHAVE = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=CHAVE, http_options={'api_version': 'v1'})
    # Teste de conexão direta
    client.models.generate_content(model="gemini-1.5-flash", contents="oi")
    status_msg = "✅ Jéssica Cloud Online"
    online = True
except Exception as e:
    status_msg = f"❌ Erro: {e}"
    online = False

st.set_page_config(page_title="Jéssica - Flavors Flight")
st.title("🤖 Jéssica: Inteligência de Pedidos")
st.subheader("Flavors Flight Catering")

st.write(f"Status do Sistema: **{status_msg}**")

# Memória da Sessão (Dura enquanto a aba estiver aberta)
if "memoria" not in st.session_state:
    st.session_state.memoria = {}

nome = st.text_input("👤 Nome da Companhia:")
pedido = st.text_area("📋 Detalhes do Pedido:", height=150)

if st.button("🚀 Analisar Pedido"):
    if online and nome and pedido:
        with st.spinner('Jéssica analisando padrões...'):
            hist = st.session_state.memoria.get(nome, "Primeiro contato.")
            prompt = f"Você é a Jéssica da Flavors Flight. Analise o pedido de {nome}. Histórico: {hist}. Pedido: {pedido}."
            
            try:
                # Tentamos o modelo estável
                response = client.models.generate_content(model="gemini-1.5-flash", contents=prompt)
                st.markdown("---")
                st.markdown(response.text)
                st.session_state.memoria[nome] = response.text
                st.success("Análise memorizada!")
            except:
                # Fallback para o modelo que funcionou no seu Playground
                response = client.models.generate_content(model="gemini-3-flash-preview", contents=prompt)
                st.markdown("---")
                st.markdown(response.text)
                st.session_state.memoria[nome] = response.text
    else:
        st.error("Verifique a conexão ou preencha os campos.")
