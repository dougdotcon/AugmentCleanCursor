# AugmentCode-Free
AugmentCode: solução gratuita e ilimitada; novas contas recebem 600 chamadas gratuitas do Claude Sonnet 4


Atualização em 18 de junho de 2025:

Nova abordagem:

Método de convite por equipe:

1. Primeiro, prepare qualquer conta (pode ser banida, expirada ou sem créditos gratuitos). No navegador, acesse https://app.augmentcode.com/account/subscription
Acesse a página do perfil, clique em Team e depois em add member para adicionar uma conta secundária como membro da equipe.
![image](https://github.com/user-attachments/assets/caa0f8dc-d189-476f-bc3f-84ee0037e03b)


2. Essa conta secundária pode usar qualquer e-mail de domínio. Após adicioná-la à equipe, ela receberá um e-mail de ativação.
![image](https://github.com/user-attachments/assets/63117ef9-1e9c-4641-99c1-9d3c9f56f435)


3. Clique no link do e-mail https://auth.augmentcode.com/invitations , faça login com a conta secundária e siga o fluxo de ativação.

4. Execute o script abaixo para limpar as configurações locais, depois faça login com a conta secundária. Assim, você poderá usar normalmente. Até o momento, o método continua funcionando.

Resumo: qualquer conta principal serve, até mesmo banida. A conta principal cria uma equipe e adiciona a secundária, que poderá usar ilimitadamente. Lembre-se de sempre logar o plugin Augment com a conta secundária e limpar as configurações locais antes de logar.

<p align="center">
  <a href="#english">English</a> | <a href="#portugues">Português</a>
</p>

---

<a name="english"></a>

# AugmentCode-Free (English)

**AugmentCode-Free** is a Python-based toolkit, now featuring a modern **Graphical User Interface (GUI)** alongside its command-line interface. It's designed to provide maintenance and tweaking utilities for VS Code, helping users manage aspects like telemetry and local cache.

## Features

### Core Functionality (Available in CLI & GUI)
-   **VS Code Database Cleaning**: Cleans specific entries from VS Code's local databases.
-   **VS Code Telemetry ID Modification**: Helps in resetting or changing telemetry identifiers stored by VS Code.

### New GUI Features
-   **Intuitive Interface**: A user-friendly graphical alternative to command-line operations.
-   **One-Click Operations**: Easily perform tasks like modifying VS Code telemetry IDs and cleaning VS Code databases with a single click.
-   **Process Management**: Automatically detects and offers to close running VS Code instances to ensure operations proceed smoothly.
-   **User Feedback**: Provides clear confirmation dialogs and status messages for all operations.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/BasicProtein/AugmentCode-Free.git](https://github.com/BasicProtein/AugmentCode-Free.git)
    cd AugmentCode-Free
    ```
2.  **Install dependencies (if any specified in `requirements.txt` or `setup.py`):**
    ```bash
    pip install .
    # or
    # pip install -r requirements.txt
    ```

## Usage

You can use AugmentCode-Free in two ways:

### 1. Graphical User Interface (GUI) - Recommended
The GUI provides an easy-to-use interface for all features.

-   **Directly (from project root):**
    ```bash
    python main.py
    ```

-   **If installed via pip (as `augment-tools-gui`):**
    ```bash
    augment-tools-gui
    ```

### 2. Command-Line Interface (CLI)
For users who prefer the command line or need to script operations.

-   **If installed via pip (as `augment-tools`):**
    ```bash
    augment-tools --help
    ```
    (Follow on-screen instructions for specific commands like `clean-db` or `modify-telemetry`)

-   **Directly (for development/advanced use, from project root):**
    Refer to `augment_tools_core/cli.py` for direct script execution details if needed.

## Disclaimer
Use these tools at your own risk. Always back up important data before running maintenance functions, especially when they modify application files. While backups might be created automatically by some functions, caution is advised.

---

<a name="portugues"></a>

# AugmentCode-Free (Português)

**AugmentCode-Free** é um conjunto de ferramentas em Python, agora com uma moderna **Interface Gráfica (GUI)** além da interface de linha de comando. Ele foi desenvolvido para fornecer utilitários de manutenção e ajustes para o VS Code, ajudando usuários a gerenciar aspectos como telemetria e cache local.

## Funcionalidades

### Funcionalidades Principais (Disponível em CLI & GUI)
-   **Limpeza do Banco de Dados do VS Code**: Limpa entradas específicas dos bancos de dados locais do VS Code.
-   **Modificação do ID de Telemetria do VS Code**: Auxilia na redefinição ou alteração dos identificadores de telemetria armazenados pelo VS Code.

### Novidades na GUI
-   **Interface Intuitiva**: Alternativa gráfica e amigável às operações por linha de comando.
-   **Operações com Um Clique**: Realize tarefas como modificar IDs de telemetria e limpar bancos de dados do VS Code com apenas um clique.
-   **Gerenciamento de Processos**: Detecta automaticamente e oferece fechar instâncias do VS Code em execução para garantir que as operações ocorram sem problemas.
-   **Feedback ao Usuário**: Fornece diálogos de confirmação e mensagens de status claras para todas as operações.

## Instalação

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/BasicProtein/AugmentCode-Free.git](https://github.com/BasicProtein/AugmentCode-Free.git)
    cd AugmentCode-Free
    ```
2.  **Instale as dependências (se especificado em `requirements.txt` ou `setup.py`):**
    ```bash
    pip install .
    # ou
    # pip install -r requirements.txt
    ```

## Como Usar

Você pode usar o AugmentCode-Free de duas formas:

### 1. Interface Gráfica (GUI) - Recomendado
A GUI oferece uma interface fácil de usar para todos os recursos.

-   **Diretamente (a partir da raiz do projeto):**
    ```bash
    python main.py
    ```

-   **Se instalado via pip (como `augment-tools-gui`):**
    ```bash
    augment-tools-gui
    ```

### 2. Interface de Linha de Comando (CLI)
Para quem prefere o terminal ou precisa automatizar operações.

-   **Se instalado via pip (como `augment-tools`):**
    ```bash
    augment-tools --help
    ```
    (Siga as instruções na tela para comandos como `clean-db` ou `modify-telemetry`)

-   **Diretamente (para desenvolvimento/uso avançado, a partir da raiz do projeto):**
    Consulte `augment_tools_core/cli.py` para detalhes sobre execução direta do script.

## Aviso
Use estas ferramentas por sua conta e risco. Sempre faça backup de dados importantes antes de executar funções de manutenção, especialmente quando elas modificam arquivos de aplicativos. Embora alguns recursos possam criar backups automaticamente, a cautela é recomendada.
