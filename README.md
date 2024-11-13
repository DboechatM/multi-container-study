# Documentação do projeto multi-container-study

## Configuração Docker-Compose para Airflow e Streamlit

Este projeto utiliza Docker Compose para configurar um ambiente de execução que inclui o Apache Airflow, PostgreSQL para persistência de dados e uma aplicação Streamlit para visualização. Abaixo está a documentação dos serviços, redes, volumes e outros aspectos do `docker-compose.yml`.

### Estrutura Geral dos Serviços

```plaintext
.
├── docker-compose.yml       # Arquivo de configuração Docker Compose
├── airflow                  # Pasta com arquivos do Airflow (Dockerfile, configurações, DAGs, etc.)
│   ├── dags                 # DAGs do Airflow
│   ├── logs                 # Logs do Airflow
│   ├── plugins              # Plugins do Airflow
├── streamlit                # Pasta com o código da aplicação Streamlit
│   ├── app                  # Aplicação Streamlit (ex. app.py)
│   └── Dockerfile           # Dockerfile para o Streamlit
└── init                     # Scripts de inicialização para o PostgreSQL
```

#### Serviços Configurados

- **postgres**: Banco de dados PostgreSQL para persistência dos dados do Airflow.
- **airflow-init**: Serviço inicializador para configurar o banco de dados do Airflow.
- **airflow-webserver**: Serviço que executa a interface web do Airflow.
- **airflow-scheduler**: Serviço responsável por agendar e gerenciar as DAGs do Airflow.
- **streamlit**: Aplicação para visualização de dados utilizando Streamlit.

#### Rede

- **airflow_net**: Rede Docker customizada para comunicação entre os serviços do projeto.

#### Volumes

- **postgres_data**: Volume para armazenar dados persistentes do PostgreSQL.

---

### Configuração dos Serviços

#### 1. Serviço `postgres`

- **Imagem**: `postgres:16.4`
- **Propósito**: Prover um banco de dados PostgreSQL para o Airflow.
- **Variáveis de Ambiente**:
  - `POSTGRES_USER`: Usuário do banco de dados (`airflow`).
  - `POSTGRES_PASSWORD`: Senha do banco de dados (`airflow`).
  - `POSTGRES_DB`: Nome do banco de dados (`airflow_db`).
- **Volumes**:
  - `postgres_data:/var/lib/postgresql/data`: Armazena dados persistentes.
  - `./init:/docker-entrypoint-initdb.d`: Executa scripts de inicialização do banco.
- **Rede**: `airflow_net`
- **Portas**: Mapeia a porta `5432` do container para `5432` do host.
- **Configuração de Log**:
  - `max-size: 10m`
  - `max-file: 3` (Para evitar crescimento descontrolado de logs)

#### 2. Serviço `airflow-init`

- **Imagem**: `apache/airflow:2.10.3`
- **Propósito**: Inicializar o banco de dados do Airflow.
- **Dependências**: Inicia após o `postgres`.
- **Variáveis de Ambiente**:
  - `AIRFLOW__CORE__SQL_ALCHEMY_CONN`: String de conexão com o PostgreSQL.
  - `AIRFLOW__CORE__EXECUTOR`: Define o executor como `LocalExecutor`.
  - `AIRFLOW__WEBSERVER__EXPOSE_CONFIG`: Exibe a configuração no webserver.
- **Comando**: `airflow db init`
- **Rede**: `airflow_net`

#### 3. Serviço `airflow-webserver`

- **Imagem**: `apache/airflow:2.10.3`
- **Propósito**: Executar a interface web do Airflow.
- **Build Context**: `./airflow` (Caso tenha um Dockerfile customizado).
- **Dependências**: Depende do `airflow-init`.
- **Variáveis de Ambiente**:
  - `AIRFLOW__CORE__SQL_ALCHEMY_CONN`: String de conexão com o PostgreSQL.
- **Portas**: Mapeia a porta `8080` do container para `8080` do host.
- **Volumes**:
  - `./dags:/opt/airflow/dags`
  - `./logs:/opt/airflow/logs`
  - `./plugins:/opt/airflow/plugins`
  - `./export:/usr/local/airflow/export` (Para exportação de relatórios)
- **Rede**: `airflow_net`
- **Configuração de Log**:
  - `max-size: 10m`
  - `max-file: 3`
- **Healthcheck**:
  - Verifica se o arquivo `airflow-webserver.pid` existe, indicando que o webserver está em execução.
  - Intervalo: 30s, Timeout: 30s, Retries: 3

#### 4. Serviço `airflow-scheduler`

- **Imagem**: `apache/airflow:2.10.3`
- **Propósito**: Agendar e gerenciar a execução das DAGs do Airflow.
- **Dependências**: Depende de `airflow-init` e `postgres`.
- **Variáveis de Ambiente**:
  - `AIRFLOW__CORE__SQL_ALCHEMY_CONN`: String de conexão com o PostgreSQL.
- **Comando**: `airflow scheduler`
- **Volumes**:
  - `./dags:/opt/airflow/dags`
  - `./logs:/opt/airflow/logs`
  - `./plugins:/opt/airflow/plugins`
- **Rede**: `airflow_net`
- **Configuração de Log**:
  - `max-size: 10m`
  - `max-file: 3`

#### 5. Serviço `streamlit`

- **Build Context**: `./streamlit` (diretório onde está o código do Streamlit)
- **Propósito**: Executar uma aplicação Streamlit para visualização de dados.
- **Variáveis de Ambiente**:
  - `POSTGRES_USER=airflow`
  - `POSTGRES_PASSWORD=airflow`
  - `POSTGRES_DB=airflow_db`
- **Volumes**:
  - `./streamlit:/app` (Código da aplicação Streamlit)
- **Portas**: Mapeia a porta `8501` do container para `8501` do host.
- **Dependências**: Depende do `postgres`.
- **Rede**: `airflow_net`
- **Comando**: `streamlit run app/app.py`

---

### Configuração da Rede

- **Nome da Rede**: `airflow_net`
  - Propósito: Facilita a comunicação entre os serviços Airflow, PostgreSQL e Streamlit.

### Configuração dos Volumes

- **postgres_data**: Volume persistente para os dados do PostgreSQL.

---
##  Construir as Imagens
```bash
docker-compose up --build
```

```JavaScript
 ✔ Network multi-container-study_airflow_net     Created         0.0s 
 ✔ Volume multi-container-study_postgres_data    Created         0.0s 
 ✔ Container multi-container-study-postgres-1    Created         0.1s 
 ✔ Container multi-container-study-streamlit-1   Created         0.1s 
 ✔ Container multi-container-study-airflow-1     Created         0.1s
```

## Acessar Aplicação

`http://localhost:8501/`
`http://localhost:8080/`

 ## Verificar o Status dos Serviços
 ```bash
 docker-compose ps
```
### Parar os Serviços
Quando terminar de usar a aplicação, você pode parar todos os containers sem removê-los com o comando:

```bash
docker-compose stop
```
Se você deseja parar e remover todos os containers, volumes e redes criados pelo Docker Compose, execute:

```bash
docker-compose down -v
```
A flag `-v` remove também os volumes associados aos containers.