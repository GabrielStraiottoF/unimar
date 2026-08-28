import json
import os
import queue
import threading
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

ARQUIVO_USUARIOS = "usuarios.json"
ARQUIVO_CHAMADOS = "chamados.json"
TECNICO_PADRAO = {"nome": "Técnico UNIMAR", "email": "tecnico@unimar.br", "senha": "tecnico123", "tipo": "tecnico"}
FOUNDRY_ENDPOINT = "FOUNDRY_ENDPOINT"
FOUNDRY_API_KEY = "FOUNDRY_API_KEY"
FOUNDRY_MODEL = "FOUNDRY_MODEL"

COR_AZUL = "#0072BC"
COR_AZUL_ESCURO = "#005A94"
COR_AZUL_MUITO_ESCURO = "#003F6B"
COR_AZUL_CLARO = "#EAF5FC"
COR_FUNDO = "#F5F7FA"
COR_CARTAO = "#FFFFFF"
COR_TEXTO = "#172B4D"
COR_SEC = "#667085"
COR_BORDA = "#DCE4EC"
COR_SUCESSO = "#16803C"
COR_ERRO = "#C62828"

F_TITULO = ("Arial", 25, "bold")
F_SUB = ("Arial", 11)
F_SECAO = ("Arial", 16, "bold")
F_LABEL = ("Arial", 10, "bold")
F_NORMAL = ("Arial", 11)
F_BOTAO = ("Arial", 11, "bold")
F_PEQUENA = ("Arial", 9)
F_MICRO = ("Arial", 8, "bold")


def carregar_env():
    caminho = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if not os.path.exists(caminho):
        return
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if not linha or linha.startswith("#") or "=" not in linha:
                    continue
                chave, valor = linha.split("=", 1)
                os.environ.setdefault(chave.strip(), valor.strip().strip('"').strip("'"))
    except OSError:
        pass


carregar_env()


class AssistenteFoundry:
    def __init__(self):
        self.client = None
        self.modelo = None

    def iniciar(self):
        endpoint = os.getenv(FOUNDRY_ENDPOINT, "").strip()
        chave = os.getenv(FOUNDRY_API_KEY, "").strip()
        modelo = os.getenv(FOUNDRY_MODEL, "").strip()
        if not endpoint or not chave or not modelo:
            raise ValueError("Configure FOUNDRY_ENDPOINT, FOUNDRY_API_KEY e FOUNDRY_MODEL no .env.")
        try:
            from openai import OpenAI
        except ImportError as erro:
            raise RuntimeError("Instale a biblioteca OpenAI com: pip install openai") from erro
        endpoint = endpoint.rstrip("/")
        if not endpoint.endswith("/openai/v1"):
            endpoint += "/openai/v1"
        self.client = OpenAI(base_url=endpoint + "/", api_key=chave)
        self.modelo = modelo

    def perguntar(self, texto):
        if not self.client:
            self.iniciar()
        resposta = self.client.chat.completions.create(
            model=self.modelo,
            messages=[
                {"role": "system", "content": "Você é o Assistente UNIMAR. Ajude estudantes com dúvidas sobre a Central de Chamados e suporte de informática. Responda de forma clara e simples."},
                {"role": "user", "content": texto},
            ],
        )
        return resposta.choices[0].message.content


assistente = AssistenteFoundry()


def salvar_json(caminho, dados):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)


def carregar_json(caminho, padrao):
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return padrao


def garantir_arquivos():
    usuarios = carregar_json(ARQUIVO_USUARIOS, {"usuarios": []})
    if not isinstance(usuarios, dict) or not isinstance(usuarios.get("usuarios"), list):
        usuarios = {"usuarios": []}
    lista = usuarios["usuarios"]
    if not any(u.get("tipo") == "tecnico" and u.get("email", "").lower() == TECNICO_PADRAO["email"] for u in lista):
        lista.append(dict(TECNICO_PADRAO))
    salvar_json(ARQUIVO_USUARIOS, usuarios)
    chamados = carregar_json(ARQUIVO_CHAMADOS, {"chamados": []})
    if not isinstance(chamados, dict) or not isinstance(chamados.get("chamados"), list):
        salvar_json(ARQUIVO_CHAMADOS, {"chamados": []})


def carregar_usuarios():
    garantir_arquivos()
    return carregar_json(ARQUIVO_USUARIOS, {"usuarios": []}).get("usuarios", [])


def carregar_chamados():
    garantir_arquivos()
    return carregar_json(ARQUIVO_CHAMADOS, {"chamados": []}).get("chamados", [])


def salvar_chamados(chamados):
    salvar_json(ARQUIVO_CHAMADOS, {"chamados": chamados})


def limpar(janela):
    for widget in janela.winfo_children():
        widget.destroy()


def configurar_janela(janela):
    janela.title("UNIMAR | Central de Chamados")
    janela.geometry("1100x800")
    janela.minsize(760, 650)
    janela.configure(bg=COR_FUNDO)


def cabecalho(janela, titulo="CENTRAL DE CHAMADOS"):
    frame = tk.Frame(janela, bg=COR_AZUL, height=82)
    frame.pack(fill="x")
    frame.pack_propagate(False)
    tk.Label(frame, text="UNIMAR", font=("Arial", 25, "bold"), bg=COR_AZUL, fg="white").pack(side="left", padx=38)
    tk.Label(frame, text=titulo, font=("Arial", 10, "bold"), bg=COR_AZUL, fg="white").pack(side="right", padx=38)


def rodape(janela):
    frame = tk.Frame(janela, bg="white", height=38, highlightbackground=COR_BORDA, highlightthickness=1)
    frame.pack(side="bottom", fill="x")
    frame.pack_propagate(False)
    tk.Label(frame, text="UNIMAR • UNIVERSIDADE DE MARÍLIA", font=F_MICRO, bg="white", fg=COR_SEC).pack(side="left", padx=25)
    tk.Label(frame, text="CENTRAL DE ATENDIMENTO", font=F_MICRO, bg="white", fg=COR_SEC).pack(side="right", padx=25)


def botao(parent, texto, comando, secundario=False):
    b = tk.Button(parent, text=texto, command=comando, font=F_BOTAO, cursor="hand2", height=1,
                  bg="white" if secundario else COR_AZUL, fg=COR_AZUL if secundario else "white",
                  activebackground=COR_AZUL_CLARO if secundario else COR_AZUL_ESCURO,
                  activeforeground=COR_AZUL if secundario else "white",
                  relief="solid" if secundario else "flat", bd=1 if secundario else 0, padx=12, pady=8)
    b.pack(fill="x", pady=4)
    return b


def campo(parent, texto, show=None):
    tk.Label(parent, text=texto.upper(), font=F_LABEL, bg=COR_CARTAO, fg=COR_TEXTO).pack(anchor="w", pady=(4, 4))
    e = tk.Entry(parent, font=F_NORMAL, bg=COR_FUNDO, fg=COR_TEXTO, show=show or "", relief="flat",
                 highlightthickness=1, highlightbackground=COR_BORDA, highlightcolor=COR_AZUL)
    e.pack(fill="x", ipady=8, pady=(0, 8))
    return e


def mostrar_login(janela):
    limpar(janela)
    cabecalho(janela, "ACESSO INSTITUCIONAL")
    area = tk.Frame(janela, bg=COR_FUNDO)
    area.pack(fill="both", expand=True, padx=60, pady=45)
    card = tk.Frame(area, bg=COR_CARTAO, highlightbackground=COR_BORDA, highlightthickness=1, padx=35, pady=28)
    card.pack(fill="x", padx=80)
    tk.Label(card, text="Bem-vindo à UNIMAR", font=F_TITULO, bg=COR_CARTAO, fg=COR_AZUL_MUITO_ESCURO).pack(anchor="w")
    tk.Label(card, text="Acesse a Central de Chamados", font=F_SUB, bg=COR_CARTAO, fg=COR_SEC).pack(anchor="w", pady=(3, 20))
    email = campo(card, "Email")
    senha = campo(card, "Senha", "*")
    mensagem = tk.Label(card, text="", font=F_PEQUENA, bg=COR_CARTAO)
    mensagem.pack(fill="x", pady=4)

    def entrar():
        e, s = email.get().strip(), senha.get().strip()
        for usuario in carregar_usuarios():
            if usuario.get("email", "").lower() == e.lower() and usuario.get("senha") == s:
                if usuario.get("tipo") == "tecnico":
                    abrir_painel_tecnico(janela, usuario)
                else:
                    abrir_inicio_usuario(janela, usuario)
                return
        mensagem.config(text="Email ou senha incorretos.", fg=COR_ERRO)

    botao(card, "ENTRAR NO SISTEMA", entrar)
    botao(card, "CRIAR NOVO CADASTRO", lambda: abrir_cadastro(janela), True)
    tk.Label(card, text="O acesso do técnico é criado automaticamente no primeiro uso.", font=F_PEQUENA, bg=COR_CARTAO, fg=COR_SEC).pack(pady=(15, 0))
    rodape(janela)
    email.focus_set()


def abrir_cadastro(janela):
    limpar(janela)
    cabecalho(janela, "NOVO CADASTRO")
    area = tk.Frame(janela, bg=COR_FUNDO)
    area.pack(fill="both", expand=True, padx=100, pady=20)
    card = tk.Frame(area, bg=COR_CARTAO, highlightbackground=COR_BORDA, highlightthickness=1, padx=30, pady=18)
    card.pack(fill="x")
    tk.Label(card, text="Criar cadastro", font=F_TITULO, bg=COR_CARTAO, fg=COR_AZUL_MUITO_ESCURO).pack(anchor="w")
    nome = campo(card, "Nome")
    email = campo(card, "Email")
    senha = campo(card, "Senha", "*")
    confirma = campo(card, "Confirmar senha", "*")
    msg = tk.Label(card, text="", font=F_PEQUENA, bg=COR_CARTAO)
    msg.pack(fill="x")

    def cadastrar():
        n, e, s, c = nome.get().strip(), email.get().strip(), senha.get(), confirma.get()
        if not n or not e or not s or not c:
            msg.config(text="Preencha todos os campos.", fg=COR_ERRO); return
        if s != c:
            msg.config(text="As senhas não coincidem.", fg=COR_ERRO); return
        usuarios = carregar_usuarios()
        if any(u.get("email", "").lower() == e.lower() for u in usuarios):
            msg.config(text="Este email já está cadastrado.", fg=COR_ERRO); return
        usuarios.append({"nome": n, "email": e, "senha": s, "tipo": "usuario"})
        salvar_json(ARQUIVO_USUARIOS, {"usuarios": usuarios})
        messagebox.showinfo("Cadastro", "Cadastro realizado com sucesso!")
        mostrar_login(janela)

    botao(card, "CADASTRAR", cadastrar)
    botao(card, "VOLTAR PARA O LOGIN", lambda: mostrar_login(janela), True)
    rodape(janela)
    nome.focus_set()


def abrir_inicio_usuario(janela, usuario):
    limpar(janela)
    cabecalho(janela, "ÁREA DO USUÁRIO")
    area = tk.Frame(janela, bg=COR_FUNDO)
    area.pack(fill="both", expand=True, padx=45, pady=28)
    tk.Label(area, text="CENTRAL DE ATENDIMENTO", font=F_MICRO, bg=COR_FUNDO, fg=COR_AZUL).pack(anchor="w")
    tk.Label(area, text=f"Olá, {usuario.get('nome', 'usuário')}!", font=F_TITULO, bg=COR_FUNDO, fg=COR_AZUL_MUITO_ESCURO).pack(anchor="w")
    tk.Label(area, text="Abra um chamado ou acompanhe suas solicitações.", font=F_SUB, bg=COR_FUNDO, fg=COR_SEC).pack(anchor="w", pady=(3, 18))
    card = tk.Frame(area, bg=COR_CARTAO, highlightbackground=COR_BORDA, highlightthickness=1, padx=25, pady=20)
    card.pack(fill="x")
    tk.Label(card, text="Meus chamados", font=F_SECAO, bg=COR_CARTAO, fg=COR_TEXTO).pack(anchor="w")
    tk.Label(card, text="Você pode abrir mais de um chamado e acompanhar o andamento de cada um.", font=F_NORMAL, bg=COR_CARTAO, fg=COR_SEC).pack(anchor="w", pady=(3, 12))
    botao(card, "ABRIR NOVO CHAMADO", lambda: abrir_novo_chamado(janela, usuario))
    botao(card, "VER MEUS CHAMADOS", lambda: abrir_meus_chamados(janela, usuario), True)
    botao(card, "ABRIR ASSISTENTE UNIMAR", lambda: abrir_chatbot(janela, usuario), True)
    botao(area, "SAIR DO SISTEMA", lambda: mostrar_login(janela), True)
    rodape(janela)


def abrir_novo_chamado(janela, usuario):
    limpar(janela)
    cabecalho(janela, "NOVO CHAMADO")
    area = tk.Frame(janela, bg=COR_FUNDO)
    area.pack(fill="both", expand=True, padx=50, pady=18)
    card = tk.Frame(area, bg=COR_CARTAO, highlightbackground=COR_BORDA, highlightthickness=1, padx=25, pady=15)
    card.pack(fill="both", expand=True)
    tk.Label(card, text="Abrir chamado", font=F_TITULO, bg=COR_CARTAO, fg=COR_AZUL_MUITO_ESCURO).pack(anchor="w")
    tk.Label(card, text="Descreva o problema para que o técnico consiga analisar sua solicitação.", font=F_SUB, bg=COR_CARTAO, fg=COR_SEC).pack(anchor="w", pady=(2, 10))
    departamento = campo(card, "Departamento")
    equipamento = campo(card, "Equipamento")
    tk.Label(card, text="DESCRIÇÃO DO PROBLEMA", font=F_LABEL, bg=COR_CARTAO, fg=COR_TEXTO).pack(anchor="w", pady=(2, 4))
    descricao = tk.Text(card, height=6, font=F_NORMAL, bg=COR_FUNDO, fg=COR_TEXTO, relief="flat", highlightthickness=1, highlightbackground=COR_BORDA)
    descricao.pack(fill="both", expand=True, pady=(0, 8))
    inicio = campo(card, "Horário em que começou (ex.: 08:30)")
    msg = tk.Label(card, text="", font=F_PEQUENA, bg=COR_CARTAO)
    msg.pack(fill="x")

    def criar():
        dep, eq, desc, hora = departamento.get().strip(), equipamento.get().strip(), descricao.get("1.0", "end").strip(), inicio.get().strip()
        if not dep or not eq or not desc or not hora:
            msg.config(text="Preencha todos os campos.", fg=COR_ERRO); return
        chamados = carregar_chamados()
        novo_id = max([int(c.get("id", 0)) for c in chamados if str(c.get("id", "0")).isdigit()] or [0]) + 1
        agora = datetime.now().strftime("%d/%m/%Y %H:%M")
        chamados.append({"id": novo_id, "departamento": dep, "nome_solicitante": usuario.get("nome", ""), "email_solicitante": usuario.get("email", ""), "equipamento": eq, "descricao": desc, "horario_inicio": hora, "data_abertura": agora, "status": "Aberto", "tecnico": TECNICO_PADRAO["email"], "descricao_finalizacao": "", "data_finalizacao": ""})
        salvar_chamados(chamados)
        messagebox.showinfo("Chamado", f"Chamado #{novo_id} criado com sucesso!")
        abrir_meus_chamados(janela, usuario)

    botao(card, "CRIAR CHAMADO", criar)
    botao(card, "VOLTAR", lambda: abrir_inicio_usuario(janela, usuario), True)
    rodape(janela)


def abrir_meus_chamados(janela, usuario):
    limpar(janela)
    cabecalho(janela, "MEUS CHAMADOS")
    area = tk.Frame(janela, bg=COR_FUNDO)
    area.pack(fill="both", expand=True, padx=35, pady=18)
    tk.Label(area, text="Minhas solicitações", font=F_TITULO, bg=COR_FUNDO, fg=COR_AZUL_MUITO_ESCURO).pack(anchor="w")
    tree = criar_tabela(area, ["ID", "Departamento", "Equipamento", "Início", "Status"])
    for c in carregar_chamados():
        if c.get("email_solicitante", "").lower() == usuario.get("email", "").lower():
            tree.insert("", "end", values=(c["id"], c["departamento"], c["equipamento"], c["horario_inicio"], c["status"]))
    botao(area, "VOLTAR PARA A CENTRAL", lambda: abrir_inicio_usuario(janela, usuario), True)
    rodape(janela)


def criar_tabela(parent, colunas):
    style = ttk.Style()
    style.configure("Treeview", font=F_PEQUENA, rowheight=30)
    style.configure("Treeview.Heading", font=F_LABEL)
    frame = tk.Frame(parent, bg=COR_CARTAO, highlightbackground=COR_BORDA, highlightthickness=1)
    frame.pack(fill="both", expand=True, pady=12)
    tree = ttk.Treeview(frame, columns=colunas, show="headings")
    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")
    scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scroll.set)
    tree.pack(side="left", fill="both", expand=True)
    scroll.pack(side="right", fill="y")
    return tree


def abrir_painel_tecnico(janela, tecnico):
    limpar(janela)
    cabecalho(janela, "PAINEL DO TÉCNICO")
    area = tk.Frame(janela, bg=COR_FUNDO)
    area.pack(fill="both", expand=True, padx=30, pady=18)
    topo = tk.Frame(area, bg=COR_FUNDO)
    topo.pack(fill="x")
    tk.Label(topo, text="Painel de chamados", font=F_TITULO, bg=COR_FUNDO, fg=COR_AZUL_MUITO_ESCURO).pack(side="left")
    tk.Label(topo, text=f"Técnico: {tecnico.get('nome')}", font=F_NORMAL, bg=COR_FUNDO, fg=COR_SEC).pack(side="right", pady=10)
    filtro = tk.Frame(area, bg=COR_CARTAO, highlightbackground=COR_BORDA, highlightthickness=1, padx=15, pady=12)
    filtro.pack(fill="x", pady=(8, 10))
    tk.Label(filtro, text="FILTRAR POR DEPARTAMENTO", font=F_LABEL, bg=COR_CARTAO, fg=COR_TEXTO).pack(side="left", padx=(0, 10))
    departamentos = ["Todos"] + sorted(set(c.get("departamento", "") for c in carregar_chamados() if c.get("departamento")))
    combo = ttk.Combobox(filtro, values=departamentos, state="readonly", width=25)
    combo.set("Todos")
    combo.pack(side="left")
    tree = criar_tabela(area, ["ID", "Departamento", "Solicitante", "Equipamento", "Início", "Status"])

    def atualizar(*_):
        for item in tree.get_children(): tree.delete(item)
        filtro_dep = combo.get()
        for c in carregar_chamados():
            if filtro_dep != "Todos" and c.get("departamento") != filtro_dep:
                continue
            tree.insert("", "end", values=(c["id"], c["departamento"], c["nome_solicitante"], c["equipamento"], c["horario_inicio"], c["status"]))

    combo.bind("<<ComboboxSelected>>", atualizar)
    atualizar()

    def detalhes():
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Chamado", "Selecione um chamado."); return
        id_chamado = tree.item(selecionado[0], "values")[0]
        chamado = next((c for c in carregar_chamados() if str(c.get("id")) == str(id_chamado)), None)
        if chamado:
            abrir_detalhes_chamado(janela, tecnico, chamado)

    botao(area, "VER CHAMADO SELECIONADO", detalhes)
    botao(area, "SAIR DO PAINEL", lambda: mostrar_login(janela), True)
    rodape(janela)


def abrir_detalhes_chamado(janela, tecnico, chamado):
    limpar(janela)
    cabecalho(janela, f"CHAMADO #{chamado['id']}")
    area = tk.Frame(janela, bg=COR_FUNDO)
    area.pack(fill="both", expand=True, padx=45, pady=22)
    card = tk.Frame(area, bg=COR_CARTAO, highlightbackground=COR_BORDA, highlightthickness=1, padx=25, pady=20)
    card.pack(fill="both", expand=True)
    tk.Label(card, text=f"Chamado #{chamado['id']}  •  {chamado['status']}", font=F_SECAO, bg=COR_CARTAO, fg=COR_AZUL_MUITO_ESCURO).pack(anchor="w")
    dados = [("Departamento", chamado["departamento"]), ("Solicitante", chamado["nome_solicitante"]), ("Equipamento", chamado["equipamento"]), ("Horário de início", chamado["horario_inicio"]), ("Data de abertura", chamado["data_abertura"])]
    for titulo, valor in dados:
        tk.Label(card, text=f"{titulo}: {valor}", font=F_NORMAL, bg=COR_CARTAO, fg=COR_TEXTO).pack(anchor="w", pady=2)
    tk.Label(card, text="DESCRIÇÃO DO PROBLEMA", font=F_LABEL, bg=COR_CARTAO, fg=COR_TEXTO).pack(anchor="w", pady=(15, 4))
    tk.Label(card, text=chamado["descricao"], font=F_NORMAL, bg=COR_AZUL_CLARO, fg=COR_TEXTO, wraplength=850, justify="left", anchor="w", padx=12, pady=12).pack(fill="x")

    if chamado.get("status") == "Finalizado":
        tk.Label(card, text="DESCRIÇÃO DA FINALIZAÇÃO", font=F_LABEL, bg=COR_CARTAO, fg=COR_TEXTO).pack(anchor="w", pady=(15, 4))
        tk.Label(card, text=chamado.get("descricao_finalizacao", ""), font=F_NORMAL, bg="#EAF7EF", fg=COR_TEXTO, wraplength=850, justify="left", anchor="w", padx=12, pady=12).pack(fill="x")
        tk.Label(card, text=f"Finalizado em: {chamado.get('data_finalizacao', '')}", font=F_PEQUENA, bg=COR_CARTAO, fg=COR_SEC).pack(anchor="w", pady=8)
    else:
        tk.Label(card, text="DESCRIÇÃO DO QUE OCORREU / SOLUÇÃO", font=F_LABEL, bg=COR_CARTAO, fg=COR_TEXTO).pack(anchor="w", pady=(15, 4))
        solucao = tk.Text(card, height=5, font=F_NORMAL, bg=COR_FUNDO, fg=COR_TEXTO, relief="flat", highlightthickness=1, highlightbackground=COR_BORDA)
        solucao.pack(fill="x")

        def finalizar():
            texto = solucao.get("1.0", "end").strip()
            if not texto:
                messagebox.showwarning("Finalizar chamado", "Descreva o que ocorreu e o que foi feito antes de finalizar."); return
            chamados = carregar_chamados()
            for item in chamados:
                if str(item.get("id")) == str(chamado.get("id")):
                    item["status"] = "Finalizado"
                    item["descricao_finalizacao"] = texto
                    item["data_finalizacao"] = datetime.now().strftime("%d/%m/%Y %H:%M")
                    item["tecnico"] = tecnico.get("email", TECNICO_PADRAO["email"])
                    break
            salvar_chamados(chamados)
            messagebox.showinfo("Chamado", "Chamado finalizado com sucesso!")
            abrir_painel_tecnico(janela, tecnico)

        botao(card, "FINALIZAR CHAMADO", finalizar)
    botao(card, "VOLTAR PARA OS CHAMADOS", lambda: abrir_painel_tecnico(janela, tecnico), True)
    rodape(janela)


def abrir_chatbot(janela, usuario):
    limpar(janela)
    cabecalho(janela, "ASSISTENTE UNIMAR")
    area = tk.Frame(janela, bg=COR_FUNDO)
    area.pack(fill="both", expand=True, padx=40, pady=18)
    tk.Label(area, text="Assistente UNIMAR", font=F_TITULO, bg=COR_FUNDO, fg=COR_AZUL_MUITO_ESCURO).pack(anchor="w")
    tk.Label(area, text="Tire dúvidas sobre a Central de Chamados.", font=F_SUB, bg=COR_FUNDO, fg=COR_SEC).pack(anchor="w")
    historico = tk.Frame(area, bg=COR_CARTAO, highlightbackground=COR_BORDA, highlightthickness=1, padx=15, pady=12)
    historico.pack(fill="both", expand=True, pady=12)
    tk.Label(historico, text="ASSISTENTE", font=F_LABEL, bg=COR_CARTAO, fg=COR_AZUL).pack(anchor="w")
    tk.Label(historico, text="Olá! Como posso ajudar?", font=F_NORMAL, bg=COR_CARTAO, fg=COR_TEXTO).pack(anchor="w", pady=(2, 12))
    entrada = tk.Entry(area, font=F_NORMAL, bg=COR_CARTAO, fg=COR_TEXTO, relief="flat", highlightthickness=1, highlightbackground=COR_BORDA)
    entrada.pack(fill="x", ipady=9)
    fila = queue.Queue()

    def enviar():
        texto = entrada.get().strip()
        if not texto: return
        tk.Label(historico, text="VOCÊ", font=F_LABEL, bg=COR_CARTAO, fg=COR_SEC).pack(anchor="w", pady=(8, 0))
        tk.Label(historico, text=texto, font=F_NORMAL, bg=COR_CARTAO, fg=COR_TEXTO, wraplength=850, justify="left").pack(anchor="w")
        entrada.delete(0, "end")
        entrada.config(state="disabled")
        enviar_btn.config(state="disabled")
        def consultar():
            try: fila.put((True, assistente.perguntar(texto)))
            except Exception as erro: fila.put((False, str(erro)))
        threading.Thread(target=consultar, daemon=True).start()

    enviar_btn = botao(area, "ENVIAR", enviar)
    def verificar():
        try: ok, resposta = fila.get_nowait()
        except queue.Empty:
            janela.after(100, verificar); return
        entrada.config(state="normal"); enviar_btn.config(state="normal")
        tk.Label(historico, text="ASSISTENTE" if ok else "ERRO", font=F_LABEL, bg=COR_CARTAO, fg=COR_AZUL if ok else COR_ERRO).pack(anchor="w", pady=(8, 0))
        tk.Label(historico, text=resposta, font=F_NORMAL, bg=COR_CARTAO, fg=COR_TEXTO, wraplength=850, justify="left").pack(anchor="w")
        janela.after(100, verificar)
    janela.after(100, verificar)
    botao(area, "VOLTAR PARA A CENTRAL", lambda: abrir_inicio_usuario(janela, usuario), True)
    rodape(janela)


def main():
    garantir_arquivos()
    janela = tk.Tk()
    configurar_janela(janela)
    mostrar_login(janela)
    janela.mainloop()


if __name__ == "__main__":
    main()
