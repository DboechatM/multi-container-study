# Streamlit Application with Docker
Este projeto utiliza Streamlit para criar uma aplicação web simples que pode ser executada dentro de um container Docker. 
A aplicação é configurada para se conectar a uma base de dados PostgreSQL utilizando a biblioteca `psycopg2` e pode fazer requisições HTTP com a biblioteca `requests`.

## Estrutura do Projeto
`app/`
`app.py:` Arquivo principal da aplicação Streamlit. Ele contém o código da aplicação.
`Dockerfile:` Arquivo Docker que configura o ambiente para a aplicação Streamlit.

## Pré-requisitos
Docker instalado.

## Dockerfile
O Dockerfile realiza as seguintes operações:
**Imagem Base:** Utiliza python:3.9-slim como imagem base para ter um ambiente leve de Python.
Instalação de Dependências do Sistema: Instala pacotes essenciais como curl, git, e build-essential, que são necessários para instalar as dependências do Python.
**Instalação de Dependências do Python:** Instala pacotes Python necessários para o aplicativo (streamlit, psycopg2-binary, requests) usando pip.
Configuração do Diretório de Trabalho: Define o diretório /app como o diretório de trabalho para o aplicativo.
**Cópia dos Arquivos:** Copia todos os arquivos da pasta local para o diretório /app no container.
Exposição da Porta 8501: Expõe a porta 8501, que é a porta padrão do Streamlit.
**Comando de Healthcheck:** Adiciona um healthcheck para verificar se o Streamlit está rodando corretamente.
**Comando de Entrada (ENTRYPOINT):** Configura o Streamlit para rodar app.py no servidor.

## Como Rodar a Aplicação
**1.Clonar o Repositório**

Clone este repositório para o seu ambiente local:

```bash
git clone https://github.com/DboechatM/multi-container-study
cd seurepositorio
```

**2.Construir a Imagem Docker**

Construa a imagem Docker utilizando o comando abaixo:

```bash
docker-compose up --build
```

**3.Execute o container a partir da imagem que foi criada:**

```bash
streamlit run app.py
```
**4.Acessar a Aplicação**
Acesse a aplicação Streamlit no navegador através do endereço http://localhost:8501.

## Personalizando app.py
O arquivo app.py deve estar na pasta `streamlit/` e contém o código da aplicação Streamlit. Ele pode ser configurado para fazer consultas ao banco de dados PostgreSQL, ou outras funcionalidades, conforme necessário.