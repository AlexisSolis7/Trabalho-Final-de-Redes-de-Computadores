#!/usr/bin/env python3
"""
Simple SDN Controller Test Script
Este é um controlador básico simulado para testes.
"""

import socket
import time
import threading

class SimpleController:
    def __init__(self, host='localhost', port=6633):
        self.host = host
        self.port = port
        self.running = False
        
    def start(self):
        """Inicia o controlador simulado"""
        self.running = True
        print(f"[INFO] Iniciando controlador SDN em {self.host}:{self.port}")
        print("[INFO] Aguardando conexões de switches...")
        
        try:
            # Simula um servidor básico
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            
            while self.running:
                try:
                    server_socket.settimeout(1.0)
                    client_socket, address = server_socket.accept()
                    print(f"[INFO] Conexão recebida de {address}")
                    
                    # Simula processamento de mensagens OpenFlow
                    threading.Thread(
                        target=self.handle_switch,
                        args=(client_socket, address)
                    ).start()
                    
                except socket.timeout:
                    continue
                except Exception as e:
                    if self.running:
                        print(f"[ERROR] Erro no servidor: {e}")
                        
        except KeyboardInterrupt:
            print("\n[INFO] Controlador interrompido pelo usuário")
        except Exception as e:
            print(f"[ERROR] Erro ao iniciar controlador: {e}")
        finally:
            server_socket.close()
            print("[INFO] Controlador encerrado")
    
    def handle_switch(self, client_socket, address):
        """Processa mensagens de um switch conectado"""
        try:
            print(f"[INFO] Processando switch {address}")
            
            # Simula troca de mensagens básicas
            while self.running:
                data = client_socket.recv(1024)
                if not data:
                    break
                    
                print(f"[DEBUG] Mensagem recebida de {address}: {len(data)} bytes")
                
                # Simula resposta do controlador
                response = b"Controller Response"
                client_socket.send(response)
                
        except Exception as e:
            print(f"[ERROR] Erro ao processar switch {address}: {e}")
        finally:
            client_socket.close()
            print(f"[INFO] Switch {address} desconectado")
    
    def stop(self):
        """Para o controlador"""
        self.running = False

def test_environment():
    """Testa o ambiente SDN básico"""
    print("="*50)
    print("TESTE DO AMBIENTE SDN")
    print("="*50)
    
    # Teste 1: Verificar Python
    print("[TESTE 1] Verificando Python...")
    import sys
    print(f"✓ Python {sys.version}")
    
    # Teste 2: Verificar módulos necessários
    print("\n[TESTE 2] Verificando módulos...")
    try:
        import socket
        print("✓ socket - OK")
        import threading
        print("✓ threading - OK")
        import time
        print("✓ time - OK")
    except ImportError as e:
        print(f"✗ Erro: {e}")
        return False
    
    # Teste 3: Teste de conectividade
    print("\n[TESTE 3] Teste de conectividade...")
    try:
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_socket.bind(('localhost', 0))  # Bind em porta aleatória
        port = test_socket.getsockname()[1]
        test_socket.close()
        print(f"✓ Porta {port} disponível para binding")
    except Exception as e:
        print(f"✗ Erro de conectividade: {e}")
        return False
    
    print("\n[RESULTADO] Ambiente básico está funcionando!")
    print("Você pode usar este controlador simulado para testes básicos.")
    return True

if __name__ == "__main__":
    print("Simple SDN Controller - Ambiente de Teste")
    print("Pressione Ctrl+C para parar\n")
    
    # Testa o ambiente primeiro
    if test_environment():
        print("\n" + "="*50)
        print("INICIANDO CONTROLADOR")
        print("="*50)
        
        controller = SimpleController()
        try:
            controller.start()
        except KeyboardInterrupt:
            controller.stop()
