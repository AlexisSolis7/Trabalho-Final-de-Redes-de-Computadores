# APRESENTAÇÃO: CONTROLADOR SDN COM ALGORITMO DIJKSTRA
## Estrutura Completa para Word/PowerPoint

---

## SLIDE 1: CAPA
**CONTROLADOR SDN COM ALGORITMO DIJKSTRA**
- Implementação de Roteamento Inteligente
- Grupo: [Nomes dos 4 integrantes]
- Data: 2 de julho de 2025

---

## PESSOA 1: O QUE É DIJKSTRA E POR QUE USAR (7-8 min)

### SLIDE 2: O QUE É O ALGORITMO DE DIJKSTRA?
**Conceito:**
- Algoritmo para encontrar o **caminho mais curto** entre dois pontos
- Trabalha com **grafos ponderados** (com pesos nos links)
- Garante encontrar a **solução ótima**

**Exemplo Visual:**
```
Rede com múltiplos caminhos:
A ----2---- B
|           |
3           1
|           |
C ----4---- D

Caminho A→D:
- A→B→D = 2+1 = 3 (MELHOR)
- A→C→D = 3+4 = 7
```

### SLIDE 3: COMO FUNCIONA (CONCEITO SIMPLES)
**Passos do Algoritmo:**
1. **Inicialização**: Marca origem com distância 0
2. **Exploração**: Visita vizinhos e calcula distâncias
3. **Seleção**: Sempre escolhe nó com menor distância
4. **Atualização**: Atualiza distâncias dos vizinhos
5. **Repetição**: Até chegar ao destino

**Garantia:** Sempre encontra o caminho ótimo!

### SLIDE 4: POR QUE DIJKSTRA EM REDES SDN?
**Problemas em Redes:**
- Múltiplos caminhos entre hosts
- Necessidade de escolher o melhor automaticamente
- Evitar congestionamentos
- Otimizar performance

**Solução SDN + Dijkstra:**
- Controle centralizado
- Visão global da topologia
- Cálculo automático do melhor caminho
- Roteamento inteligente

### SLIDE 5: PROBLEMA vs SOLUÇÃO
**ANTES (Redes Tradicionais):**
- Roteamento estático ou protocolos complexos
- Decisões locais em cada switch
- Sem visão global da rede

**DEPOIS (SDN + Dijkstra):**
- Controlador centralizado com visão global
- Cálculo automático do melhor caminho
- Roteamento otimizado e eficiente

---

## PESSOA 2: COMO IMPLEMENTAMOS NO PROJETO (8-9 min)

### SLIDE 6: FERRAMENTAS UTILIZADAS
**Stack Tecnológico:**
- **Ryu Framework**: Controlador SDN em Python
- **NetworkX**: Biblioteca para grafos e algoritmos
- **Mininet**: Simulador de rede para testes
- **OpenFlow**: Protocolo de comunicação

**Por que essas escolhas?**
- Ryu: Framework maduro e bem documentado
- NetworkX: Implementação otimizada do Dijkstra
- Mininet: Ambiente de teste realista

### SLIDE 7: REPRESENTAÇÃO DA REDE COMO GRAFO
**Mapeamento Rede → Grafo:**
- **Switches** = Nós do grafo
- **Links** = Arestas do grafo  
- **Pesos** = Custo do link (latência, largura de banda)

**Código:**
```python
# Estruturas principais
self.topology_graph = nx.Graph()  # Grafo da topologia
self.switches = {}                # Switches conectados
self.links = {}                   # Links entre switches
self.hosts = {}                   # Localização dos hosts
```

### SLIDE 8: DESCOBERTA AUTOMÁTICA DA TOPOLOGIA
**Como descobrimos a rede:**

**Código - Detectar Switches:**
```python
@set_ev_cls(event.EventSwitchEnter)
def switch_enter_handler(self, ev):
    """Detecta quando um switch se conecta"""
    switch = ev.switch
    dpid = switch.dp.id
    self.switches[dpid] = switch
    self.topology_graph.add_node(dpid)
    self.logger.info("🔗 Switch conectado: DPID=%s", dpid)
```

**Código - Detectar Links:**
```python
@set_ev_cls(event.EventLinkAdd)
def link_add_handler(self, ev):
    """Detecta quando um link é adicionado"""
    link = ev.link
    src_dpid = link.src.dpid
    dst_dpid = link.dst.dpid
    
    # Adicionar link ao grafo
    self.topology_graph.add_edge(src_dpid, dst_dpid, weight=1)
    self.links[(src_dpid, dst_dpid)] = (src_port, dst_port)
```

### SLIDE 9: APLICAÇÃO DO DIJKSTRA
**Função Principal:**
```python
def dijkstra_shortest_path(self, src_dpid, dst_dpid):
    """Implementação do algoritmo de Dijkstra"""
    try:
        if src_dpid == dst_dpid:
            return [src_dpid]
        
        # Usa NetworkX para calcular caminho ótimo
        path = nx.shortest_path(self.topology_graph, 
                               src_dpid, dst_dpid, weight='weight')
        
        self.logger.info("🛤️ Dijkstra: Caminho %s -> %s: %s", 
                        src_dpid, dst_dpid, path)
        return path
    except Exception as e:
        self.logger.error("❌ Erro no Dijkstra: %s", e)
        return None
```

### SLIDE 10: INTEGRAÇÃO DIJKSTRA + SDN
**Fluxo de Integração:**
1. **Topologia descoberta** automaticamente
2. **Grafo atualizado** em tempo real
3. **Dijkstra calculado** quando necessário
4. **Resultado aplicado** via OpenFlow flows

**Vantagem:** Automação completa do processo!

---

## PESSOA 3: FUNCIONAMENTO DO CONTROLADOR (8-9 min)

### SLIDE 11: FLUXO DE FUNCIONAMENTO
**5 Passos Principais:**
1. **Switch conecta** → Topologia atualizada no grafo
2. **Pacote chega** → Controlador recebe PacketIn
3. **Dijkstra calcula** → Melhor caminho encontrado
4. **Flows instalados** → Switches aprendem como rotear
5. **Próximos pacotes** → Roteados automaticamente

### SLIDE 12: PROCESSAMENTO DE PACOTES
**Função Principal:**
```python
@set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
def packet_in_handler(self, ev):
    """Processa PacketIn usando Dijkstra"""
    
    # 1. Extrair informações do pacote
    dpid = datapath.id
    src_mac = eth.src
    dst_mac = eth.dst
    
    # 2. Aprender localização do host origem
    self.hosts[src_mac] = (dpid, in_port)
    
    # 3. Se destino conhecido, usar Dijkstra
    if dst_mac in self.hosts:
        dst_dpid, dst_port = self.hosts[dst_mac]
        
        # 4. Calcular caminho ótimo
        path = self.dijkstra_shortest_path(dpid, dst_dpid)
        
        # 5. Instalar flows no caminho
        self.install_path_flows(path, src_mac, dst_mac)
```

### SLIDE 13: INSTALAÇÃO DE FLOWS OPENFLOW
**Como instalamos as regras:**
```python
def install_path_flows(self, path, src_mac, dst_mac):
    """Instala flows ao longo do caminho calculado"""
    
    # Para cada switch no caminho
    for i in range(len(path) - 1):
        current_dpid = path[i]
        next_dpid = path[i + 1]
        
        # Encontrar porta de saída
        out_port = self.links[(current_dpid, next_dpid)][0]
        
        # Criar regra OpenFlow
        match = parser.OFPMatch(eth_dst=dst_mac)
        actions = [parser.OFPActionOutput(out_port)]
        
        # Instalar no switch
        self.add_flow(datapath, 10, match, actions)
```

### SLIDE 14: EXEMPLO PRÁTICO PASSO-A-PASSO
**Cenário:** h1 quer enviar para h2

**Topologia:**
```
h1 - s1 - s2 - s3 - h2
```

**Passos:**
1. h1 envia pacote → s1 recebe
2. s1 não conhece h2 → PacketIn para controlador
3. Controlador calcula: caminho s1→s2→s3
4. Controlador instala flows:
   - s1: "para h2 → sair porta 2"
   - s2: "para h2 → sair porta 2" 
   - s3: "para h2 → sair porta host"
5. Próximos pacotes seguem automaticamente

### SLIDE 15: LOGS DO SISTEMA EM AÇÃO
**Saída do Controlador:**
```
🚀 Controlador Dijkstra iniciado!
🔗 Switch conectado: DPID=1
🔗 Switch conectado: DPID=2
🔗 Link adicionado: 1:2 -> 2:1
📊 Topologia atualizada - Nodes: 2, Links: 1
🛤️ Dijkstra: Caminho 1 -> 2: [1, 2]
📦 Flow instalado: Switch 1 -> porta 2
```

---

## PESSOA 4: TESTES E DEMONSTRAÇÃO PRÁTICA (8-9 min)

### SLIDE 16: AMBIENTE DE TESTE
**Mininet - Simulador de Rede:**
- Simula switches, hosts e links
- Funciona com controladores SDN reais
- Permite testes em ambiente controlado

**Setup:**
- Terminal 1: `ryu-manager dijkstra_controller.py`
- Terminal 2: `sudo python3 dijkstra_topologia.py`

### SLIDE 17: TOPOLOGIAS TESTADAS
**Topologia Linear:**
```
h1 - s1 - s2 - s3 - h2

Teste: h1 ping h2
Caminho: s1 → s2 → s3
```

**Topologia Complexa:**
```
     h1
     |
    s1 --- s2 --- s4
     |     |      |
    s3 --- s5 --- h2
     |
    h3

Múltiplos caminhos possíveis:
h1 → h2: s1→s2→s4 OU s1→s3→s5→s4
```

### SLIDE 18: COMANDOS DE TESTE EXECUTADOS
**No Terminal Mininet:**
```bash
mininet> pingall          # Testa conectividade geral
*** Results: 0% dropped (6/6 received)

mininet> h1 ping h2       # Teste específico
PING 10.0.0.2 from 10.0.0.1: 64 bytes from 10.0.0.2: seq=0 time=1.5 ms

mininet> dpctl dump-flows # Ver regras instaladas
cookie=0x0, duration=12.5s, table=0, priority=10, dl_dst=00:00:00:00:00:02 actions=output:2

mininet> net             # Ver topologia
h1 h1-eth0:s1-eth1
s1 lo: s1-eth1:h1-eth0 s1-eth2:s2-eth1
```

### SLIDE 19: RESULTADOS OBSERVADOS
**✅ Sucessos Comprovados:**

**1. Cálculo Automático:**
```
Log: 🛤️ Dijkstra: Caminho 1 -> 3: [1, 2, 3]
```

**2. Flows Corretos:**
```
Log: 📦 Flow instalado: Switch 1 -> porta 2 (para h2)
Log: 📦 Flow instalado: Switch 2 -> porta 2 (para h2)
```

**3. Conectividade Total:**
```
mininet> pingall
*** Results: 0% dropped (6/6 received)
```

**4. Roteamento Eficiente:**
- Sempre escolhe caminho mais curto
- Próximos pacotes seguem automaticamente

### SLIDE 20: VANTAGENS ALCANÇADAS
**🎯 Objetivos Atingidos:**

**Roteamento Inteligente:**
- Sistema calcula automaticamente melhor caminho
- Sem configuração manual necessária

**Eficiência:**
- Usa recursos de rede de forma ótima
- Evita caminhos desnecessariamente longos

**Flexibilidade:**
- Funciona com qualquer topologia
- Adapta-se a mudanças automaticamente

**Simplicidade:**
- Código limpo e modular
- Fácil de entender e modificar

### SLIDE 21: DEMONSTRAÇÃO AO VIVO
**[DEMO - Se possível]**

**Mostrar em funcionamento:**
1. Controlador executando
2. Logs com cálculos Dijkstra
3. Mininet com conectividade
4. Comandos de teste em tempo real

**Se não for possível demo ao vivo:**
- Screenshots dos logs
- Vídeo gravado previamente
- Explicação com código

---

## SLIDE 22: CONCLUSÕES
**O que aprendemos:**
- Integração Dijkstra + SDN é viável e eficiente
- Ryu + NetworkX facilitam implementação
- Testes com Mininet validam funcionamento

**Resultados:**
- Roteamento automático e inteligente
- Sistema funcional e testado
- Código extensível para melhorias futuras

**Próximos passos:**
- Implementar pesos dinâmicos nos links
- Adicionar load balancing
- Interface web para monitoramento

---

## SLIDE 23: PERGUNTAS?
**Obrigado pela atenção!**

**Contatos do grupo:**
- [Nome 1] - [email]
- [Nome 2] - [email]  
- [Nome 3] - [email]
- [Nome 4] - [email]

---

## ANEXOS PARA CÓDIGO

### ARQUIVO 1: dijkstra_controller.py (Principais funções)
[Copiar trechos principais do arquivo para anexo]

### ARQUIVO 2: dijkstra_topologia.py (Topologias de teste)
[Copiar estrutura das topologias]

### ARQUIVO 3: Logs de execução
[Copiar saída real do sistema]

---

## INSTRUÇÕES PARA MONTAR NO WORD:

1. **Copie cada seção** como um slide/página
2. **Para screenshots do código:**
   - Use a extensão "Polacode" no VS Code
   - Ou copie o código formatado direto
3. **Para diagramas:**
   - Use desenhos simples no Word
   - Ou ferramentas como draw.io
4. **Para demo:**
   - Grave um vídeo curto
   - Ou prepare screenshots

**Esta estrutura te dá uma apresentação completa e focada no essencial!** 🎯
