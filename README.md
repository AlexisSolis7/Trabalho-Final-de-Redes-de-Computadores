# Controlador SDN com Algoritmo de Dijkstra

Um controlador SDN (Software-Defined Networking) implementado com Ryu que utiliza o algoritmo de Dijkstra para calcular rotas ótimas entre hosts na rede.

## 🎯 Funcionalidades

- **Roteamento Ótimo**: Usa algoritmo de Dijkstra para encontrar o caminho mais curto
- **Auto-descoberta**: Detecta automaticamente a topologia da rede
- **Instalação Proativa**: Instala flows preemptivamente em todos os switches
- **Logs Detalhados**: Sistema completo de logging para debug e análise
- **Testes Automatizados**: Scripts prontos para validar o funcionamento

## 🔧 Arquitetura

```
Mininet Topology ←→ OpenFlow ←→ Ryu Controller
                                      ↓
                               Dijkstra Algorithm
                                      ↓
                               Flow Installation
```

## 📦 Requisitos do Sistema

- **Sistema Operacional**: Linux (testado no Ubuntu 20.04+)
- **Python**: 3.8 ou superior
- **Privilégios**: sudo (para Mininet)

## 🚀 Instalação Rápida

### 1. Clonar o Repositório
```bash
git clone https://github.com/AlexisSolis7/Trabalho-Final-de-Redes-de-Computadores.git
cd Trabalho-Final-de-Redes-de-Computadores
```

### 2. Instalar Dependências
```bash
# Atualizar sistema
sudo apt update

# Instalar Python e dependências básicas
sudo apt install -y python3 python3-pip python3-venv

# Instalar Mininet e Open vSwitch
sudo apt install -y mininet openvswitch-switch

# Criar ambiente virtual
python3 -m venv ryu_env
source ryu_env/bin/activate

# Instalar Ryu e dependências
pip install --upgrade pip
pip install setuptools==66.1.1  # Versão compatível
pip install eventlet==0.33.3    # Versão compatível
pip install ryu networkx
```

### 3. Tornar Scripts Executáveis
```bash
chmod +x *.sh
```

## 🎮 Como Usar

### Execução em 2 Terminais

**Terminal 1 - Controlador:**
```bash
./start_controller.sh
```

**Terminal 2 - Teste:**
```bash
./run_test.sh
```

### Ou Teste Rápido
```bash
./quick_test.sh
```

## 📁 Estrutura do Projeto

```
├── dijkstra_controller.py    # Controlador principal com Dijkstra
├── dijkstra_test.py         # Script de teste com topologias
├── start_controller.sh      # Inicia o controlador
├── run_test.sh             # Executa testes completos
├── quick_test.sh           # Teste rápido e simples
├── outros_arquivos/        # Arquivos auxiliares e versões antigas
└── README.md              # Esta documentação
```

## 🧪 Testes Disponíveis

### 1. Topologia em Árvore
```
     h1     h2
      |     |
     s1 --- s2 --- s3
            |      |
           h3     h4
```

### 2. Topologia Linear
```
h1 - s1 - s2 - s3 - h2
```

## 🔍 Como Funciona o Algoritmo

1. **Descoberta da Topologia**: O controlador escuta eventos do OpenFlow para mapear switches e links
2. **Construção do Grafo**: Cria um grafo da rede usando NetworkX
3. **Cálculo de Rotas**: Para cada par de hosts, calcula o caminho mais curto com Dijkstra
4. **Instalação de Flows**: Instala flows proativamente em todos os switches do caminho

## 📊 Logs e Debug

O controlador gera logs detalhados mostrando:
- Descoberta de switches e links
- Cálculo de caminhos ótimos
- Instalação de flow entries
- Estatísticas de rede

## 🐛 Solução de Problemas

### Erro: "Address already in use"
```bash
sudo fuser -k 6633/tcp
```

### Erro: "Module not found"
```bash
source ryu_env/bin/activate
pip install ryu networkx
```

### Mininet não funciona
```bash
sudo mn -c  # Limpar configurações antigas
```

## 🤝 Contribuições

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📜 Licença

Este projeto é open source e está disponível sob a licença MIT.

## 👥 Autores

- **Alexis Solis** - *Desenvolvimento inicial* - [GitHub](https://github.com/AlexisSolis7)

## 🔗 Links Úteis

- [Documentação do Ryu](https://ryu.readthedocs.io/)
- [Mininet](http://mininet.org/)
- [OpenFlow](https://opennetworking.org/sdn-definition/)
- [Algoritmo de Dijkstra](https://pt.wikipedia.org/wiki/Algoritmo_de_Dijkstra)