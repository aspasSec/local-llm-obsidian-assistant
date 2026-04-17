# knowledge_sources.py
import requests
from bs4 import BeautifulSoup
import PyPDF2
from typing import List

class KnowledgeExtractor:
    @staticmethod
    def from_url(url: str) -> str:
        """Extrai texto de sites"""
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove scripts e styles
        for script in soup(["script", "style"]):
            script.decompose()
        
        return soup.get_text()
    
    @staticmethod
    def from_pdf(pdf_path: str) -> str:
        """Extrai texto de PDFs"""
        text = ""
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text
    
    def add_to_vectorstore(self, content: str, source_type: str, metadata: dict):
        """Adiciona novo conteúdo ao ChromaDB"""
        # Implementar lógica para adicionar embeddings
        pass