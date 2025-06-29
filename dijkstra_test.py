#!/usr/bin/env python3
"""
Script de teste para o controlador Dijkstra
Cria uma topologia em árvore para testar o algoritmo
"""

from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.topo import Topo
from mininet.log import setLogLevel
from mininet.cli import CLI

class TreeTopo(Topo):
    """
    Topologia em árvore para testar Dijkstra
    
         h1     h2
          |     |
         s1 --- s2 --- s3
                |      |
               h3     h4
    """
    def build(self):
        # Adicionar switches
        s1 = self.addSwitch('s1', dpid='0000000000000001')
        s2 = self.addSwitch('s2', dpid='0000000000000002')
        s3 = self.addSwitch('s3', dpid='0000000000000003')
        
        # Adicionar hosts
        h1 = self.addHost('h1', mac='00:00:00:00:00:01', ip='10.0.0.1/24')
        h2 = self.addHost('h2', mac='00:00:00:00:00:02', ip='10.0.0.2/24')
        h3 = self.addHost('h3', mac='00:00:00:00:00:03', ip='10.0.0.3/24')
        h4 = self.addHost('h4', mac='00:00:00:00:00:04', ip='10.0.0.4/24')
        
        # Adicionar links
        self.addLink(h1, s1)  # h1 -> s1
        self.addLink(h2, s2)  # h2 -> s2
        self.addLink(h3, s2)  # h3 -> s2
        self.addLink(h4, s3)  # h4 -> s3
        
        # Links entre switches
        self.addLink(s1, s2)  # s1 <-> s2
        self.addLink(s2, s3)  # s2 <-> s3

class LinearTopo(Topo):
    """
    Topologia linear para testar Dijkstra
    h1 - s1 - s2 - s3 - h2
    """
    def build(self):
        # Switches
        s1 = self.addSwitch('s1', dpid='0000000000000001')
        s2 = self.addSwitch('s2', dpid='0000000000000002')
        s3 = self.addSwitch('s3', dpid='0000000000000003')
        
        # Hosts
        h1 = self.addHost('h1', mac='00:00:00:00:00:01', ip='10.0.0.1/24')
        h2 = self.addHost('h2', mac='00:00:00:00:00:02', ip='10.0.0.2/24')
        
        # Links
        self.addLink(h1, s1)
        self.addLink(s1, s2)
        self.addLink(s2, s3)
        self.addLink(s3, h2)

def run_dijkstra_test():
    """
    Executa testes do controlador Dijkstra
    """
    setLogLevel('info')
    
    print("🚀 Iniciando teste do Controlador Dijkstra")
    print("=" * 50)
    
    # Escolher topologia
    print("Escolha a topologia:")
    print("1) Árvore (4 hosts, 3 switches)")
    print("2) Linear (2 hosts, 3 switches)")
    
    choice = input("Digite sua escolha (1-2): ").strip()
    
    if choice == "1":
        topo = TreeTopo()
        print("📐 Topologia: Árvore")
    elif choice == "2":
        topo = LinearTopo()
        print("📐 Topologia: Linear")
    else:
        print("❌ Opção inválida, usando árvore")
        topo = TreeTopo()
    
    # Criar controlador remoto
    controller = RemoteController('c0', ip='127.0.0.1', port=6633)
    
    # Criar rede
    net = Mininet(topo=topo, controller=controller)
    
    try:
        # Iniciar rede
        net.start()
        print("✅ Rede iniciada")
        
        # Aguardar convergência
        print("⏳ Aguardando descoberta da topologia...")
        import time
        time.sleep(5)
        
        # Testes automáticos
        print("\n🧪 Executando testes automáticos...")
        
        # Teste 1: Conectividade básica
        print("\n1️⃣ Teste de conectividade:")
        result = net.pingAll()
        if result == 0:
            print("✅ Todos os hosts se comunicam")
        else:
            print(f"⚠️ {result}% de perda de pacotes")
        
        # Teste 2: Caminhos específicos
        print("\n2️⃣ Teste de caminhos específicos:")
        hosts = net.hosts
        if len(hosts) >= 2:
            h1, h2 = hosts[0], hosts[1]
            print(f"🔗 Testando {h1.name} -> {h2.name}")
            result = net.ping([h1, h2])
            print(f"📊 Resultado: {result}% perda")
        
        # Teste 3: Iperf (se disponível)
        print("\n3️⃣ Teste de throughput:")
        if len(hosts) >= 2:
            try:
                result = net.iperf([hosts[0], hosts[1]], seconds=5)
                print(f"📈 Throughput: {result}")
            except:
                print("⚠️ iperf não disponível")
        
        # CLI interativo
        print("\n🖥️ Entrando no modo interativo...")
        print("Comandos úteis:")
        print("  pingall         - Testa conectividade")
        print("  h1 ping h2      - Ping específico")
        print("  dump            - Mostra topologia")
        print("  links           - Mostra links")
        print("  exit            - Sair")
        
        CLI(net)
        
    except KeyboardInterrupt:
        print("\n🛑 Teste interrompido pelo usuário")
    finally:
        print("🧹 Limpando rede...")
        net.stop()

if __name__ == '__main__':
    run_dijkstra_test()
