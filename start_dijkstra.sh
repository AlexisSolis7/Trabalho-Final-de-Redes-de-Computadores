#!/bin/bash
# Script para iniciar o controlador Dijkstra
# Arquivo: start_dijkstra.sh

echo "🧠 Iniciando Controlador Dijkstra..."
echo "===================================="

# Ativar ambiente virtual
cd /home/oem/ryu_ambiente_final
source ryu_env/bin/activate

echo "📡 Controlador Dijkstra rodando na porta 6633"
echo "🔍 Algoritmo: Shortest Path com NetworkX"
echo "📊 Topologia: Auto-descoberta"
echo "🛑 Para parar: Ctrl+C"
echo ""

# Iniciar o controlador com verbose
ryu-manager --verbose --wsapi-port 8080 \
  --observe-links \
  simple_switch_13.py
