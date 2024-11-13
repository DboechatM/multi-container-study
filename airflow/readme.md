# Documentação do Airflow com Docker

Este projeto configura uma instância do Airflow usando Docker, com serviços de `airflow-init`, `airflow-webserver`, e `scheduler`, além de um banco de dados PostgreSQL para persistência dos dados do Airflow.

## Estrutura do Projeto

O projeto segue a seguinte estrutura de diretórios:

```plaintext
airflow
├── dags/                       # Diretório para armazenar DAGs
├── export/                     # Diretório para exportação de dados
├── init/                       # Arquivos de inicialização do banco de dados
│   └── create_airflow_db.sql   # Script SQL para criação do banco de dados
├── logs/                       # Diretório para logs do Airflow
│   └── dag_processor_manager/  # Logs específicos do processamento das DAGs
├── scheduler/                  # Diretório do scheduler do Airflow
└── plugins/                    # Diretório para plugins customizados
```

Arquivos Importantes
`dockerfile`: Definição de como o ambiente do Airflow será configurado.
`create_airflow_db.sql`: Script SQL para configurar o banco de dados do Airflow no PostgreSQL.

## Serviços no Docker Compose
Os seguintes serviços foram configurados no `docker-compose.yml`:

`airflow-init`: Serviço inicial para configurar o banco de dados do Airflow.
`airflow-webserver`: Serviço principal que disponibiliza a interface web do Airflow.
`scheduler`: Serviço que realiza o agendamento e execução das DAGs.

## Rede
Foi configurada uma rede chamada airflow_net para permitir a comunicação entre os serviços.

## Portas
As portas configuradas para o projeto incluem:

`8501`: Porta para o serviço do Streamlit, caso necessário.
`8080`: Porta para acesso à interface do Airflow.

## Configuração e Execução
**1. Clonar o Repositório**
Para clonar o repositório, use o comando:

```bash
git clone https://github.com/seuusuario/seurepositorio.git
```

**2. Entre no diretório do projeto:**
```bash
cd seurepositorio
```
**3. Construir e Inicializar o Ambiente**
Para construir os containers e inicializar o ambiente do Airflow, use o comando:
```bash
docker-compose up --build
```
**Esse comando irá:**
- Construir os containers de cada serviço, incluindo o airflow-init.
- Executar o serviço de airflow-webserver para acessar o Airflow via interface web.
- Executar o serviço scheduler para gerenciar as DAGs.


**4. Configurar o Banco de Dados**
Para configurar o banco de dados PostgreSQL para o Airflow, você pode usar o script create_airflow_db.sql localizado na pasta init/. Esse script deve ser executado durante a inicialização do serviço airflow-init.

**5. Acessar a Interface Web do Airflow**
Após inicializar o ambiente, a interface web do Airflow estará disponível em:

http://localhost:8080

Utilize o usuário e senha configurados no docker-compose.yml para acessar.