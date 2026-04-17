import os
import sys
import time
from rag import load_db, get_context_for_query, search_similar
from llm import ask_gemini
from llm_local import OllamaLLM
from dotenv import load_dotenv
from rag import notify_obsidian

load_dotenv()

# Configuração
USE_LOCAL_LLM = os.getenv("USE_LOCAL_LLM", "False").lower() == "true"
LOCAL_MODEL = os.getenv("LOCAL_MODEL", "llama3.2:3b")
SHOW_CONTEXT = os.getenv("SHOW_CONTEXT", "False").lower() == "true"

class JarvisChat:
    def __init__(self, use_local=False, model_name=None):
        """
        Inicializa o assistente Jarvis
        
        Args:
            use_local: Se True, usa Ollama local. Se False, usa Gemini API
            model_name: Nome do modelo local (ex: "llama3.2:3b")
        """
        print("🚀 Inicializando Jarvis...")
        
        # Carrega o banco de dados vetorial
        try:
            self.db = load_db()
            print("✅ Banco de dados carregado com sucesso")
        except FileNotFoundError:
            print("⚠️  Banco de dados não encontrado!")
            resposta = input("Deseja criar o banco agora? (s/n): ")
            if resposta.lower() == 's':
                from rag import create_db
                create_db()
                self.db = load_db()
            else:
                print("❌ Sem banco de dados, encerrando...")
                sys.exit(1)
        
        # Configura o LLM
        if use_local:
            model = model_name or LOCAL_MODEL
            print(f"🤖 Usando LLM local: {model}")
            self.llm = OllamaLLM(model=model)
        else:
            print("🤖 Usando Gemini API")
            self.llm = None
        
        self.conversation_history = []
        self.max_history = 5

    def animar_busca(self):
        frames = ["⏳", "⌛", "⏳", "⌛"]
        for frame in frames:
            sys.stdout.write(f"\r{frame} Buscando no banco de dados...")
            sys.stdout.flush()
            time.sleep(0.15)
        sys.stdout.write("\r✅ Busca concluída!     \n")
    
    def get_conversation_context(self):
        if not self.conversation_history:
            return ""
        
        context = "\n## Histórico da conversa:\n"
        for item in self.conversation_history[-self.max_history:]:
            context += f"Usuário: {item['user']}\n"
            context += f"Assistente: {item['assistant']}\n\n"
        
        return context
    
    def build_prompt(self, question: str, context: str):
        """Constrói o prompt com contexto e histórico"""
        conversation_context = self.get_conversation_context()
        
        prompt = f"""Você é o Jarvis, um assistente pessoal inteligente especializado em segurança da informação e tecnologia.

{conversation_context}

## Contexto das minhas notas pessoais (se relevante):
{context}

## Pergunta atual:
{question}

## Instruções:
- Use o contexto das minhas notas quando for relevante
- Se não houver informação no contexto, use seu conhecimento geral
- Seja conciso mas completo
- Mantenha um tom profissional e amigável
- Se não souber algo, diga honestamente

## Resposta:"""
        
        return prompt
    
    def ask(self, question: str) -> str:
        """Faz uma pergunta ao Jarvis"""
        
        # ANIMAÇÃO ANTES DA BUSCA
        self.animar_busca()
        
        # Busca contexto relevante
        try:
            docs = self.db.similarity_search(question, k=3)
            
            if docs:
                context = "\n\n".join(
                    f"[Fonte: {doc.metadata.get('source', 'nota')}]\n{doc.page_content}"
                    for i, doc in enumerate(docs, 1)
                )
                if SHOW_CONTEXT:
                    print(f"\n📚 Contexto encontrado: {len(docs)} documentos")
                
                # Salva no Obsidian se tiver documentos
                try:
                    notify_obsidian(question, docs)
                    print("📝 Busca salva no Obsidian!")
                except:
                    pass  # Ignora erro do Obsidian
            else:
                context = "Nenhum contexto relevante encontrado nas notas."
                if SHOW_CONTEXT:
                    print("\n⚠️ Nenhum contexto encontrado")
        
        except Exception as e:
            print(f"⚠️ Erro ao buscar contexto: {e}")
            context = "Erro ao acessar banco de dados"
            docs = []
        
        # Constrói prompt
        prompt = self.build_prompt(question, context)
        
        # Obtém resposta do LLM
        try:
            if self.llm:
                response = self.llm.generate(prompt)
            else:
                response = ask_gemini(prompt)
            
            # Salva no histórico
            self.conversation_history.append({
                "user": question,
                "assistant": response
            })
            
            return response
        
        except Exception as e:
            error_msg = f"Erro ao obter resposta: {str(e)}"
            print(f"❌ {error_msg}")
            return "Desculpe, tive um problema ao processar sua pergunta. Verifique as configurações do LLM."
    
    def stream_ask(self, question: str):
        """
        Versão com streaming para resposta em tempo real (apenas LLM local)
        """
        if not self.llm:
            print("⚠️ Streaming disponível apenas com LLM local")
            return self.ask(question)
        
        # ANIMAÇÃO ANTES DA BUSCA
        self.animar_busca()
        
        # Busca contexto
        docs = self.db.similarity_search(question, k=3)
        context = "\n\n".join([doc.page_content for doc in docs]) if docs else ""
        
        # Salva no Obsidian se tiver documentos
        if docs:
            try:
                notify_obsidian(question, docs)
                print("📝 Busca salva no Obsidian!")
            except:
                pass
        
        # Constrói prompt
        prompt = self.build_prompt(question, context)
        
        # Gera resposta em streaming
        print("\n🤖 ", end="", flush=True)
        full_response = ""
        for chunk in self.llm.stream_generate(prompt):
            print(chunk, end="", flush=True)
            full_response += chunk
        
        print("\n")
        
        # Salva no histórico
        self.conversation_history.append({
            "user": question,
            "assistant": full_response
        })
        
        return full_response
    
    def clear_history(self):
        """Limpa o histórico da conversa"""
        self.conversation_history = []
        print("🧹 Histórico da conversa limpo")
    
    def run_cli(self):
        """Executa o chat interativo no terminal"""
        print("\n" + "="*50)
        print("🧠 Jarvis - Assistente Pessoal Inteligente")
        print("="*50)
        print("\nComandos especiais:")
        print("  /sair, /exit, /quit  - Fechar o assistente")
        print("  /clear                - Limpar histórico da conversa")
        print("  /context              - Mostrar/ocultar contexto")
        print("  /stats                - Mostrar estatísticas")
        print("\n" + "-"*50 + "\n")
        
        while True:
            try:
                pergunta = input(">> ").strip()
                
                if not pergunta:
                    continue
                
                # Comandos especiais
                if pergunta.lower() in ["/sair", "/exit", "/quit", "sair", "exit", "quit"]:
                    print("\n👋 Até logo! Jarvis encerrando...\n")
                    break
                
                elif pergunta.lower() == "/clear":
                    self.clear_history()
                    continue
                
                elif pergunta.lower() == "/context":
                    global SHOW_CONTEXT
                    SHOW_CONTEXT = not SHOW_CONTEXT
                    print(f"📚 Exibir contexto: {'Ativado' if SHOW_CONTEXT else 'Desativado'}")
                    continue
                
                elif pergunta.lower() == "/stats":
                    self.show_stats()
                    continue
                
                # Processa pergunta normal
                if self.llm and hasattr(self.llm, 'stream_generate'):
                    self.stream_ask(pergunta)
                else:
                    resposta = self.ask(pergunta)
                    print(f"\n🤖 {resposta}\n")
            
            except KeyboardInterrupt:
                print("\n\n👋 Interrompido pelo usuário. Até logo!\n")
                break
            
            except Exception as e:
                print(f"\n❌ Erro inesperado: {e}\n")
    
    def show_stats(self):
        """Mostra estatísticas do assistente"""
        print("\n📊 Estatísticas do Jarvis:")
        print(f"  - Total de interações: {len(self.conversation_history)}")
        print(f"  - LLM: {'Local (Ollama)' if self.llm else 'Gemini API'}")
        if self.llm:
            print(f"  - Modelo local: {LOCAL_MODEL}")
        print(f"  - Banco de dados: {self.db._collection.count()} documentos")
        print(f"  - Histórico máximo: {self.max_history} interações\n")


def main():
    """Função principal para iniciar o chat"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Jarvis - Assistente Pessoal")
    parser.add_argument("--local", action="store_true", help="Usar LLM local (Ollama)")
    parser.add_argument("--model", type=str, default="llama3.2:3b", help="Modelo local")
    parser.add_argument("--question", type=str, help="Fazer uma pergunta única e sair")
    
    args = parser.parse_args()
    
    # Verifica se Ollama está rodando para modo local
    if args.local:
        import requests
        try:
            requests.get("http://localhost:11434/api/tags", timeout=2)
            print("✅ Ollama detectado")
        except:
            print("❌ Ollama não está rodando!")
            print("Inicie o Ollama primeiro: ollama serve")
            print("Ou remova a flag --local para usar Gemini API")
            sys.exit(1)
    
    # Inicializa Jarvis
    jarvis = JarvisChat(use_local=args.local, model_name=args.model)
    
    # Modo pergunta única
    if args.question:
        resposta = jarvis.ask(args.question)
        print(f"\nPergunta: {args.question}")
        print(f"Resposta: {resposta}\n")
    else:
        # Modo interativo
        jarvis.run_cli()


if __name__ == "__main__":
    main()