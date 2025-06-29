#!/usr/bin/env python3
"""
Teste simples do Ryu - verificação de funcionamento
"""

print("="*50)
print("TESTE DO AMBIENTE RYU")
print("="*50)

# Teste 1: Importação básica do Ryu
print("[TESTE 1] Importando módulos do Ryu...")
try:
    import ryu
    print("✓ ryu - OK")
    
    from ryu.base import app_manager
    print("✓ ryu.base.app_manager - OK")
    
    from ryu.controller import ofp_event
    print("✓ ryu.controller.ofp_event - OK")
    
    from ryu.ofproto import ofproto_v1_3
    print("✓ ryu.ofproto.ofproto_v1_3 - OK")
    
    print("\n[RESULTADO] ✓ Todos os módulos do Ryu foram importados com sucesso!")
    
except ImportError as e:
    print(f"✗ Erro na importação: {e}")
    exit(1)

# Teste 2: Verificação de informações do Ryu
print(f"\n[TESTE 2] Ryu instalado em: {ryu.__file__}")
try:
    import pkg_resources
    version = pkg_resources.get_distribution("ryu").version
    print(f"Versão do Ryu: {version}")
except:
    print("Versão: Não foi possível determinar (mas está funcionando)")

# Teste 3: Criação básica de uma aplicação
print("\n[TESTE 3] Testando criação de aplicação básica...")
try:
    class TestApp(app_manager.RyuApp):
        def __init__(self, *args, **kwargs):
            super(TestApp, self).__init__(*args, **kwargs)
    
    print("✓ Classe de aplicação criada com sucesso!")
    
except Exception as e:
    print(f"✗ Erro ao criar aplicação: {e}")
    exit(1)

print("\n" + "="*50)
print("CONCLUSÃO: RYU ESTÁ FUNCIONANDO CORRETAMENTE!")
print("="*50)
print("\nPara executar o controlador simple_switch_13.py:")
print("1. Ative o ambiente virtual: source ryu_env/bin/activate")
print("2. Execute: ryu-manager simple_switch_13.py")
print("\nO Ryu irá aguardar conexões de switches OpenFlow na porta 6633.")
