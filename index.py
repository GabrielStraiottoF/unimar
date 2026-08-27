import json
import os
import tkinter as tk
from tkinter import messagebox

ARQUIVO_USUARIOS = "usuarios.json"

# Identidade visual inspirada na comunicação institucional da UNIMAR.
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
COR_ERRO_FUNDO = "#FDECEC"
COR_SUCESSO_FUNDO = "#EAF7EF"

FONTE_MARCA = ("Arial", 22, "bold")
FONTE_MARCA_SECUNDARIA = ("Arial", 9)
FONTE_TITULO = ("Arial", 25, "bold")
FONTE_SUBTITULO = ("Arial", 11)
FONTE_SECAO = ("Arial", 15, "bold")
FONTE_LABEL = ("Arial", 10, "bold")
FONTE_PADRAO = ("Arial", 11)
FONTE_BOTAO = ("Arial", 10, "bold")
FONTE_PEQUENA = ("Arial", 9)


# -----------------------------------------------------------------------------
# Persistência
# -----------------------------------------------------------------------------

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
            dados = json.load(arquivo)
            return dados.get("usuarios", [])
    except (json.JSONDecodeError, OSError):
        return []


def salvar_usuarios(usuarios):
    with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as arquivo:
        json.dump({"usuarios": usuarios}, arquivo, ensure_ascii=False, indent=4)


# -----------------------------------------------------------------------------
# Componentes visuais
# -----------------------------------------------------------------------------

def configurar_janela(janela):
    janela.title("UNIMAR | Central de Chamados")
    janela.geometry("760x760")
    janela.minsize(760, 760)
    janela.maxsize(760, 760)
    janela.configure(bg=COR_FUNDO)

    # Centraliza a janela sem depender de recursos externos.
    janela.update_idletasks()
    largura = 760
    altura = 760
    x = (janela.winfo_screenwidth() - largura) // 2
    y = (janela.winfo_screenheight() - altura) // 2
    janela.geometry(f"{largura}x{altura}+{x}+{y}")


def limpar_janela(janela):
    for widget in janela.winfo_children():
        widget.destroy()


def criar_cabecalho(janela):
    cabecalho = tk.Frame(janela, bg=COR_AZUL, height=96)
    cabecalho.pack(fill="x")
    cabecalho.pack_propagate(False)

    marca = tk.Frame(cabecalho, bg=COR_AZUL)
    marca.pack(side="left", padx=44, pady=14)

    tk.Label(
        marca,
        text="UNIMAR",
        font=FONTE_MARCA,
        bg=COR_AZUL,
        fg=COR_CARTAO,
    ).pack(anchor="w")

    tk.Label(
        marca,
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
    ).pack(side="right", padx=44)


def criar_rodape(janela):
    rodape = tk.Frame(
        janela,
        bg=COR_CARTAO,
        height=48,
        highlightbackground=COR_BORDA,
        highlightthickness=1,
    )
    rodape.pack(side="bottom", fill="x")
    rodape.pack_propagate(False)

    tk.Label(
        rodape,
        text="UNIMAR • Universidade de Marília",
        font=FONTE_PEQUENA,
        bg=COR_CARTAO,
        fg=COR_TEXTO_SECUNDARIO,
    ).pack(side="left", padx=32, pady=15)

    tk.Label(
        rodape,
        text="Central de Atendimento",
        font=FONTE_PEQUENA,
        bg=COR_CARTAO,
        fg=COR_TEXTO_SECUNDARIO,
    ).pack(side="right", padx=32, pady=15)


def criar_conteudo(janela):
    conteudo = tk.Frame(janela, bg=COR_FUNDO)
    conteudo.pack(fill="both", expand=True)
    return conteudo


def criar_titulo(parent, texto, subtitulo=None):
    tk.Label(
        parent,
        text=texto,
        font=FONTE_TITULO,
        bg=COR_FUNDO,
        fg=COR_AZUL_MUITO_ESCURO,
    ).pack(pady=(28, 5))

    if subtitulo:
        tk.Label(
            parent,
            text=subtitulo,
            font=FONTE_SUBTITULO,
            bg=COR_FUNDO,
            fg=COR_TEXTO_SECUNDARIO,
        ).pack(pady=(0, 18))


def criar_card(parent, largura=500, padx=30, pady=26):
    card = tk.Frame(
        parent,
        bg=COR_CARTAO,
        highlightbackground=COR_BORDA,
        highlightthickness=1,
        padx=padx,
        pady=pady,
    )
    card.pack(padx=30, fill="x", ipadx=max(0, (largura - 560) // 2))
    return card


def criar_campo(parent, texto, show=None):
    bloco = tk.Frame(parent, bg=COR_CARTAO)
    bloco.pack(fill="x", pady=(0, 13))

    tk.Label(
        bloco,
        text=texto,
        font=FONTE_LABEL,
        bg=COR_CARTAO,
        fg=COR_TEXTO,
    ).pack(anchor="w", pady=(0, 5))

    entrada = tk.Entry(
        bloco,
        font=FONTE_PADRAO,
        bg=COR_FUNDO,
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

    entrada.pack(fill="x", ipady=9)
    return entrada


def criar_botao(parent, texto, comando, secundario=False):
    if secundario:
        normal = COR_CARTAO
        texto_cor = COR_AZUL
        ativo = COR_AZUL_CLARO
        relevo = "solid"
        borda = 1
    else:
        normal = COR_AZUL
        texto_cor = COR_CARTAO
        ativo = COR_AZUL_ESCURO
        relevo = "flat"
        borda = 0

    botao = tk.Button(
        parent,
        text=texto,
        font=FONTE_BOTAO,
        bg=normal,
        fg=texto_cor,
        activebackground=ativo,
        activeforeground=texto_cor,
        relief=relevo,
        bd=borda,
        highlightthickness=0,
        cursor="hand2",
        command=comando,
        padx=18,
        pady=8,
    )
    botao.pack(fill="x", pady=(4, 0))
    return botao


def criar_mensagem(parent):
    mensagem = tk.Label(
        parent,
        text="",
        font=FONTE_PEQUENA,
        bg=COR_CARTAO,
        wraplength=460,
    )
    mensagem.pack(fill="x", pady=(0, 8))
    return mensagem


def mostrar_mensagem(mensagem, texto, sucesso=False):
    mensagem.config(
        text=texto,
        fg=COR_SUCESSO if sucesso else COR_ERRO,
    )


def criar_aviso(parent, texto, tipo="info"):
    if tipo == "sucesso":
        fundo, cor = COR_SUCESSO_FUNDO, COR_SUCESSO
    elif tipo == "erro":
        fundo, cor = COR_ERRO_FUNDO, COR_ERRO
    else:
        fundo, cor = COR_AZUL_CLARO, COR_AZUL_MUITO_ESCURO

    aviso = tk.Frame(parent, bg=fundo, padx=16, pady=11)
    aviso.pack(fill="x", pady=(16, 0))

    tk.Label(
        aviso,
        text=texto,
        font=FONTE_PEQUENA,
        bg=fundo,
        fg=cor,
        wraplength=500,
        justify="center",
    ).pack()
    return aviso


# -----------------------------------------------------------------------------
# Autenticação e cadastro — lógica original preservada.
# -----------------------------------------------------------------------------

def verificar_login(email, senha, mensagem, janela):
    email = email.strip()
    senha = senha.strip()

    if not email or not senha:
        mostrar_mensagem(mensagem, "Informe o email e a senha.")
        return

    for usuario in carregar_usuarios():
        if (
            usuario.get("email", "").lower() == email.lower()
            and usuario.get("senha") == senha
        ):
            mostrar_mensagem(mensagem, "Login bem-sucedido!", sucesso=True)
            messagebox.showinfo(
                "Login",
                f"Bem-vindo(a), {usuario.get('nome', 'usuário')}!",
            )
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


# -----------------------------------------------------------------------------
# Telas
# -----------------------------------------------------------------------------

def abrir_login(janela):
    limpar_janela(janela)
    criar_cabecalho(janela)
    conteudo = criar_conteudo(janela)

    criar_titulo(
        conteudo,
        "Central de Chamados",
        "Atendimento, suporte e serviços para a comunidade UNIMAR",
    )

    card = criar_card(conteudo, largura=500, padx=34, pady=27)

    tk.Label(
        card,
        text="Acesse sua conta",
        font=FONTE_SECAO,
        bg=COR_CARTAO,
        fg=COR_AZUL_MUITO_ESCURO,
    ).pack(anchor="w", pady=(0, 20))

    email = criar_campo(card, "Email")
    senha = criar_campo(card, "Senha", show="*")
    mensagem = criar_mensagem(card)

    criar_botao(
        card,
        "ENTRAR",
        lambda: verificar_login(email.get(), senha.get(), mensagem, janela),
    )
    criar_botao(
        card,
        "Criar cadastro",
        lambda: abrir_cadastro(janela),
        secundario=True,
    )

    criar_aviso(
        card,
        "Ambiente destinado ao atendimento e suporte da comunidade acadêmica.",
    )
    criar_rodape(janela)
    email.focus_set()


def abrir_cadastro(janela):
    limpar_janela(janela)
    criar_cabecalho(janela)
    conteudo = criar_conteudo(janela)

    criar_titulo(
        conteudo,
        "Criar cadastro",
        "Cadastre-se para acessar a Central de Chamados da UNIMAR",
    )

    card = criar_card(conteudo, largura=500, padx=30, pady=22)

    campos = [
        criar_campo(card, "Nome"),
        criar_campo(card, "Email"),
        criar_campo(card, "Senha", show="*"),
        criar_campo(card, "Confirmar senha", show="*"),
    ]
    mensagem = criar_mensagem(card)

    criar_botao(
        card,
        "CADASTRAR",
        lambda: realizar_cadastro(
            *(campo.get() for campo in campos),
            mensagem,
        ),
    )
    criar_botao(
        card,
        "Voltar para o login",
        lambda: abrir_login(janela),
        secundario=True,
    )

    criar_aviso(
        card,
        "Seus dados continuam sendo armazenados localmente em usuarios.json.",
    )
    criar_rodape(janela)
    campos[0].focus_set()


def abrir_inicio(janela, usuario):
    limpar_janela(janela)
    criar_cabecalho(janela)
    conteudo = criar_conteudo(janela)

    criar_titulo(
        conteudo,
        "Central de Chamados",
        "Bem-vindo ao ambiente de atendimento da UNIMAR",
    )

    card_usuario = criar_card(conteudo, largura=500, padx=26, pady=20)

    tk.Label(
        card_usuario,
        text="USUÁRIO CONECTADO",
        font=FONTE_PEQUENA,
        bg=COR_CARTAO,
        fg=COR_AZUL,
    ).pack(anchor="w")

    tk.Label(
        card_usuario,
        text=usuario.get("nome", "usuário"),
        font=FONTE_SECAO,
        bg=COR_CARTAO,
        fg=COR_TEXTO,
    ).pack(anchor="w", pady=(4, 1))

    tk.Label(
        card_usuario,
        text=usuario.get("email", ""),
        font=FONTE_PEQUENA,
        bg=COR_CARTAO,
        fg=COR_TEXTO_SECUNDARIO,
    ).pack(anchor="w")

    painel = tk.Frame(
        conteudo,
        bg=COR_AZUL_CLARO,
        padx=26,
        pady=21,
        highlightbackground="#C7E5F6",
        highlightthickness=1,
    )
    painel.pack(padx=30, pady=16, fill="x", ipadx=60)

    tk.Label(
        painel,
        text="Atendimento e suporte",
        font=FONTE_SECAO,
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

    criar_botao(
        conteudo,
        "SAIR",
        lambda: abrir_login(janela),
        secundario=True,
    ).pack_configure(padx=220, pady=(2, 0))

    criar_rodape(janela)


def main():
    garantir_arquivo_usuarios()
    janela = tk.Tk()
    configurar_janela(janela)
    abrir_login(janela)
    janela.mainloop()


if __name__ == "__main__":
    main()
