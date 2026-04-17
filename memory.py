# memory.py
from typing import List, Dict
from datetime import datetime

class ConversationMemory:
    def __init__(self, max_history=10):
        self.history: List[Dict] = []
        self.max_history = max_history
    
    def add_interaction(self, user_input: str, assistant_response: str):
        self.history.append({
            "user": user_input,
            "assistant": assistant_response,
            "timestamp": datetime.now().isoformat()
        })
        
        # Mantém apenas as últimas N interações
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
    
    def get_context(self) -> str:
        """Formata histórico para contexto"""
        if not self.history:
            return ""
        
        context = "Histórico da conversa:\n"
        for item in self.history[-3:]:  # Últimas 3 interações
            context += f"Usuário: {item['user']}\n"
            context += f"Assistente: {item['assistant']}\n"
        
        return context