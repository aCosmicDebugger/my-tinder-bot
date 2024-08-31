# Tinder Bot

Este é um bot para o Tinder que automatiza o processo de "swiping" usando o Selenium WebDriver com o Brave Browser. 

## Requisitos

- Python 3.x
- Brave Browser
- ChromeDriver (para Brave)
- `pip` (para instalar dependências)
- `git` (para versionamento)

## Configuração

### 1. Clonando o Repositório

Clone o repositório usando Git:

```sh
git clone https://github.com/aCosmicDebugger/my-tinder-bot.git
cd my-tinder-bot
```


### 2. Criando um Ambiente Virtual
Crie e ative um ambiente virtual para isolar as dependências do projeto:

```sh
python -m venv venv
source venv/bin/activate
```
No windows, use:
```sh 
venv\Scripts\activate
```

### 3. Instalando Dependências
Instale as dependências do projeto usando pip:

```sh
pip install -r requirements.txt
```

### 4. Configurando o Arquivo .env
Crie um arquivo .env na raiz do projeto e adicione suas credenciais e o caminho para o Brave Browser. O arquivo deve ter o seguinte formato:

```env
# Informações de login do Tinder
TINDER_USERNAME=seu_usuario
TINDER_PASSWORD=sua_senha

# Caminho para o ChromeDriver
CHROMEDRIVER_PATH=/caminho/para/chromedriver

# Caminho para o Brave Browser
BRAVE_BROWSER_PATH=/caminho/para/brave

```
### 5. . Executando o Bot
Depois de configurar o arquivo .env, execute o bot com o seguinte comando:

```sh
bash run_tinder_bot.sh
```