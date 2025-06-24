"""
Command-line interface for Augment VIP
"""

import os
import sys
import subprocess
import click
from pathlib import Path

try:
    from stem import Signal
    from stem.control import Controller
    STEM_AVAILABLE = True
except ImportError:
    STEM_AVAILABLE = False

from . import __version__
from .utils import info, success, error, warning
from .db_cleaner import clean_vscode_db
from .id_modifier import modify_telemetry_ids

@click.group()
@click.version_option(version=__version__)
def cli():
    """Augment VIP - Tools for managing VS Code settings"""
    pass

@cli.command()
def clean():
    """Clean VS Code databases by removing Augment-related entries"""
    if clean_vscode_db():
        success("Database cleaning completed successfully")
    else:
        error("Database cleaning failed")
        sys.exit(1)

@cli.command()
def modify_ids():
    """Modify VS Code telemetry IDs"""
    if modify_telemetry_ids():
        success("Telemetry ID modification completed successfully")
    else:
        error("Telemetry ID modification failed")
        sys.exit(1)

@cli.command()
def all():
    """Run all tools (clean and modify IDs)"""
    info("Running all tools...")
    
    clean_result = clean_vscode_db()
    modify_result = modify_telemetry_ids()
    
    if clean_result and modify_result:
        success("All operations completed successfully")
    else:
        error("Some operations failed")
        sys.exit(1)

@cli.command()
@click.option('--socks-port', default=9050, help="Porta SOCKS do Tor")
@click.option('--control-port', default=9051, help="Porta de controle do Tor")
@click.option('--tor-path', default='tor', help="Caminho para o executável Tor")
def mask_ip(socks_port, control_port, tor_path):
    """
    Inicia um proxy Tor e exporta HTTP_PROXY/HTTPS_PROXY.
    """
    if not STEM_AVAILABLE:
        error("Biblioteca 'stem' não está disponível. Instale com: pip install stem")
        sys.exit(1)
    
    # 1. Inicia Tor (em background)
    info(f"Iniciando Tor na porta SOCKS {socks_port}...")
    try:
        tor_proc = subprocess.Popen([
            tor_path,
            f'--SocksPort', str(socks_port),
            f'--ControlPort', str(control_port),
            '--Log', 'notice stdout'
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Aguarda um pouco para o Tor inicializar
        import time
        time.sleep(3)
        
        success("Tor iniciado com sucesso")
    except FileNotFoundError:
        error(f"Executável Tor não encontrado em '{tor_path}'. Certifique-se de que o Tor está instalado.")
        sys.exit(1)
    except Exception as e:
        error(f"Erro ao iniciar Tor: {e}")
        sys.exit(1)

    # 2. Gera novo circuito (opcional, para trocar IP imediatamente)
    try:
        with Controller.from_port(port=control_port) as controller:
            controller.authenticate()  # se tiver senha, ajustar aqui
            controller.signal(Signal.NEWNYM)
            info("Solicitado novo circuito Tor (IP trocado).")
    except Exception as e:
        warning(f"Não foi possível trocar circuito Tor: {e}")

    # 3. Exporta variáveis de ambiente
    proxy = f"socks5h://127.0.0.1:{socks_port}"
    os.environ['HTTP_PROXY'] = proxy
    os.environ['HTTPS_PROXY'] = proxy
    success(f"Variáveis HTTP_PROXY e HTTPS_PROXY definidas para {proxy}")
    info("Lembre-se de manter esse processo em execução enquanto usar as outras ferramentas.")
    info("Para encerrar o Tor, use Ctrl+C ou encerre o processo manualmente.")

@cli.command()
def clear_network():
    """
    Limpa cache de DNS e resets de rede (Windows/macOS/Linux).
    """
    info("Executando limpeza de cache e reset de rede...")
    try:
        if sys.platform.startswith('win'):
            subprocess.run(['ipconfig', '/flushdns'], check=True)
            success("Cache DNS limpo (Windows).")
        elif sys.platform == 'darwin':
            subprocess.run(['sudo', 'killall', '-HUP', 'mDNSResponder'], check=True)
            success("Cache DNS limpo (macOS).")
        else:  # assume Linux
            # systemd-resolve
            subprocess.run(['sudo', 'systemd-resolve', '--flush-caches'], check=True)
            success("Cache DNS limpo (Linux).")
    except subprocess.CalledProcessError as e:
        error(f"Falha ao limpar cache de DNS: {e}")
        sys.exit(1)
    except FileNotFoundError:
        error("Comando não encontrado. Certifique-se de que está executando com privilégios adequados.")
        sys.exit(1)
    
    success("Limpeza de caches concluída.")

@cli.command()
def install():
    """Install Augment VIP"""
    info("Installing Augment VIP...")
    
    # This is a placeholder for any installation steps
    # In Python, most of the installation is handled by pip/setup.py
    
    success("Augment VIP installed successfully")
    info("You can now use the following commands:")
    info("  - augment-vip clean: Clean VS Code databases")
    info("  - augment-vip modify-ids: Modify telemetry IDs")
    info("  - augment-vip all: Run all tools")
    info("  - augment-vip mask-ip: Start Tor proxy for IP masking")
    info("  - augment-vip clear-network: Clear DNS and network caches")

def main():
    """Main entry point for the CLI"""
    try:
        cli()
    except Exception as e:
        error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
