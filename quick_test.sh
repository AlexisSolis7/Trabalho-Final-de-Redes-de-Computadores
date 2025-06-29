#!/bin/bash
# Teste simples do controlador Dijkstra usando comandos Mininet diretos
# Arquivo: simple_dijkstra_test.sh

echo "🧠 Teste Simples do Controlador Dijkstra"
echo "========================================"

# Verificar se o controlador está rodando
if ! nc -z 127.0.0.1 6633 2>/dev/null; then
    echo "❌ ERRO: Controlador não está rodando!"
    echo "🚀 Execute primeiro: ./start_controller.sh"
    exit 1
fi

echo "✅ Controlador detectado"
echo ""

echo "🔧 Escolha o teste:"
echo "1) Topologia Simples (2 hosts, 1 switch)"
echo "2) Topologia Linear (4 hosts, 3 switches)"  
echo "3) Topologia Árvore (6 hosts, 5 switches)"
echo ""
read -p "Digite sua escolha (1-3): " choice

case $choice in
    1)
        echo "🔗 Executando topologia simples..."
        echo "💡 Comandos úteis no Mininet:"
        echo "   pingall    - Testa conectividade"
        echo "   h1 ping h2 - Ping específico"
        echo "   exit       - Sair"
        echo ""
        sudo mn --controller remote,ip=127.0.0.1,port=6633 --topo single,2
        ;;
    2)
        echo "🔗 Executando topologia linear..."
        echo "💡 Teste: h1 ping h4 (passará por 3 switches)"
        echo ""
        sudo mn --controller remote,ip=127.0.0.1,port=6633 --topo linear,4
        ;;
    3)
        echo "🔗 Executando topologia árvore..."
        echo "💡 Teste: Vários caminhos possíveis para Dijkstra"
        echo ""
        sudo mn --controller remote,ip=127.0.0.1,port=6633 --topo tree,depth=2,fanout=3
        ;;
    *)
        echo "❌ Opção inválida!"
        exit 1
        ;;
esac

echo ""
echo "🧹 Limpando ambiente..."
sudo mn -c

echo "✅ Teste concluído!"
