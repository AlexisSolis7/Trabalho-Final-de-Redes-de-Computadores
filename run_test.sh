#!/bin/bash
# Script wrapper para executar teste Dijkstra com sudo
# Arquivo: run_test.sh

echo "🧪 Executando Teste do Controlador Dijkstra"
echo "============================================"
echo ""
echo "⚠️  Este script precisa de privilégios sudo para o Mininet"
echo ""

# Verificar se o controlador está rodando
if ! nc -z 127.0.0.1 6633 2>/dev/null; then
    echo "❌ ERRO: Controlador Ryu não está rodando na porta 6633"
    echo ""
    echo "🚀 Para iniciar o controlador, execute em outro terminal:"
    echo "   ./start_controller.sh"
    echo ""
    exit 1
fi

echo "✅ Controlador detectado na porta 6633"
echo ""

# Executar teste com sudo
echo "🔐 Executando teste com sudo..."
sudo python3 dijkstra_test.py
