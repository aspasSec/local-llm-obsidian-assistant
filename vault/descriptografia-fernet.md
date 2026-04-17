# 🔐 Descriptografia de Arquivo com Fernet (Python)

## 🧠 Resumo
Script em Python que utiliza criptografia simétrica com Fernet para descriptografar um arquivo usando uma chave previamente gerada.

## 🏷️ Tags
#criptografia #python #fernet #seguranca #arquivo

---

## 📚 Conceito

Esse script usa o módulo:

- cryptography.fernet

Fernet é um método de criptografia simétrica que:
- usa a mesma chave para criptografar e descriptografar
- garante confidencialidade + integridade

---

## 🔑 Chave utilizada

txt
0B8KeSGboeH3H_UT7V7J4PgrZ6PzUDjX9zvOpOyV_xE=

Código:
from cryptography.fernet import Fernet

# lê arquivo que contém a chave
with open("chave_simetrica.txt", "rb") as arquivo_chave:
    chave = arquivo_chave.read()

fernet = Fernet(chave)

# abre arquivo criptografado
with open("teste.txt", "rb") as arquivo_criptografado:
    criptografado = arquivo_criptografado.read()

# descriptografa arquivo
arquivo_descriptografado = fernet.decrypt(criptografado)

# salva a descriptografia
with open("teste.txt", "wb") as descriptografado:
    descriptografado.write(arquivo_descriptografado)

---