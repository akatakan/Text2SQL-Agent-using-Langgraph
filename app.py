import streamlit as st
from src.core.models import AgentState
from src.analysis.graph import create_graph
from src.core.config import Config
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

if 'query_result' not in st.session_state:
    st.session_state.query_result = None
if 'chart_type' not in st.session_state:
    st.session_state.chart_type = "Bar"


st.set_page_config(
    page_title="SQL Sorgulama Asistanı",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 SQL Sorgulama Asistanı")
st.markdown("""
Bu uygulama, doğal dil ile yazılan sorguları SQL'e çevirir ve veritabanında çalıştırır.
Sorgunuzu yazın ve sonuçları görüntüleyin.
""")


with st.sidebar:
    st.header("⚙️ Ayarlar")

    st.text_input("Veritabanı URL", value=Config.DATABASE_URL)
    
    provider = st.selectbox(
        "LLM Sağlayıcı",
        ["Ollama", "OpenAI"],
        index=0 if Config.USE_OLLAMA else 1
    )
    
    if provider == "OpenAI":
        Config.USE_OPENAI = True
        Config.USE_OLLAMA = False
        model = st.text_input("OpenAI Model", value="gpt-3.5-turbo")
        api_key = st.text_input("OpenAI API Key", type="password")
    else:
        Config.USE_OLLAMA = True
        Config.USE_OPENAI = False
        model = st.text_input("Ollama Model", value=Config.LLM_MODEL)
        base_url = st.text_input("Ollama Base URL", value=Config.OLLAMA_BASE_URL)
     
    temperature = st.slider(
        "Sıcaklık",
        min_value=0.0,
        max_value=1.0,
        value=float(Config.LLM_TEMPERATURE),
        step=0.1
    )


query = st.text_area(
    "Sorgunuzu yazın:",
    placeholder="Örnek: Show me the total number of employees for each level",
    height=100
)

if st.button("🚀 Sorguyu Çalıştır", type="primary"):
    if not query:
        st.error("Lütfen bir sorgu yazın!")
    else:
        with st.spinner("Sorgu işleniyor..."):
            try:
                
                initial_state = AgentState(
                    user_query=query,
                    attempts=0,
                    correct_attempts=0,
                )
                graph = create_graph()
                final_state = graph.invoke(initial_state)
                
                
                st.session_state.query_result = final_state
                
                
                st.success("Sorgu başarıyla çalıştırıldı!")
                
               
                with st.expander("🤔 Mantıksal Adımlar"):
                    st.markdown(final_state["sql_reasoning"])
                
                
                with st.expander("📝 Oluşturulan SQL Sorgusu"):
                    st.code(final_state["generated_sql"], language="sql")
                
            except Exception as e:
                st.error(f"Bir hata oluştu: {str(e)}")
                st.session_state.query_result = None

if st.session_state.query_result:
    final_state = st.session_state.query_result
    
    st.header("📊 Sonuçlar")
    if final_state["execution_result"].success:
        df = pd.DataFrame(final_state["execution_result"].data)
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )
        
        
        if not df.empty and len(df.columns) == 2:
            col1, col2 = st.columns([1, 3])
            with col1:
                st.session_state.chart_type = st.selectbox(
                    "Grafik türü seçin:",
                    ["Bar", "Line", "Scatter"],
                    index=["Bar", "Line", "Scatter"].index(st.session_state.chart_type)
                )
            
            with col2:
                if st.session_state.chart_type == "Bar":
                    st.bar_chart(df, x=df.columns[0],y=df.columns[1],use_container_width=True)
                elif st.session_state.chart_type == "Line":
                    st.line_chart(df, x=df.columns[0],y=df.columns[1],use_container_width=True)
                else:
                    st.scatter_chart(df, x=df.columns[0],y=df.columns[1], use_container_width=True)

    else:
        st.error(f"Sorgu hatası: {final_state['execution_result'].error}")
    
    
    if final_state["report_summary"]:
        with st.expander("📝 Özet"):
            st.markdown(final_state["report_summary"])


with st.expander("❓ Nasıl Kullanılır?"):
    st.markdown("""
    1. Yan panelden LLM sağlayıcı ve model seçin
    2. Sorgunuzu doğal dil ile yazın
    3. 'Sorguyu Çalıştır' butonuna tıklayın
    4. Sonuçları ve grafikleri inceleyin
    
    **Örnek Sorgular:**
    - Show me the total number of employees for each level
    - What is the average salary by department?
    - Show me the highest paid employees in each department
    """) 