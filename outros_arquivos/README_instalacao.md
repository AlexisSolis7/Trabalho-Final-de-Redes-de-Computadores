# 🚀 Guia Completo de Instalação do Ryu SDN Framework

## 📋 Índice
- [Visão Geral](#visão-geral)
- [Pré-requisitos](#pré-requisitos)
- [Instalação Passo-a-Passo](#instalação-passo-a-passo)
- [Problemas Comuns e Soluções](#problemas-comuns-e-soluções)
- [Verificação da Instalação](#verificação-da-instalação)
- [Instalação do Mininet](#instalação-do-mininet)
- [Primeiro Teste](#primeiro-teste)
- [Estrutura do Projeto](#estrutura-do-projeto)

## 🎯 Visão Geral

Este guia te ajudará a instalar o **Ryu SDN Framework** do zero, mesmo que você nunca tenha instalado antes. Baseado em experiência real com todos os erros que podem acontecer!

## ⚠️ Pré-requisitos

### Sistema Operacional
- **Ubuntu 20.04 LTS** ou **22.04 LTS** (recomendado)
- **Linux Mint** (testado e funcionando)
- Mínimo 4GB RAM, 8GB recomendado

### Permissões
```bash
# Você precisará de sudo para alguns comandos
sudo apt update
```

## 🔧 Instalação Passo-a-Passo

### Passo 1: Atualizar o Sistema
```bash
sudo apt update && sudo apt upgrade -y
```

### Passo 2: Instalar Python 3.8 (CRUCIAL!)
⚠️ **IMPORTANTE**: O Ryu tem problemas de compatibilidade com Python 3.11+ e 3.12+

```bash
# Adicionar repositório para versões antigas do Python
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update

# Instalar Python 3.8 e dependências
sudo apt install python3.8 python3.8-venv python3.8-dev
```

### Passo 3: Criar Diretório do Projeto
```bash
mkdir -p ~/ryu_ambiente_final
cd ~/ryu_ambiente_final
```

### Passo 4: Criar Ambiente Virtual
```bash
# Criar ambiente virtual com Python 3.8
python3.8 -m venv ryu_env

# Ativar o ambiente virtual
source ryu_env/bin/activate

# Verificar a versão (deve mostrar Python 3.8.x)
python --version
```

### Passo 5: Instalar Setuptools Compatível
⚠️ **PROBLEMA COMUM**: Versões novas do setuptools causam erro!

```bash
# Instalar versão compatível do setuptools
pip install --upgrade pip
pip install "setuptools<45" wheel
```

### Passo 6: Instalar Eventlet Compatível
⚠️ **PROBLEMA COMUM**: Eventlet novo não funciona com Ryu!

```bash
# Instalar versão específica do eventlet
pip install "eventlet==0.30.2"
```

### Passo 7: Instalar o Ryu
```bash
# Agora sim, instalar o Ryu
pip install ryu
```

## 🐛 Problemas Comuns e Soluções

### Erro 1: AttributeError com setuptools
```
AttributeError: 'types.SimpleNamespace' object has no attribute 'get_script_args'
```

**Solução:**
```bash
pip install "setuptools<45"
```

### Erro 2: ImportError com eventlet
```
ImportError: cannot import name 'ALREADY_HANDLED' from 'eventlet.wsgi'
```

**Solução:**
```bash
pip install "eventlet==0.30.2"
```

### Erro 3: Comando não encontrado
```
ryu-manager: comando não encontrado
```

**Soluções:**
1. Verificar se o ambiente virtual está ativo:
```bash
source ryu_env/bin/activate
```

2. Verificar se o Ryu foi instalado:
```bash
pip list | grep ryu
```

### Erro 4: Problemas com Python 3.12+
Se você estiver usando Python 3.12 ou superior, o Ryu não funcionará!

**Solução: Use Python 3.8**
```bash
# Remover ambiente antigo
rm -rf ryu_env

# Criar novo com Python 3.8
python3.8 -m venv ryu_env
source ryu_env/bin/activate
```

### Erro 5: Ambiente Python externamente gerenciado
```
error: externally-managed-environment
```

**Solução: Use ambiente virtual (já fazemos isso acima)**

## ✅ Verificação da Instalação

### Teste 1: Importar Ryu
```bash
cd ~/ryu_ambiente_final
source ryu_env/bin/activate
python -c "import ryu; print('✓ Ryu importado com sucesso!')"
```

### Teste 2: Verificar ryu-manager
```bash
which ryu-manager
# Deve mostrar: ~/ryu_ambiente_final/ryu_env/bin/ryu-manager
```

### Teste 3: Executar script de teste
Crie um arquivo `test_ryu.py`:
```python
#!/usr/bin/env python3
import ryu
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.ofproto import ofproto_v1_3

print("✅ Ryu funcionando perfeitamente!")
print(f"📍 Ryu instalado em: {ryu.__file__}")

class TestApp(app_manager.RyuApp):
    def __init__(self, *args, **kwargs):
        super(TestApp, self).__init__(*args, **kwargs)

print("✅ Classe de aplicação criada com sucesso!")
```

Execute:
```bash
python test_ryu.py
```

## 🌐 Instalação do Mininet

O Mininet é necessário para testar o controlador:

```bash
# Instalar Mininet e Open vSwitch
sudo apt install mininet openvswitch-switch openvswitch-testcontroller

# Testar instalação
sudo mn --test pingall
```

## 🧪 Primeiro Teste

### Passo 1: Criar controlador simples
Arquivo `simple_switch_13.py`:
```python
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, CONFIG_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet

class SimpleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.mac_to_port = {}

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                        ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                           actions)]
        mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                              match=match, instructions=inst)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth_pkt = pkt.get_protocol(ethernet.ethernet)
        dst = eth_pkt.dst
        src = eth_pkt.src

        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})

        self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)
        self.mac_to_port[dpid][src] = in_port

        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = [parser.OFPActionOutput(out_port)]

        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst)
            self.add_flow(datapath, 1, match, actions)

        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)
```

### Passo 2: Executar o teste
**Terminal 1 - Controlador:**
```bash
cd ~/ryu_ambiente_final
source ryu_env/bin/activate
ryu-manager simple_switch_13.py
```

**Terminal 2 - Mininet:**
```bash
sudo mn --controller remote,ip=127.0.0.1,port=6633 --topo single,2
```

**No prompt do Mininet:**
```
mininet> pingall
mininet> h1 ping h2
mininet> exit
```

## 📁 Estrutura do Projeto

```
~/ryu_ambiente_final/
├── ryu_env/                 # Ambiente virtual Python 3.8
├── simple_switch_13.py      # Controlador básico
├── test_ryu.py             # Script de teste
├── logs/                   # Logs do sistema
├── results/                # Resultados de testes
├── graphs/                 # Gráficos gerados
└── README.md              # Este arquivo
```

## 🎯 Scripts Úteis

### Ativar ambiente (sempre necessário)
```bash
cd ~/ryu_ambiente_final
source ryu_env/bin/activate
```

### Limpeza do Mininet
```bash
sudo mn -c
```

### Ver logs detalhados
```bash
ryu-manager --verbose simple_switch_13.py
```

## 🔍 Verificação Final

Se tudo estiver funcionando, você deve ver:

1. **Controlador iniciando:**
```
loading app simple_switch_13.py
instantiating app simple_switch_13.py of SimpleSwitch13
```

2. **Mininet conectando:**
```
*** Adding controller
*** Starting controller
c0 
*** Starting 1 switches
s1 ...
```

3. **Ping funcionando:**
```
*** Ping: testing ping reachability
h1 -> h2 
h2 -> h1 
*** Results: 0% dropped (2/2 received)
```

## 🆘 Ajuda Adicional

### Se nada funcionar:
1. Verificar versão do Python: `python --version` (deve ser 3.8.x)
2. Verificar ambiente ativo: `which python` (deve apontar para ryu_env)
3. Reinstalar tudo do zero seguindo este guia
4. Verificar logs de erro detalhadamente

### Comandos de debug:
```bash
# Ver pacotes instalados
pip list

# Ver versões específicas
pip show ryu setuptools eventlet

# Logs detalhados do sistema
dmesg | tail
```

## 📚 Próximos Passos

Agora que o Ryu está funcionando:
1. ✅ Implementar switch L2 com aprendizado MAC
2. ✅ Experimentar com roteamento IP básico
3. ✅ Personalizar regras de encaminhamento
4. ✅ Avaliar performance com diferentes topologias

---

**🎉 Parabéns! Você agora tem um ambiente Ryu SDN totalmente funcional!**

---

*Criado baseado em experiência real de instalação e troubleshooting. Todos os erros mencionados foram realmente encontrados e resolvidos durante o processo de instalação.*
