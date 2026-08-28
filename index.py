import json
import os
import queue
import threading
import tkinter as tk
from tkinter import messagebox

ARQUIVO_USUARIOS = "usuarios.json"
FOUNDRY_ENDPOINT = "FOUNDRY_ENDPOINT"
FOUNDRY_API_KEY = "FOUNDRY_API_KEY"
FOUNDRY_MODEL = "FOUNDRY_MODEL"

COR_AZUL = "#0072BC"
COR_AZUL_ESCURO = "#005A94"
COR_AZUL_MUITO_ESCURO = "#003F6B"
COR_AZUL_CLARO = "#EAF5FC"
COR_AZUL_PALETA = "#F3F9FD"
COR_FUNDO = "#F5F7FA"
COR_CARTAO = "#FFFFFF"
COR_TEXTO = "#172B4D"
COR_TEXTO_SECUNDARIO = "#667085"
COR_BORDA = "#DCE4EC"
COR_SUCESSO = "#16803C"
COR_ERRO = "#C62828"

FONTE_MARCA = ("Arial", 25, "bold")
FONTE_MARCA_SECUNDARIA = ("Arial", 8, "bold")
FONTE_TITULO = ("Arial", 25, "bold")
FONTE_SUBTITULO = ("Arial", 11)
FONTE_SECAO = ("Arial", 16, "bold")
FONTE_LABEL = ("Arial", 10, "bold")
FONTE_PADRAO = ("Arial", 11)
FONTE_BOTAO = ("Arial", 11, "bold")
FONTE_PEQUENA = ("Arial", 9)
FONTE_MICRO = ("Arial", 8)


def carregar_env():
    caminho = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if not os.path.exists(caminho):
        return
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                if not linha or linha.startswith("#") or "=" not in linha:
                    continue
                chave, valor = linha.split("=", 1)
                chave = chave.strip()
                valor = valor.strip().strip('"').strip("'")
                if chave and chave not in os.environ:
                    os.environ[chave] = valor
    except OSError:
        pass


carregar_env()


class AssistenteFoundry:
    def __init__(self):
        self.client = None
        self.modelo = None
        self.inicializado = False

    def iniciar(self):
        endpoint = os.getenv(FOUNDRY_ENDPOINT, "").strip()
        api_key = os.getenv(FOUNDRY_API_KEY, "").strip()
        modelo = os.getenv(FOUNDRY_MODEL, "").strip()
        if not endpoint or not api_key or not modelo:
            raise ValueError("Configure FOUNDRY_ENDPOINT, FOUNDRY_API_KEY e FOUNDRY_MODEL no .env.")
        try:
            from openai import OpenAI
        except ImportError as erro:
            raise RuntimeError("A biblioteca OpenAI não está instalada. Execute: pip install openai") from erro
        endpoint = endpoint.rstrip("/")
        if not endpoint.endswith("/openai/v1"):
            endpoint = f"{endpoint}/openai/v1"
        self.client = OpenAI(base_url=f"{endpoint}/", api_key=api_key)
        self.modelo = modelo
        self.inicializado = True

    def perguntar(self, texto):
        if not self.inicializado:
            self.iniciar()
        try:
            resposta = self.client.responses.create(model=self.modelo, input=texto)
            return resposta.output_text
        except Exception as erro_responses:
            try:
                resposta = self.client.chat.completions.create(
                    model=self.modelo,
                    messages=[
                        {"role": "system", "content": "Você é o Assistente UNIMAR, um chatbot de apoio à Central de Chamados. Responda de forma clara, educada e adequada para estudantes."},
                        {"role": "user", "content": texto},
                    ],
                )
                return resposta.choices[0].message.content
            except Exception as erro_chat:
                raise RuntimeError(f"Não foi possível consultar o modelo. Responses: {erro_responses}; Chat Completions: {erro_chat}") from erro_chat


assistente = AssistenteFoundry()


def garantir_arquivo_usuarios():
    if not os.path.exists(ARQUIVO_USUARIOS):
        salvar_usuarios([])
        return
    try:
        with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        if not isinstance(dados, dict) or not isinstance(dados.get("usuarios"), list):
            salvar_usuarios([])
    except (json.JSONDecodeError, OSError):
        salvar_usuarios([])


def carregar_usuarios():
    garantir_arquivo_usuarios()
    try:
        with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo).get("usuarios", [])
    except (json.JSONDecodeError, OSError):
        return []


def salvar_usuarios(usuarios):
    with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as arquivo:
        json.dump({"usuarios": usuarios}, arquivo, ensure_ascii=False, indent=4)


def configurar_janela(janela):
    janela.title("UNIMAR | Central de Chamados")
    largura, altura = 1100, 800
    janela.geometry(f"{largura}x{altura}")
    janela.minsize(720, 560)
    janela.configure(bg=COR_FUNDO)
    janela.update_idletasks()
    x = max((janela.winfo_screenwidth() - largura) // 2, 0)
    y = max((janela.winfo_screenheight() - altura) // 2, 0)
    janela.geometry(f"{largura}x{altura}+{x}+{y}")


def limpar_janela(janela):
    for widget in janela.winfo_children():
        widget.destroy()


def criar_cabecalho(janela):
    cabecalho = tk.Frame(janela, bg=COR_AZUL, height=112)
    cabecalho.pack(fill="x")
    cabecalho.pack_propagate(False)
    marca = tk.Frame(cabecalho, bg=COR_AZUL)
    marca.pack(side="left", padx=48, pady=19)
    tk.Label(marca, text="UNIMAR", font=FONTE_MARCA, bg=COR_AZUL, fg=COR_CARTAO).pack(anchor="w")
    tk.Label(marca, text="UNIVERSIDADE DE MARÍLIA", font=FONTE_MARCA_SECUNDARIA, bg=COR_AZUL, fg=COR_CARTAO).pack(anchor="w")
    sistema = tk.Frame(cabecalho, bg=COR_AZUL)
    sistema.pack(side="right", padx=48, pady=19)
    tk.Label(sistema, text="AMBIENTE INSTITUCIONAL", font=FONTE_MICRO, bg=COR_AZUL, fg="#D9EFFB").pack(anchor="e")
    tk.Label(sistema, text="CENTRAL DE CHAMADOS", font=("Arial", 12, "bold"), bg=COR_AZUL, fg=COR_CARTAO).pack(anchor="e", pady=(5, 0))


def criar_rodape(janela):
    rodape = tk.Frame(janela, bg=COR_CARTAO, height=50, highlightbackground=COR_BORDA, highlightthickness=1)
    rodape.pack(side="bottom", fill="x")
    rodape.pack_propagate(False)
    tk.Label(rodape, text="UNIMAR  •  UNIVERSIDADE DE MARÍLIA", font=("Arial", 8, "bold"), bg=COR_CARTAO, fg=COR_TEXTO_SECUNDARIO).pack(side="left", padx=38, pady=16)
    tk.Label(rodape, text="CENTRAL DE ATENDIMENTO  •  AMBIENTE ACADÊMICO", font=FONTE_MICRO, bg=COR_CARTAO, fg=COR_TEXTO_SECUNDARIO).pack(side="right", padx=38, pady=16)


def criar_conteudo(janela):
    conteudo = tk.Frame(janela, bg=COR_FUNDO)
    conteudo.pack(fill="both", expand=True)
    return conteudo


def criar_campo(parent, texto, show=None):
    bloco = tk.Frame(parent, bg=COR_CARTAO)
    bloco.pack(fill="x", pady=(0, 15))
    tk.Label(bloco, text=texto.upper(), font=FONTE_LABEL, bg=COR_CARTAO, fg=COR_TEXTO).pack(anchor="w", pady=(0, 6))
    entrada = tk.Entry(bloco, font=FONTE_PADRAO, bg=COR_FUNDO, fg=COR_TEXTO, insertbackground=COR_AZUL, relief="flat", bd=0, highlightthickness=1, highlightbackground=COR_BORDA, highlightcolor=COR_AZUL)
    if show:
        entrada.config(show=show)
    entrada.pack(fill="x", ipady=11)
    return entrada


def criar_botao(parent, texto, comando, secundario=False):
    fundo = COR_CARTAO if secundario else COR_AZUL
    texto_cor = COR_AZUL if secundario else COR_CARTAO
    hover = COR_AZUL_CLARO if secundario else COR_AZUL_ESCURO
    altura = 54 if secundario else 50
    container = tk.Frame(parent, bg=COR_BORDA if secundario else fundo)
    container.pack(fill="x", pady=(7 if secundario else 4, 0))
    container.grid_propagate(False)
    container.configure(height=altura)
    container.pack_propagate(False)
    botao = tk.Button(
        container, text=texto, font=FONTE_BOTAO, bg=fundo, fg=texto_cor,
        activebackground=hover, activeforeground=texto_cor,
        relief="solid" if secundario else "flat", bd=1 if secundario else 0,
        highlightthickness=0, cursor="hand2", command=comando, padx=14, pady=0,
        anchor="center", wraplength=600,
    )
    botao.pack(fill="both", expand=True, padx=1 if secundario else 0, pady=1 if secundario else 0)
    botao.bind("<Enter>", lambda _e: botao.configure(bg=hover))
    botao.bind("<Leave>", lambda _e: botao.configure(bg=fundo))
    return botao


def criar_mensagem(parent):
    mensagem = tk.Label(parent, text="", font=FONTE_PEQUENA, bg=COR_CARTAO, wraplength=520, justify="center")
    mensagem.pack(fill="x", pady=(0, 9))
    return mensagem


def mostrar_mensagem(mensagem, texto, sucesso=False):
    mensagem.config(text=texto, fg=COR_SUCESSO if sucesso else COR_ERRO)


def criar_badge(parent, texto):
    badge = tk.Frame(parent, bg=COR_AZUL_CLARO, padx=11, pady=6)
    badge.pack(anchor="w", pady=(0, 15))
    tk.Label(badge, text=texto.upper(), font=FONTE_MICRO, bg=COR_AZUL_CLARO, fg=COR_AZUL_MUITO_ESCURO).pack()
    return badge


def criar_aviso(parent, texto, tipo="info"):
    if tipo == "sucesso":
        fundo, cor = "#EAF7EF", COR_SUCESSO
    elif tipo == "erro":
        fundo, cor = "#FDECEC", COR_ERRO
    else:
        fundo, cor = COR_AZUL_PALETA, COR_AZUL_MUITO_ESCURO
    aviso = tk.Frame(parent, bg=fundo, highlightbackground=COR_BORDA, highlightthickness=1, padx=15, pady=11)
    aviso.pack(fill="x", pady=(18, 0))
    tk.Label(aviso, text=texto, font=FONTE_PEQUENA, bg=fundo, fg=cor, wraplength=760, justify="center").pack(fill="x")
    return aviso


def criar_painel_lateral(parent):
    painel = tk.Frame(parent, bg=COR_AZUL_MUITO_ESCURO, width=310)
    painel.pack(side="left", fill="y", padx=(0, 30))
    painel.pack_propagate(False)
    tk.Frame(painel, bg=COR_AZUL, height=5).pack(fill="x")
    corpo = tk.Frame(painel, bg=COR_AZUL_MUITO_ESCURO)
    corpo.pack(fill="both", expand=True, padx=28, pady=31)
    tk.Label(corpo, text="UNIMAR", font=("Arial", 34, "bold"), bg=COR_AZUL_MUITO_ESCURO, fg=COR_CARTAO).pack(anchor="w")
    tk.Label(corpo, text="UNIVERSIDADE DE MARÍLIA", font=("Arial", 8, "bold"), bg=COR_AZUL_MUITO_ESCURO, fg="#D7EBF7").pack(anchor="w", pady=(2, 31))
    tk.Frame(corpo, bg="#4A83A9", height=1).pack(fill="x", pady=(0, 28))
    tk.Label(corpo, text="AMBIENTE ACADÊMICO", font=FONTE_MICRO, bg=COR_AZUL_MUITO_ESCURO, fg="#A9D5EC").pack(anchor="w")
    tk.Label(corpo, text="Central de\nChamados", font=("Arial", 24, "bold"), bg=COR_AZUL_MUITO_ESCURO, fg=COR_CARTAO, justify="left").pack(anchor="w", pady=(7, 18))
    tk.Label(corpo, text="Atendimento e suporte para\na comunidade acadêmica da UNIMAR.", font=("Arial", 10), bg=COR_AZUL_MUITO_ESCURO, fg="#D7EBF7", justify="left").pack(anchor="w")
    bloco = tk.Frame(corpo, bg="#0A4D77", padx=17, pady=17)
    bloco.pack(side="bottom", fill="x")
    tk.Label(bloco, text="UNIVERSIDADE  •  EDUCAÇÃO  •  TECNOLOGIA", font=FONTE_MICRO, bg="#0A4D77", fg=COR_CARTAO).pack(anchor="w")
    return painel


def verificar_login(email, senha, mensagem, janela):
    email, senha = email.strip(), senha.strip()
    if not email or not senha:
        mostrar_mensagem(mensagem, "Informe o email e a senha.")
        return
    for usuario in carregar_usuarios():
        if usuario.get("email", "").lower() == email.lower() and usuario.get("senha") == senha:
            mostrar_mensagem(mensagem, "Login bem-sucedido!", sucesso=True)
            messagebox.showinfo("Login", f"Bem-vindo(a), {usuario.get('nome', 'usuário')}!")
            abrir_inicio(janela, usuario)
            return
    mostrar_mensagem(mensagem, "Email ou senha incorretos.")


def realizar_cadastro(nome, email, senha, confirmar_senha, mensagem):
    nome, email = nome.strip(), email.strip()
    senha, confirmar_senha = senha.strip(), confirmar_senha.strip()
    if not nome or not email or not senha or not confirmar_senha:
        mostrar_mensagem(mensagem, "Preencha todos os campos.")
        return
    if "@" not in email or "." not in email.split("@")[-1]:
        mostrar_mensagem(mensagem, "Informe um email válido.")
        return
    if len(senha) < 4:
        mostrar_mensagem(mensagem, "A senha deve ter pelo menos 4 caracteres.")
        return
    if senha != confirmar_senha:
        mostrar_mensagem(mensagem, "As senhas não coincidem.")
        return
    usuarios = carregar_usuarios()
    if any(u.get("email", "").lower() == email.lower() for u in usuarios):
        mostrar_mensagem(mensagem, "Este email já está cadastrado.")
        return
    usuarios.append({"nome": nome, "email": email, "senha": senha})
    salvar_usuarios(usuarios)
    mostrar_mensagem(mensagem, "Cadastro realizado com sucesso!", sucesso=True)


def adicionar_mensagem_chat(historico, autor, texto, cor):
    bloco = tk.Frame(historico, bg=COR_CARTAO)
    bloco.pack(fill="x", pady=(0, 12))
    tk.Label(bloco, text=autor, font=FONTE_LABEL, bg=COR_CARTAO, fg=cor).pack(anchor="w")
    tk.Label(bloco, text=texto, font=FONTE_PADRAO, bg=COR_CARTAO, fg=COR_TEXTO, justify="left", anchor="w", wraplength=760).pack(fill="x", anchor="w", pady=(3, 0))


def abrir_chatbot(janela, usuario):
    limpar_janela(janela)
    criar_cabecalho(janela)
    conteudo = criar_conteudo(janela)
    area = tk.Frame(conteudo, bg=COR_FUNDO)
    area.pack(fill="both", expand=True, padx=58, pady=24)
    tk.Label(area, text="ASSISTENTE UNIMAR", font=("Arial", 9, "bold"), bg=COR_FUNDO, fg=COR_AZUL).pack(anchor="w")
    tk.Label(area, text="Assistente da Central de Chamados", font=FONTE_TITULO, bg=COR_FUNDO, fg=COR_AZUL_MUITO_ESCURO).pack(anchor="w", pady=(3, 2))
    tk.Label(area, text=f"Olá, {usuario.get('nome', 'usuário')}. Pergunte sobre atendimento e suporte.", font=FONTE_SUBTITULO, bg=COR_FUNDO, fg=COR_TEXTO_SECUNDARIO).pack(anchor="w", pady=(0, 14))
    card = tk.Frame(area, bg=COR_CARTAO, highlightbackground=COR_BORDA, highlightthickness=1, padx=24, pady=20)
    card.pack(fill="both", expand=True)
    historico = tk.Frame(card, bg=COR_CARTAO)
    historico.pack(fill="both", expand=True)
    adicionar_mensagem_chat(historico, "ASSISTENTE UNIMAR", "Olá! Sou o assistente da Central de Chamados. Como posso ajudar?", COR_AZUL)
    entrada_frame = tk.Frame(card, bg=COR_CARTAO)
    entrada_frame.pack(fill="x", pady=(10, 0))
    entrada = tk.Entry(entrada_frame, font=FONTE_PADRAO, bg=COR_FUNDO, fg=COR_TEXTO, insertbackground=COR_AZUL, relief="flat", bd=0, highlightthickness=1, highlightbackground=COR_BORDA, highlightcolor=COR_AZUL)
    entrada.pack(side="left", fill="x", expand=True, ipady=12)
    fila = queue.Queue()

    def processar_resposta():
        try:
            tipo, valor = fila.get_nowait()
        except queue.Empty:
            janela.after(100, processar_resposta)
            return
        botao.config(state="normal")
        entrada.config(state="normal")
        adicionar_mensagem_chat(historico, "ASSISTENTE UNIMAR" if tipo == "ok" else "SISTEMA", valor, COR_AZUL if tipo == "ok" else COR_ERRO)
        janela.after(100, processar_resposta)

    def enviar():
        texto = entrada.get().strip()
        if not texto:
            return
        adicionar_mensagem_chat(historico, "VOCÊ", texto, COR_TEXTO_SECUNDARIO)
        entrada.delete(0, "end")
        entrada.config(state="disabled")
        botao.config(state="disabled")
        def consultar():
            try:
                fila.put(("ok", assistente.perguntar(texto)))
            except Exception as erro:
                fila.put(("erro", f"Não foi possível consultar o agente: {erro}"))
        threading.Thread(target=consultar, daemon=True).start()

    botao = criar_botao(entrada_frame, "ENVIAR", enviar)
    botao.pack_forget()
    botao.pack(side="right", fill="y", padx=(10, 0))
    criar_botao(card, "←  VOLTAR PARA A CENTRAL", lambda: abrir_inicio(janela, usuario), secundario=True)
    criar_aviso(card, "O assistente utiliza um agente configurado no Microsoft Foundry. As credenciais não devem ser colocadas no código.")
    entrada.bind("<Return>", lambda _event: enviar())
    entrada.focus_set()
    criar_rodape(janela)
    janela.after(100, processar_resposta)


def aplicar_responsividade(janela, area, coluna=None, painel=None):
    if not janela.winfo_exists():
        return
    largura = janela.winfo_width()
    altura = janela.winfo_height()
    margem = max(18, min(58, largura // 18))
    area.pack_configure(padx=margem)
    if painel is not None:
        if largura < 850:
            painel.pack_forget()
        elif not painel.winfo_ismapped():
            painel.pack(side="left", fill="y", padx=(0, max(18, min(30, largura // 40))) )
        largura_painel = max(230, min(310, int(largura * 0.29)))
        painel.configure(width=largura_painel)
    if coluna is not None:
        coluna.pack_configure(padx=0)
    if altura < 700:
        area.pack_configure(pady=12)
    else:
        area.pack_configure(pady=24)


def registrar_responsividade(janela, area, coluna=None, painel=None):
    def redimensionar(_event=None):
        aplicar_responsividade(janela, area, coluna, painel)
    janela.bind("<Configure>", redimensionar, add="+")
    janela.after_idle(redimensionar)


def abrir_login(janela):
    limpar_janela(janela)
    criar_cabecalho(janela)
    conteudo = criar_conteudo(janela)
    area = tk.Frame(conteudo, bg=COR_FUNDO)
    area.pack(fill="both", expand=True, padx=58, pady=28)
    painel = criar_painel_lateral(area)
    coluna = tk.Frame(area, bg=COR_FUNDO)
    coluna.pack(side="left", fill="both", expand=True)
    tk.Label(coluna, text="ACESSO INSTITUCIONAL", font=("Arial", 9, "bold"), bg=COR_FUNDO, fg=COR_AZUL).pack(anchor="w", pady=(4, 6))
    tk.Label(coluna, text="Bem-vindo à UNIMAR", font=("Arial", 25, "bold"), bg=COR_FUNDO, fg=COR_AZUL_MUITO_ESCURO).pack(anchor="w")
    tk.Label(coluna, text="Entre para acessar o ambiente de atendimento institucional.", font=FONTE_SUBTITULO, bg=COR_FUNDO, fg=COR_TEXTO_SECUNDARIO).pack(anchor="w", pady=(5, 21))
    card = tk.Frame(coluna, bg=COR_CARTAO, highlightbackground=COR_BORDA, highlightthickness=1, padx=34, pady=29)
    card.pack(fill="x")
    criar_badge(card, "Acesso seguro ao ambiente")
    tk.Label(card, text="Acesse sua conta", font=FONTE_SECAO, bg=COR_CARTAO, fg=COR_TEXTO).pack(anchor="w", pady=(0, 21))
    email = criar_campo(card, "Email")
    senha = criar_campo(card, "Senha", show="*")
    mensagem = criar_mensagem(card)
    criar_botao(card, "ENTRAR NO SISTEMA", lambda: verificar_login(email.get(), senha.get(), mensagem, janela))
    criar_botao(card, "CRIAR NOVO CADASTRO", lambda: abrir_cadastro(janela), secundario=True)
    criar_aviso(card, "Central de atendimento destinada à comunidade acadêmica da Universidade de Marília.")
    criar_rodape(janela)
    registrar_responsividade(janela, area, coluna, painel)
    email.focus_set()


def abrir_cadastro(janela):
    limpar_janela(janela)
    criar_cabecalho(janela)
    conteudo = criar_conteudo(janela)
    area = tk.Frame(conteudo, bg=COR_FUNDO)
    area.pack(fill="both", expand=True, padx=58, pady=22)
    painel = criar_painel_lateral(area)
    coluna = tk.Frame(area, bg=COR_FUNDO)
    coluna.pack(side="left", fill="both", expand=True)
    tk.Label(coluna, text="COMUNIDADE UNIMAR", font=("Arial", 9, "bold"), bg=COR_FUNDO, fg=COR_AZUL).pack(anchor="w", pady=(0, 6))
    tk.Label(coluna, text="Criar cadastro", font=("Arial", 25, "bold"), bg=COR_FUNDO, fg=COR_AZUL_MUITO_ESCURO).pack(anchor="w")
    tk.Label(coluna, text="Cadastre-se para acessar a Central de Chamados da UNIMAR.", font=FONTE_SUBTITULO, bg=COR_FUNDO, fg=COR_TEXTO_SECUNDARIO).pack(anchor="w", pady=(5, 17))
    card = tk.Frame(coluna, bg=COR_CARTAO, highlightbackground=COR_BORDA, highlightthickness=1, padx=34, pady=22)
    card.pack(fill="x")
    campos = [criar_campo(card, "Nome"), criar_campo(card, "Email"), criar_campo(card, "Senha", show="*"), criar_campo(card, "Confirmar senha", show="*")]
    mensagem = criar_mensagem(card)
    criar_botao(card, "CADASTRAR", lambda: realizar_cadastro(*(campo.get() for campo in campos), mensagem))
    criar_botao(card, "←  VOLTAR PARA O LOGIN", lambda: abrir_login(janela), secundario=True)
    criar_aviso(card, "O cadastro continua utilizando o armazenamento local existente em usuarios.json.")
    criar_rodape(janela)
    registrar_responsividade(janela, area, coluna, painel)
    campos[0].focus_set()


def abrir_inicio(janela, usuario):
    limpar_janela(janela)
    criar_cabecalho(janela)
    conteudo = criar_conteudo(janela)
    area = tk.Frame(conteudo, bg=COR_FUNDO)
    area.pack(fill="both", expand=True, padx=58, pady=28)
    tk.Label(area, text="AMBIENTE ACADÊMICO", font=("Arial", 9, "bold"), bg=COR_FUNDO, fg=COR_AZUL).pack(anchor="w")
    tk.Label(area, text="Central de Chamados", font=FONTE_TITULO, bg=COR_FUNDO, fg=COR_AZUL_MUITO_ESCURO).pack(anchor="w", pady=(3, 2))
    tk.Label(area, text="Bem-vindo ao ambiente institucional de atendimento da UNIMAR.", font=FONTE_SUBTITULO, bg=COR_FUNDO, fg=COR_TEXTO_SECUNDARIO).pack(anchor="w", pady=(0, 21))
    topo = tk.Frame(area, bg=COR_FUNDO)
    topo.pack(fill="x")
    topo.columnconfigure(0, weight=1)
    topo.columnconfigure(1, weight=1)
    card_usuario = tk.Frame(topo, bg=COR_CARTAO, highlightbackground=COR_BORDA, highlightthickness=1, padx=26, pady=22)
    card_usuario.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
    tk.Label(card_usuario, text="USUÁRIO CONECTADO", font=FONTE_MICRO, bg=COR_CARTAO, fg=COR_AZUL).pack(anchor="w")
    tk.Label(card_usuario, text=usuario.get("nome", "usuário"), font=("Arial", 19, "bold"), bg=COR_CARTAO, fg=COR_TEXTO).pack(anchor="w", pady=(5, 1))
    tk.Label(card_usuario, text=usuario.get("email", ""), font=FONTE_PEQUENA, bg=COR_CARTAO, fg=COR_TEXTO_SECUNDARIO).pack(anchor="w")
    card_institucional = tk.Frame(topo, bg=COR_AZUL_MUITO_ESCURO, padx=26, pady=22)
    card_institucional.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
    tk.Label(card_institucional, text="UNIVERSIDADE DE MARÍLIA", font=FONTE_MICRO, bg=COR_AZUL_MUITO_ESCURO, fg="#A9D5EC").pack(anchor="w")
    tk.Label(card_institucional, text="Atendimento institucional", font=("Arial", 17, "bold"), bg=COR_AZUL_MUITO_ESCURO, fg=COR_CARTAO).pack(anchor="w", pady=(5, 2))
    tk.Label(card_institucional, text="Um ambiente preparado para apoiar a comunidade acadêmica.", font=FONTE_PEQUENA, bg=COR_AZUL_MUITO_ESCURO, fg="#D7EBF7", justify="left", wraplength=430).pack(anchor="w")
    painel = tk.Frame(area, bg=COR_CARTAO, highlightbackground=COR_BORDA, highlightthickness=1, padx=28, pady=24)
    painel.pack(fill="x", pady=20)
    tk.Label(painel, text="ATENDIMENTO E SUPORTE", font=FONTE_MICRO, bg=COR_CARTAO, fg=COR_AZUL).pack(anchor="w")
    tk.Label(painel, text="Central de Chamados", font=FONTE_SECAO, bg=COR_CARTAO, fg=COR_TEXTO).pack(anchor="w", pady=(4, 3))
    tk.Label(painel, text="A área de chamados está em desenvolvimento. Agora você também pode conversar com o Assistente UNIMAR para receber orientação.", font=FONTE_PADRAO, bg=COR_CARTAO, fg=COR_TEXTO_SECUNDARIO, wraplength=900, justify="left").pack(anchor="w", fill="x")
    criar_botao(painel, "ABRIR ASSISTENTE UNIMAR", lambda: abrir_chatbot(janela, usuario))
    info = tk.Frame(painel, bg=COR_AZUL_PALETA, padx=16, pady=13)
    info.pack(fill="x", pady=(16, 0))
    tk.Label(info, text="ASSISTENTE DE IA  •  MICROSOFT FOUNDRY  •  CENTRAL DE ATENDIMENTO", font=FONTE_MICRO, bg=COR_AZUL_PALETA, fg=COR_AZUL_MUITO_ESCURO).pack(anchor="w")
    criar_botao(area, "SAIR DO SISTEMA", lambda: abrir_login(janela), secundario=True)
    criar_rodape(janela)
    registrar_responsividade(janela, area)


def main():
    garantir_arquivo_usuarios()
    janela = tk.Tk()
    configurar_janela(janela)
    abrir_login(janela)
    janela.mainloop()


if __name__ == "__main__":
    main()
