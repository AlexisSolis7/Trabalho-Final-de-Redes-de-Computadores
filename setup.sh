#!/bin/bash

# 🚀 Script de Instalação Automática - Controlador SDN Dijkstra
# Autor: Equipe de Desenvolvimento
# Versão: 1.0

set -e  # Parar script em caso de erro

echo "🌐 === INSTALAÇÃO DO CONTROLADOR SDN DIJKSTRA === 🌐"
echo ""

# Verificar se está rodando como usuário normal (não root)
if [[ $EUID -eq 0 ]]; then
   echo "❌ Este script não deve ser executado como root"
   echo "💡 Execute como usuário normal: ./setup.sh"
   exit 1
fi

# Verificar distribuição Linux
if ! command -v apt &> /dev/null; then
    echo "❌ Este script requer Ubuntu/Debian (comando apt)"
    exit 1
fi

echo "📋 Verificando pré-requisitos..."

# Verificar Python 3.8+
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if ! python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)"; then
    echo "❌ Python 3.8+ é necessário. Versão atual: $python_version"
    exit 1
fi

echo "✅ Python $python_version encontrado"

# Atualizar sistema
echo "🔄 Atualizando sistema..."
sudo apt update

# Instalar dependências do sistema
echo "📦 Instalando dependências do sistema..."
sudo apt install -y \
    python3-pip \
    python3-dev \
    python3-venv \
    build-essential \
    git \
    curl \
    wget

# Verificar se Mininet já está instalado
if ! command -v mn &> /dev/null; then
    echo "🌐 Instalando Mininet..."
    sudo apt install -y mininet
    
    # Verificar instalação do Open vSwitch
    if ! command -v ovs-vsctl &> /dev/null; then
        echo "🔌 Instalando Open vSwitch..."
        sudo apt install -y openvswitch-switch
    fi
else
    echo "✅ Mininet já instalado"
fi

# Criar ambiente virtual se não existir
if [ ! -d "ryu_env" ]; then
    echo "🐍 Criando ambiente virtual Python..."
    python3 -m venv ryu_env
else
    echo "✅ Ambiente virtual já existe"
fi

# Ativar ambiente virtual
echo "⚡ Ativando ambiente virtual..."
source ryu_env/bin/activate

# Atualizar pip
echo "📈 Atualizando pip..."
pip install --upgrade pip

# Instalar dependências Python
echo "📚 Instalando dependências Python..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "❌ Arquivo requirements.txt não encontrado!"
    exit 1
fi

# Verificar instalação do Ryu
echo "🧪 Testando instalação do Ryu..."
if python -c "import ryu" 2>/dev/null; then
    echo "✅ Ryu instalado com sucesso"
else
    echo "❌ Erro na instalação do Ryu"
    exit 1
fi

# Verificar instalação do NetworkX
echo "🕸️ Testando NetworkX..."
if python -c "import networkx" 2>/dev/null; then
    echo "✅ NetworkX instalado com sucesso"
else
    echo "❌ Erro na instalação do NetworkX"
    exit 1
fi

# Criar diretórios necessários
echo "📁 Criando estrutura de diretórios..."
mkdir -p logs tests/results

# Configurar permissões para Mininet
echo "🔐 Configurando permissões..."
sudo usermod -a -G sudo $USER

# Testar conectividade básica do Mininet
echo "🧪 Testando Mininet..."
sudo mn --test pingall --topo single,2 > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Mininet funcionando corretamente"
else
    echo "⚠️ Aviso: Teste do Mininet falhou (pode funcionar mesmo assim)"
fi

echo ""
echo "🎉 === INSTALAÇÃO CONCLUÍDA COM SUCESSO! === 🎉"
echo ""
echo "🚀 Para executar o projeto:"
echo "   1. source ryu_env/bin/activate"
echo "   2. ryu-manager dijkstra_controller.py"
echo "   3. Em outro terminal: sudo python3 dijkstra_topologia.py"
echo ""
echo "📖 Para mais informações: cat README.md"
echo "🆘 Problemas? Verifique os logs em: logs/"
echo ""
echo "✨ Boa sorte com seu projeto SDN! ✨"
