#!/bin/bash
# Script para iniciar o controlador Ryu
# Arquivo: start_ryu.sh

echo "🚀 Iniciando Controlador Ryu..."
echo "================================"

# Ativar ambiente virtual
cd /home/oem/ryu_ambiente_final
source ryu_env/bin/activate

echo "📡 Controlador rodando na porta 6633"
echo "📊 Interface web disponível em http://localhost:8080"
echo "🛑 Para parar: Ctrl+C"
echo ""

# Iniciar o controlador com verbose e interface web
ryu-manager --verbose --wsapi-port 8080 simple_switch_13.py
