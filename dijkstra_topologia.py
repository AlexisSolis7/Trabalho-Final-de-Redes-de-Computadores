#!/usr/bin/env python3
"""
Topologia de Teste para Controlador Dijkstra
Cria diferentes topologias para testar o algoritmo de shortest path
"""

from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.topo import Topo
from mininet.log import setLogLevel
from mininet.cli import CLI

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

class LinearTestTopo(Topo):
    """
    Topologia linear simples para testar Dijkstra
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
    Executa teste do controlador Dijkstra
    """
    print("="*60)
    print("🚀 TESTE DO CONTROLADOR DIJKSTRA")
    print("="*60)
    
    # Configurar log level
    setLogLevel('info')
    
    print("\nEscolha a topologia para teste:")
    print("1) Topologia Complexa (5 switches, 3 hosts, múltiplos caminhos)")
    print("2) Topologia Linear (3 switches, 2 hosts, caminho único)")
    
    choice = input("\nDigite sua escolha (1 ou 2): ").strip()
    
    if choice == "1":
        print("\n🌐 Iniciando topologia complexa...")
        topo = DijkstraTestTopo()
        topo_name = "Complexa"
    elif choice == "2":
        print("\n🌐 Iniciando topologia linear...")
        topo = LinearTestTopo()
        topo_name = "Linear"
    else:
        print("\n🌐 Opção inválida! Usando topologia complexa...")
        topo = DijkstraTestTopo()
        topo_name = "Complexa"
    
    # Criar controlador remoto (deve estar rodando na porta 6633)
    controller = RemoteController('c0', ip='127.0.0.1', port=6633)
    
    # Criar rede Mininet
    net = Mininet(topo=topo, controller=controller)
    
    print(f"\n⚡ Iniciando rede com topologia {topo_name}...")
    net.start()
    
    print("\n📊 Informações da rede:")
    print("- Controlador: 127.0.0.1:6633")
    print("- Topologia:", topo_name)
    
    if choice == "1":
        print("- Hosts: h1(10.0.0.1), h2(10.0.0.2), h3(10.0.0.3)")
        print("- Switches: s1, s2, s3, s4, s5")
        print("\n🧪 Testes sugeridos:")
        print("   mininet> pingall")
        print("   mininet> h1 ping h2  # Caminho: s1->s2->s4")
        print("   mininet> h1 ping h3  # Caminho: s1->s3")
        print("   mininet> h2 ping h3  # Caminho: s4->s5->s3")
    else:
        print("- Hosts: h1(10.0.0.1), h2(10.0.0.2)")
        print("- Switches: s1, s2, s3")
        print("\n🧪 Testes sugeridos:")
        print("   mininet> pingall")
        print("   mininet> h1 ping h2  # Caminho: s1->s2->s3")
    
    print("\n" + "="*60)
    print("🎯 CLI DO MININET - Digite 'help' para ver comandos")
    print("🛑 Digite 'exit' para sair")
    print("="*60)
    
    # Iniciar CLI
    CLI(net)
    
    # Cleanup
    print("\n🧹 Finalizando rede...")
    net.stop()
    print("✅ Teste finalizado!")

if __name__ == '__main__':
    try:
        run_dijkstra_test()
    except KeyboardInterrupt:
        print("\n\n🛑 Teste interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        print(" Certifique-se de que o controlador esteja rodando!")
        print("   Terminal 1: ryu-manager dijkstra_controller.py")
