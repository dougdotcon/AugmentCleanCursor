#!/usr/bin/env python3
"""
Script de inicialização - AugmentCode-Free GUI
Este arquivo está obsoleto, use main.py para iniciar a GUI
"""

import sys

print("⚠️  Aviso: run_gui.py está obsoleto")
print("✅ Use main.py para iniciar a interface GUI")
print("💡 Comando: python main.py")
print()

# Inicia automaticamente o main.py
try:
    from main import main
    main()
except Exception as e:
    print(f"❌ Falha ao iniciar: {e}")
    print("Execute diretamente: python main.py")
    sys.exit(1)
