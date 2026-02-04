import streamlit as st
import google.generativeai as genai

# Configuração da API
try:
    CHAVE = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=CHAVE)
    # Usamos o modelo 'gemini-pro', o mais estável de todos
    model = genai.GenerativeModel('gemini-pro')
    status_msg = "✅ Jéssica Cloud: Online"
    online = True
except Exception as e:
    status_msg = f"❌ Erro de Conexão: {e}"
    online = False

st.set_page_config(page_title="Jéssica - Flavors Flight", page_icon="🤖")
st.title("🤖 Jéssica: Inteligência de Pedidos")
st.caption("Flavors Flight Catering")

st.write(f"Status do Sistema: **{status_msg}**")

# Memória da Sessão (Persiste enquanto a aba estiver aberta)
if "memoria" not in st.session_state:
    st.session_state.memoria = {}

nome = st.text_input("👤 Companhia Aérea:")
pedido = st.text_area("📋 Detalhes do Pedido:", height=150)

if st.button("🚀 Analisar Pedido"):
    if online and nome and pedido:
        with st.spinner('Analisando histórico e padrões...'):
            hist = st.session_state.memoria.get(nome, "Primeiro pedido registrado.")
            
            prompt = f"""
            Você é a Jéssica da Flavors Flight Catering. 
            Analise o pedido atual da {nome} levando em conta o histórico.
            Histórico: {hist}
            Pedido Atual: {pedido}
            
            Retorne: Preferências identificadas, Alertas e 3 Perguntas para a produção.
            """
            
            try:
                response = model.generate_content(prompt)
                st.markdown("---")
                st.subheader(f"💡 Insights para {nome}")
                st.markdown(response.text)
                
                # Salva o resultado na memória para a próxima consulta
                st.session_state.memoria[nome] = response.text
                st.success("Análise concluída e memorizada!")
            except Exception as e:
                st.error(f"Erro na análise: {e}")
    else:
        st.warning("Preencha os campos ou verifique a conexão.")
