import tkinter as tk
from tkinter import messagebox, ttk

from assistente import AssistenteFoundry
from estudos import (
    concluir_tarefa,
    criar_projeto,
    criar_tarefa,
    excluir_tarefa,
    progresso_projeto,
    projetos_do_usuario,
    tarefas_do_usuario,
)
from historico import historico_do_usuario, registrar_evento
from usuarios import autenticar, cadastrar_usuario

COR_AZUL = "#0072BC"
COR_AZUL_ESCURO = "#005A94"
COR_AZUL_CLARO = "#EAF5FC"
COR_FUNDO = "#F5F7FA"
COR_CARTAO = "#FFFFFF"
COR_TEXTO = "#172B4D"
COR_SEC = "#667085"
COR_BORDA = "#DCE4EC"
COR_SUCESSO = "#16803C"
COR_ERRO = "#C62828"

F_TITULO = ("Arial", 25, "bold")
F_SECAO = ("Arial", 16, "bold")
F_NORMAL = ("Arial", 11)
F_LABEL = ("Arial", 10, "bold")
F_BOTAO = ("Arial", 10, "bold")
F_PEQUENA = ("Arial", 9)


class Aplicacao(tk.Tk):
    """Aplicação principal do UNIMAR Study."""

    def __init__(self):
        super().__init__()
        self.title("UNIMAR Study | Organize. Estude. Evolua.")
        self.geometry("1100x760")
        self.minsize(850, 620)
        self.configure(bg=COR_FUNDO)
        self.usuario_atual = None
        self.assistente = AssistenteFoundry()
        self.bind("<Escape>", lambda e: self.mostrar_dashboard() if self.usuario_atual else None)
        self.mostrar_login()

    def limpar(self):
        for widget in self.winfo_children():
            widget.destroy()

    def cabecalho(self, subtitulo):
        frame = tk.Frame(self, bg=COR_AZUL, height=78)
        frame.pack(fill="x")
        frame.pack_propagate(False)
        tk.Label(frame, text="UNIMAR STUDY", font=("Arial", 22, "bold"), bg=COR_AZUL, fg="white").pack(side="left", padx=30)
        tk.Label(frame, text=subtitulo.upper(), font=("Arial", 9, "bold"), bg=COR_AZUL, fg="white").pack(side="right", padx=30)

    def rodape(self):
        frame = tk.Frame(self, bg="white", height=34, highlightbackground=COR_BORDA, highlightthickness=1)
        frame.pack(side="bottom", fill="x")
        frame.pack_propagate(False)
        tk.Label(frame, text="UNIMAR STUDY • ORGANIZE. ESTUDE. EVOLUA.", font=("Arial", 8, "bold"), bg="white", fg=COR_SEC).pack(side="left", padx=20)

    def botao(self, parent, texto, comando, secundario=False):
        botao = tk.Button(parent, text=texto, command=comando, font=F_BOTAO, cursor="hand2", padx=12, pady=8,
                          bg="white" if secundario else COR_AZUL, fg=COR_AZUL if secundario else "white",
                          activebackground=COR_AZUL_CLARO if secundario else COR_AZUL_ESCURO,
                          activeforeground=COR_AZUL if secundario else "white",
                          relief="solid" if secundario else "flat", bd=1 if secundario else 0)
        botao.pack(fill="x", pady=4)
        return botao

    def campo(self, parent, texto, variable=None, show=None):
        tk.Label(parent, text=texto.upper(), font=F_LABEL, bg=COR_CARTAO, fg=COR_TEXTO).pack(anchor="w", pady=(5, 4))
        entrada = tk.Entry(parent, textvariable=variable, show=show or "", font=F_NORMAL, bg=COR_FUNDO,
                           fg=COR_TEXTO, relief="flat", highlightthickness=1, highlightbackground=COR_BORDA,
                           highlightcolor=COR_AZUL)
        entrada.pack(fill="x", ipady=7, pady=(0, 6))
        return entrada

    def mostrar_login(self):
        self.usuario_atual = None
        self.limpar()
        self.cabecalho("Acesso")
        area = tk.Frame(self, bg=COR_FUNDO)
        area.pack(fill="both", expand=True, padx=80, pady=45)
        card = tk.Frame(area, bg=COR_CARTAO, highlightbackground=COR_BORDA, highlightthickness=1, padx=38, pady=30)
        card.pack(fill="x", padx=100)
        tk.Label(card, text="Bem-vindo de volta", font=F_TITULO, bg=COR_CARTAO, fg=COR_AZUL_ESCURO).pack(anchor="w")
        tk.Label(card, text="Organize suas tarefas, acompanhe seus projetos e evolua nos estudos.",
                 font=F_NORMAL, bg=COR_CARTAO, fg=COR_SEC, wraplength=650).pack(anchor="w", pady=(4, 20))
        email = tk.StringVar()
        senha = tk.StringVar()
        entrada_email = self.campo(card, "Email", email)
        self.campo(card, "Senha", senha, "*")
        mensagem = tk.Label(card, text="", font=F_PEQUENA, bg=COR_CARTAO)
        mensagem.pack(fill="x", pady=3)

        def entrar():
            usuario = autenticar(email.get(), senha.get())
            if usuario is None:
                mensagem.config(text="Email ou senha incorretos.", fg=COR_ERRO)
                return
            self.usuario_atual = usuario
            registrar_evento(usuario["email"], "login", "Usuário realizou login.")
            self.mostrar_dashboard()

        self.botao(card, "ENTRAR", entrar)
        self.botao(card, "CRIAR CONTA", self.mostrar_cadastro, True)
        entrada_email.bind("<Return>", lambda e: entrar())
        entrada_email.focus_set()
        self.rodape()

    def mostrar_cadastro(self):
        self.limpar()
        self.cabecalho("Novo cadastro")
        area = tk.Frame(self, bg=COR_FUNDO)
        area.pack(fill="both", expand=True, padx=100, pady=30)
        card = tk.Frame(area, bg=COR_CARTAO, highlightbackground=COR_BORDA, highlightthickness=1, padx=35, pady=25)
        card.pack(fill="x")
        tk.Label(card, text="Criar sua conta", font=F_TITULO, bg=COR_CARTAO, fg=COR_AZUL_ESCURO).pack(anchor="w")
        tk.Label(card, text="Seu histórico, tarefas e projetos serão vinculados à sua conta.", font=F_NORMAL,
                 bg=COR_CARTAO, fg=COR_SEC).pack(anchor="w", pady=(3, 18))
        nome, email, senha, confirmar = (tk.StringVar() for _ in range(4))
        self.campo(card, "Nome", nome)
        self.campo(card, "Email", email)
        self.campo(card, "Senha", senha, "*")
        self.campo(card, "Confirmar senha", confirmar, "*")
        mensagem = tk.Label(card, text="", font=F_PEQUENA, bg=COR_CARTAO)
        mensagem.pack(fill="x")

        def cadastrar():
            ok, texto = cadastrar_usuario(nome.get(), email.get(), senha.get(), confirmar.get())
            mensagem.config(text=texto, fg=COR_SUCESSO if ok else COR_ERRO)
            if ok:
                messagebox.showinfo("Cadastro", texto)
                self.mostrar_login()

        self.botao(card, "CADASTRAR", cadastrar)
        self.botao(card, "VOLTAR PARA O LOGIN", self.mostrar_login, True)
        self.rodape()

    def criar_menu(self, parent):
        menu = tk.Frame(parent, bg=COR_CARTAO, width=190, highlightbackground=COR_BORDA, highlightthickness=1)
        menu.pack(side="left", fill="y", padx=(0, 15))
        menu.pack_propagate(False)
        tk.Label(menu, text="MENU", font=F_LABEL, bg=COR_CARTAO, fg=COR_SEC).pack(anchor="w", padx=18, pady=(18, 10))
        for texto, comando in (("Dashboard", self.mostrar_dashboard), ("Minhas tarefas", self.mostrar_tarefas),
                               ("Meus projetos", self.mostrar_projetos), ("Histórico", self.mostrar_historico),
                               ("Assistente", self.mostrar_assistente)):
            self.botao(menu, texto, comando)
        tk.Frame(menu, bg=COR_CARTAO).pack(fill="both", expand=True)
        self.botao(menu, "Sair", self.mostrar_login, True)

    def area_principal(self, titulo, descricao):
        self.limpar()
        self.cabecalho(titulo)
        area = tk.Frame(self, bg=COR_FUNDO)
        area.pack(fill="both", expand=True, padx=25, pady=25)
        self.criar_menu(area)
        conteudo = tk.Frame(area, bg=COR_FUNDO)
        conteudo.pack(side="left", fill="both", expand=True)
        tk.Label(conteudo, text=titulo, font=F_TITULO, bg=COR_FUNDO, fg=COR_AZUL_ESCURO).pack(anchor="w")
        if descricao:
            tk.Label(conteudo, text=descricao, font=F_NORMAL, bg=COR_FUNDO, fg=COR_SEC).pack(anchor="w", pady=(3, 15))
        return conteudo

    def mostrar_dashboard(self):
        if not self.usuario_atual:
            return self.mostrar_login()
        conteudo = self.area_principal("Dashboard", "Um resumo da sua rotina de estudos.")
        tarefas = tarefas_do_usuario(self.usuario_atual["email"])
        projetos = projetos_do_usuario(self.usuario_atual["email"])
        concluidas = sum(1 for t in tarefas if t.get("concluida"))
        cards = tk.Frame(conteudo, bg=COR_FUNDO)
        cards.pack(fill="x")
        for coluna, (titulo, valor) in enumerate((("Tarefas", len(tarefas)), ("Pendentes", len(tarefas)-concluidas), ("Concluídas", concluidas), ("Projetos", len(projetos)))):
            card = tk.Frame(cards, bg=COR_CARTAO, padx=18, pady=15, highlightbackground=COR_BORDA, highlightthickness=1)
            card.grid(row=0, column=coluna, sticky="nsew", padx=4)
            tk.Label(card, text=titulo, font=F_LABEL, bg=COR_CARTAO, fg=COR_SEC).pack(anchor="w")
            tk.Label(card, text=str(valor), font=("Arial", 25, "bold"), bg=COR_CARTAO, fg=COR_AZUL_ESCURO).pack(anchor="w", pady=(5, 0))
            cards.columnconfigure(coluna, weight=1)
        destaque = tk.Frame(conteudo, bg=COR_CARTAO, padx=20, pady=18, highlightbackground=COR_BORDA, highlightthickness=1)
        destaque.pack(fill="both", expand=True, pady=18)
        tk.Label(destaque, text="Próximas tarefas", font=F_SECAO, bg=COR_CARTAO, fg=COR_TEXTO).pack(anchor="w")
        pendentes = [t for t in tarefas if not t.get("concluida")][:6]
        if not pendentes:
            tk.Label(destaque, text="Nenhuma tarefa pendente.", font=F_NORMAL, bg=COR_CARTAO, fg=COR_SUCESSO).pack(anchor="w", pady=15)
        for tarefa in pendentes:
            tk.Label(destaque, text=f"• {tarefa['titulo']} — {tarefa.get('prioridade', 'Média')}", font=F_NORMAL, bg=COR_CARTAO, fg=COR_TEXTO).pack(anchor="w", pady=4)
        self.rodape()

    def mostrar_tarefas(self):
        conteudo = self.area_principal("Minhas tarefas", "Crie, conclua e acompanhe suas atividades.")
        self.botao(conteudo, "+ NOVA TAREFA", self.mostrar_nova_tarefa)
        lista = tk.Frame(conteudo, bg=COR_CARTAO, highlightbackground=COR_BORDA, highlightthickness=1)
        lista.pack(fill="both", expand=True, pady=12)
        tarefas = tarefas_do_usuario(self.usuario_atual["email"])
        if not tarefas:
            tk.Label(lista, text="Você ainda não possui tarefas.", font=F_NORMAL, bg=COR_CARTAO, fg=COR_SEC).pack(pady=40)
        for tarefa in tarefas:
            linha = tk.Frame(lista, bg=COR_CARTAO, padx=15, pady=9)
            linha.pack(fill="x")
            estado = tk.BooleanVar(value=tarefa.get("concluida", False))
            tk.Checkbutton(linha, variable=estado, bg=COR_CARTAO, activebackground=COR_CARTAO,
                           command=lambda i=tarefa["id"]: self.alternar_tarefa(i)).pack(side="left")
            texto = f"{tarefa['titulo']}  |  {tarefa.get('prioridade', 'Média')}"
            if tarefa.get("prazo"):
                texto += f"  |  Prazo: {tarefa['prazo']}"
            tk.Label(linha, text=texto, font=F_NORMAL, bg=COR_CARTAO,
                     fg=COR_SEC if tarefa.get("concluida") else COR_TEXTO).pack(side="left", fill="x", expand=True)
            tk.Button(linha, text="Excluir", command=lambda i=tarefa["id"]: self.excluir_tarefa(i), font=F_PEQUENA,
                      bg="white", relief="flat").pack(side="right")
        self.rodape()

    def alternar_tarefa(self, id_tarefa):
        ok, texto = concluir_tarefa(self.usuario_atual["email"], id_tarefa)
        if not ok:
            messagebox.showinfo("Tarefa", texto)
        self.mostrar_tarefas()

    def excluir_tarefa(self, id_tarefa):
        if not messagebox.askyesno("Excluir tarefa", "Deseja realmente excluir esta tarefa?"):
            return
        ok, texto = excluir_tarefa(self.usuario_atual["email"], id_tarefa)
        if ok:
            self.mostrar_tarefas()
        else:
            messagebox.showwarning("Tarefa", texto)

    def mostrar_nova_tarefa(self):
        self.limpar()
        self.cabecalho("Nova tarefa")
        area = tk.Frame(self, bg=COR_FUNDO)
        area.pack(fill="both", expand=True, padx=90, pady=30)
        card = tk.Frame(area, bg=COR_CARTAO, padx=30, pady=25, highlightbackground=COR_BORDA, highlightthickness=1)
        card.pack(fill="both", expand=True)
        tk.Label(card, text="Criar tarefa", font=F_TITULO, bg=COR_CARTAO, fg=COR_AZUL_ESCURO).pack(anchor="w")
        titulo, prazo, prioridade = tk.StringVar(), tk.StringVar(), tk.StringVar(value="Média")
        self.campo(card, "Título", titulo)
        self.campo(card, "Prazo (opcional)", prazo)
        tk.Label(card, text="PRIORIDADE", font=F_LABEL, bg=COR_CARTAO, fg=COR_TEXTO).pack(anchor="w", pady=(5, 4))
        prioridades = tk.Frame(card, bg=COR_CARTAO)
        prioridades.pack(anchor="w")
        for valor in ("Baixa", "Média", "Alta"):
            tk.Radiobutton(prioridades, text=valor, value=valor, variable=prioridade, bg=COR_CARTAO, activebackground=COR_CARTAO).pack(side="left", padx=(0, 12))
        tk.Label(card, text="DESCRIÇÃO", font=F_LABEL, bg=COR_CARTAO, fg=COR_TEXTO).pack(anchor="w", pady=(12, 4))
        descricao = tk.Text(card, height=8, font=F_NORMAL, bg=COR_FUNDO, relief="flat", highlightthickness=1, highlightbackground=COR_BORDA)
        descricao.pack(fill="both", expand=True)

        def salvar():
            ok, texto, _ = criar_tarefa(self.usuario_atual["email"], titulo.get(), descricao.get("1.0", "end"), prioridade.get(), prazo.get())
            if ok:
                messagebox.showinfo("Tarefa", texto)
                self.mostrar_tarefas()
            else:
                messagebox.showwarning("Tarefa", texto)

        self.botao(card, "CRIAR TAREFA", salvar)
        self.botao(card, "VOLTAR", self.mostrar_tarefas, True)
        self.rodape()

    def mostrar_projetos(self):
        conteudo = self.area_principal("Meus projetos", "Organize trabalhos escolares e acompanhe o progresso.")
        self.botao(conteudo, "+ NOVO PROJETO", self.mostrar_novo_projeto)
        lista = tk.Frame(conteudo, bg=COR_FUNDO)
        lista.pack(fill="both", expand=True, pady=12)
        projetos = projetos_do_usuario(self.usuario_atual["email"])
        if not projetos:
            tk.Label(lista, text="Crie seu primeiro projeto escolar.", font=F_NORMAL, bg=COR_FUNDO, fg=COR_SEC).pack(pady=40)
        for projeto in projetos:
            total, concluidas, percentual = progresso_projeto(self.usuario_atual["email"], projeto["id"])
            card = tk.Frame(lista, bg=COR_CARTAO, padx=18, pady=15, highlightbackground=COR_BORDA, highlightthickness=1)
            card.pack(fill="x", pady=5)
            tk.Label(card, text=projeto["nome"], font=F_SECAO, bg=COR_CARTAO, fg=COR_TEXTO).pack(anchor="w")
            tk.Label(card, text=projeto.get("descricao", ""), font=F_PEQUENA, bg=COR_CARTAO, fg=COR_SEC).pack(anchor="w", pady=3)
            tk.Label(card, text=f"{concluidas} de {total} tarefas concluídas • {percentual}%", font=F_NORMAL, bg=COR_CARTAO, fg=COR_AZUL).pack(anchor="w", pady=4)
        self.rodape()

    def mostrar_novo_projeto(self):
        self.limpar()
        self.cabecalho("Novo projeto")
        area = tk.Frame(self, bg=COR_FUNDO)
        area.pack(fill="both", expand=True, padx=90, pady=30)
        card = tk.Frame(area, bg=COR_CARTAO, padx=30, pady=25, highlightbackground=COR_BORDA, highlightthickness=1)
        card.pack(fill="both", expand=True)
        tk.Label(card, text="Criar projeto", font=F_TITULO, bg=COR_CARTAO, fg=COR_AZUL_ESCURO).pack(anchor="w")
        nome = tk.StringVar()
        self.campo(card, "Nome do projeto", nome)
        tk.Label(card, text="DESCRIÇÃO", font=F_LABEL, bg=COR_CARTAO, fg=COR_TEXTO).pack(anchor="w", pady=(12, 4))
        descricao = tk.Text(card, height=10, font=F_NORMAL, bg=COR_FUNDO, relief="flat", highlightthickness=1, highlightbackground=COR_BORDA)
        descricao.pack(fill="both", expand=True)

        def salvar():
            ok, texto, _ = criar_projeto(self.usuario_atual["email"], nome.get(), descricao.get("1.0", "end"))
            if ok:
                messagebox.showinfo("Projeto", texto)
                self.mostrar_projetos()
            else:
                messagebox.showwarning("Projeto", texto)

        self.botao(card, "CRIAR PROJETO", salvar)
        self.botao(card, "VOLTAR", self.mostrar_projetos, True)
        self.rodape()

    def mostrar_historico(self):
        conteudo = self.area_principal("Histórico", "Acompanhe as ações realizadas dentro do aplicativo.")
        tabela_frame = tk.Frame(conteudo, bg=COR_CARTAO, highlightbackground=COR_BORDA, highlightthickness=1)
        tabela_frame.pack(fill="both", expand=True)
        tabela = ttk.Treeview(tabela_frame, columns=("data", "tipo", "descricao"), show="headings")
        for coluna, titulo, largura in (("data", "Data", 130), ("tipo", "Ação", 150), ("descricao", "Descrição", 400)):
            tabela.heading(coluna, text=titulo)
            tabela.column(coluna, width=largura, anchor="w")
        scroll = ttk.Scrollbar(tabela_frame, orient="vertical", command=tabela.yview)
        tabela.configure(yscrollcommand=scroll.set)
        tabela.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        for evento in reversed(historico_do_usuario(self.usuario_atual["email"])):
            tabela.insert("", "end", values=(evento.get("data", ""), evento.get("tipo", ""), evento.get("descricao", "")))
        self.rodape()

    def mostrar_assistente(self):
        conteudo = self.area_principal("Assistente de Estudos", "Peça ajuda para entender conteúdos ou organizar sua rotina.")
        pergunta = tk.Text(conteudo, height=5, font=F_NORMAL, bg=COR_CARTAO, relief="flat", highlightthickness=1, highlightbackground=COR_BORDA)
        pergunta.pack(fill="x")
        resposta = tk.Text(conteudo, height=14, font=F_NORMAL, bg=COR_CARTAO, relief="flat", highlightthickness=1, highlightbackground=COR_BORDA, state="disabled")
        resposta.pack(fill="both", expand=True, pady=12)

        def perguntar():
            texto = pergunta.get("1.0", "end").strip()
            if not texto:
                messagebox.showwarning("Assistente", "Digite uma pergunta.")
                return
            try:
                resultado = self.assistente.perguntar(texto)
                registrar_evento(self.usuario_atual["email"], "assistente", "Usuário consultou o Assistente de Estudos.")
            except Exception as erro:
                resultado = f"Não foi possível consultar o assistente.\n\n{erro}"
            resposta.config(state="normal")
            resposta.delete("1.0", "end")
            resposta.insert("1.0", resultado)
            resposta.config(state="disabled")

        self.botao(conteudo, "PERGUNTAR", perguntar)
        pergunta.bind("<Control-Return>", lambda e: perguntar())
        self.rodape()
