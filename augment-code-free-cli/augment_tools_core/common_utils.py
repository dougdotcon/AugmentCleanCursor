"""
Funções utilitárias comuns para Augment Tools Core
"""
import os
import platform
import shutil
import uuid
from pathlib import Path
from typing import Dict, Union # Adicionado Union para type hinting

try:
    from colorama import init, Fore, Style
    init(autoreset=True)  # Inicializa colorama para suporte ao Windows e reset automático de estilos
    IS_COLORAMA_AVAILABLE = True
except ImportError:
    IS_COLORAMA_AVAILABLE = False

# --- Funções de Mensagem no Console ---
def print_message(prefix: str, message: str, color_code: str = "") -> None:
    """Função auxiliar para imprimir mensagens com cor opcional."""
    if IS_COLORAMA_AVAILABLE and color_code:
        print(f"{color_code}{prefix}{Style.RESET_ALL} {message}")
    else:
        print(f"{prefix} {message}")

def print_info(message: str) -> None:
    """Imprime uma mensagem informativa (azul se colorama estiver disponível)."""
    prefix = "[INFO]"
    color = Fore.BLUE if IS_COLORAMA_AVAILABLE else ""
    print_message(prefix, message, color)

def print_success(message: str) -> None:
    """Imprime uma mensagem de sucesso (verde se colorama estiver disponível)."""
    prefix = "[SUCCESS]"
    color = Fore.GREEN if IS_COLORAMA_AVAILABLE else ""
    print_message(prefix, message, color)

def print_warning(message: str) -> None:
    """Imprime uma mensagem de aviso (amarelo se colorama estiver disponível)."""
    prefix = "[WARNING]"
    color = Fore.YELLOW if IS_COLORAMA_AVAILABLE else ""
    print_message(prefix, message, color)

def print_error(message: str) -> None:
    """Imprime uma mensagem de erro (vermelho se colorama estiver disponível)."""
    prefix = "[ERROR]"
    color = Fore.RED if IS_COLORAMA_AVAILABLE else ""
    print_message(prefix, message, color)

# --- Funções de Caminho do VS Code ---
def get_os_specific_vscode_paths() -> Dict[str, Path]:
    """
    Determina e retorna caminhos específicos do sistema operacional para arquivos de configuração do VS Code.

    Returns:
        Um dicionário contendo caminhos 'state_db' e 'storage_json'.
    Raises:
        SystemExit: Se o sistema operacional não for suportado ou APPDATA não for encontrado no Windows.
    """
    system = platform.system()
    paths: Dict[str, Path] = {}

    try:
        if system == "Windows":
            appdata = os.environ.get("APPDATA")
            if not appdata:
                print_error("Variável de ambiente APPDATA não encontrada. Não é possível localizar dados do VS Code.")
                raise SystemExit(1)
            base_dir = Path(appdata) / "Code" / "User"
        elif system == "Darwin":  # macOS
            base_dir = Path.home() / "Library" / "Application Support" / "Code" / "User"
        elif system == "Linux":
            base_dir = Path.home() / ".config" / "Code" / "User"
        else:
            print_error(f"Sistema operacional não suportado: {system}")
            raise SystemExit(1)

        paths["state_db"] = base_dir / "globalStorage" / "state.vscdb"
        paths["storage_json"] = base_dir / "globalStorage" / "storage.json"
        return paths
    except Exception as e:
        print_error(f"Falha ao determinar caminhos do VS Code: {e}")
        raise SystemExit(1)

# --- Função de Backup de Arquivo ---
def create_backup(file_path: Union[str, Path]) -> Union[Path, None]:
    """
    Cria um backup do arquivo especificado.

    Args:
        file_path: O caminho para o arquivo a ser feito backup.

    Returns:
        O caminho para o arquivo de backup se bem-sucedido, None caso contrário.
    """
    original_path = Path(file_path)
    if not original_path.exists():
        print_error(f"Arquivo não encontrado para backup: {original_path}")
        return None

    backup_path = original_path.with_suffix(original_path.suffix + ".backup")
    try:
        shutil.copy2(original_path, backup_path)
        print_success(f"Backup criado com sucesso em: {backup_path}")
        return backup_path
    except Exception as e:
        print_error(f"Falha ao criar backup para {original_path}: {e}")
        return None

# --- Funções de Geração de ID ---
def generate_new_machine_id() -> str:
    """Gera uma nova string hexadecimal de 64 caracteres para machineId."""
    return uuid.uuid4().hex + uuid.uuid4().hex

def generate_new_device_id() -> str:
    """Gera uma nova string UUID v4 padrão para devDeviceId."""
    return str(uuid.uuid4())

if __name__ == '__main__':
    # Teste rápido para as funções utilitárias
    print_info("Testando common_utils.py...")

    print_info("Exibindo caminhos do VS Code detectados:")
    try:
        vscode_paths = get_os_specific_vscode_paths()
        print_success(f"  State DB: {vscode_paths['state_db']}")
        print_success(f"  Storage JSON: {vscode_paths['storage_json']}")
    except SystemExit:
        print_warning("Não foi possível recuperar caminhos do VS Code neste sistema (esperado se executado em ambiente isolado).")


    print_info("Gerando IDs de exemplo:")
    machine_id = generate_new_machine_id()
    device_id = generate_new_device_id()
    print_success(f"  Machine ID gerado: {machine_id} (Comprimento: {len(machine_id)})")
    print_success(f"  Device ID gerado: {device_id}")

    # Para testar backup, você precisaria de um arquivo dummy.
    # Exemplo:
    # test_file = Path("dummy_test_file.txt")
    # with open(test_file, "w") as f:
    #     f.write("Este é um arquivo de teste para backup.")
    # backup_result = create_backup(test_file)
    # if backup_result:
    #     print_info(f"Teste de backup bem-sucedido. Backup em: {backup_result}")
    #     if backup_result.exists():
    #         backup_result.unlink() # Limpa backup
    # if test_file.exists():
    #     test_file.unlink() # Limpa arquivo de teste

    print_info("Testando tipos de mensagem:")
    print_success("Esta é uma mensagem de sucesso.")
    print_warning("Esta é uma mensagem de aviso.")
    print_error("Esta é uma mensagem de erro.")
    print_info("Testes do common_utils.py concluídos.")