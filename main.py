import streamlit as st
import google.generativeai as genai

# Tenta ler a nova chave
try:
    CHAVE = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=CHAVE)
    # Usamos o modelo mais básico e aceito universalmente
    model = genai.GenerativeModel('gemini-1.5-flash')
    status_msg = "✅ Jéssica Online"
    online = True
except Exception as e:
    status_msg = f"❌ Erro: {e}"
    online = False

st.title("🤖 Jéssica Cloud: Flavors Flight")
st.write(f"Status: {status_msg}")

nome = st.text_input("👤 Companhia Aérea:")
pedido = st.text_area("📋 Detalhes do Pedido:")

if st.button("🚀 Analisar"):
    if online and nome and pedido:
        with st.spinner('Processando...'):
            try:
                # Se o 1.5 der erro, o sistema tentará o 1.0 automaticamente
                response = model.generate_content(pedido)
                st.markdown(response.text)
            except:
                model_alt = genai.GenerativeModel('gemini-pro')
                response = model_alt.generate_content(pedido)
                st.markdown(response.text)
    else:
        st.warning("Verifique os campos.")
