# INSTRUÇÕES PARA SCREENSHOTS DO CÓDIGO NO VS CODE

## 📸 COMO TIRAR PRINTS BONITOS DO CÓDIGO

---

## OPÇÃO 1: EXTENSÃO POLACODE (RECOMENDADA)

### Instalação:
1. Abra VS Code
2. Vá em Extensions (Ctrl+Shift+X)
3. Pesquise "Polacode"
4. Instale a extensão

### Como usar:
1. Abra o arquivo de código
2. Selecione o trecho que quer capturar
3. Ctrl+Shift+P → digite "Polacode"
4. Escolha "Polacode: Start"
5. Ajuste o tema e configurações
6. Clique em "Save" para salvar a imagem

---

## OPÇÃO 2: EXTENSÃO CODESNAP

### Instalação:
1. Extensions → pesquise "CodeSnap"
2. Instale

### Como usar:
1. Selecione o código
2. Ctrl+Shift+P → "CodeSnap"
3. Escolha configurações
4. Salve a imagem

---

## OPÇÃO 3: MANUAL (SEM EXTENSÃO)

### Configurar VS Code para prints bonitos:
1. **Tema:** File → Preferences → Color Theme → "Dark+" ou "Light+"
2. **Fonte:** Settings → "Editor: Font Family" → "Fira Code" ou "Consolas"
3. **Tamanho:** Settings → "Editor: Font Size" → 14-16
4. **Zoom:** Ctrl + "+" para aumentar
5. **Print Screen:** Use ferramenta de captura do sistema

---

## 📋 TRECHOS ESPECÍFICOS PARA CAPTURAR

### SCREENSHOT 1: Estruturas de Dados
**Arquivo:** dijkstra_controller.py
**Linhas:** 23-32
```python
# Estruturas de dados para Dijkstra
self.mac_to_port = {}      # {dpid: {mac: port}}
self.topology_graph = nx.Graph()  # Grafo da topologia
self.switches = {}         # {dpid: switch_object}
self.hosts = {}           # {mac: (dpid, port)}
self.links = {}           # {(src_dpid, dst_dpid): (src_port, dst_port)}
```

### SCREENSHOT 2: Descoberta de Switch
**Arquivo:** dijkstra_controller.py
**Linhas:** 34-42
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

### SCREENSHOT 3: Algoritmo Dijkstra
**Arquivo:** dijkstra_controller.py
**Linhas:** 95-108
```python
def dijkstra_shortest_path(self, src_dpid, dst_dpid):
    """Implementação do algoritmo de Dijkstra"""
    try:
        if src_dpid == dst_dpid:
            return [src_dpid]
        
        if self.topology_graph.has_node(src_dpid) and self.topology_graph.has_node(dst_dpid):
            path = nx.shortest_path(self.topology_graph, src_dpid, dst_dpid, weight='weight')
            self.logger.info("🛤️ Dijkstra: Caminho %s -> %s: %s", src_dpid, dst_dpid, path)
            return path
```

### SCREENSHOT 4: Topologia de Teste
**Arquivo:** dijkstra_topologia.py
**Linhas:** 13-35
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
```

### SCREENSHOT 5: Comandos de Execução
**Terminal bash:**
```bash
cd /home/oem/ryu_ambiente_final
source ryu_env/bin/activate
ryu-manager dijkstra_controller.py
```

### SCREENSHOT 6: Logs do Sistema
**Terminal output:**
```
🚀 Controlador Dijkstra iniciado!
🔗 Switch conectado: DPID=1
🛤️ Dijkstra: Caminho 1 -> 3: [1, 2, 3]
📦 Flow instalado: Switch 1 -> porta 2
```

---

## 🎨 CONFIGURAÇÕES RECOMENDADAS PARA PRINTS

### Tema VS Code:
- **Dark Theme:** "One Dark Pro" ou "Dark+"
- **Light Theme:** "Light+" ou "GitHub Light"

### Fonte:
- **Fira Code** (com ligatures)
- **JetBrains Mono**
- **Consolas** (padrão Windows)

### Tamanho:
- **Para apresentação:** 16-18pt
- **Para documento:** 14pt

### Cores:
- Syntax highlighting ativado
- Line numbers visíveis
- Indentation guides ativados

---

## 📝 ORGANIZAÇÃO DOS SCREENSHOTS

### Para cada pessoa da apresentação:

**PESSOA 1:**
- Screenshot: Conceito Dijkstra (diagrama simples)
- Screenshot: Exemplo de grafo com pesos

**PESSOA 2:**
- Screenshot: Estruturas de dados
- Screenshot: Função dijkstra_shortest_path()
- Screenshot: Importações (NetworkX, Ryu)

**PESSOA 3:**
- Screenshot: switch_enter_handler()
- Screenshot: packet_in_handler()
- Screenshot: install_path_flows()

**PESSOA 4:**
- Screenshot: Topologia de teste
- Screenshot: Comandos de execução
- Screenshot: Logs do sistema
- Screenshot: Resultados pingall

---

## 💡 DICAS EXTRAS

1. **Consistência:** Use o mesmo tema em todos os prints
2. **Qualidade:** Resolução alta (pelo menos 1920x1080)
3. **Foco:** Destaque apenas o código relevante
4. **Legibilidade:** Fonte grande o suficiente para projeção
5. **Contexto:** Inclua número das linhas se necessário

**Agora você pode criar screenshots profissionais do código!** 📸
