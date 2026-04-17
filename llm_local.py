import requests
import json
from typing import Optional, Generator

class OllamaLLM:
    def __init__(self, model="llama3.2:3b", base_url="http://localhost:11434"):
        self.base_url = base_url
        self.model = model
        self._check_availability()
    
    def _check_availability(self):
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            response.raise_for_status()

            models = response.json().get("models", [])
            model_names = [m["name"] for m in models]
            
            if self.model not in model_names:
                print(f"⚠️ Modelo {self.model} não encontrado localmente")
                print(f"Modelos disponíveis: {', '.join(model_names)}")
                resposta = input(f"Deseja baixar {self.model}? (s/n): ")
                if resposta.lower() == 's':
                    self.pull_model()
        except:
            raise ConnectionError(
                "Ollama não está rodando. Inicie com 'ollama serve' no terminal"
            )
    
    def pull_model(self):
        """Baixa o modelo do Ollama registry"""
        print(f"📥 Baixando modelo {self.model}...")
        response = requests.post(
            f"{self.base_url}/api/pull",
            json={"name": self.model},
            stream=True
        )
        
        for line in response.iter_lines():
            if line:
                data = json.loads(line)
                if "status" in data:
                    print(f"  {data['status']}")
        
        print(f"✅ Modelo {self.model} baixado com sucesso!")
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": self.model,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "num_predict": 2048  # Limite de tokens
                }
            }
        )
        
        response.raise_for_status()
        return response.json()["message"]["content"]
    
    def stream_generate(self, prompt: str, system_prompt: Optional[str] = None) -> Generator[str, None, None]:
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": self.model,
                "messages": messages,
                "stream": True,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "num_predict": 2048
                }
            },
            stream=True
        )
        
        for line in response.iter_lines():
            if line:
                data = json.loads(line)
                if "message" in data and "content" in data["message"]:
                    yield data["message"]["content"]
