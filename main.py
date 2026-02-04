import streamlit as st
from google import genai

# A Jéssica vai ler a chave de um cofre seguro na nuvem
CHAVE_API = st.secrets["GEMINI_API_KEY"]

try:
    client = genai.Client(api_key=CHAVE_API, http_options={'api_version': 'v1'})
    status = "✅ Online"
except:
    status = "❌ Erro de Conexão"

st.title("🤖 Jéssica Cloud: Flavors Flight")
st.write(f"Status: {status}")

nome = st.text_input("👤 Cliente:")
pedido = st.text_area("📋 Detalhes do Pedido:")

if st.button("🚀 Analisar Pedido"):
    if nome and pedido:
        with st.spinner('Jéssica pensando...'):
            response = client.models.generate_content(model="gemini-1.5-flash", contents=pedido)
            st.subheader("💡 Insights")
            st.markdown(response.text)
    else:
        st.warning("Preencha os campos.")
