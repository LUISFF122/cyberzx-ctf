from flask import Flask, request, render_template_string, jsonify
import time
import json
import os
from datetime import datetime
from user_agents import parse  # pip install user-agents

app = Flask(__name__)

# ================= CONFIGURAÇÕES DO CYBERZX =================
ADMIN_USER = "cyberzx"
ADMIN_PASS = "senha_super_secreta_123"   # Mude isso!
TOKEN_PREMIO = "CYBERZX{Voce_Conseguiu_Invadir_O_Servidor}"
LOG_FILE = "logs.json"
RATE_LIMIT_SEGUNDOS = 30
# ============================================================

rate_limit = {}

# ---------- Função para salvar logs ----------
def salvar_log(ip, user_agent_str, username=None, senha=None, sucesso=False, evento="acesso"):
    try:
        ua = parse(user_agent_str)
        so = ua.os.family + " " + ua.os.version_string
        navegador = ua.browser.family + " " + ua.browser.version_string
        dispositivo = ua.device.family
    except:
        so, navegador, dispositivo = "Desconhecido", "Desconhecido", "Desconhecido"

    log_entry = {
        "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "ip": ip,
        "sistema": so,
        "navegador": navegador,
        "dispositivo": dispositivo,
        "evento": evento,
        "usuario_tentado": username,
        "senha_tentada": senha if senha else "---",
        "sucesso": sucesso,
        "user_agent_raw": user_agent_str
    }

    # Lê logs existentes e adiciona o novo
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except:
            logs = []
    logs.append(log_entry)
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)

# ---------- Template HTML com design NEON VERMELHO ----------
LOGIN_PAGE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<title>CyberZX // Acesso Restrito</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
    * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Courier New', monospace; }
    body {
        background: #0a0000;
        background-image:
            radial-gradient(circle at 50% 50%, rgba(255,0,0,0.15) 0%, transparent 70%),
            linear-gradient(rgba(255,0,0,0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,0,0,0.05) 1px, transparent 1px);
        background-size: 100% 100%, 40px 40px, 40px 40px;
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #ff3333;
        overflow: hidden;
    }
    .container {
        background: rgba(10, 0, 0, 0.85);
        border: 2px solid #ff0000;
        border-radius: 12px;
        padding: 45px 55px;
        box-shadow:
            0 0 10px #ff0000,
            0 0 25px #ff0000,
            0 0 50px rgba(255,0,0,0.5),
            inset 0 0 20px rgba(255,0,0,0.2);
        animation: pulse 3s infinite alternate;
        max-width: 480px;
        width: 90%;
        position: relative;
    }
    @keyframes pulse {
        from { box-shadow: 0 0 10px #ff0000, 0 0 25px #ff0000, 0 0 50px rgba(255,0,0,0.5), inset 0 0 20px rgba(255,0,0,0.2); }
        to   { box-shadow: 0 0 20px #ff0000, 0 0 45px #ff0000, 0 0 90px rgba(255,0,0,0.8), inset 0 0 30px rgba(255,0,0,0.4); }
    }
    h1 {
        font-size: 28px;
        text-align: center;
        letter-spacing: 4px;
        color: #ff0000;
        text-shadow: 0 0 5px #ff0000, 0 0 15px #ff0000, 0 0 30px #ff0000;
        margin-bottom: 8px;
    }
    .sub {
        text-align: center;
        font-size: 12px;
        color: #ff6666;
        letter-spacing: 2px;
        margin-bottom: 30px;
        opacity: 0.8;
    }
    .ascii {
        text-align: center;
        font-size: 10px;
        color: #ff0000;
        text-shadow: 0 0 8px #ff0000;
        margin-bottom: 20px;
        line-height: 1.1;
        white-space: pre;
    }
    label {
        display: block;
        font-size: 12px;
        margin-bottom: 6px;
        color: #ff5555;
        letter-spacing: 1px;
    }
    input {
        width: 100%;
        padding: 12px;
        margin-bottom: 20px;
        background: rgba(255,0,0,0.05);
        border: 1px solid #ff0000;
        border-radius: 6px;
        color: #ff3333;
        font-size: 14px;
        font-family: 'Courier New', monospace;
        outline: none;
        transition: 0.3s;
    }
    input:focus {
        box-shadow: 0 0 15px #ff0000, inset 0 0 10px rgba(255,0,0,0.2);
        background: rgba(255,0,0,0.1);
    }
    button {
        width: 100%;
        padding: 14px;
        background: transparent;
        border: 2px solid #ff0000;
        border-radius: 6px;
        color: #ff0000;
        font-size: 16px;
        font-weight: bold;
        letter-spacing: 3px;
        cursor: pointer;
        text-shadow: 0 0 5px #ff0000;
        box-shadow: 0 0 10px #ff0000, inset 0 0 10px rgba(255,0,0,0.2);
        transition: 0.3s;
    }
    button:hover {
        background: #ff0000;
        color: #000;
        text-shadow: none;
        box-shadow: 0 0 30px #ff0000, 0 0 60px #ff0000;
    }
    .msg {
        text-align: center;
        margin-top: 15px;
        font-size: 13px;
        color: #ff0000;
        text-shadow: 0 0 8px #ff0000;
        min-height: 18px;
    }
    .footer {
        text-align: center;
        font-size: 10px;
        color: #661111;
        margin-top: 25px;
        letter-spacing: 1px;
    }
    .blink { animation: blink 1s infinite; }
    @keyframes blink { 50% { opacity: 0.3; } }
</style>
</head>
<body>
    <div class="container">
        <div class="ascii">
  ██████╗██╗   ██╗██████╗ ███████╗██████╗ ███████╗██╗  ██╗
 ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗╚══███╔╝╚██╗██╔╝
 ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝  ███╔╝  ╚███╔╝
 ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗ ███╔╝   ██╔██╗
 ╚██████╗   ██║   ██████╔╝███████╗██║  ██║███████╗██╔╝ ██╗
  ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
        </div>
        <h1>ACESSO RESTRITO</h1>
        <p class="sub">// SISTEMA DE SEGURANÇA ATIVO <span class="blink">_</span></p>

        <form method="POST">
            <label>> USUÁRIO</label>
            <input type="text" name="username" placeholder="digite o usuário..." autocomplete="off">
            <label>> SENHA</label>
            <input type="password" name="password" placeholder="digite a senha...">
            <button type="submit">[ ENTRAR ]</button>
        </form>
        <p class="msg">{{ mensagem }}</p>
        <p class="footer">© CyberZX CTF // Todos os acessos são monitorados</p>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def login():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ip and ',' in ip:
        ip = ip.split(',')[0].strip()
    ua = request.headers.get('User-Agent', 'Desconhecido')
    agora = time.time()

    # Rate Limit
    if ip in rate_limit:
        if agora - rate_limit[ip] < RATE_LIMIT_SEGUNDOS:
            restante = int(RATE_LIMIT_SEGUNDOS - (agora - rate_limit[ip]))
            salvar_log(ip, ua, evento=f"BLOQUEADO por rate limit ({restante}s restantes)")
            return f"<body style='background:#000;color:#f00;font-family:monospace;text-align:center;padding-top:50px;'><h1>⛔ BLOQUEADO</h1><p>Aguarde {restante} segundos.</p></body>", 429
    rate_limit[ip] = agora

    if request.method == 'POST':
        user = request.form.get('username', '')
        senha = request.form.get('password', '')

        if user == ADMIN_USER and senha == ADMIN_PASS:
            salvar_log(ip, ua, user, senha, sucesso=True, evento="LOGIN SUCESSO")
            return f"""
            <body style='background:#000;color:#0f0;font-family:monospace;text-align:center;padding-top:80px;'>
                <h1 style='text-shadow:0 0 20px #0f0;'>✔ ACESSO CONCEDIDO</h1>
                <p style='font-size:20px;'>Bem-vindo, Admin!</p>
                <p style='margin-top:40px;color:#ff0;text-shadow:0 0 15px #ff0;font-size:22px;'>TOKEN: <b>{TOKEN_PREMIO}</b></p>
                <p style='color:#666;margin-top:40px;'>Tire print desta tela e envie para o CyberZX.</p>
            </body>"""
        else:
            salvar_log(ip, ua, user, senha, sucesso=False, evento="LOGIN FALHA")
            return render_template_string(LOGIN_PAGE, mensagem="> ACESSO NEGADO. Credenciais inválidas.")

    # GET normal
    salvar_log(ip, ua, evento="VISITA")
    return render_template_string(LOGIN_PAGE, mensagem="")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
