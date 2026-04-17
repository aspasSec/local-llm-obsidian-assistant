# agents.py
class Agent:
    def __init__(self, name: str, expertise: str, llm):
        self.name = name
        self.expertise = expertise
        self.llm = llm
    
    def can_handle(self, query: str) -> bool:
        keywords = {
            "code": ["python", "código", "função", "classe"],
            "productivity": ["tarefa", "agenda", "projeto", "prazo"],
            "research": ["pesquisar", "buscar", "encontrar", "site"]
        }
        return any(kw in query.lower() for kw in keywords.get(self.expertise, []))

class AgentOrchestrator:
    def __init__(self, llm):
        self.agents = [
            Agent("CodeAssistant", "code", llm),
            Agent("ProductivityBot", "productivity", llm),
            Agent("ResearchAgent", "research", llm)
        ]
        self.default_agent = Agent("General", "general", llm)
    
    def route_query(self, query: str):
        for agent in self.agents:
            if agent.can_handle(query):
                return agent
        return self.default_agent