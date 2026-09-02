import hashlib

from dados import carregar_json, salvar_json

ARQUIVO_USUARIOS = "usuarios.json"


def _hash_senha(senha):
    return hashlib.sha256(senha.encode("utf-8")).hexdigest()


def carregar_usuarios():
    dados = carregar_json(ARQUIVO_USUARIOS, {"usuarios": []})
    if not isinstance(dados, dict) or not isinstance(dados.get("usuarios"), list):
        return []
    return dados["usuarios"]


def cadastrar_usuario(nome, email, senha, confirmar):
    nome = nome.strip()
    email = email.strip().lower()

    if not nome or not email or not senha or not confirmar:
        return False, "Preencha todos os campos."
    if "@" not in email or "." not in email.split("@")[-1]:
        return False, "Informe um email válido."
    if senha != confirmar:
        return False, "As senhas não coincidem."
    if len(senha) < 4:
        return False, "A senha deve possuir pelo menos 4 caracteres."

    usuarios = carregar_usuarios()
    if any(u.get("email", "").lower() == email for u in usuarios):
        return False, "Este email já está cadastrado."

    usuarios.append({
        "nome": nome,
        "email": email,
        "senha": _hash_senha(senha),
        "tipo": "usuario",
    })
    salvar_json(ARQUIVO_USUARIOS, {"usuarios": usuarios})
    return True, "Cadastro realizado com sucesso!"


def autenticar(email, senha):
    email = email.strip().lower()
    senha_hash = _hash_senha(senha.strip())

    for usuario in carregar_usuarios():
        if usuario.get("email", "").lower() == email and usuario.get("senha") == senha_hash:
            return usuario
    return None
