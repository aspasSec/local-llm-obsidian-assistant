# 🧨 Pós-Exploração no Active Directory (NetExec)

## 🧠 Resumo
O NetExec se tornou a principal ferramenta para exploração e auditoria em ambientes Active Directory, focando no abuso de credenciais e configurações inseguras.

## 🏷️ Tags
#activeDirectory #redteam #blueteam #lateralMovement #credenciais

---

## 📚 Conteúdo

O Active Directory continua sendo um dos principais alvos de ataque, pois seu comprometimento dá acesso total à rede.

Em 2026:
- CrackMapExec → substituído por NetExec (nxc)

---

### ⚙️ O que é o NetExec

Ferramenta de automação para:
- execução remota
- auditoria de segurança

Protocolos suportados:
- SMB
- WMI
- WinRM
- LDAP
- MSSQL

---

### 🔴 Uso no Red Team

- execução de comandos em massa
- exploração de credenciais
- movimentação lateral

👉 foco não é CVE, e sim:
**configuração fraca**

---

### 🔵 Uso no Blue Team

- validação de segurança
- teste de visibilidade
- análise de logs (SIEM/EDR)

👉 se funcionar fácil = problema sério

---

### 💣 Técnicas principais

#### Pass-the-Hash (PtH)
- uso de hashes NTLM
- autenticação sem senha
- exploração em escala

#### Enumeração LDAP
- mapeamento de usuários
- identificação de contas vulneráveis

#### SMB Relay
- intercepta autenticação
- executa código remoto sem senha

---

### 🚨 Indicadores de ataque

- múltiplos logons em curto tempo
- origem única → múltiplos destinos
- criação de serviços remotos
- tráfego SMB/RPC suspeito

---

## 🛡️ Mitigações

- SMB Signing obrigatório
- LAPS (senhas únicas)
- MFA
- desativar LLMNR/NBT-NS
- Credential Guard

---

## 🧠 Conceito-chave

👉 ataques modernos exploram:
- erro humano
- má configuração
- credenciais reutilizadas

---

## 💡 Insights

- NetExec é mais auditoria do que ataque
- Se ele entra fácil, sua base tá fraca
- Segurança moderna = higiene básica bem feita

---

## 🔗 Conexões
[[Movimento Lateral]]
[[Credenciais]]
[[Hardening]]