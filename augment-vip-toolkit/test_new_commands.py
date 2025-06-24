#!/usr/bin/env python3
"""
Script de teste para os novos comandos mask-ip e clear-network
"""

import subprocess
import sys
import os

def test_help():
    """Testa se os novos comandos aparecem no help"""
    print("Testando help dos novos comandos...")
    
    try:
        result = subprocess.run(['augment-vip', '--help'], 
                              capture_output=True, text=True, check=True)
        
        if 'mask-ip' in result.stdout and 'clear-network' in result.stdout:
            print("✅ Comandos mask-ip e clear-network aparecem no help")
            return True
        else:
            print("❌ Comandos não aparecem no help")
            return False
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar help: {e}")
        return False

def test_clear_network_help():
    """Testa o help do comando clear-network"""
    print("\nTestando help do comando clear-network...")
    
    try:
        result = subprocess.run(['augment-vip', 'clear-network', '--help'], 
                              capture_output=True, text=True, check=True)
        
        if 'Limpa cache de DNS' in result.stdout:
            print("✅ Help do clear-network está correto")
            return True
        else:
            print("❌ Help do clear-network não está correto")
            return False
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar help do clear-network: {e}")
        return False

def test_mask_ip_help():
    """Testa o help do comando mask-ip"""
    print("\nTestando help do comando mask-ip...")
    
    try:
        result = subprocess.run(['augment-vip', 'mask-ip', '--help'], 
                              capture_output=True, text=True, check=True)
        
        if 'Inicia um proxy Tor' in result.stdout:
            print("✅ Help do mask-ip está correto")
            return True
        else:
            print("❌ Help do mask-ip não está correto")
            return False
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar help do mask-ip: {e}")
        return False

def test_dependencies():
    """Testa se as dependências estão instaladas"""
    print("\nTestando dependências...")
    
    try:
        import stem
        print("✅ Biblioteca 'stem' está disponível")
        stem_available = True
    except ImportError:
        print("❌ Biblioteca 'stem' não está disponível")
        stem_available = False
    
    try:
        import requests
        print("✅ Biblioteca 'requests' está disponível")
        requests_available = True
    except ImportError:
        print("❌ Biblioteca 'requests' não está disponível")
        requests_available = False
    
    return stem_available and requests_available

def main():
    """Função principal de teste"""
    print("🧪 Testando novos comandos do Augment VIP")
    print("=" * 50)
    
    tests = [
        test_help,
        test_clear_network_help,
        test_mask_ip_help,
        test_dependencies
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"Resultados: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 Todos os testes passaram!")
        return 0
    else:
        print("⚠️  Alguns testes falharam")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 