# CÓDIGOS PRINCIPAIS PARA A APRESENTAÇÃO
## Trechos formatados para copiar no Word

---

## CÓDIGO 1: ESTRUTURAS DE DADOS PRINCIPAIS

```python
class DijkstraSwitch13(app_manager.RyuApp):
    def __init__(self, *args, **kwargs):
        super(DijkstraSwitch13, self).__init__(*args, **kwargs)
        
        # Estruturas de dados para Dijkstra
        self.mac_to_port = {}           # {dpid: {mac: port}}
        self.topology_graph = nx.Graph() # Grafo da topologia  
        self.switches = {}              # {dpid: switch_object}
        self.hosts = {}                 # {mac: (dpid, port)}
        self.links = {}                 # {(src_dpid, dst_dpid): (src_port, dst_port)}
        
        self.logger.info("🚀 Controlador Dijkstra iniciado!")
```

---

## CÓDIGO 2: DESCOBERTA DE SWITCHES

```python
@set_ev_cls(event.EventSwitchEnter)
def switch_enter_handler(self, ev):
    """Detecta quando um switch se conecta"""
    switch = ev.switch
    dpid = switch.dp.id
    
    # Adicionar switch ao grafo
    self.switches[dpid] = switch
    self.topology_graph.add_node(dpid)
    
    self.logger.info("🔗 Switch conectado: DPID=%s", dpid)
    self._update_topology()
```

---

## CÓDIGO 3: DESCOBERTA DE LINKS

```python
@set_ev_cls(event.EventLinkAdd)
def link_add_handler(self, ev):
    """Detecta quando um link é adicionado"""
    link = ev.link
    src_dpid = link.src.dpid
    dst_dpid = link.dst.dpid
    src_port = link.src.port_no
    dst_port = link.dst.port_no
    
    # Adicionar link ao grafo (peso = 1)
    self.topology_graph.add_edge(src_dpid, dst_dpid, weight=1)
    self.links[(src_dpid, dst_dpid)] = (src_port, dst_port)
    self.links[(dst_dpid, src_dpid)] = (dst_port, src_port)
    
    self.logger.info("🔗 Link adicionado: %s:%s -> %s:%s", 
                    src_dpid, src_port, dst_dpid, dst_port)
```

---

## CÓDIGO 4: ALGORITMO DIJKSTRA

```python
def dijkstra_shortest_path(self, src_dpid, dst_dpid):
    """Implementação do algoritmo de Dijkstra"""
    try:
        # Caso especial: mesmo switch
        if src_dpid == dst_dpid:
            return [src_dpid]
        
        # Verificar se nós existem no grafo
        if (self.topology_graph.has_node(src_dpid) and 
            self.topology_graph.has_node(dst_dpid)):
            
            # Usar NetworkX para calcular caminho ótimo
            path = nx.shortest_path(self.topology_graph, 
                                  src_dpid, dst_dpid, weight='weight')
            
            self.logger.info("🛤️ Dijkstra: Caminho %s -> %s: %s", 
                           src_dpid, dst_dpid, path)
            return path
        else:
            self.logger.warning("❌ Dijkstra: Não há caminho entre %s e %s", 
                              src_dpid, dst_dpid)
            return None
            
    except Exception as e:
        self.logger.error("❌ Erro no Dijkstra: %s", e)
        return None
```

---

## CÓDIGO 5: PROCESSAMENTO DE PACOTES

```python
@set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
def packet_in_handler(self, ev):
    """Processa PacketIn usando algoritmo de Dijkstra"""
    msg = ev.msg
    datapath = msg.datapath
    dpid = datapath.id
    in_port = msg.match['in_port']

    # Extrair informações do pacote
    pkt = packet.Packet(msg.data)
    eth = pkt.get_protocols(ethernet.ethernet)[0]
    dst_mac = eth.dst
    src_mac = eth.src

    # Aprender localização do host origem
    if dpid not in self.mac_to_port:
        self.mac_to_port[dpid] = {}
    self.mac_to_port[dpid][src_mac] = in_port
    self.hosts[src_mac] = (dpid, in_port)

    # Se destino conhecido, usar Dijkstra
    if dst_mac in self.hosts:
        dst_dpid, dst_port = self.hosts[dst_mac]
        src_dpid = dpid
        
        # Calcular caminho mais curto com Dijkstra
        path = self.dijkstra_shortest_path(src_dpid, dst_dpid)
        
        if path:
            # Instalar flows ao longo do caminho
            self.install_path_flows(path, src_mac, dst_mac, in_port, msg.data)
```

---

## CÓDIGO 6: INSTALAÇÃO DE FLOWS

```python
def install_path_flows(self, path, src_mac, dst_mac, in_port, packet_out_data):
    """Instala flows ao longo do caminho calculado por Dijkstra"""
    if not path or len(path) < 2:
        return

    # Para cada switch no caminho (exceto o último)
    for i in range(len(path) - 1):
        current_dpid = path[i]
        next_dpid = path[i + 1]
        
        # Encontrar a porta de saída para o próximo switch
        if (current_dpid, next_dpid) in self.links:
            out_port = self.links[(current_dpid, next_dpid)][0]
            
            # Obter o datapath do switch atual
            if current_dpid in self.switches:
                datapath = self.switches[current_dpid].dp
                parser = datapath.ofproto_parser
                
                # Criar regra OpenFlow
                match = parser.OFPMatch(eth_dst=dst_mac)
                actions = [parser.OFPActionOutput(out_port)]
                
                # Instalar flow com prioridade alta
                self.add_flow(datapath, 10, match, actions)
                
                self.logger.info("📦 Flow instalado: Switch %s -> porta %s (para %s)", 
                               current_dpid, out_port, dst_mac)
```

---

## CÓDIGO 7: TOPOLOGIA COMPLEXA (dijkstra_topologia.py)

```python
class DijkstraTestTopo(Topo):
    """
    Topologia otimizada para testar Dijkstra
    
    Estrutura:
         h1
         |
        s1 --- s2 --- s4
         |     |      |
        s3 --- s5 --- h2
         |
        h3
    """
    def build(self):
        # Adicionar switches
        s1 = self.addSwitch('s1', dpid='0000000000000001')
        s2 = self.addSwitch('s2', dpid='0000000000000002') 
        s3 = self.addSwitch('s3', dpid='0000000000000003')
        s4 = self.addSwitch('s4', dpid='0000000000000004')
        s5 = self.addSwitch('s5', dpid='0000000000000005')
        
        # Adicionar hosts
        h1 = self.addHost('h1', mac='00:00:00:00:00:01', ip='10.0.0.1/24')
        h2 = self.addHost('h2', mac='00:00:00:00:00:02', ip='10.0.0.2/24') 
        h3 = self.addHost('h3', mac='00:00:00:00:00:03', ip='10.0.0.3/24')
        
        # Conectar hosts aos switches
        self.addLink(h1, s1)  # h1 -> s1
        self.addLink(h2, s4)  # h2 -> s4  
        self.addLink(h3, s3)  # h3 -> s3
        
        # Links entre switches (múltiplos caminhos)
        self.addLink(s1, s2)  # s1 <-> s2
        self.addLink(s1, s3)  # s1 <-> s3
        self.addLink(s2, s4)  # s2 <-> s4
        self.addLink(s2, s5)  # s2 <-> s5
        self.addLink(s3, s5)  # s3 <-> s5
        self.addLink(s4, s5)  # s4 <-> s5
```

---

## CÓDIGO 8: COMANDOS DE EXECUÇÃO

```bash
# Terminal 1 - Controlador
cd /home/oem/ryu_ambiente_final
source ryu_env/bin/activate
ryu-manager --verbose dijkstra_controller.py

# Terminal 2 - Topologia
cd /home/oem/ryu_ambiente_final
sudo python3 dijkstra_topologia.py

# Comandos no Mininet
mininet> pingall          # Testa conectividade geral
mininet> h1 ping h2       # Ping específico
mininet> dpctl dump-flows # Ver regras OpenFlow instaladas
mininet> net             # Ver estrutura da topologia
mininet> exit            # Sair do Mininet
```

---

## LOGS EXEMPLO DO SISTEMA

```
🚀 Controlador Dijkstra iniciado!
loading app dijkstra_controller.py
🔗 Switch conectado: DPID=1
🔗 Switch conectado: DPID=2
🔗 Switch conectado: DPID=3
🔗 Link adicionado: 1:2 -> 2:1
🔗 Link adicionado: 2:3 -> 3:2
📊 Topologia atualizada - Nodes: 3, Links: 2
📨 Packet-In: switch=1, src=00:00:00:00:00:01, dst=00:00:00:00:00:02
🛤️ Dijkstra: Caminho 1 -> 3: [1, 2, 3]
📦 Flow instalado: Switch 1 -> porta 2 (para 00:00:00:00:00:02)
📦 Flow instalado: Switch 2 -> porta 2 (para 00:00:00:00:00:02)
📦 Flow final instalado: Switch 3 -> Host porta 1
```

---

## RESULTADOS DOS TESTES

```bash
mininet> pingall
*** Ping: testing ping reachability
h1 -> h2 h3 
h2 -> h1 h3 
h3 -> h1 h2 
*** Results: 0% dropped (6/6 received)

mininet> h1 ping -c 3 h2
PING 10.0.0.2 (10.0.0.2) 56(84) bytes of data.
64 bytes from 10.0.0.2: icmp_seq=1 ttl=64 time=1.52 ms
64 bytes from 10.0.0.2: icmp_seq=2 ttl=64 time=0.085 ms
64 bytes from 10.0.0.2: icmp_seq=3 ttl=64 time=0.074 ms
--- 10.0.0.2 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, average=0.56 ms
```

---

## INSTRUÇÕES PARA USO NO WORD:

1. **Copie cada código** e cole no Word
2. **Formate como código:** Use fonte Courier New, tamanho 10
3. **Para destacar:** Use background cinza claro
4. **Para prints do VS Code:** Use extensão "Polacode" ou "CodeSnap"
5. **Para diagramas:** Desenhe no Word ou use draw.io

**Agora você tem todo o conteúdo formatado para montar a apresentação!** 📝
