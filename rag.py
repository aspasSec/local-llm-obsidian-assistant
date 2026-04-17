import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma  
from langchain_huggingface import HuggingFaceEmbeddings  
from dotenv import load_dotenv


load_dotenv()
DB_PATH = "db"
OBSIDIAN_API_KEY = os.getenv("OBSIDIAN_API_KEY")
OBSIDIAN_PORT = os.getenv("OBSIDIAN_PORT", "27123")

def test_obsidian_connection():
    try:
        import requests
        response = requests.get(
            f"https://localhost:{OBSIDIAN_PORT}/",
            headers={"Authorization": f"Bearer {OBSIDIAN_API_KEY}"},
            verify=False,
            timeout=2
        )
        return response.status_code == 200
    except:
        return False

def get_embeddings():
    """Retorna o modelo de embeddings atualizado"""
    return HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},  # Força uso de CPU
        encode_kwargs={'normalize_embeddings': True}  # Normaliza embeddings
    )


def create_db(obsidian_path=None):
    """
    Cria o banco de dados vetorial a partir das notas do Obsidian
    
    Args:
        obsidian_path: Caminho do vault Obsidian. Se None, usa o caminho padrão
    """

    if obsidian_path is None:
        obsidian_path = r"C:\Users\eumar\OneDrive\Documentos\Obsidian Vault"
    print(f"📂 Verificando caminho: {obsidian_path}")
    
    if not os.path.exists(obsidian_path):
        print(f"❌ ERRO: Caminho não encontrado: {obsidian_path}")
        print("Verifique se o caminho está correto!")
        return None
    
    md_files = []
    for root, dirs, files in os.walk(obsidian_path):
        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))
    
    print(f"📄 Encontrados {len(md_files)} arquivos Markdown")
    
    if len(md_files) == 0:
        print("❌ Nenhum arquivo .md encontrado!")
        print(f"Verifique se a pasta contém arquivos Markdown: {obsidian_path}")
        return None
    
    # Carrega todos os arquivos .md
    loader = DirectoryLoader(
        obsidian_path,
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        recursive=True,
        show_progress=True
    )
    
    docs = loader.load()
    print(f"✅ Carregados {len(docs)} documentos")
    
    # Divide os documentos em chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", " ", ""],
        length_function=len
    )
    
    chunks = splitter.split_documents(docs)
    print(f"✂️  Divididos em {len(chunks)} chunks")
    
    # Cria embeddings e vectorstore
    embeddings = get_embeddings()
    
    print("🔨 Criando banco de dados vetorial...")
    
    # Remove o banco antigo se existir
    if os.path.exists(DB_PATH):
        import shutil
        shutil.rmtree(DB_PATH)
        print("🗑️  Banco antigo removido")
    
    # Cria novo banco (agora sem .persist())
    db = Chroma.from_documents(
        chunks,
        embeddings,
        persist_directory=DB_PATH,
        collection_name="jarvis_obsidian"
    )
    
    # Na nova versão, o Chroma persiste automaticamente
    print(f"💾 Banco de dados salvo em: {DB_PATH}")
    print(f"✅ Banco criado com {db._collection.count()} documentos")
    
    return db

def notify_obsidian(pergunta: str, docs: list, resposta: str = None):
    """Envia busca para o Obsidian"""
    if not docs:
        return
    
    import requests
    import time
    
    timestamp = int(time.time())
    date_str = time.strftime('%Y-%m-%d')
    
    note_content = f"""# 🔍 Busca Jarvis - {time.strftime('%H:%M:%S')}

## Pergunta
{pergunta}

## Contexto encontrado
"""
    for i, doc in enumerate(docs, 1):
        note_content += f"\n### Documento {i}\n{doc.page_content[:300]}...\n"
    
    if resposta:
        note_content += f"\n## Resposta\n{resposta}\n"
    
    try:
        response = requests.put(
            f"https://localhost:{OBSIDIAN_PORT}/vault/Jarvis/Busca_{date_str}_{timestamp}.md",
            headers={"Authorization": f"Bearer {OBSIDIAN_API_KEY}"},
            data=note_content.encode('utf-8'),
            verify=False,
            timeout=5
        )
        if response.status_code in [200, 201]:
            print("📝 Busca salva no Obsidian!")
    except:
        pass

def load_db():
    """
    Carrega o banco de dados vetorial existente
    
    Returns:
        Chroma: Vectorstore carregado
    
    Raises:
        FileNotFoundError: Se o banco não existir
    """
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(
            f"Banco de dados não encontrado em {DB_PATH}. "
            "Execute create_db() primeiro."
        )
    
    embeddings = get_embeddings()
    
    db = Chroma(
        persist_directory=DB_PATH,
        embedding_function=embeddings,
        collection_name="jarvis_obsidian"
    )
    
    # Verifica se o banco tem documentos
    collection_count = db._collection.count()
    print(f"✅ Banco de dados carregado: {collection_count} documentos")
    
    if collection_count == 0:
        print("⚠️  Banco está vazio! Execute create_db() para popular.")
    
    return db

def search_similar(query: str, k: int = 4, db=None):
    """
    Busca documentos similares no banco
    
    Args:
        query: Texto da consulta
        k: Número de resultados
        db: Vectorstore (se None, carrega o padrão)
    
    Returns:
        Lista de documentos similares
    """
    if db is None:
        db = load_db()
    
    results = db.similarity_search(query, k=k)
    
    print(f"🔍 Encontrados {len(results)} resultados para: '{query[:50]}...'")
    return results

def get_context_for_query(query: str, k: int = 4) -> str:
    """
    Obtém o contexto relevante para uma pergunta
    
    Args:
        query: Pergunta do usuário
        k: Número de documentos a recuperar
    
    Returns:
        String com contexto formatado
    """
    try:
        docs = search_similar(query, k=k)
        
        context_parts = []
        for i, doc in enumerate(docs, 1):
            source = doc.metadata.get('source', 'fonte desconhecida')
            file_name = os.path.basename(source)
            context_parts.append(f"[Documento {i} - {file_name}]:\n{doc.page_content}\n")
        
        return "\n".join(context_parts)
    
    except FileNotFoundError:
        print("⚠️  Banco de dados não encontrado. Criando novo banco...")
        create_db()
        return get_context_for_query(query, k)

def update_db(obsidian_path=None):
    """
    Atualiza o banco de dados (recria do zero)
    """
    print("🔄 Recriando banco de dados...")
    
    # Remove banco antigo se existir
    if os.path.exists(DB_PATH):
        import shutil
        shutil.rmtree(DB_PATH)
        print("🗑️  Banco antigo removido")
    
    # Cria novo banco
    create_db(obsidian_path)
    print("✅ Banco de dados atualizado!")

def add_document(text: str, metadata: dict = None):
    """
    Adiciona um documento diretamente ao banco
    
    Args:
        text: Texto do documento
        metadata: Metadados adicionais (opcional)
    """
    db = load_db()
    
    if metadata is None:
        metadata = {"source": "manual_addition"}
    
    from langchain_core.documents import Document
    doc = Document(page_content=text, metadata=metadata)
    
    db.add_documents([doc])
    db.persist()
    print(f"✅ Documento adicionado: {metadata.get('source', 'manual')}")

# Exemplo de uso direto
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "create":
            print("🚀 Criando banco de dados...")
            create_db()
        
        elif command == "update":
            print("🚀 Atualizando banco de dados...")
            update_db()
        
        elif command == "search" and len(sys.argv) > 2:
            query = " ".join(sys.argv[2:])
            results = search_similar(query)
            for i, doc in enumerate(results, 1):
                print(f"\n--- Resultado {i} ---")
                print(f"Fonte: {doc.metadata.get('source', 'desconhecida')}")
                print(f"Conteúdo: {doc.page_content[:200]}...")

        elif command == "test-obsidian":
            if test_obsidian_connection():
                    print("✅ Conexão OK!")
            else:
                    print("❌ Falha na conexão")
        
        else:
            print("Comandos disponíveis:")
            print("  python rag.py create       - Cria banco de dados")
            print("  python rag.py update       - Atualiza banco de dados")
            print("  python rag.py search <termo> - Busca no banco")
    else:
        print("📚 Sistema RAG - Jarvis")
        print("Comandos disponíveis:")
        print("  python rag.py create       - Cria banco de dados")
        print("  python rag.py update       - Atualiza banco de dados")
        print("  python rag.py search <termo> - Busca no banco")