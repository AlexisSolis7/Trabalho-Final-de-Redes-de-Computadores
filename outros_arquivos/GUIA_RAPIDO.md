# 🚀 Guia Rápido: Como Testar o Controlador Dijkstra

## ⚡ Execução Rápida (2 Terminais)

### **Terminal 1 - Controlador:**
```bash
cd ~/ryu_ambiente_final
./start_dijkstra.sh
```

**✅ Aguarde ver:** `🚀 Controlador Dijkstra iniciado!`

### **Terminal 2 - Teste:**
```bash
cd ~/ryu_ambiente_final
./simple_dijkstra_test.sh
```

**Escolha uma opção (recomendo 2 ou 3 para ver Dijkstra funcionando)**

## 🧪 **Comandos de Teste no Mininet**

Quando estiver no prompt `mininet>`:

### **Teste Básico:**
```
mininet> pingall
mininet> h1 ping h2
```

### **Ver Topologia:**
```
mininet> dump
mininet> links
mininet> nodes
```

### **Teste de Performance:**
```
mininet> iperf h1 h2
```

### **Sair:**
```
mininet> exit
```

## 📊 **O que Observar nos Logs**

### **No Terminal do Controlador, você verá:**
```
🔗 Switch conectado: DPID=1
🔗 Link adicionado: 1:2 -> 2:1
📦 PacketIn: Switch=1, MAC src=00:00:00:00:00:01, dst=00:00:00:00:00:02
🎯 Calculando caminho: src (switch 1) -> dst (switch 3)
🛤️ Dijkstra: Caminho 1 -> 3: [1, 2, 3]
📥 Flow instalado: Switch=1, dst=00:00:00:00:00:02 -> porta=2
📤 Encaminhando pacote para porta 2
```

## 🎯 **Evidências do Algoritmo Dijkstra**

### **1. Descoberta de Topologia:**
- `🔗 Switch conectado`
- `🔗 Link adicionado`

### **2. Cálculo do Caminho:**
- `🎯 Calculando caminho`
- `🛤️ Dijkstra: Caminho X -> Y: [lista de switches]`

### **3. Instalação de Flows:**
- `📥 Flow instalado` em cada switch do caminho

### **4. Roteamento Otimizado:**
- Todos os pacotes seguem o **menor caminho** calculado
- Não há floods desnecessários após o aprendizado

## ❌ **Resolução de Problemas**

### **"Controlador não está rodando"**
```bash
# Verificar se porta 6633 está em uso
netstat -tuln | grep 6633

# Se não aparecer nada, iniciar controlador
./start_dijkstra.sh
```

### **"Mininet must run as root"**
```bash
# Usar sudo
sudo python3 test_dijkstra.py

# Ou usar o script wrapper
./run_dijkstra_test.sh
```

### **"Módulo networkx não encontrado"**
```bash
source ryu_env/bin/activate
pip install networkx
```

### **Limpar ambiente após teste:**
```bash
sudo mn -c
```

## 🏆 **Teste de Sucesso**

**✅ O Dijkstra está funcionando se você ver:**

1. **Descoberta automática** de switches e links
2. **Cálculo de caminhos** nos logs: `🛤️ Dijkstra: Caminho...`
3. **Conectividade 100%** no `pingall`
4. **Flows instalados** em múltiplos switches para um mesmo destino

---

**🎉 Pronto! Agora você tem um controlador SDN com roteamento Dijkstra funcionando!**
