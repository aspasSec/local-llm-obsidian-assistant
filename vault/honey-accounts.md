# 🛡️ Honey Accounts no Active Directory

## 🧠 Resumo
Honey Accounts são contas falsas no AD usadas como armadilhas para detectar acessos indevidos e ataques de identidade.

## 🏷️ Tags
#activeDirectory #deteccao #seguranca #identity

---

## 📚 Conteúdo

No atual cenário de cibersegurança, proteger o Active Directory (AD) tornou-se uma necessidade crítica...

Ataques direcionados contra identidades como:
- Kerberoasting
- DCSync
- Movimento lateral
- Escalonamento de privilégios

...estão cada vez mais sofisticados e difíceis de detectar com métodos tradicionais.

### 🔍 O que são Honey Accounts?

Honey Accounts são contas fictícias criadas dentro do Active Directory com o objetivo exclusivo de detectar acessos não autorizados.

Diferente das contas normais:
- Não são usadas por pessoas reais
- Não participam de processos
- Não possuem uso legítimo

👉 Qualquer interação = **forte indicativo de invasão**

---

### 🎯 Objetivo

Detectar:
- Reconhecimento de contas
- Tentativas de login
- Uso de credenciais roubadas
- Escalada de privilégio

---

### 🚨 Vantagens

#### Detecção precoce
Permite identificar o atacante antes dele comprometer contas reais.

#### Redução de falsos positivos
Como não há uso legítimo:
→ qualquer evento é suspeito

#### Inteligência de ataque
Permite observar:
- técnicas usadas
- comportamento do invasor

---

### ⚙️ Implementação

- Criar contas falsas no AD
- Nomear como contas “atrativas” (ex: admin, service)
- Integrar com SIEM
- Monitorar autenticações

---

### 🧠 Boas práticas

- Não dar privilégios reais
- Tornar a conta convincente
- Monitoramento em tempo real
- Combinar com outras defesas

---

## 💡 Insights (MEU / SEU CÉREBRO)

- Isso é literalmente um “sensor humano fake”
- Excelente contra ataques stealth
- Funciona melhor com Zero Trust

---

## 🔗 Conexões
[[Active Directory]]
[[Detecção de Ameaças]]
[[Movimento Lateral]]