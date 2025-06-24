import click
from pathlib import Path

# Assumindo que outros módulos estão no mesmo pacote (augment_tools_core)
from .common_utils import (
    get_os_specific_vscode_paths,
    print_info,
    print_success,
    print_error,
    print_warning
)
from .database_manager import clean_vscode_database
from .telemetry_manager import modify_vscode_telemetry_ids

@click.group(context_settings=dict(help_option_names=['-h', '--help']))
def main_cli():
    """
    AugmentCode-Free: Ferramentas de Manutenção do VS Code.
    Fornece utilitários para limpar bancos de dados do VS Code e modificar IDs de telemetria.
    """
    # Saudação inicial ou configuração pode ir aqui se necessário,
    # mas tipicamente grupos click não imprimem por conta própria.
    # print_info("Ferramentas AugmentCode-Free Inicializadas.") # Removido para saída CLI mais limpa
    pass

@main_cli.command("clean-db")
@click.option('--keyword', default='augment', show_default=True, help='Palavra-chave para pesquisar e remover do banco de dados (não diferencia maiúsculas/minúsculas).')
def clean_db_command(keyword: str):
    """Limpa o banco de dados de estado do VS Code (state.vscdb) removendo entradas que correspondem à palavra-chave."""
    print_info(f"Executando: Limpeza do Banco de Dados (palavra-chave: '{keyword}')")
    paths = get_os_specific_vscode_paths()
    if not paths:
        print_error("Não foi possível determinar caminhos do VS Code para seu sistema operacional. Abortando.")
        return

    db_path_str = paths.get("state_db")
    if not db_path_str:
        print_error("Caminho state.vscdb do VS Code não encontrado na configuração específica do sistema operacional. Abortando.")
        return
    
    db_path = Path(db_path_str)
    if not db_path.is_file(): # Verificação mais específica que exists()
        print_warning(f"Arquivo de banco de dados não existe ou não é um arquivo no local esperado: {db_path}")
        print_error("Abortando limpeza do banco de dados pois o arquivo de banco de dados não foi encontrado.")
        return

    if clean_vscode_database(db_path, keyword):
        # Mensagens de sucesso/erro agora são principalmente tratadas dentro de clean_vscode_database
        print_info("Processo de limpeza do banco de dados finalizado.") 
    else:
        print_error("Processo de limpeza do banco de dados reportou erros. Verifique mensagens anteriores.")

@main_cli.command("modify-ids")
def modify_ids_command():
    """Modifica IDs de telemetria do VS Code (machineId, devDeviceId) em storage.json."""
    print_info("Executando: Modificação de ID de Telemetria")
    paths = get_os_specific_vscode_paths()
    if not paths:
        print_error("Não foi possível determinar caminhos do VS Code para seu sistema operacional. Abortando.")
        return

    storage_path_str = paths.get("storage_json")
    if not storage_path_str:
        print_error("Caminho storage.json do VS Code não encontrado na configuração específica do sistema operacional. Abortando.")
        return

    storage_path = Path(storage_path_str)
    if not storage_path.is_file(): # Verificação mais específica
        print_warning(f"Arquivo de armazenamento não existe ou não é um arquivo no local esperado: {storage_path}")
        print_error("Abortando modificação de ID de telemetria pois o arquivo de armazenamento não foi encontrado.")
        return

    if modify_vscode_telemetry_ids(storage_path):
        print_info("Processo de modificação de ID de telemetria finalizado.")
    else:
        print_error("Processo de modificação de ID de telemetria reportou erros. Verifique mensagens anteriores.")

@main_cli.command("run-all")
@click.option('--keyword', default='augment', show_default=True, help='Palavra-chave para limpeza do banco de dados (não diferencia maiúsculas/minúsculas).')
@click.pass_context # Para chamar outros comandos
def run_all_command(ctx, keyword: str):
    """Executa todas as ferramentas disponíveis: clean-db e depois modify-ids."""
    print_info("Executando: Executar Todas as Ferramentas")
    
    print_info("--- Etapa 1: Limpeza do Banco de Dados ---")
    # Usando try-except para permitir que o segundo comando execute mesmo se o primeiro falhar
    try:
        ctx.invoke(clean_db_command, keyword=keyword)
    except Exception as e:
        print_error(f"Ocorreu um erro durante a etapa de limpeza do banco de dados: {e}")
        print_warning("Prosseguindo para a próxima etapa apesar do erro.")
    
    print_info("--- Etapa 2: Modificação de ID de Telemetria ---")
    try:
        ctx.invoke(modify_ids_command)
    except Exception as e:
        print_error(f"Ocorreu um erro durante a etapa de modificação de ID de telemetria: {e}")

    print_success("Todas as ferramentas finalizaram sua sequência de execução.")

if __name__ == '__main__':
    # Isso torna o script executável diretamente para desenvolvimento/teste.
    # Exemplo: python -m augment_tools_core.cli clean-db
    # Ou, se no diretório augment_tools_core: python cli.py clean-db
    # A forma típica de distribuir um app click é via um entry point em setup.py
    main_cli()