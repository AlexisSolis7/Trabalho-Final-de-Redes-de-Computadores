#!/bin/bash
# Script para testes automatizados
# Arquivo: run_tests.sh

echo "🧪 Suite de Testes SDN"
echo "====================="

# Função para limpar ambiente
cleanup() {
    echo "🧹 Limpando ambiente..."
    sudo mn -c > /dev/null 2>&1
    sudo killall ryu-manager > /dev/null 2>&1
    sleep 2
}

# Função para testar conectividade básica
test_connectivity() {
    echo "📡 Teste 1: Conectividade Básica"
    echo "--------------------------------"
    
    # Iniciar controlador em background
    cd /home/oem/ryu_ambiente_final
    source ryu_env/bin/activate
    ryu-manager simple_switch_13.py &
    RYU_PID=$!
    
    sleep 3
    
    # Executar teste de conectividade
    echo "🔗 Testando topologia simples..."
    timeout 30 sudo mn --controller remote,ip=127.0.0.1 --test pingall
    
    # Parar controlador
    kill $RYU_PID 2>/dev/null
    sleep 2
}

# Função para testar aprendizado MAC
test_mac_learning() {
    echo ""
    echo "🧠 Teste 2: Aprendizado MAC"
    echo "---------------------------"
    echo "✅ Verificar logs do controlador para evidência de aprendizado"
    echo "✅ Observar redução de floods após aprendizado inicial"
}

# Função para coletar estatísticas
collect_stats() {
    echo ""
    echo "📊 Teste 3: Coleta de Estatísticas"
    echo "----------------------------------"
    echo "📈 Dados serão salvos em logs/"
    mkdir -p logs
    echo "$(date): Teste executado" >> logs/test_history.log
}

# Executar testes
echo "🚀 Iniciando bateria de testes..."
echo ""

cleanup
test_connectivity
test_mac_learning
collect_stats

cleanup

echo ""
echo "✅ Testes concluídos!"
echo "📄 Verificar logs em: logs/"
echo "📊 Próximo passo: Análise de performance"
