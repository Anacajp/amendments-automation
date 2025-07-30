# Automação de Emendas Parlamentares

Este projeto automatiza o processo de download, atualização e integração de planilhas de emendas parlamentares, facilitando a gestão e atualização de dados em Google Sheets de forma eficiente e rastreável.

## Funcionalidades
- Download automático de arquivos de emendas de fontes especificadas
- Atualização de planilhas Google Sheets com os dados baixados
- Exposição de endpoints HTTP para health check e execução da automação
- Estrutura pronta para execução em container Docker e integração com Google Cloud Run
- Logging detalhado para rastreabilidade

## Estrutura do Projeto
```
├── config/                # Configurações e credenciais
├── download/              # Planilhas baixadas
├── src/                   # Código-fonte principal
│   ├── downloader.py      # Módulo de download
│   ├── updater.py         # Módulo de atualização de planilhas
│   ├── main.py            # Orquestrador da automação
│   └── server.py          # Servidor Flask
├── requirements.txt       # Dependências do projeto
├── Dockerfile             # Containerização
├── entrypoint.sh          # Script de entrada para o container
├── cloudbuild.yaml        # Configuração para Google Cloud Build
└── README.md              # Documentação
```

## Como Usar

### 1. Pré-requisitos
- Python 3.12+
- Docker (opcional, para execução em container)
- Credenciais do Google (coloque o arquivo `google_credentials.json` em `config/`)

### 2. Instalação
```bash
pip install -r requirements.txt
```

### 3. Execução Local
```bash
python src/main.py
```

### 4. Executando via Docker
```bash
docker build -t amendments-automation .
docker run --env-file .env.example -v $(pwd)/config:/app/config amendments-automation
```

### 5. Endpoints HTTP
- `GET /health` — Verifica se o serviço está online
- `POST /run` — Executa o processo de automação

## Variáveis de Ambiente
Configure as variáveis necessárias no arquivo `.env.example` e renomeie para `.env` conforme necessário.

## Contribuição
Pull requests são bem-vindos! Para grandes mudanças, abra uma issue primeiro para discutir o que você gostaria de modificar.

---

> Desenvolvido por Ana Carolina Pacheco.
