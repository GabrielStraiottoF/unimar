import json
import os
import tkinter as tk
from tkinter import messagebox

ARQUIVO_USUARIOS = "usuarios.json"

# Paleta inspirada na identidade visual da UNIMAR
COR_AZUL = "#0072BC"
COR_AZUL_ESCURO = "#005A94"
COR_AZUL_MUITO_ESCURO = "#003F6B"
COR_AZUL_CLARO = "#EAF5FC"
COR_FUNDO = "#F4F7FA"
COR_CARTAO = "#FFFFFF"
COR_TEXTO = "#1D2939"
COR_TEXTO_SECUNDARIO = "#667085"
COR_BORDA = "#D9E2EC"
COR_SUCESSO = "#16803C"
COR_ERRO = "#C62828"

# Fontes mantidas simples para facilitar a leitura e a manutenção
FONTE_MARCA = ("Arial", 22, "bold")
FONTE_MARCA_SECUNDARIA = ("Arial", 9)
FONTE_TITULO = ("Arial", 25, "bold")
FONTE_SUBTITULO = ("Arial", 13)
FONTE_LABEL = ("Arial", 10, "bold")
FONTE_PADRAO = ("Arial", 11)
FONTE_DESTAQUE = ("Arial", 15, "bold")
FONTE_BOTAO = ("Arial", 11, "bold")
FONTE_PEQUENA = ("Arial", 9)


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
    janela.geometry("720x720")
    janela.configure(bg=COR_FUNDO)
    janela.resizable(False, False)


def limpar_janela(janela):
    for widget in janela.winfo_children():
        widget.destroy()


def criar_cabecalho(janela):
    cabecalho = tk.Frame(janela, bg=COR_AZUL, height=92)
    cabecalho.pack(fill="x")
    cabecalho.pack_propagate(False)

    bloco_marca = tk.Frame(cabecalho, bg=COR_AZUL)
    bloco_marca.pack(side="left", padx=42, pady=14)

    tk.Label(
        bloco_marca,
        text="UNIMAR",
        font=FONTE_MARCA,
        bg=COR_AZUL,
        fg=COR_CARTAO,
    ).pack(anchor="w")

    tk.Label(
        bloco_marca,
        text="UNIVERSIDADE DE MARÍLIA",
        font=FONTE_MARCA_SECUNDARIA,
        bg=COR_AZUL,
        fg=COR_CARTAO,
    ).pack(anchor="w", pady=(1, 0))

    tk.Label(
        cabecalho,
        text="CENTRAL DE CHAMADOS",
        font=("Arial", 10, "bold"),
        bg=COR_AZUL,
        fg=COR_CARTAO,
    ).pack(side="right", padx=42)


def criar_rodape(janela):
    rodape = tk.Frame(janela, bg=COR_CARTAO, height=46)
    rodape.pack(side="bottom", fill="x")
    rodape.pack_propagate(False)

    tk.Label(
        rodape,
        text="UNIMAR • Universidade de Marília",
        font=FONTE_PEQUENA,
        bg=COR_CARTAO,
        fg=COR_TEXTO_SECUNDARIO,
    ).pack(side="left", padx=30, pady=14)

    tk.Label(
        rodape,
        text="Central de Atendimento",
        font=FONTE_PEQUENA,
        bg=COR_CARTAO,
        fg=COR_TEXTO_SECUNDARIO,
    ).pack(side="right", padx=30, pady=14)


def criar_titulo(janela, texto, subtitulo=None):
    tk.Label(
        janela,
        text=texto,
        font=FONTE_TITULO,
        bg=COR_FUNDO,
        fg=COR_AZUL_MUITO_ESCURO,
    ).pack(pady=(36, 7))

    if subtitulo:
        tk.Label(
            janela,
            text=subtitulo,
            font=FONTE_SUBTITULO,
            bg=COR_FUNDO,
            fg=COR_TEXTO_SECUNDARIO,
        ).pack(pady=(0, 22))


def criar_label(janela, texto):
    tk.Label(
        janela,
        text=texto,
        font=FONTE_LABEL,
        bg=COR_FUNDO,
        fg=COR_TEXTO,
    ).pack(anchor="w", padx=150, pady=(4, 3))


def criar_entrada(janela, show=""):
    entrada = tk.Entry(
        janela,
        width=44,
        font=FONTE_PADRAO,
        bg=COR_CARTAO,
        fg=COR_TEXTO,
        insertbackground=COR_AZUL,
        relief="flat",
        bd=0,
        highlightthickness=1,
        highlightbackground=COR_BORDA,
        highlightcolor=COR_AZUL,
    )

    if show:
        entrada.config(show=show)

    entrada.pack(ipady=9, pady=(0, 10))
    return entrada


def criar_botao(janela, texto, comando, secundario=False):
    cor_fundo = COR_CARTAO if secundario else COR_AZUL
    cor_texto = COR_AZUL if secundario else COR_CARTAO
    cor_hover = COR_AZUL_CLARO if secundario else COR_AZUL_ESCURO

    botao = tk.Button(
        janela,
        text=texto,
        width=23,
        font=FONTE_BOTAO,
        bg=cor_fundo,
        fg=cor_texto,
        activebackground=cor_hover,
        activeforeground=COR_AZUL_MUITO_ESCURO if secundario else COR_CARTAO,
        relief="solid" if secundario else "flat",
        bd=1 if secundario else 0,
        highlightthickness=0,
        cursor="hand2",
        command=comando,
    )
    botao.pack(pady=5, ipady=6)
    return botao


def criar_aviso(janela, texto, tipo="info"):
    cores = {
        "info": (COR_AZUL_CLARO, COR_AZUL_MUITO_ESCURO),
        "sucesso": ("#EAF7EF", COR_SUCESSO),
        "erro": ("#FDECEC", COR_ERRO),
    }
    fundo, texto_cor = cores[tipo]

    aviso = tk.Frame(janela, bg=fundo, padx=16, pady=10)
    aviso.pack(padx=130, pady=12, fill="x")

    tk.Label(
        aviso,
        text=texto,
        font=FONTE_PEQUENA,
        bg=fundo,
        fg=texto_cor,
    ).pack()

    return aviso


def verificar_login(email, senha, mensagem, janela):
    email = email.strip()
    senha = senha.strip()

    if not email or not senha:
        mensagem.config(text="Informe o email e a senha.", fg=COR_ERRO)
        return

    for usuario in carregar_usuarios():
        if (
            usuario.get("email", "").lower() == email.lower()
            and usuario.get("senha") == senha
        ):
            mensagem.config(text="Login bem-sucedido!", fg=COR_SUCESSO)
            messagebox.showinfo(
                "Login",
                f"Bem-vindo(a), {usuario.get('nome', 'usuário')}!",
            )
            abrir_inicio(janela, usuario)
            return

    mensagem.config(text="Email ou senha incorretos.", fg=COR_ERRO)


def realizar_cadastro(nome, email, senha, confirmar_senha, mensagem):
    nome, email = nome.strip(), email.strip()
    senha, confirmar_senha = senha.strip(), confirmar_senha.strip()

    if not nome or not email or not senha or not confirmar_senha:
        mensagem.config(text="Preencha todos os campos.", fg=COR_ERRO)
        return

    if "@" not in email or "." not in email.split("@")[-1]:
        mensagem.config(text="Informe um email válido.", fg=COR_ERRO)
        return

    if len(senha) < 4:
        mensagem.config(
            text="A senha deve ter pelo menos 4 caracteres.",
            fg=COR_ERRO,
        )
        return

    if senha != confirmar_senha:
        mensagem.config(text="As senhas não coincidem.", fg=COR_ERRO)
        return

    usuarios = carregar_usuarios()

    if any(u.get("email", "").lower() == email.lower() for u in usuarios):
        mensagem.config(text="Este email já está cadastrado.", fg=COR_ERRO)
        return

    usuarios.append({"nome": nome, "email": email, "senha": senha})
    salvar_usuarios(usuarios)
    mensagem.config(text="Cadastro realizado com sucesso!", fg=COR_SUCESSO)


def abrir_cadastro(janela):
    limpar_janela(janela)
    criar_cabecalho(janela)
    criar_titulo(
        janela,
        "Criar cadastro",
        "Cadastre-se para acessar a Central de Chamados da UNIMAR",
    )

    cartao = tk.Frame(
        janela,
        bg=COR_CARTAO,
        highlightbackground=COR_BORDA,
        highlightthickness=1,
        padx=25,
        pady=18,
    )
    cartao.pack(padx=110, fill="x")

    campos = []
    for texto in ("Nome", "Email", "Senha", "Confirmar senha"):
        tk.Label(
            cartao,
            text=texto,
            font=FONTE_LABEL,
            bg=COR_CARTAO,
            fg=COR_TEXTO,
        ).pack(anchor="w", pady=(3, 3))

        campo = tk.Entry(
            cartao,
            width=48,
            font=FONTE_PADRAO,
            bg=COR_FUNDO,
            fg=COR_TEXTO,
            insertbackground=COR_AZUL,
            relief="flat",
            highlightthickness=1,
            highlightbackground=COR_BORDA,
            highlightcolor=COR_AZUL,
        )

        if "Senha" in texto:
            campo.config(show="*")

        campo.pack(ipady=8, pady=(0, 8))
        campos.append(campo)

    mensagem = tk.Label(
        cartao,
        text="",
        font=FONTE_PEQUENA,
        bg=COR_CARTAO,
    )
    mensagem.pack(pady=5)

    criar_botao(
        cartao,
        "Cadastrar",
        lambda: realizar_cadastro(
            *(campo.get() for campo in campos),
            mensagem,
        ),
    )
    criar_botao(
        cartao,
        "Voltar para o login",
        lambda: abrir_login(janela),
        secundario=True,
    )
    criar_rodape(janela)


def abrir_login(janela):
    limpar_janela(janela)
    criar_cabecalho(janela)
    criar_titulo(
        janela,
        "Central de Chamados",
        "Atendimento, suporte e serviços para a comunidade UNIMAR",
    )

    cartao = tk.Frame(
        janela,
        bg=COR_CARTAO,
        highlightbackground=COR_BORDA,
        highlightthickness=1,
        padx=35,
        pady=25,
    )
    cartao.pack(padx=155, fill="x")

    tk.Label(
        cartao,
        text="Acesse sua conta",
        font=FONTE_DESTAQUE,
        bg=COR_CARTAO,
        fg=COR_AZUL_MUITO_ESCURO,
    ).pack(pady=(0, 18))

    tk.Label(
        cartao,
        text="Email",
        font=FONTE_LABEL,
        bg=COR_CARTAO,
        fg=COR_TEXTO,
    ).pack(anchor="w", pady=(0, 3))

    email = tk.Entry(
        cartao,
        width=43,
        font=FONTE_PADRAO,
        bg=COR_FUNDO,
        fg=COR_TEXTO,
        insertbackground=COR_AZUL,
        relief="flat",
        highlightthickness=1,
        highlightbackground=COR_BORDA,
        highlightcolor=COR_AZUL,
    )
    email.pack(ipady=9, pady=(0, 13))

    tk.Label(
        cartao,
        text="Senha",
        font=FONTE_LABEL,
        bg=COR_CARTAO,
        fg=COR_TEXTO,
    ).pack(anchor="w", pady=(0, 3))

    senha = tk.Entry(
        cartao,
        width=43,
        font=FONTE_PADRAO,
        bg=COR_FUNDO,
        fg=COR_TEXTO,
        insertbackground=COR_AZUL,
        relief="flat",
        show="*",
        highlightthickness=1,
        highlightbackground=COR_BORDA,
        highlightcolor=COR_AZUL,
    )
    senha.pack(ipady=9, pady=(0, 8))

    mensagem = tk.Label(
        cartao,
        text="",
        font=FONTE_PEQUENA,
        bg=COR_CARTAO,
    )
    mensagem.pack(pady=5)

    criar_botao(
        cartao,
        "Entrar",
        lambda: verificar_login(email.get(), senha.get(), mensagem, janela),
    )
    criar_botao(
        cartao,
        "Criar cadastro",
        lambda: abrir_cadastro(janela),
        secundario=True,
    )

    criar_aviso(
        janela,
        "Ambiente destinado ao atendimento e suporte da comunidade acadêmica.",
    )
    criar_rodape(janela)


def abrir_inicio(janela, usuario):
    limpar_janela(janela)
    criar_cabecalho(janela)
    criar_titulo(
        janela,
        "Central de Chamados",
        "Bem-vindo ao ambiente de atendimento da UNIMAR",
    )

    cartao_usuario = tk.Frame(
        janela,
        bg=COR_CARTAO,
        highlightbackground=COR_BORDA,
        highlightthickness=1,
        padx=25,
        pady=20,
    )
    cartao_usuario.pack(padx=115, fill="x")

    tk.Label(
        cartao_usuario,
        text="USUÁRIO CONECTADO",
        font=FONTE_PEQUENA,
        bg=COR_CARTAO,
        fg=COR_AZUL,
    ).pack(anchor="w")

    tk.Label(
        cartao_usuario,
        text=usuario.get("nome", "usuário"),
        font=FONTE_DESTAQUE,
        bg=COR_CARTAO,
        fg=COR_TEXTO,
    ).pack(anchor="w", pady=(4, 0))

    tk.Label(
        cartao_usuario,
        text=usuario.get("email", ""),
        font=FONTE_PEQUENA,
        bg=COR_CARTAO,
        fg=COR_TEXTO_SECUNDARIO,
    ).pack(anchor="w", pady=(2, 0))

    painel = tk.Frame(janela, bg=COR_AZUL_CLARO, padx=25, pady=20)
    painel.pack(padx=115, pady=18, fill="x")

    tk.Label(
        painel,
        text="Atendimento e suporte",
        font=FONTE_DESTAQUE,
        bg=COR_AZUL_CLARO,
        fg=COR_AZUL_MUITO_ESCURO,
    ).pack(anchor="w")

    tk.Label(
        painel,
        text="A área de chamados está em desenvolvimento.",
        font=FONTE_PADRAO,
        bg=COR_AZUL_CLARO,
        fg=COR_TEXTO,
    ).pack(anchor="w", pady=(7, 2))

    tk.Label(
        painel,
        text="Em breve você poderá registrar e acompanhar suas solicitações.",
        font=FONTE_PEQUENA,
        bg=COR_AZUL_CLARO,
        fg=COR_TEXTO_SECUNDARIO,
    ).pack(anchor="w")

    criar_botao(janela, "Sair", lambda: abrir_login(janela), secundario=True)
    criar_rodape(janela)


def main():
    garantir_arquivo_usuarios()
    janela = tk.Tk()
    configurar_janela(janela)
    abrir_login(janela)
    janela.mainloop()


if __name__ == "__main__":
    main()
