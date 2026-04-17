python chat.py --local --model llama3.2:3b

# 🤖 Local LLM Assistant with Obsidian RAG

Um assistente pessoal inteligente que aprende com suas notas do Obsidian usando RAG (Retrieval-Augmented Generation) e LLMs locais via Ollama.

## ✨ Funcionalidades

- 📝 **RAG com Obsidian**: Indexa automaticamente suas notas Markdown
- 🤖 **LLM Local**: Usa Ollama para rodar modelos localmente (sem internet)
- 💬 **Chat Interativo**: Interface CLI para conversar com seu assistente
- 🔍 **Busca Semântica**: Encontra informações relevantes nas suas notas
- 📓 **Integração com Obsidian**: Salva automaticamente as buscas no seu vault

## 📋 Pré-requisitos

- **Python 3.10+** - [Download](https://www.python.org/downloads/)
- **Ollama** - [Download para Windows](https://ollama.com/download/windows)
- **Obsidian** (opcional) - [Download](https://obsidian.md/)

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/local-llm-obsidian-assistant.git
cd local-llm-obsidian-assistant

2. Crie um ambiente virtual
bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
3. Instale as dependências
bash
pip install -r requirements.txt

4. Baixe um modelo LLM local
bash
# Modelo leve (recomendado para começar)
ollama pull llama3.2:1b

# Ou modelo um pouco maior
ollama pull llama3.2:3b

5. Configure o caminho do Obsidian
Edite o arquivo rag.py e altere o caminho do seu vault:

python
obsidian_path = r"C:\Users\SeuUsuario\Documents\Obsidian Vault"
6. Configure as variáveis de ambiente
Crie um arquivo .env na raiz do projeto:

env
# Configuração do Ollama
USE_LOCAL_LLM=True
LOCAL_MODEL=llama3.2:1b
SHOW_CONTEXT=True

# Configuração do Obsidian (opcional)
OBSIDIAN_API_KEY=sua_chave_aqui
OBSIDIAN_PORT=27123
Nota: A integração com Obsidian é opcional. Se não quiser usar, ignore as configurações do Obsidian.

🎯 Primeira execução
1. Crie o banco de dados (apenas uma vez)
bash
python -c "from rag import create_db; create_db()"
Isso vai ler todas as suas notas do Obsidian e criar um banco vetorial.

2. Inicie o assistente
bash
python chat.py --local --model llama3.2:1b
📖 Uso diário
Comandos básicos
bash
# Ativar ambiente virtual
venv\Scripts\activate

# Iniciar o chat
python chat.py --local --model llama3.2:1b
Comandos dentro do chat
Comando	Descrição
/sair ou /exit	Fechar o assistente
/clear	Limpar histórico da conversa
/context	Mostrar/esconder contexto usado
/stats	Ver estatísticas de uso

Exemplo de uso
text
>> O que é phishing?

⏳ Buscando no banco de dados...
✅ Busca concluída!

📚 Contexto encontrado: 3 documentos

🤖 Phishing é um tipo de ataque cibernético onde criminosos...
🔄 Atualizando o banco de dados
Quando você adicionar ou modificar notas no Obsidian:

bash
python -c "from rag import create_db; create_db()"
🛠️ Solução de problemas
Erro: Ollama não encontrado
bash
# Verifique se o Ollama está instalado
ollama --version

# Se não funcionar, adicione ao PATH ou use o caminho completo
"C:\Program Files\Ollama\ollama.exe" --version
Erro: Modelo não responde
bash
# Teste o modelo diretamente
ollama run llama3.2:1b "Olá"

# Se não funcionar, use um modelo mais leve
ollama pull llama3.2:1b
Erro: Banco de dados vazio
bash
# Recrie o banco
python -c "from rag import create_db; create_db()"
Erro: Pouca memória RAM
Use um modelo mais leve:

bash
ollama pull llama3.2:1b  # Apenas 1.3GB
# ou
ollama pull qwen2.5:0.5b  # Apenas 395MB
📁 Estrutura do projeto
text
local-llm-obsidian-assistant/
├── chat.py              # Interface CLI
├── rag.py               # Sistema RAG
├── llm.py               # Cliente Gemini (opcional)
├── llm_local.py         # Cliente Ollama
├── requirements.txt     # Dependências
├── .env                 # Configurações (não commitar)
├── db/                  # Banco ChromaDB (gerado)
└── README.md
📦 Dependências
txt
langchain-chroma>=0.1.0
langchain-huggingface>=0.1.0
langchain-text-splitters>=0.3.0
chromadb>=0.4.22
sentence-transformers>=2.2.2
python-dotenv>=1.0.0
requests>=2.31.0
🤝 Contribuindo
Sinta-se à vontade para abrir issues ou pull requests!

📄 Licença
MIT License

⚠️ Aviso
Este projeto é para fins educacionais. Use as ferramentas de segurança apenas em sistemas autorizados.

Desenvolvido com 🧠 para aprender com seu conhecimento pessoal

text

## 📝 Também crie o arquivo `.gitignore`:

```gitignore
# Banco de dados
db/

# Ambiente virtual
venv/
env/
ENV/

# Arquivos de configuração com senhas
.env

# Cache do Python
__pycache__/
*.pyc
*.pyo
*.pyd

# IDE
.vscode/
.idea/

# Logs
*.log

# Sistema
.DS_Store
Thumbs.db