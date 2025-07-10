# Controlador SDN com Algoritmo Dijkstra

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Ryu](https://img.shields.io/badge/Ryu-Framework-green.svg)](https://ryu-sdn.org)
[![OpenFlow](https://img.shields.io/badge/OpenFlow-1.3-orange.svg)](https://opennetworking.org)
[![Mininet](https://img.shields.io/badge/Mininet-2.3+-red.svg)](http://mininet.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Implementação de um controlador SDN inteligente que utiliza o algoritmo Dijkstra para roteamento otimizado em redes definidas por software.**

## Visão Geral

Este projeto implementa um controlador SDN usando o framework Ryu que aplica o algoritmo Dijkstra para encontrar e instalar os caminhos mais curtos entre hosts na rede. O sistema é projetado para ambientes acadêmicos e demonstrações de conceitos SDN.

## Estrutura do Repositório

```
ryu_ambiente_final/
├── dijkstra_controller.py      # Controlador principal com Dijkstra
├── dijkstra_topologia.py       # Topologias de teste do Mininet
├── requirements.txt            # Dependências do projeto
├── setup.sh                    # Script de instalação automática
├── LICENSE                     # Licença MIT
└── README.md                   # Este arquivo
```

##  Início Rápido

### Pré-requisitos

- **Sistema Operacional**: Ubuntu 18.04+ / Debian 9+
- **Python**: 3.8 ou superior
- **Privilégios**: sudo (para Mininet)
- **RAM**: Mínimo 2GB recomendado

### Instalação Automática

```bash
git clone https://github.com/seu-usuario/ryu_ambiente_final.git
cd ryu_ambiente_final
chmod +x setup.sh
./setup.sh
```

### Instalação Manual

```bash
# 1. Instalar dependências do sistema
sudo apt update
sudo apt install python3-pip python3-dev build-essential

# 2. Criar ambiente virtual
python3 -m venv ryu_env
source ryu_env/bin/activate

# 3. Instalar dependências Python
pip install -r requirements.txt

# 4. Instalar Mininet (se necessário)
git clone https://github.com/mininet/mininet
cd mininet
sudo ./util/install.sh -nfv
```

## Como Executar

### Execução Local (Uma Máquina)

#### Terminal 1 - Controlador SDN
```bash
cd ryu_ambiente_final
source ryu_env/bin/activate
ryu-manager dijkstra_controller.py --verbose
```

#### Terminal 2 - Topologia Mininet
```bash
cd ryu_ambiente_final
sudo python3 dijkstra_topologia.py
```

### Execução Distribuída (Duas Máquinas)

#### Máquina 1 (Controlador)
```bash
# Descobrir IP da máquina
ip addr show | grep "inet " | grep -v 127.0.0.1

# Executar controlador
source ryu_env/bin/activate
ryu-manager dijkstra_controller.py --verbose
```

#### Máquina 2 (Mininet)
```bash
# Editar dijkstra_topologia.py
# Alterar: controller_ip = "127.0.0.1"  
# Para:    controller_ip = "IP_DA_MAQUINA_1"

sudo python3 dijkstra_topologia.py
```

> **⚠️ Importante**: Configurar firewall para permitir porta 6653 (OpenFlow)

## Testando a Rede

### Testes Básicos de Conectividade

```bash
# No prompt do Mininet
mininet> pingall                    # Teste completo de conectividade
mininet> h1 ping -c 4 h2           # Ping específico entre hosts
mininet> iperf h1 h2               # Teste de performance
```

### Visualização e Debugging

```bash
# Visualizar topologia descoberta
mininet> net

# Verificar flows instalados
mininet> dpctl dump-flows

# Ver portas dos switches
mininet> dpctl show

# Logs detalhados do controlador
tail -f /tmp/ryu.log
```

## Como Funciona

### Fluxo do Algoritmo

1. **Descoberta de Topologia**
   - Detecta switches e hosts automaticamente
   - Mapeia links e suas capacidades
   - Constrói grafo da rede em tempo real

2. **Cálculo de Rotas**
   - Aplica algoritmo Dijkstra usando NetworkX
   - Considera peso dos links (latência/banda)
   - Encontra caminho ótimo entre origem e destino

3. **Instalação de Flows**
   - Instala regras OpenFlow nos switches do caminho
   - Configura match fields e actions
   - Otimiza tabelas de flows para performance

4. **Roteamento Adaptativo**
   - Monitora mudanças na topologia
   - Recalcula rotas quando necessário
   - Garante alta disponibilidade da rede

### Características Técnicas

- **Alto Desempenho**: Cálculos otimizados com NetworkX
- **Confiável**: Tratamento de erros e reconexão automática
- **Escalável**: Suporta topologias complexas
- **Flexível**: Fácil personalização de métricas

## Topologias Disponíveis

### Topologia Complexa (Padrão)

```
    h1 ---- s1 ---- s2 ---- h2
            |        |
            s3 ---- s4
            |        |
           h3       s5
```

- **5 switches**, **3 hosts**
- **Múltiplos caminhos** entre h1-h2
- **Redundância** para alta disponibilidade
- **Teste ideal** para demonstrar Dijkstra

### Topologia Linear

```
h1 ---- s1 ---- s2 ---- s3 ---- h2
```

- **3 switches**, **2 hosts**
- **Caminho único** (mais simples)
- **Ideal para testes básicos**

## Desenvolvimento e Contribuição

### Estrutura do Código

```python
# dijkstra_controller.py - Componentes principais:
class DijkstraController(app_manager.RyuApp):
    ├── topology_discovery()    # Descobre topologia
    ├── calculate_shortest_path() # Algoritmo Dijkstra  
    ├── install_flows()         # Instala regras OpenFlow
    └── packet_in_handler()     # Processa pacotes novos
```

### Executando Testes

```bash
# Testes unitários
python -m pytest tests/ -v

# Teste de integração
./scripts/integration_test.sh

# Benchmark de performance  
python tests/benchmark_dijkstra.py
```

### Debug e Logs

```bash
# Logs detalhados
export RYU_LOG_LEVEL=DEBUG
ryu-manager dijkstra_controller.py

# Monitoramento em tempo real
watch -n 1 "sudo ovs-ofctl dump-flows s1"
```

## Equipe de Desenvolvimento

| Membro | Papel | Contato |
|-----------|----------|------------|
| **[Alexis Solis]** | Desenvolvedor Principal | seu.email@universidade.edu |
| **[Nome 2]** | Testes e Validação | email2@universidade.edu |
| **[Nome 3]** | Documentação | email3@universidade.edu |

## Agradecimentos

- **Ryu Framework** - Fundação SDN robusta
- **NetworkX** - Biblioteca de algoritmos de grafos
- **Mininet** - Ambiente de simulação de redes
- **Universidade [Nome]** - Suporte acadêmico

---

<div align="center">

**⭐ Se este projeto foi útil, deixe uma estrela!**

[![GitHub stars](https://img.shields.io/github/stars/seu-usuario/ryu_ambiente_final.svg?style=social&label=Star)](https://github.com/seu-usuario/ryu_ambiente_final)

</div>
