#!/usr/bin/env python3
"""
AugmentCode-Free - Programa Principal
Inicia a interface gráfica do usuário

Este é o programa principal de inicialização das ferramentas AugmentCode-Free.
Clique duas vezes neste arquivo ou execute 'python main.py' no terminal para iniciar a interface GUI.

Funcionalidades incluem:
- Limpeza do banco de dados do VS Code
- Modificação dos IDs de telemetria do VS Code  
- Execução de todas as ferramentas disponíveis
"""

import sys
import os
from pathlib import Path

def main():
    """Função principal - Inicia a aplicação GUI"""
    print("=" * 50)
    print("🚀 Iniciando ferramentas AugmentCode-Free...")
    print("=" * 50)
    print()
    
    # Adiciona o diretório atual ao caminho do Python
    current_dir = Path(__file__).parent
    sys.path.insert(0, str(current_dir))
    
    try:
        # Importa e inicia a GUI
        from gui import main as gui_main
        
        print("✅ Iniciando interface gráfica...")
        print("💡 Dica: Se a interface não aparecer, verifique se há firewall ou software de segurança bloqueando")
        print()
        
        # Inicia a GUI
        gui_main()
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print()
        print("🔧 Soluções:")
        print("1. Certifique-se de que todas as dependências estão instaladas: pip install -r requirements.txt")
        print("2. Certifique-se de que a versão do Python é 3.7 ou superior")
        print("3. Certifique-se de que todos os arquivos do projeto estão no mesmo diretório")
        print("4. Para outros problemas, abra uma issue")
        input("\nPressione Enter para sair...")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Erro ao iniciar a GUI: {e}")
        print()
        print("🔧 Possíveis soluções:")
        print("1. Reinstale as dependências: pip install -r requirements.txt")
        print("2. Verifique se o ambiente Python está configurado corretamente")
        print("3. Certifique-se de que há permissões suficientes do sistema")
        print("4. Para outros problemas, abra uma issue")
        input("\nPressione Enter para sair...")
        sys.exit(1)


if __name__ == "__main__":
    main()
