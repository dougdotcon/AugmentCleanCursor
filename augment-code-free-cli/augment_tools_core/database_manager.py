import sqlite3
import shutil
from pathlib import Path
import logging
from .common_utils import print_info, print_success, print_warning, print_error, create_backup

# Configura logging básico
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_vscode_database(db_path: Path, keyword: str = "augment") -> bool:
    """
    Limpa o banco de dados SQLite do VS Code removendo entradas que contêm uma palavra-chave específica.

    Args:
        db_path: Caminho para o banco de dados SQLite state.vscdb do VS Code.
        keyword: A palavra-chave para pesquisar na coluna 'key' da 'ItemTable'.
                 Entradas contendo esta palavra-chave serão removidas.

    Returns:
        True se o banco de dados foi limpo com sucesso ou se nenhuma limpeza foi necessária,
        False caso contrário.
    """
    if not db_path.exists():
        print_error(f"Arquivo de banco de dados não encontrado: {db_path}")
        return False

    print_info(f"Tentando limpar banco de dados do VS Code: {db_path}")
    print_info(f"Palavra-chave alvo para limpeza: '{keyword}'")

    backup_path = None
    try:
        # 1. Cria um backup
        print_info("Fazendo backup do banco de dados...")
        backup_path = create_backup(db_path)
        if not backup_path:
            # Mensagem de erro já impressa por create_backup
            return False
        print_success(f"Banco de dados feito backup com sucesso em: {backup_path}")

        # 2. Conecta ao banco de dados SQLite
        print_info(f"Conectando ao banco de dados: {db_path}")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        print_success("Conectado com sucesso ao banco de dados.")

        # 3. Encontra e conta entradas a serem deletadas
        query_select = f"SELECT key FROM ItemTable WHERE key LIKE ?"
        like_pattern = f"%{keyword}%"
        
        print_info(f"Pesquisando entradas com palavra-chave '{keyword}'...")
        cursor.execute(query_select, (like_pattern,))
        entries_to_delete = cursor.fetchall()
        
        num_entries_to_delete = len(entries_to_delete)

        if num_entries_to_delete == 0:
            print_success(f"Nenhuma entrada encontrada com palavra-chave '{keyword}'. Banco de dados já está limpo.")
            conn.close()
            return True

        print_warning(f"Encontradas {num_entries_to_delete} entradas contendo '{keyword}':")
        for i, entry in enumerate(entries_to_delete):
            print_info(f"  {i+1}. {entry[0]}")

        # Confirma antes da deleção (opcional, mas bom para segurança)
        # confirm = input(f"Prosseguir com a deleção dessas {num_entries_to_delete} entradas? (sim/não): ").strip().lower()
        # if confirm != 'sim':
        #     print_info("Deleção cancelada pelo usuário.")
        #     conn.close()
        #     return True # Ou False, dependendo do comportamento desejado para cancelamento

        # 4. Deleta as entradas
        print_info(f"Deletando {num_entries_to_delete} entradas...")
        query_delete = f"DELETE FROM ItemTable WHERE key LIKE ?"
        cursor.execute(query_delete, (like_pattern,))
        conn.commit()
        
        deleted_rows = cursor.rowcount
        if deleted_rows == num_entries_to_delete:
            print_success(f"Deletadas com sucesso {deleted_rows} entradas contendo '{keyword}'.")
        else:
            # Este caso idealmente não deveria acontecer se o select e delete usarem os mesmos critérios
            # e não houver modificações concorrentes.
            print_warning(f"Tentou deletar {num_entries_to_delete} entradas, mas {deleted_rows} foram reportadas deletadas pelo banco de dados.")
            # Ainda podemos considerar um sucesso parcial se algumas linhas foram deletadas.
            if deleted_rows > 0:
                 print_success(f"Sucesso parcial: {deleted_rows} entradas deletadas.")
            else:
                 print_error("Nenhuma entrada foi deletada apesar de terem sido encontradas. Verifique permissões do banco de dados ou logs.")
                 # Tenta restaurar backup se nenhuma linha foi deletada apesar de terem sido encontradas
                 raise sqlite3.Error("Incompatibilidade entre deleções esperadas e reais, e nenhuma linha foi deletada.")


        # 5. Fecha a conexão
        conn.close()
        print_success("Processo de limpeza do banco de dados concluído.")
        return True

    except sqlite3.Error as e:
        print_error(f"Erro SQLite ocorreu: {e}")
        if backup_path and backup_path.exists():
            print_warning(f"Tentando restaurar banco de dados do backup: {backup_path}")
            try:
                shutil.copy2(backup_path, db_path)
                print_success("Banco de dados restaurado com sucesso do backup.")
            except Exception as restore_e:
                print_error(f"Falha ao restaurar banco de dados do backup: {restore_e}")
                print_error(f"O banco de dados original {db_path} pode estar corrompido ou em estado inconsistente.")
                print_error(f"O backup está disponível em: {backup_path}")
        return False
    except Exception as e:
        print_error(f"Um erro inesperado ocorreu: {e}")
        # Lógica similar de restauração de backup poderia ser adicionada aqui se considerado necessário
        # Por enquanto, focando em erros SQLite para restauração.
        return False

if __name__ == '__main__':
    # Isto é para teste direto deste módulo, não parte do CLI.
    print_info("Executando database_manager.py diretamente para teste.")
    
    # --- IMPORTANTE ---
    # Para teste, você DEVE fornecer um caminho válido para um arquivo state.vscdb do VS Code.
    # É altamente recomendado usar uma CÓPIA do seu state.vscdb real para teste
    # para evitar perda acidental de dados na sua configuração do VS Code.
    #
    # Exemplo:
    # test_db_path = Path.home() / "AppData" / "Roaming" / "Code" / "User" / "globalStorage" / "state.vscdb" # Windows
    # test_db_path = Path.home() / ".config" / "Code" / "User" / "globalStorage" / "state.vscdb" # Linux
    # test_db_path = Path.home() / "Library" / "Application Support" / "Code" / "User" / "globalStorage" / "state.vscdb" # macOS

    # Cria um banco de dados dummy para teste se você não quiser usar um real
    dummy_db_path = Path("./test_state.vscdb")
    
    # Cria uma cópia para teste para evitar modificar o dummy original
    test_dummy_db_path = Path("./test_state_copy.vscdb")

    if dummy_db_path.exists():
        dummy_db_path.unlink() # Deleta se existir de execução anterior

    conn_test = sqlite3.connect(dummy_db_path)
    cursor_test = conn_test.cursor()
    cursor_test.execute("CREATE TABLE IF NOT EXISTS ItemTable (key TEXT PRIMARY KEY, value BLOB)")
    test_data = [
        ("storage.testKey1", b"testValue1"),
        ("augment.testKey2", b"testValue2"),
        ("another.augment.key", b"testValue3"),
        ("noKeywordHere", b"testValue4"),
        ("prefix.augment", b"testValue5"),
    ]
    cursor_test.executemany("INSERT OR IGNORE INTO ItemTable VALUES (?, ?)", test_data)
    conn_test.commit()
    conn_test.close()
    print_success(f"Criado banco de dados dummy em {dummy_db_path} com dados de teste.")

    # Faz uma cópia para testar
    shutil.copy2(dummy_db_path, test_dummy_db_path)
    print_info(f"Copiado banco de dados dummy para {test_dummy_db_path} para teste de limpeza.")

    print_info("\n--- Caso de Teste 1: Limpeza com palavra-chave padrão 'augment' ---")
    if clean_vscode_database(test_dummy_db_path, keyword="augment"):
        print_success("Caso de Teste 1: Limpeza bem-sucedida.")
    else:
        print_error("Caso de Teste 1: Limpeza falhou.")

    # Verifica conteúdo após limpeza
    conn_verify = sqlite3.connect(test_dummy_db_path)
    cursor_verify = conn_verify.cursor()
    cursor_verify.execute("SELECT key FROM ItemTable")
    remaining_keys = [row[0] for row in cursor_verify.fetchall()]
    print_info(f"Chaves restantes em {test_dummy_db_path}: {remaining_keys}")
    expected_keys = ["storage.testKey1", "noKeywordHere"]
    assert all(k in remaining_keys for k in expected_keys) and len(remaining_keys) == len(expected_keys), \
        f"Verificação do Caso de Teste 1 Falhou! Esperado {expected_keys}, obtido {remaining_keys}"
    print_success("Caso de Teste 1: Verificação bem-sucedida.")
    conn_verify.close()


    print_info("\n--- Caso de Teste 2: Limpeza com uma palavra-chave que não encontra nada ('nonexistent') ---")
    # Re-copia o dummy db original para um teste fresco
    shutil.copy2(dummy_db_path, test_dummy_db_path)
    if clean_vscode_database(test_dummy_db_path, keyword="nonexistent"):
        print_success("Caso de Teste 2: Limpeza reportou sucesso (como esperado, nenhum item para limpar).")
    else:
        print_error("Caso de Teste 2: Limpeza falhou.")
    
    conn_verify_2 = sqlite3.connect(test_dummy_db_path)
    cursor_verify_2 = conn_verify_2.cursor()
    cursor_verify_2.execute("SELECT COUNT(*) FROM ItemTable")
    count_after_no_keyword = cursor_verify_2.fetchone()[0]
    assert count_after_no_keyword == len(test_data), \
        f"Verificação do Caso de Teste 2 Falhou! Esperado {len(test_data)} itens, obtido {count_after_no_keyword}"
    print_success("Caso de Teste 2: Verificação bem-sucedida (nenhum item foi deletado).")
    conn_verify_2.close()

    print_info("\n--- Caso de Teste 3: Arquivo de banco de dados não existe ---")
    non_existent_db_path = Path("./non_existent_db.vscdb")
    if non_existent_db_path.exists():
        non_existent_db_path.unlink() # Garante que não existe
        
    if not clean_vscode_database(non_existent_db_path):
        print_success("Caso de Teste 3: Tratou arquivo de banco de dados inexistente corretamente (retornou False).")
    else:
        print_error("Caso de Teste 3: Falhou ao tratar arquivo de banco de dados inexistente.")

    # Limpa arquivos dummy
    if dummy_db_path.exists():
        dummy_db_path.unlink()
    if test_dummy_db_path.exists():
        test_dummy_db_path.unlink()
    print_info("\nArquivos de banco de dados dummy limpos.")
    print_success("Todos os testes do database_manager concluídos.")
