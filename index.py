import json
import os
import tkinter as tk
from tkinter import messagebox

ARQUIVO_USUARIOS = "usuarios.json"

# Cores inspiradas na identidade visual da Unimar
COR_AZUL = "#0072BC"
COR_AZUL_ESCURO = "#005A94"
COR_AZUL_CLARO = "#EAF5FC"
COR_FUNDO = "#F5F7FA"
COR_TEXTO = "#1F2933"
COR_TEXTO_SECUNDARIO = "#667085"
COR_BRANCO = "#FFFFFF"
COR_BORDA = "#D9E2EC"
COR_SUCESSO = "#16803C"
COR_ERRO = "#C62828"

# Fontes simples e fáceis de entender
FONTE_MARCA = ("Arial", 20, "bold")
FONTE_MARCA_SECUNDARIA = ("Arial", 9)
FONTE_TITULO = ("Arial", 24, "bold")
FONTE_SUBTITULO = ("Arial", 22, "bold")
FONTE_PADRAO = ("Arial", 11)
FONTE_DESTAQUE = ("Arial", 14, "bold")
FONTE_BOTAO = ("Arial", 11, "bold")
FONTE_RODAPE = ("Arial", 9)


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
    janela.geometry("620x680")
    janela.configure(bg=COR_FUNDO)
    janela.resizable(False, False)


def limpar_janela(janela):
    for widget in janela.winfo_children():
        widget.destroy()


def criar_cabecalho(janela):
    cabecalho = tk.Frame(janela, bg=COR_AZUL, height=88)
    cabecalho.pack(fill="x")
    cabecalho.pack_propagate(False)

    bloco_marca = tk.Frame(cabecalho, bg=COR_AZUL)
    bloco_marca.pack(side="left", padx=30, pady=12)

    tk.Label(
        bloco_marca,
        text="UNIMAR",
        font=FONTE_MARCA,
        bg=COR_AZUL,
        fg=COR_BRANCO,
    ).pack(anchor="w")

    tk.Label(
        bloco_marca,
        text="UNIVERSIDADE DE MARÍLIA",
        font=FONTE_MARCA_SECUNDARIA,
        bg=COR_AZUL,
        fg=COR_BRANCO,
    ).pack(anchor="w")


def criar_titulo(janela, texto, fonte=FONTE_TITULO, pady=(35, 25)):
    tk.Label(
        janela,
        text=texto,
        font=fonte,
        bg=COR_FUNDO,
        fg=COR_AZUL,
    ).pack(pady=pady)


def criar_subtitulo(janela, texto):
    tk.Label(
        janela,
        text=texto,
        font=FONTE_PADRAO,
        bg=COR_FUNDO,
        fg=COR_TEXTO_SECUNDARIO,
    ).pack(pady=(0, 18))


def criar_label(janela, texto):
    tk.Label(
        janela,
        text=texto,
        font=FONTE_PADRAO,
        bg=COR_FUNDO,
        fg=COR_TEXTO,
    ).pack()


def criar_entrada(janela, show=""):
    entrada = tk.Entry(
        janela,
        width=40,
        font=FONTE_PADRAO,
        bg=COR_BRANCO,
        fg=COR_TEXTO,
        insertbackground=COR_TEXTO,
        relief="solid",
        bd=1,
        highlightthickness=1,
        highlightbackground=COR_BORDA,
        highlightcolor=COR_AZUL,
    )

    if show:
        entrada.config(show=show)

    entrada.pack(ipady=8, pady=(5, 15))
    return entrada


def criar_botao(janela, texto, comando):
    botao = tk.Button(
        janela,
        text=texto,
        width=20,
        font=FONTE_BOTAO,
        bg=COR_AZUL,
        fg=COR_BRANCO,
        activebackground=COR_AZUL_ESCURO,
        activeforeground=COR_BRANCO,
        relief="flat",
        bd=0,
        cursor="hand2",
        command=comando,
    )
    botao.pack(pady=5, ipady=5)
    return botao


def criar_rodape(janela):
    rodape = tk.Frame(janela, bg=COR_BRANCO, height=48)
    rodape.pack(side="bottom", fill="x")
    rodape.pack_propagate(False)

    tk.Label(
        rodape,
        text="UNIMAR • Universidade de Marília",
        font=FONTE_RODAPE,
        bg=COR_BRANCO,
        fg=COR_TEXTO_SECUNDARIO,
    ).pack(pady=14)


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
    criar_titulo(janela, "Criar cadastro")
    criar_subtitulo(janela, "Acesse a Central de Chamados da UNIMAR")

    campos = []

    for texto in ("Nome", "Email", "Senha", "Confirmar senha"):
        criar_label(janela, texto)
        mostrar_senha = "*" if "Senha" in texto else ""
        campo = criar_entrada(janela, mostrar_senha)
        campos.append(campo)

    mensagem = tk.Label(
        janela,
        text="",
        font=FONTE_PADRAO,
        bg=COR_FUNDO,
    )
    mensagem.pack(pady=8)

    criar_botao(
        janela,
        "Cadastrar",
        lambda: realizar_cadastro(
            *(campo.get() for campo in campos),
            mensagem,
        ),
    )
    criar_botao(janela, "Voltar para o login", lambda: abrir_login(janela))
    criar_rodape(janela)


def abrir_login(janela):
    limpar_janela(janela)
    criar_cabecalho(janela)
    criar_titulo(janela, "Central de Chamados", pady=(45, 12))
    criar_subtitulo(janela, "Atendimento, suporte e serviços da UNIMAR")

    criar_label(janela, "Email")
    email = criar_entrada(janela)

    criar_label(janela, "Senha")
    senha = criar_entrada(janela, "*")

    mensagem = tk.Label(
        janela,
        text="",
        font=FONTE_PADRAO,
        bg=COR_FUNDO,
    )
    mensagem.pack(pady=8)

    criar_botao(
        janela,
        "Entrar",
        lambda: verificar_login(email.get(), senha.get(), mensagem, janela),
    )
    criar_botao(janela, "Criar cadastro", lambda: abrir_cadastro(janela))

    tk.Label(
        janela,
        text="Tecnologia, inovação e atendimento para a comunidade acadêmica.",
        font=FONTE_RODAPE,
        bg=COR_FUNDO,
        fg=COR_TEXTO_SECUNDARIO,
    ).pack(pady=(20, 0))

    criar_rodape(janela)


def abrir_inicio(janela, usuario):
    limpar_janela(janela)
    criar_cabecalho(janela)
    criar_titulo(
        janela,
        "Central de Chamados",
        fonte=FONTE_SUBTITULO,
        pady=(45, 12),
    )
    criar_subtitulo(janela, "Bem-vindo ao ambiente de atendimento da UNIMAR")

    cartao_usuario = tk.Frame(
        janela,
        bg=COR_BRANCO,
        highlightbackground=COR_BORDA,
        highlightthickness=1,
    )
    cartao_usuario.pack(padx=70, pady=10, fill="x")

    tk.Label(
        cartao_usuario,
        text="USUÁRIO CONECTADO",
        font=FONTE_RODAPE,
        bg=COR_BRANCO,
        fg=COR_AZUL,
    ).pack(pady=(14, 4))

    tk.Label(
        cartao_usuario,
        text=usuario.get("nome", "usuário"),
        font=FONTE_DESTAQUE,
        bg=COR_BRANCO,
        fg=COR_TEXTO,
    ).pack(pady=(0, 14))

    tk.Label(
        janela,
        text="Área de chamados ainda em desenvolvimento.",
        font=FONTE_PADRAO,
        bg=COR_FUNDO,
        fg=COR_TEXTO_SECUNDARIO,
    ).pack(pady=18)

    criar_botao(janela, "Sair", lambda: abrir_login(janela))
    criar_rodape(janela)


def main():
    garantir_arquivo_usuarios()
    janela = tk.Tk()
    configurar_janela(janela)
    abrir_login(janela)
    janela.mainloop()


if __name__ == "__main__":
    main()
