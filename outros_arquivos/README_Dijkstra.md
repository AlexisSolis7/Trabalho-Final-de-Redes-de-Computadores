# 🧠 Controlador SDN com Algoritmo de Dijkstra

## 📋 Visão Geral

Este controlador implementa o **algoritmo de Dijkstra** para encontrar os caminhos mais curtos entre switches em uma rede SDN, substituindo o simples aprendizado MAC por roteamento otimizado.

## 🎯 Características

### ✅ **Funcionalidades Principais:**
- **Dijkstra Shortest Path**: Caminhos ótimos entre qualquer par de switches
- **Auto-descoberta de Topologia**: Detecta switches e links automaticamente
- **Roteamento Proativo**: Instala flows ao longo do caminho completo
- **Logs Detalhados**: Visualização completa do processo de roteamento

### 📊 **Algoritmo Implementado:**

#### **1. Descoberta de Topologia:**
```python
# Detecta switches conectados
@set_ev_cls(event.EventSwitchEnter)
def switch_enter_handler(self, ev)

# Detecta links entre switches  
@set_ev_cls(event.EventLinkAdd)
def link_add_handler(self, ev)
```

#### **2. Estrutura de Dados:**
```python
self.topology_graph = nx.Graph()    # Grafo da rede
self.switches = {}                  # {dpid: switch_object}
self.hosts = {}                     # {mac: (dpid, port)}
self.links = {}                     # {(src_dpid, dst_dpid): (src_port, dst_port)}
```

#### **3. Algoritmo de Dijkstra:**
```python
def dijkstra_shortest_path(self, src_dpid, dst_dpid):
    # Usa NetworkX para calcular caminho mais curto
    path = nx.shortest_path(self.topology_graph, src_dpid, dst_dpid, weight='weight')
    return path
```

#### **4. Instalação de Flows:**
```python
def install_path(self, path, src_mac, dst_mac, first_port, last_port):
    # Instala flow entry em cada switch do caminho
    for i in range(len(path)):
        # Determina porta de saída para próximo hop
        # Instala regra: match(dst_mac) -> action(forward_port)
```

## 🚀 **Como Usar**

### **Passo 1: Iniciar Controlador**
```bash
cd /home/oem/ryu_ambiente_final
./start_dijkstra.sh
```

### **Passo 2: Executar Testes**
```bash
# Em outro terminal
python3 test_dijkstra.py
```

### **Passo 3: Mininet Manual**
```bash
# Topologia personalizada
sudo mn --controller remote,ip=127.0.0.1 --topo tree,depth=2,fanout=3
```

## 📈 **Comparação: Simple vs Dijkstra**

| Aspecto | Simple Learning | Dijkstra |
|---------|----------------|----------|
| **Algoritmo** | Backward Learning | Shortest Path |
| **Roteamento** | Por switch local | End-to-end otimizado |
| **Caminhos** | Primeiro disponível | Mais curto (menor hops) |
| **Convergência** | Flood inicial | Descoberta de topologia |
| **Complexidade** | O(1) | O(V log V + E) |
| **Memória** | Tabela MAC local | Grafo global |
| **Otimalidade** | Não garantida | Caminho ótimo garantido |

## 🧪 **Cenários de Teste**

### **Topologia 1: Árvore**
```
     h1     h2
      |     |
     s1 --- s2 --- s3
            |      |
           h3     h4
```

**Teste:** `h1 ping h4`
- **Simple**: h1→s1→s2→(flood)→s3→h4
- **Dijkstra**: h1→s1→s2→s3→h4 (caminho direto calculado)

### **Topologia 2: Linear**
```
h1 - s1 - s2 - s3 - h2
```

**Teste:** `h1 ping h2`
- **Simple**: Aprende hop-by-hop
- **Dijkstra**: Calcula s1→s2→s3 e instala flows completos

### **Topologia 3: Mesh**
```
    s1 ---- s2
   / |      | \
  /  |      |  \
s4 --|------|- s3
```

**Teste:** Múltiplos caminhos possíveis
- **Dijkstra**: Sempre escolhe o menor número de hops

## 📊 **Logs e Debugging**

### **Logs do Controlador:**
```
📦 PacketIn: Switch=1, MAC src=00:00:00:00:00:01, dst=00:00:00:00:00:04, porta=1
🎯 Calculando caminho: 00:00:00:00:00:01 (switch 1) -> 00:00:00:00:00:04 (switch 3)
🛤️ Dijkstra: Caminho 1 -> 3: [1, 2, 3]
📥 Flow instalado: Switch=1, dst=00:00:00:00:00:04 -> porta=2
📥 Flow instalado: Switch=2, dst=00:00:00:00:00:04 -> porta=3  
📥 Flow instalado: Switch=3, dst=00:00:00:00:00:04 -> porta=2
📤 Encaminhando pacote para porta 2
```

### **Comandos de Debug:**
```bash
# Ver flows instalados
sudo ovs-ofctl dump-flows s1
sudo ovs-ofctl dump-flows s2

# Ver topologia descoberta  
# (nos logs do controlador)

# Estatísticas de latência
h1 ping -c 10 h2
```

## 🎯 **Melhorias Implementadas**

### **1. Descoberta Automática:**
- Não precisa configurar topologia manualmente
- Adapta-se a mudanças de topologia em tempo real

### **2. Roteamento Otimizado:**
- Sempre usa o caminho com menor número de hops
- Reduz latência end-to-end

### **3. Flows Proativos:**
- Instala regras em todos os switches do caminho
- Reduz carga no controlador para pacotes subsequentes

### **4. Logs Detalhados:**
- Rastreamento completo do processo de decisão
- Fácil debug e análise de performance

## 🔧 **Parâmetros Configuráveis**

### **Pesos dos Links:**
```python
# Atualmente: peso = 1 para todos os links
self.topology_graph.add_edge(src_dpid, dst_dpid, weight=1)

# Pode ser modificado para:
# - Largura de banda: weight = 1/bandwidth
# - Latência: weight = latency_ms  
# - Utilização: weight = current_load
```

### **Timeouts dos Flows:**
```python
# Flows permanentes (padrão)
timeout = 0

# Flows temporários (para economizar memória)
timeout = 30  # segundos
```

## 📚 **Próximos Passos**

### **Semana 2 - Implementação Básica:**
- ✅ Algoritmo de Dijkstra funcionando
- ✅ Descoberta automática de topologia
- ✅ Roteamento end-to-end
- ✅ Testes de conectividade

### **Semana 3 - Personalização:**
- 🔲 Pesos dinâmicos baseados em largura de banda
- 🔲 Load balancing com múltiplos caminhos
- 🔲 Recuperação automática de falhas
- 🔲 Métricas de performance detalhadas

---

**🎉 Agora você tem um controlador SDN com roteamento otimizado usando Dijkstra!**
