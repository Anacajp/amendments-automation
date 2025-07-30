#!/bin/bash

# Script para rodar a aplicação no container
echo "Iniciando automação de emendas..."

# Verificar se as variáveis de ambiente estão definidas
if [ -z "$GOOGLE_SHEET_ID" ]; then
    echo "GOOGLE_SHEET_ID não definido"
    exit 1
fi

# Executar o script principal
python src/main.py

echo "Automação concluída!"