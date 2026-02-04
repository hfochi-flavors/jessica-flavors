import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURAÇÃO (PUXA DO COFRE SECRETS) ---
try:
    CHAVE = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=CHAVE)
    # Usamos o modelo estável que raramente dá erro 404
    model = genai.GenerativeModel('gemini-1.5-flash')
    status_msg = "✅ Jéssica Cloud: Online"
    online = True
except Exception as e:
    status_msg = f"❌ Erro de Conexão: {e}"
    online = False

# --- 2. INTERFACE ---
st.set_page_config(page_title="Jéssica - Flavors Flight", page_icon="🤖")
st.title("🤖 Jéssica: Inteligência de Pedidos")
st.caption("Flavors Flight Catering - Sistema de Apoio")

st.write(f"Status do Sistema: **{status_msg}**")

# Memória da Sessão (Persiste enquanto você não fechar a aba)
if "memoria" not in st.session_state:
    st.session_state.memoria = {}

nome = st.text_input("👤 Companhia Aérea (Ex: Azul, Latam):")
pedido = st.text_area("📋 Detalhes do Pedido Atual:", height=150)

if st.button("🚀 Analisar e Memorizar"):
    if online and nome and pedido:
        with st.spinner('Jéssica está processando a análise...'):
            # Busca histórico na memória da sessão
            hist = st.session_state.memoria.get(nome, "Este é o primeiro pedido registrado para este cliente.")
            
            prompt = f"""
            Você é a Jéssica, assistente de IA da Flavors Flight Catering. 
            Analise o pedido da {nome}.
            
            HISTÓRICO RECENTE: {hist}
            PEDIDO ATUAL: {pedido}
            
            Por favor, forneça:
            1. Resumo rápido do pedido.
            2. Preferências identificadas (ex: tipos de proteína, embalagens).
            3. Alertas (se algo parece fora do padrão ou falta informação).
            4. 3 Perguntas para o time de produção validar.
            """
            
            try:
                # Chamada estável
                response = model.generate_content(prompt)
                
                st.markdown("---")
                st.subheader(f"💡 Insights para {nome}")
                st.markdown(response.text)
                
                # Salva a análise na memória para a próxima vez que você digitar o mesmo nome
                st.session_state.memoria[nome] = response.text
                st.success("Análise concluída e memorizada!")
                
            except Exception as e:
                st.error(f"Erro na análise: {e}. Tente novamente em instantes.")
    else:
        st.warning("Certifique-se de que o sistema está Online e os campos preenchidos.")
