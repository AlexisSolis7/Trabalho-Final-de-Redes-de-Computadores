#!/bin/bash
# Script para iniciar diferentes topologias Mininet
# Arquivo: start_mininet.sh

echo "🌐 Configurador de Topologias Mininet"
echo "====================================="
echo ""
echo "Escolha uma topologia:"
echo "1) Simples (2 hosts, 1 switch)"
echo "2) Linear (4 hosts, 3 switches)"
echo "3) Árvore (8 hosts, 3 níveis)"
echo "4) Personalizada"
echo ""
read -p "Digite sua escolha (1-4): " choice

case $choice in
    1)
        echo "🔗 Iniciando topologia simples..."
        sudo mn --controller remote,ip=127.0.0.1,port=6633 --topo single,2
        ;;
    2)
        echo "🔗 Iniciando topologia linear..."
        sudo mn --controller remote,ip=127.0.0.1,port=6633 --topo linear,3
        ;;
    3)
        echo "🔗 Iniciando topologia em árvore..."
        sudo mn --controller remote,ip=127.0.0.1,port=6633 --topo tree,depth=2,fanout=2
        ;;
    4)
        echo "🔗 Iniciando modo interativo..."
        sudo mn --controller remote,ip=127.0.0.1,port=6633
        ;;
    *)
        echo "❌ Opção inválida!"
        exit 1
        ;;
esac
