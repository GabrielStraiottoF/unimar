import tkinter as tk
from tkinter import messagebox

from estudos import (
    buscar_projeto,
    concluir_tarefa,
    criar_projeto,
    criar_tarefa,
    excluir_projeto,
    excluir_tarefa,
    projetos_do_usuario,
    progresso_projeto,
    tarefas_do_usuario,
)
from historico import historico_do_usuario
from usuarios import autenticar, cadastrar_usuario

FUNDO = "#f4f4f4"
BRANCO = "#ffffff"
TEXTO = "#222222"


class Aplicacao(tk.Tk):
    """Interface simples usando os conceitos apresentados nas Aulas 1 e 2."""

    def __init__(self):
        super().__init__()
        self.title("UNIMAR Study")
        self.geometry("760x560")
        self.minsize(650, 500)
        self.configure(bg=FUNDO)
        self.usuario_atual = None
        self.bind("<Escape>", lambda evento: self.mostrar_inicio())
        self.mostrar_login()

    def limpar(self):
        for widget in self.winfo_children():
            widget.destroy()

    def titulo(self, texto, tamanho=22):
        label = tk.Label(
            self, text=texto, font=("Arial", tamanho, "bold"),
            bg=FUNDO, fg=TEXTO,
        )
        label.pack(pady=(25, 10))
        return label

    def campo(self, pai, texto, variavel, senha=False):
        tk.Label(
            pai, text=texto, font=("Arial", 11),
            bg=BRANCO, fg=TEXTO,
        ).pack(anchor="w", pady=(8, 3))
        entry = tk.Entry(
            pai, textvariable=variavel, font=("Arial", 11),
            show="*" if senha else "",
        )
        entry.pack(fill="x", ipady=6)
        return entry

    def botao(self, pai, texto, comando, largura=18):
        return tk.Button(
            pai, text=texto, command=comando,
            font=("Arial", 10, "bold"), width=largura, pady=7,
        )

    # LOGIN E CADASTRO

    def mostrar_login(self):
        self.limpar()
        self.usuario_atual = None
        self.titulo("UNIMAR STUDY", 24)
        tk.Label(
            self, text="Organize seus estudos de forma simples.",
            bg=FUNDO, fg="#555555", font=("Arial", 11),
        ).pack()

        caixa = tk.Frame(self, bg=BRANCO, padx=35, pady=25)
        caixa.pack(pady=25, ipadx=20)
        email = tk.StringVar()
        senha = tk.StringVar()
        self.campo(caixa, "E-mail", email)
        self.campo(caixa, "Senha", senha, senha=True)

        def entrar():
            usuario = autenticar(email.get(), senha.get())
            if usuario is None:
                messagebox.showerror("Login", "E-mail ou senha incorretos.")
                return
            self.usuario_atual = usuario
            self.mostrar_inicio()

        self.botao(caixa, "ENTRAR", entrar).pack(pady=(18, 8))
        self.botao(caixa, "CRIAR CONTA", self.mostrar_cadastro).pack()

    def mostrar_cadastro(self):
        self.limpar()
        self.titulo("CRIAR CONTA")
        caixa = tk.Frame(self, bg=BRANCO, padx=35, pady=20)
        caixa.pack(pady=10, ipadx=20)

        nome = tk.StringVar()
        email = tk.StringVar()
        senha = tk.StringVar()
        confirmar = tk.StringVar()
        self.campo(caixa, "Nome", nome)
        self.campo(caixa, "E-mail", email)
        self.campo(caixa, "Senha", senha, senha=True)
        self.campo(caixa, "Confirmar senha", confirmar, senha=True)

        def cadastrar():
            sucesso, mensagem = cadastrar_usuario(
                nome.get(), email.get(), senha.get(), confirmar.get()
            )
            if not sucesso:
                messagebox.showerror("Cadastro", mensagem)
                return
            messagebox.showinfo("Cadastro", mensagem)
            self.mostrar_login()

        botoes = tk.Frame(caixa, bg=BRANCO)
        botoes.pack(pady=(18, 0))
        self.botao(botoes, "CADASTRAR", cadastrar, 15).pack(side="left", padx=5)
        self.botao(botoes, "VOLTAR", self.mostrar_login, 15).pack(side="left", padx=5)

    # INÍCIO

    def mostrar_inicio(self):
        if self.usuario_atual is None:
            self.mostrar_login()
            return

        self.limpar()
        self.titulo("UNIMAR STUDY")
        nome = self.usuario_atual.get("nome", "Aluno")
        tk.Label(
            self, text=f"Olá, {nome}!", font=("Arial", 13),
            bg=FUNDO, fg=TEXTO,
        ).pack(pady=(0, 20))

        menu = tk.Frame(self, bg=FUNDO)
        menu.pack()
        botoes = [
            ("TAREFAS", self.mostrar_tarefas),
            ("PROJETOS", self.mostrar_projetos),
            ("HISTÓRICO", self.mostrar_historico),
            ("ASSISTENTE", self.mostrar_assistente),
        ]
        for indice, (texto, comando) in enumerate(botoes):
            linha = indice // 2
            coluna = indice % 2
            self.botao(menu, texto, comando, 20).grid(
                row=linha, column=coluna, padx=8, pady=8
            )
        self.botao(self, "SAIR", self.mostrar_login, 20).pack(pady=25)

    # TAREFAS

    def mostrar_tarefas(self):
        self.limpar()
        self.titulo("MINHAS TAREFAS")
        topo = tk.Frame(self, bg=FUNDO)
        topo.pack(fill="x", padx=30)
        self.botao(topo, "+ NOVA TAREFA", self.mostrar_nova_tarefa, 18).pack(side="left")
        self.botao(topo, "VOLTAR", self.mostrar_inicio, 12).pack(side="right")

        lista = tk.Frame(self, bg=BRANCO, padx=15, pady=10)
        lista.pack(fill="both", expand=True, padx=30, pady=15)
        tarefas = tarefas_do_usuario(self.usuario_atual["email"])

        if not tarefas:
            tk.Label(
                lista, text="Nenhuma tarefa cadastrada.",
                bg=BRANCO, fg="#555555", font=("Arial", 11),
            ).pack(pady=30)
            return

        for tarefa in tarefas:
            self.mostrar_linha_tarefa(lista, tarefa)

    def mostrar_linha_tarefa(self, pai, tarefa):
        linha = tk.Frame(pai, bg=BRANCO)
        linha.pack(fill="x", pady=6)

        concluida = bool(tarefa.get("concluida", False))
        variavel = tk.BooleanVar(value=concluida)
        check = tk.Checkbutton(
            linha,
            variable=variavel,
            bg=BRANCO,
            state="disabled" if concluida else "normal",
        )
        check.pack(side="left")

        texto_status = "CONCLUÍDA" if concluida else "PENDENTE"
        texto = f"{tarefa.get('titulo', '')}  |  {texto_status}"
        if tarefa.get("prioridade"):
            texto += f"  |  {tarefa.get('prioridade')}"

        tk.Label(
            linha, text=texto, bg=BRANCO, fg=TEXTO,
            font=("Arial", 10, "bold" if concluida else "normal"),
            anchor="w",
        ).pack(side="left", fill="x", expand=True)

        self.botao(
            linha, "DETALHES",
            lambda id_tarefa=tarefa["id"]: self.mostrar_detalhes_tarefa(id_tarefa),
            10,
        ).pack(side="left", padx=3)

        if not concluida:
            self.botao(
                linha, "CONCLUIR",
                lambda id_tarefa=tarefa["id"]: self.concluir(id_tarefa),
                9,
            ).pack(side="left", padx=3)

        self.botao(
            linha, "EXCLUIR",
            lambda id_tarefa=tarefa["id"]: self.excluir(id_tarefa),
            9,
        ).pack(side="left", padx=3)

    def mostrar_detalhes_tarefa(self, id_tarefa):
        tarefa = next(
            (
                t for t in tarefas_do_usuario(self.usuario_atual["email"])
                if str(t.get("id")) == str(id_tarefa)
            ),
            None,
        )
        if tarefa is None:
            messagebox.showerror("Tarefa", "Tarefa não encontrada.")
            return

        projeto = buscar_projeto(
            self.usuario_atual["email"], tarefa.get("projeto_id")
        ) if tarefa.get("projeto_id") is not None else None
        nome_projeto = projeto.get("nome") if projeto else "Sem projeto"
        status = "CONCLUÍDA" if tarefa.get("concluida") else "PENDENTE"

        detalhes = (
            f"Título: {tarefa.get('titulo', '')}\n\n"
            f"Status: {status}\n"
            f"Prioridade: {tarefa.get('prioridade', 'Média')}\n"
            f"Prazo: {tarefa.get('prazo') or 'Não informado'}\n"
            f"Projeto: {nome_projeto}\n\n"
            f"Descrição:\n{tarefa.get('descricao') or 'Nenhuma descrição informada.'}"
        )
        messagebox.showinfo("Detalhes da tarefa", detalhes)

    def concluir(self, id_tarefa):
        sucesso, mensagem = concluir_tarefa(
            self.usuario_atual["email"], id_tarefa
        )
        if sucesso:
            messagebox.showinfo("Tarefa", mensagem)
        else:
            messagebox.showwarning("Tarefa", mensagem)
        self.mostrar_tarefas()

    def excluir(self, id_tarefa):
        confirmar = messagebox.askyesno(
            "Excluir tarefa", "Deseja realmente excluir esta tarefa?"
        )
        if not confirmar:
            return
        sucesso, mensagem = excluir_tarefa(
            self.usuario_atual["email"], id_tarefa
        )
        if sucesso:
            messagebox.showinfo("Tarefa", mensagem)
        else:
            messagebox.showerror("Tarefa", mensagem)
        self.mostrar_tarefas()

    def mostrar_nova_tarefa(self):
        self.limpar()
        self.titulo("NOVA TAREFA")
        caixa = tk.Frame(self, bg=BRANCO, padx=35, pady=20)
        caixa.pack(pady=10, fill="x", padx=70)

        titulo = tk.StringVar()
        prioridade = tk.StringVar(value="Média")
        prazo = tk.StringVar()
        projeto_id = tk.StringVar(value="nenhum")
        self.campo(caixa, "Título", titulo)

        tk.Label(
            caixa, text="Descrição", bg=BRANCO, fg=TEXTO,
            font=("Arial", 11),
        ).pack(anchor="w", pady=(8, 3))
        descricao = tk.Text(caixa, height=4, font=("Arial", 11))
        descricao.pack(fill="x")

        tk.Label(
            caixa, text="Prioridade", bg=BRANCO, fg=TEXTO,
            font=("Arial", 11),
        ).pack(anchor="w", pady=(10, 3))
        opcoes = tk.Frame(caixa, bg=BRANCO)
        opcoes.pack(anchor="w")
        for opcao in ("Baixa", "Média", "Alta"):
            tk.Radiobutton(
                opcoes, text=opcao, variable=prioridade,
                value=opcao, bg=BRANCO,
            ).pack(side="left", padx=(0, 12))

        tk.Label(
            caixa, text="Projeto", bg=BRANCO, fg=TEXTO,
            font=("Arial", 11),
        ).pack(anchor="w", pady=(10, 3))
        projetos = projetos_do_usuario(self.usuario_atual["email"])
        projeto_opcoes = [("Sem projeto", "nenhum")]
        projeto_opcoes.extend(
            (p.get("nome", "Projeto"), str(p.get("id"))) for p in projetos
        )
        for nome_projeto, valor in projeto_opcoes:
            tk.Radiobutton(
                caixa, text=nome_projeto, variable=projeto_id,
                value=valor, bg=BRANCO, anchor="w",
            ).pack(fill="x")

        self.campo(caixa, "Prazo (opcional)", prazo)
        botoes = tk.Frame(caixa, bg=BRANCO)
        botoes.pack(pady=18)

        def salvar():
            id_projeto = None if projeto_id.get() == "nenhum" else projeto_id.get()
            sucesso, mensagem, _ = criar_tarefa(
                self.usuario_atual["email"], titulo.get(),
                descricao.get("1.0", "end").strip(), prioridade.get(),
                prazo.get(), id_projeto,
            )
            if sucesso:
                messagebox.showinfo("Tarefa", mensagem)
                self.mostrar_tarefas()
            else:
                messagebox.showerror("Tarefa", mensagem)

        self.botao(botoes, "SALVAR", salvar, 15).pack(side="left", padx=5)
        self.botao(botoes, "CANCELAR", self.mostrar_tarefas, 15).pack(side="left", padx=5)

    # PROJETOS

    def mostrar_projetos(self):
        self.limpar()
        self.titulo("MEUS PROJETOS")
        topo = tk.Frame(self, bg=FUNDO)
        topo.pack(fill="x", padx=30)
        self.botao(topo, "+ NOVO PROJETO", self.mostrar_novo_projeto, 18).pack(side="left")
        self.botao(topo, "VOLTAR", self.mostrar_inicio, 12).pack(side="right")

        lista = tk.Frame(self, bg=BRANCO, padx=20, pady=15)
        lista.pack(fill="both", expand=True, padx=30, pady=15)
        projetos = projetos_do_usuario(self.usuario_atual["email"])

        if not projetos:
            tk.Label(
                lista, text="Nenhum projeto cadastrado.",
                bg=BRANCO, fg="#555555",
            ).pack(pady=30)
            return

        for projeto in projetos:
            total, concluidas, percentual = progresso_projeto(
                self.usuario_atual["email"], projeto["id"]
            )
            frame = tk.Frame(lista, bg=BRANCO)
            frame.pack(fill="x", pady=8)
            tk.Label(
                frame, text=projeto.get("nome", ""),
                font=("Arial", 12, "bold"), bg=BRANCO, fg=TEXTO,
            ).pack(side="left", fill="x", expand=True)
            tk.Label(
                frame,
                text=f"{concluidas}/{total} concluídas ({percentual}%)",
                bg=BRANCO, fg="#555555", width=24,
            ).pack(side="left")
            self.botao(
                frame, "ABRIR",
                lambda id_projeto=projeto["id"]: self.mostrar_projeto(id_projeto),
                8,
            ).pack(side="left", padx=3)
            self.botao(
                frame, "EXCLUIR",
                lambda id_projeto=projeto["id"]: self.excluir_projeto(id_projeto),
                8,
            ).pack(side="left", padx=3)

    def mostrar_projeto(self, id_projeto):
        projeto = buscar_projeto(self.usuario_atual["email"], id_projeto)
        if projeto is None:
            messagebox.showerror("Projeto", "Projeto não encontrado.")
            self.mostrar_projetos()
            return

        self.limpar()
        self.titulo(projeto.get("nome", "PROJETO"))
        tk.Label(
            self, text=projeto.get("descricao") or "Sem descrição.",
            bg=FUNDO, fg="#555555", wraplength=650,
            justify="left",
        ).pack(pady=(0, 10))

        total, concluidas, percentual = progresso_projeto(
            self.usuario_atual["email"], id_projeto
        )
        tk.Label(
            self,
            text=f"Progresso: {concluidas} de {total} tarefas concluídas — {percentual}%",
            bg=FUNDO, fg=TEXTO, font=("Arial", 11, "bold"),
        ).pack(pady=(0, 10))

        lista = tk.Frame(self, bg=BRANCO, padx=15, pady=10)
        lista.pack(fill="both", expand=True, padx=30, pady=10)
        tarefas = [
            t for t in tarefas_do_usuario(self.usuario_atual["email"])
            if str(t.get("projeto_id")) == str(id_projeto)
        ]
        if not tarefas:
            tk.Label(
                lista, text="Nenhuma tarefa está vinculada a este projeto.",
                bg=BRANCO, fg="#555555",
            ).pack(pady=30)
        else:
            for tarefa in tarefas:
                self.mostrar_linha_tarefa(lista, tarefa)

        botoes = tk.Frame(self, bg=FUNDO)
        botoes.pack(pady=10)
        self.botao(
            botoes, "EXCLUIR PROJETO",
            lambda: self.excluir_projeto(id_projeto), 18,
        ).pack(side="left", padx=5)
        self.botao(
            botoes, "VOLTAR", self.mostrar_projetos, 15,
        ).pack(side="left", padx=5)

    def excluir_projeto(self, id_projeto):
        projeto = buscar_projeto(self.usuario_atual["email"], id_projeto)
        if projeto is None:
            messagebox.showerror("Projeto", "Projeto não encontrado.")
            self.mostrar_projetos()
            return

        confirmar = messagebox.askyesno(
            "Excluir projeto",
            f"Deseja excluir o projeto \"{projeto.get('nome', '')}\"?\n\n"
            "As tarefas vinculadas serão mantidas, mas ficarão sem projeto.",
        )
        if not confirmar:
            return

        sucesso, mensagem = excluir_projeto(
            self.usuario_atual["email"], id_projeto
        )
        if sucesso:
            messagebox.showinfo("Projeto", mensagem)
        else:
            messagebox.showerror("Projeto", mensagem)
        self.mostrar_projetos()

    def mostrar_novo_projeto(self):
        self.limpar()
        self.titulo("NOVO PROJETO")
        caixa = tk.Frame(self, bg=BRANCO, padx=35, pady=20)
        caixa.pack(pady=15, fill="x", padx=70)
        nome = tk.StringVar()
        self.campo(caixa, "Nome do projeto", nome)
        tk.Label(
            caixa, text="Descrição", bg=BRANCO, fg=TEXTO,
        ).pack(anchor="w", pady=(10, 3))
        descricao = tk.Text(caixa, height=5)
        descricao.pack(fill="x")
        botoes = tk.Frame(caixa, bg=BRANCO)
        botoes.pack(pady=18)

        def salvar():
            sucesso, mensagem, _ = criar_projeto(
                self.usuario_atual["email"], nome.get(),
                descricao.get("1.0", "end").strip(),
            )
            if sucesso:
                messagebox.showinfo("Projeto", mensagem)
                self.mostrar_projetos()
            else:
                messagebox.showerror("Projeto", mensagem)

        self.botao(botoes, "SALVAR", salvar, 15).pack(side="left", padx=5)
        self.botao(botoes, "CANCELAR", self.mostrar_projetos, 15).pack(side="left", padx=5)

    # HISTÓRICO

    def mostrar_historico(self):
        self.limpar()
        self.titulo("HISTÓRICO")
        caixa = tk.Frame(self, bg=BRANCO, padx=20, pady=15)
        caixa.pack(fill="both", expand=True, padx=30, pady=10)
        eventos = list(reversed(historico_do_usuario(self.usuario_atual["email"])))
        if not eventos:
            tk.Label(
                caixa, text="Nenhuma atividade registrada.",
                bg=BRANCO, fg="#555555",
            ).pack(pady=30)
        else:
            for evento in eventos:
                tk.Label(
                    caixa,
                    text=f"{evento.get('data', '')} - {evento.get('descricao', '')}",
                    bg=BRANCO, fg=TEXTO, anchor="w", justify="left",
                ).pack(fill="x", pady=4)
        self.botao(self, "VOLTAR", self.mostrar_inicio, 15).pack(pady=15)

    # ASSISTENTE

    def mostrar_assistente(self):
        self.limpar()
        self.titulo("ASSISTENTE DE ESTUDOS")
        caixa = tk.Frame(self, bg=BRANCO, padx=25, pady=20)
        caixa.pack(fill="both", expand=True, padx=40, pady=10)
        tk.Label(
            caixa, text="Digite uma dúvida sobre seus estudos:",
            bg=BRANCO, fg=TEXTO, font=("Arial", 11),
        ).pack(anchor="w")
        pergunta = tk.Text(caixa, height=5, font=("Arial", 11))
        pergunta.pack(fill="x", pady=8)
        resposta = tk.Text(caixa, height=8, font=("Arial", 10), state="disabled")
        resposta.pack(fill="both", expand=True, pady=8)

        def perguntar():
            texto = pergunta.get("1.0", "end").strip()
            if not texto:
                messagebox.showwarning("Assistente", "Digite uma pergunta.")
                return
            try:
                from assistente import AssistenteFoundry
                resultado = AssistenteFoundry().perguntar(texto)
            except Exception as erro:
                resultado = f"Não foi possível usar o assistente agora.\n\n{erro}"
            resposta.config(state="normal")
            resposta.delete("1.0", "end")
            resposta.insert("1.0", resultado)
            resposta.config(state="disabled")

        botoes = tk.Frame(caixa, bg=BRANCO)
        botoes.pack()
        self.botao(botoes, "PERGUNTAR", perguntar, 15).pack(side="left", padx=5)
        self.botao(botoes, "VOLTAR", self.mostrar_inicio, 15).pack(side="left", padx=5)
        pergunta.bind("<Control-Return>", lambda evento: perguntar())
