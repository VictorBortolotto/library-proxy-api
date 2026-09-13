# Library Proxy API

A **Library** é uma aplicação desenvolvida como **MVP (Minimum Viable Product)** para fins acadêmicos, no contexto de uma **Pós-Graduação em Engenharia de Software**.

O projeto tem como objetivo demonstrar, de forma prática, conceitos de arquitetura de software, comunicação entre APIs, autenticação, gerenciamento de empréstimos e utilização de diferentes tecnologias e padrões de desenvolvimento.

Este repositório contém a **API Proxy** da aplicação, responsável por atuar como porta de entrada para os clientes e encaminhar as requisições para a API responsável pelas regras de negócio.

A API Proxy possui como principais responsabilidades a **autenticação dos usuários**, **geração e validação de tokens JWT** e a comunicação com a API de regras de negócio utilizando **gRPC**.

> **Nota:** Este projeto possui finalidade **exclusivamente acadêmica e demonstrativa**. As funcionalidades, regras de negócio e decisões de arquitetura foram definidas para atender aos objetivos do MVP e **não representam necessariamente requisitos, regras ou necessidades de um sistema real de gerenciamento de bibliotecas**. O projeto não deve ser considerado uma solução pronta para utilização em ambiente de produção.

---

## Arquitetura

A aplicação é composta por duas APIs:

* **Library Proxy API**: porta de entrada da aplicação, responsável pela autenticação, geração e validação de tokens JWT e encaminhamento das requisições.
* **Library API**: responsável pelas regras de negócio, operações de CRUD, acesso ao banco de dados e integração com serviços externos.

A comunicação entre a **Library Proxy API** e a **Library API** é realizada utilizando **gRPC**.

A **Library API** também disponibiliza uma interface HTTP e realiza a comunicação com a API externa **ViaCEP** para consulta de informações de endereço a partir de um CEP.

```text
                         ┌──────────────────────┐
                         │       Cliente        │
                         └──────────┬───────────┘
                                    │
                                    │ HTTP
                                    ▼
                         ┌──────────────────────┐
                         │  Library Proxy API   │
                         │       :8081          │
                         │                      │
                         │ • Autenticação       │
                         │ • JWT                │
                         │ • Validação          │
                         │ • Proxy              │
                         └──────────┬───────────┘
                                    │
                                    │ gRPC
                                    ▼
              ┌─────────────────────────────────────┐
              │           Library API               │
              │                                     │
              │ HTTP: :8080                         │
              │ gRPC: :50051                        │
              │                                     │
              │ • Regras de negócio                 │
              │ • Operações CRUD                    │
              │ • Banco de dados                    │
              │ • Integrações externas              │
              └──────────────┬──────────────┬───────┘
                             │              │
                             │              │ HTTP
                             │              ▼
                             │     ┌──────────────────┐
                             │     │     ViaCEP API   │
                             │     │                  │
                             │     │ • Consulta CEP   │
                             │     │ • Dados endereço │
                             │     └──────────────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │      SQLite      │
                    │                  │
                    │ • Persistência   │
                    │ • Tabelas        │
                    └──────────────────┘
```

### Fluxo de comunicação

De forma simplificada, uma requisição realizada pelo cliente segue o seguinte fluxo:

```text
Cliente
   │
   │ HTTP
   ▼
Library Proxy API
   │
   │ gRPC
   ▼
Library API
   │
   ├──► SQLite
   │
   └──► ViaCEP API
```

---

## Funcionalidades

A API disponibiliza funcionalidades relacionadas ao gerenciamento da biblioteca.

### Usuários

* Criação de usuários
* Login
* Geração de tokens JWT
* Autenticação das requisições

### Clientes

* Cadastro de clientes
* Atualização de clientes
* Desativação de clientes

### Livros

* Cadastro de livros
* Atualização de livros
* Consulta de livros
* Exclusão de livros

### Empréstimos

* Cadastro de empréstimos de livros
* Atualização de empréstimos
* Consulta de empréstimos

---

## Tecnologias utilizadas

* **Python**
* **Flask** — desenvolvimento da API HTTP
* **PyJWT** — geração e validação de tokens JWT
* **gRPC** — comunicação entre a API Proxy e a API de regras de negócio
* **Docker** — containerização da aplicação
* **Docker Compose** — gerenciamento dos containers
* **Swagger** — documentação da API

---

# Como executar o projeto

Existem duas formas de executar o projeto:

1. Utilizando **Docker**
2. Executando diretamente no ambiente local

> Para utilizar todas as funcionalidades da aplicação, a **Library API** também deverá estar em execução, pois a comunicação entre as APIs é realizada através de gRPC.

---

# Executando com Docker

## Pré-requisitos

Antes de iniciar, certifique-se de possuir instalado:

* Docker
* Docker Compose

## 1. Clonar o repositório

```bash
git clone https://github.com/VictorBortolotto/library-proxy-api.git
```

## 2. Acessar a pasta do projeto

```bash
cd library-proxy-api
```

## 3. Acessar a pasta do Docker

```bash
cd docker
```

## 4. Construir e iniciar o container

```bash
docker compose up --build
```

Após a execução, a API Proxy estará disponível na porta **8081**.

Uma saída semelhante à seguinte deverá ser apresentada:

```text
library-proxy  | * Serving Flask app 'br.com.app.src.main.Main'
library-proxy  | * Debug mode: off
library-proxy  | WARNING: This is a development server. Do not use it in a production deployment.
library-proxy  | * Running on all addresses (0.0.0.0)
library-proxy  | * Running on http://127.0.0.1:8081
library-proxy  | * Running on http://172.19.0.2:8081
library-proxy  | Press CTRL+C to quit
```

A API poderá ser acessada através de:

```text
http://localhost:8081
```

Para interromper os containers:

```bash
docker compose down
```

---

# Executando sem Docker

Também é possível executar a aplicação diretamente no ambiente local.

## 1. Clonar o repositório

```bash
git clone https://github.com/VictorBortolotto/library-proxy-api.git
```

## 2. Acessar a pasta do projeto

```bash
cd library-proxy-api
```

## 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

## 4. Acessar a pasta principal da aplicação

```bash
cd br/com/app/src/main
```

## 5. Iniciar a aplicação

```bash
flask --app Main run -p 8081
```

Após iniciar, deverá ser apresentada uma saída semelhante a:

```text
* Serving Flask app 'Main'
* Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment.
* Running on http://127.0.0.1:8081
Press CTRL+C to quit
```

A API estará disponível em:

```text
http://localhost:8081
```

---

# Configuração da comunicação gRPC

A comunicação entre a **Library Proxy API** e a **Library API** é realizada através do **gRPC**.

A configuração do endereço do servidor gRPC depende da forma como a aplicação está sendo executada.

## Utilizando Docker

Quando as aplicações estão sendo executadas através do Docker Compose, o endereço utilizado deve ser o **nome do serviço/container definido no Docker Compose**:

```python
channel = grpc.insecure_channel("library-api:50051")
```

Nesse cenário, `library-api` é resolvido internamente pela rede do Docker Compose.

## Executando localmente

Quando a aplicação é executada diretamente no computador, sem Docker, o endereço deve apontar para o servidor local:

```python
channel = grpc.insecure_channel("localhost:50051")
```

> **Importante:** caso a Library API esteja executando localmente na porta `50051`, utilize `localhost:50051`.

---

# Integração com a ViaCEP API

A **Library API** possui uma integração com a **ViaCEP API**, utilizada para consultar informações de endereço a partir de um CEP.

A integração com o serviço externo é realizada pela **Library API**. A API Proxy não acessa diretamente a ViaCEP.

O fluxo da consulta ocorre da seguinte forma:

```text
Cliente
   │
   │ HTTP
   ▼
Library Proxy API
   │
   │ gRPC
   ▼
Library API
   │
   │ HTTP
   ▼
ViaCEP API
   │
   │ JSON
   ▼
Library API
   │
   │ gRPC
   ▼
Library Proxy API
   │
   │ HTTP
   ▼
Cliente
```

A consulta à ViaCEP utiliza o seguinte padrão de endpoint:

```text
https://viacep.com.br/ws/{cep}/json/
```

Onde `{cep}` deve ser substituído pelo CEP que deseja consultar.

Por exemplo:

```text
https://viacep.com.br/ws/88870000/json/
```

A ViaCEP retorna os dados do endereço em formato **JSON**, que são processados pela Library API.

Entre as informações disponibilizadas pelo serviço estão:

* CEP
* Logradouro
* Complemento
* Bairro
* Localidade
* UF
* Estado
* Região
* Código IBGE
* DDD
* Código SIAFI

A integração com a ViaCEP foi implementada como parte da demonstração de comunicação com um **serviço externo**, contribuindo para os objetivos acadêmicos do projeto.

> **Observação:** A disponibilidade e os dados retornados pela ViaCEP dependem do serviço externo.

---

# Regeneração dos arquivos gRPC

Os arquivos Python utilizados pelo gRPC são gerados a partir dos arquivos `.proto` localizados em:

```text
br/com/app/src/main/proto
```

Caso seja necessário regenerar os arquivos da pasta `generated`, execute os comandos abaixo a partir da raiz do projeto.

### Book Loan

```bash
python -m grpc_tools.protoc -I=br/com/app/src/main/proto --python_out=br/com/app/src/main/generated --grpc_python_out=br/com/app/src/main/generated br/com/app/src/main/proto/book_loan.proto
```

### Book

```bash
python -m grpc_tools.protoc -I=br/com/app/src/main/proto --python_out=br/com/app/src/main/generated --grpc_python_out=br/com/app/src/main/generated br/com/app/src/main/proto/book.proto
```

### Client

```bash
python -m grpc_tools.protoc -I=br/com/app/src/main/proto --python_out=br/com/app/src/main/generated --grpc_python_out=br/com/app/src/main/generated br/com/app/src/main/proto/client.proto
```

### User

```bash
python -m grpc_tools.protoc -I=br/com/app/src/main/proto --python_out=br/com/app/src/main/generated --grpc_python_out=br/com/app/src/main/generated br/com/app/src/main/proto/user.proto
```

### Zip Code

```bash
python -m grpc_tools.protoc -I=br/com/app/src/main/proto --python_out=br/com/app/src/main/generated --grpc_python_out=br/com/app/src/main/generated br/com/app/src/main/proto/zip_code.proto
```

---

# Ajuste dos imports dos arquivos gerados

Dependendo da versão do `grpc_tools` e da estrutura do projeto, pode ser necessário ajustar os imports dos arquivos `*_pb2_grpc.py` gerados.

Por exemplo, caso seja gerado:

```python
import zip_code_pb2 as zip__code__pb2
```

altere para:

```python
from generated import zip_code_pb2 as zip__code__pb2
```

Esse ajuste pode ser necessário para que os arquivos gerados encontrem corretamente os módulos dentro do pacote `generated`.

---

# Documentação da API

A aplicação possui documentação da API através do **Swagger**.

Após iniciar a aplicação, a documentação pode ser acessada pelo seguinte endereço:

```text
http://localhost:8081/apidocs/#/
```

Através do Swagger é possível visualizar os endpoints disponíveis, seus parâmetros, respostas e realizar requisições diretamente pela interface de documentação.

---

# Portas utilizadas

| Serviço           | Protocolo |   Porta |
| ----------------- | --------- | ------: |
| Library Proxy API | HTTP      |  `8081` |
| Library API       | HTTP      |  `8080` |
| Library API       | gRPC      | `50051` |

---

# Observações

* A **Library Proxy API** é a porta de entrada da aplicação.
* A autenticação e o gerenciamento dos tokens JWT são realizados no Proxy.
* As regras de negócio são executadas pela **Library API**.
* A comunicação entre as APIs utiliza **gRPC**.
* A **Library API** é responsável pela comunicação com o banco de dados.
* A **Library API** realiza a integração com a **ViaCEP API**.
* Quando executadas através do Docker Compose, as APIs podem se comunicar utilizando os nomes dos respectivos serviços.
* Quando executadas localmente, a comunicação deve utilizar `localhost`.
* Para executar as funcionalidades que dependem da API de regras de negócio, é necessário que a **Library API** esteja em execução.
* Este projeto possui finalidade acadêmica e demonstrativa e não representa necessariamente os requisitos de um sistema real de gerenciamento de bibliotecas.

---

# Autor

**Victor Augusto Campos Bortolotto**

<img style="width: 100px; height: 100px" src="https://avatars.githubusercontent.com/u/50971139?v=4" alt=""/>

[![Linkedin Badge](https://img.shields.io/badge/-LinkedIn-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/victor-augusto-campos-bortolotto/)](https://www.linkedin.com/in/victor-augusto-campos-bortolotto/) 
[![Gmail Badge](https://img.shields.io/badge/-victorcamposbortolottowork@gmail.com-c14438?style=flat-square&logo=Gmail&logoColor=white&link=mailto:victorcamposbortolottowork@gmail.com)](mailto:victorcamposbortolottowork@gmail.com)
