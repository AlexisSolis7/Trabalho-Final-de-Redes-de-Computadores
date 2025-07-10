from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, CONFIG_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.topology import event, switches
from ryu.topology.api import get_switch, get_link, get_host
import networkx as nx

class DijkstraSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(DijkstraSwitch13, self).__init__(*args, **kwargs)
        # Estruturas de dados para Dijkstra
        self.mac_to_port = {}      # {dpid: {mac: port}}
        self.topology_graph = nx.Graph()  # Grafo da topologia
        self.switches = {}         # {dpid: switch_object}
        self.hosts = {}           # {mac: (dpid, port)}
        self.links = {}           # {(src_dpid, dst_dpid): (src_port, dst_port)}
        
        self.logger.info(" Controlador Dijkstra iniciado!")

    @set_ev_cls(event.EventSwitchEnter)
    def switch_enter_handler(self, ev):
        """Detecta quando um switch se conecta"""
        switch = ev.switch
        dpid = switch.dp.id
        self.switches[dpid] = switch
        self.topology_graph.add_node(dpid)
        self.logger.info("🔗 Switch conectado: DPID=%s", dpid)
        self._update_topology()

    @set_ev_cls(event.EventLinkAdd)
    def link_add_handler(self, ev):
        """Detecta quando um link é adicionado"""
        link = ev.link
        src_dpid = link.src.dpid
        dst_dpid = link.dst.dpid
        src_port = link.src.port_no
        dst_port = link.dst.port_no
        
        # Adicionar link ao grafo (peso = 1 para todos os links)
        self.topology_graph.add_edge(src_dpid, dst_dpid, weight=1)
        self.links[(src_dpid, dst_dpid)] = (src_port, dst_port)
        self.links[(dst_dpid, src_dpid)] = (dst_port, src_port)
        
        self.logger.info("🔗 Link adicionado: %s:%s -> %s:%s", 
                        src_dpid, src_port, dst_dpid, dst_port)
        self._update_topology()

    def _update_topology(self):
        """Atualiza o conhecimento da topologia"""
        switch_list = get_switch(self, None)
        self.switches = {sw.dp.id: sw for sw in switch_list}
        
        link_list = get_link(self, None)
        self.topology_graph.clear()
        self.links.clear()
        
        # Adicionar switches ao grafo
        for switch in switch_list:
            self.topology_graph.add_node(switch.dp.id)
        
        # Adicionar links ao grafo
        for link in link_list:
            src_dpid = link.src.dpid
            dst_dpid = link.dst.dpid
            src_port = link.src.port_no
            dst_port = link.dst.port_no
            
            self.topology_graph.add_edge(src_dpid, dst_dpid, weight=1)
            self.links[(src_dpid, dst_dpid)] = (src_port, dst_port)
        
        self.logger.info("📊 Topologia atualizada: %d switches, %d links", 
                        len(self.switches), len(self.links)//2)

    def dijkstra_shortest_path(self, src_dpid, dst_dpid):
        """
        Implementação do algoritmo de Dijkstra
        Retorna: lista de switches no caminho mais curto
        """
        try:
            if src_dpid == dst_dpid:
                return [src_dpid]
            
            # Usar NetworkX para calcular caminho mais curto
            path = nx.shortest_path(self.topology_graph, src_dpid, dst_dpid, weight='weight')
            self.logger.info("🛤️  Dijkstra: Caminho %s -> %s: %s", src_dpid, dst_dpid, path)
            return path
        except nx.NetworkXNoPath:
            self.logger.warning("❌ Dijkstra: Não há caminho entre %s e %s", src_dpid, dst_dpid)
            return None
        except Exception as e:
            self.logger.error("❌ Erro no Dijkstra: %s", e)
            return None

    def install_path(self, path, src_mac, dst_mac, first_port, last_port):
        """
        Instala flows ao longo do caminho calculado por Dijkstra
        """
        if not path or len(path) < 1:
            return False
        
        for i in range(len(path)):
            dpid = path[i]
            datapath = self.switches[dpid].dp
            ofproto = datapath.ofproto
            parser = datapath.ofproto_parser
            
            # Determinar porta de saída
            if i == len(path) - 1:  # Último switch
                out_port = last_port
            else:  # Switch intermediário
                next_dpid = path[i + 1]
                out_port = self.links.get((dpid, next_dpid), [None])[0]
            
            if out_port is None:
                self.logger.error("❌ Porta não encontrada para switch %s", dpid)
                continue
            
            # Criar match e actions
            match = parser.OFPMatch(eth_dst=dst_mac)
            actions = [parser.OFPActionOutput(out_port)]
            
            # Instalar flow
            self.add_flow(datapath, 10, match, actions)
            self.logger.info("📥 Flow instalado: Switch=%s, dst=%s -> porta=%s", 
                           dpid, dst_mac, out_port)
        
        return True

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        """
        Processa PacketIn usando algoritmo de Dijkstra para roteamento
        """
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']
        dpid = datapath.id

        # Analisar pacote Ethernet
        pkt = packet.Packet(msg.data)
        eth_pkt = pkt.get_protocol(ethernet.ethernet)
        
        if eth_pkt is None:
            return
        
        dst_mac = eth_pkt.dst
        src_mac = eth_pkt.src

        # Filtrar pacotes de descoberta (LLDP, etc.)
        if eth_pkt.ethertype == 0x88cc:  # LLDP
            return

        self.logger.info("📦 PacketIn: Switch=%s, MAC src=%s, dst=%s, porta=%s", 
                        dpid, src_mac, dst_mac, in_port)

        # Aprender localização do MAC origem
        self.mac_to_port.setdefault(dpid, {})
        self.mac_to_port[dpid][src_mac] = in_port
        self.hosts[src_mac] = (dpid, in_port)

        # Verificar se conhecemos o destino
        if dst_mac not in self.hosts:
            self.logger.info("🌊 MAC destino %s desconhecido - FLOOD", dst_mac)
            # Flood para descobrir o destino
            actions = [parser.OFPActionOutput(ofproto.OFPP_FLOOD)]
            out = parser.OFPPacketOut(
                datapath=datapath, buffer_id=msg.buffer_id, 
                in_port=in_port, actions=actions, data=msg.data)
            datapath.send_msg(out)
            return

        # Destino conhecido - usar Dijkstra para encontrar caminho
        dst_dpid, dst_port = self.hosts[dst_mac]
        src_dpid = dpid

        self.logger.info("🎯 Calculando caminho: %s (switch %s) -> %s (switch %s)", 
                        src_mac, src_dpid, dst_mac, dst_dpid)

        # Calcular caminho mais curto com Dijkstra
        path = self.dijkstra_shortest_path(src_dpid, dst_dpid)
        
        if path is None:
            self.logger.warning("❌ Caminho não encontrado - FLOOD")
            actions = [parser.OFPActionOutput(ofproto.OFPP_FLOOD)]
        else:
            # Instalar flows ao longo do caminho
            self.install_path(path, src_mac, dst_mac, in_port, dst_port)
            
            # Encaminhar este pacote
            if len(path) == 1:  # Mesmo switch
                out_port = dst_port
            else:  # Próximo switch no caminho
                next_dpid = path[1]
                out_port = self.links.get((src_dpid, next_dpid), [None])[0]
            
            if out_port is None:
                self.logger.error("❌ Porta não encontrada")
                actions = [parser.OFPActionOutput(ofproto.OFPP_FLOOD)]
            else:
                actions = [parser.OFPActionOutput(out_port)]
                self.logger.info("📤 Encaminhando pacote para porta %s", out_port)

        # Enviar PacketOut
        out = parser.OFPPacketOut(
            datapath=datapath, buffer_id=msg.buffer_id,
            in_port=in_port, actions=actions, data=msg.data)
        datapath.send_msg(out)

    def add_flow(self, datapath, priority, match, actions, timeout=0):
        """
        Adiciona flow entry no switch
        """
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Criar instrução para adicionar à tabela de fluxo
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]

        # Criar mensagem MOD_FLOW com timeout opcional
        mod = parser.OFPFlowMod(
            datapath=datapath, 
            priority=priority, 
            match=match,
            instructions=inst,
            idle_timeout=timeout,
            hard_timeout=timeout * 2 if timeout > 0 else 0
        )

        # Enviar a mensagem
        datapath.send_msg(mod)

    def show_topology_stats(self):
        """
        Mostra estatísticas da topologia atual
        """
        self.logger.info("📊 === ESTATÍSTICAS DA TOPOLOGIA ===")
        self.logger.info("🔢 Switches: %d", len(self.switches))
        self.logger.info("🔗 Links: %d", len(self.links)//2)
        self.logger.info("💻 Hosts conhecidos: %d", len(self.hosts))
        
        for mac, (dpid, port) in self.hosts.items():
            self.logger.info("   🖥️  %s -> Switch %s, Porta %s", mac, dpid, port)
        
        # Mostrar caminhos possíveis
        switch_ids = list(self.switches.keys())
        for i, src in enumerate(switch_ids):
            for dst in switch_ids[i+1:]:
                try:
                    path = nx.shortest_path(self.topology_graph, src, dst)
                    distance = nx.shortest_path_length(self.topology_graph, src, dst)
                    self.logger.info("🛤️  Caminho %s -> %s: %s (distância: %d)", 
                                   src, dst, path, distance)
                except:
                    pass

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        """
        Instala flow padrão para enviar pacotes desconhecidos ao controlador
        """
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Instalar table-miss flow entry
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                        ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)
        
        self.logger.info("🔧 Flow padrão instalado no switch %s", datapath.id)
