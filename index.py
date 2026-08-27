#Bibliotecas
import tkinter as tk
import json
import os

#config padrão
if not os.path.exists("usuarios.json"):
    with open("usuarios.json", "w") as arquivo:
        json.dump({}, arquivo)



#Funções
def config_padrao():
    janela = tk.Tk()
    janela.title("Aplicativo de Chamados")
    janela.geometry("600x600")
    janela.configure(bg="#170250")
    return janela

def verificar_login(email, senha, mensagem):
    with open("usuarios.json", "r") as arquivo:
        dados = json.load(arquivo)

    usuarios = dados.get("usuarios", [])
    usuario_encontrado = None

    for usuario in usuarios:
        if usuario["email"] == email and usuario["senha"] == senha:
            usuario_encontrado = usuario
            break

    if usuario_encontrado:
        mensagem.config(text="Login bem-sucedido!", fg="green")
    else:
        mensagem.config(text="Email ou senha incorretos.", fg="red")

def cadastro():
    config_padrao()

def login():
    config_padrao()
    email = tk.Entry(janela)
    email.insert(0, "Email: ")
    email.pack()
    email = email.get()

    senha = tk.Entry(janela)
    senha.insert(0, "Senha: ")
    senha.pack()
    senha = senha.get()

    mensagem = tk.Label(janela, text="")
    mensagem.pack()
    tk.Button(janela, text="Login", command=lambda: verificar_login(email, senha, mensagem)).pack()

def main():
    log = tk.Button(janela, text="Login")
    if log == True:
        login()
    janela.mainloop()

main()
