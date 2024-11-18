import streamlit as st
import pandas as pd
import psycopg2
from dotenv import load_dotenv
import os

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Configurar conexão com o PostgreSQL
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")  # Host correto
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "airflow")
DB_USER = os.getenv("POSTGRES_USER", "airflow")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "airflow")

# Função para conectar ao banco de dados PostgreSQL
@st.cache_resource  # Cache da conexão para evitar reconectar sempre
def get_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        )
        return conn
    except Exception as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return None
    
def fetch_data_as_dataframe(query):
    conn = get_connection()
    if conn:
        try:
            return pd.read_sql_query(query, conn)
        except Exception as e:
            st.error(f"Erro ao carregar dados: {e}")
        finally:
            conn.close()
    else:
        st.error("Conexão com o banco de dados falhou.")
        return pd.DataFrame()

# Layout do aplicativo Streamlit
st.title("Streamlit com PostgreSQL")

# Consulta e exibição de dados
query = "SELECT * FROM wine_reviews LIMIT 10;"  # Exemplo de consulta
st.write("Exibindo os primeiros 10 registros da tabela `wine_reviews`:")

df = fetch_data_as_dataframe(query)

if not df.empty:
    st.dataframe(df)  # Exibe os dados em uma tabela interativa
else:
    st.warning("Nenhum dado encontrado.")
