# AWS Weather Data Pipeline

Este projeto é um **pipeline de dados na AWS** que coleta informações climáticas da [Open-Meteo API](https://open-meteo.com/), processa e enriquece os dados em diferentes camadas, armazenando-os de forma estruturada no **Amazon S3**.  

O objetivo é construir um **data lake em camadas (raw, processed, enriched)**, aplicando boas práticas de engenharia de dados com Python, Polars e Wrangler, além de integrar modelo de IA para enriquecimento de dados.

---

## 🛠️ Arquitetura do Projeto

O pipeline consiste nas seguintes camadas:  

1. **Raw**
   - Coleta os dados da API Open-Meteo via `requests`.  
   - Armazena em JSON no S3, particionando por **data de extração**.  

2. **Processed**
   - Converte os arquivos JSON em DataFrames com **Polars**.  
   - Separa um único dataset em **três tabelas distintas**.  
   - Salva em formato **Parquet**, particionado por **ano/mês/dia**.  

3. **Enriched**
   - Analisa uma das tabelas processadas.  
   - Utiliza o modelo do DeepSeek via **OpenRouter** para gerar descrições textuais do clima (ex: "Dia quente com alta umidade").  
   - Armazena novamente em Parquet, particionado por **ano/mês/dia** e **estado**.  

---

## 📂 Estrutura de Pastas

```bash
├── .gitignore
├── README.md
├── requirements-test.txt
├── requirements.txt
├── src
│   ├── common
│   │   ├── configs
│   │   │   └── env_vars.py         # Variáveis de ambiente
│   │   ├── local.env               # Template de configuração local
│   │   └── services
│   │       ├── api.py              # Conexão com APIs externas
│   │       └── s3.py               # Funções utilitárias para S3
│   ├── enrichment
│   │   ├── etl
│   │   │   ├── extract.py          # Extração de dados da camada processed
│   │   │   ├── load.py             # Carregamento para enriched
│   │   │   └── transform.py        # Enriquecimento com IA
│   │   ├── job.py
│   │   └── lambda_function.py
│   ├── ingestion
│   │   ├── data
│   │   │   └── states_mapping.py   # Mapeamento de lat/long das capitais brasileiras
│   │   ├── job.py
│   │   └── lambda_function.py
│   └── processing
│       ├── etl
│       │   ├── extract.py          # Extração da camada raw
│       │   ├── load.py             # Carregamento para processed
│       │   └── transform.py        # Explode JSON e aplica schema
│       ├── schema
│       │   └── column_mapping.py   # Tipagem e normalização de colunas
│       ├── job.py
│       └── lambda_function.py
└── test
    └── __init__.py                 # Testes unitários

```
---

## 💻 Tecnologias Utilizadas

- **Linguagem**: Python (versão 3.10)
- **Bibliotecas principais**:  
  - [Polars](https://pola-rs.github.io/polars/) → manipulação de DataFrames  
  - [AWS Wrangler](https://github.com/awslabs/aws-data-wrangler) → integração com S3
  - [Requests](https://docs.python-requests.org/) → coleta de dados da API  
  - [OpenRouter](https://openrouter.ai/) → enriquecimento de dados com modelos de IA  

---

## ✅ Próximos Passos

- [ ] Criar **Infraestrutura como Código (IaC)** com Terraform.  
- [ ] Adicionar **testes unitários** em `test/`.  
