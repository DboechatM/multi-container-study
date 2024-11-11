# Use uma imagem Python base
FROM python:3.9-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto para o contêiner
COPY . /app

# Instala as dependências
RUN pip install requests beautifulsoup4 sqlite3

# Comando para rodar o script de scraping
CMD ["python", "scraper.py"]



-----


# Usa a imagem base do Python 3.11
FROM python:3.11

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências para o container
COPY requirements.txt .

# Instala as dependências listadas no requirements.txt
RUN pip install -r requirements.txt

# Copia todo o conteúdo do diretório atual para o container
COPY . .

# Cria um diretório específico para o banco de dados
RUN mkdir -p /app/data

# Exponha a porta do Streamlit (padrão é 8501)
EXPOSE 8501

# Comando para rodar a aplicação
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]
