import json
import os
from datetime import datetime

ARQUIVO_USUARIOS = "usuarios.json"
ARQUIVO_CHAMADOS = "chamados.json"
TECNICO_PADRAO = {"nome": "Técnico UNIMAR", "email": "tecnico@unimar.br", "senha": "tecnico123", "tipo": "tecnico"}
FOUNDRY_ENDPOINT = "FOUNDRY_ENDPOINT"
FOUNDRY_API_KEY = "FOUNDRY_API_KEY"
FOUNDRY_MODEL = "FOUNDRY_MODEL"


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
                os.environ.setdefault(chave.strip(), valor.strip().strip('"').strip("'"))
    except OSError:
        pass


def salvar_json(caminho, dados):
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)


def carregar_json(caminho, padrao):
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return padrao


def garantir_arquivos():
    usuarios = carregar_json(ARQUIVO_USUARIOS, {"usuarios": []})
    if not isinstance(usuarios, dict) or not isinstance(usuarios.get("usuarios"), list):
        usuarios = {"usuarios": []}
    if not any(u.get("tipo") == "tecnico" and u.get("email", "").lower() == TECNICO_PADRAO["email"] for u in usuarios["usuarios"]):
        usuarios["usuarios"].append(dict(TECNICO_PADRAO))
    salvar_json(ARQUIVO_USUARIOS, usuarios)

    chamados = carregar_json(ARQUIVO_CHAMADOS, {"chamados": []})
    if not isinstance(chamados, dict) or not isinstance(chamados.get("chamados"), list):
        salvar_json(ARQUIVO_CHAMADOS, {"chamados": []})


def carregar_usuarios():
    garantir_arquivos()
    return carregar_json(ARQUIVO_USUARIOS, {"usuarios": []}).get("usuarios", [])


def cadastrar_usuario(nome, email, senha, confirmar):
    nome, email = nome.strip(), email.strip()
    if not nome or not email or not senha or not confirmar:
        return False, "Preencha todos os campos."
    if "@" not in email or "." not in email.split("@")[-1]:
        return False, "Informe um email válido."
    if senha != confirmar:
        return False, "As senhas não coincidem."
    usuarios = carregar_usuarios()
    if any(u.get("email", "").lower() == email.lower() for u in usuarios):
        return False, "Este email já está cadastrado."
    usuarios.append({"nome": nome, "email": email, "senha": senha, "tipo": "usuario"})
    salvar_json(ARQUIVO_USUARIOS, {"usuarios": usuarios})
    return True, "Cadastro realizado com sucesso!"


def autenticar(email, senha):
    email, senha = email.strip(), senha.strip()
    for usuario in carregar_usuarios():
        if usuario.get("email", "").lower() == email.lower() and usuario.get("senha") == senha:
            return usuario
    return None


def carregar_chamados():
    garantir_arquivos()
    return carregar_json(ARQUIVO_CHAMADOS, {"chamados": []}).get("chamados", [])


def salvar_chamados(chamados):
    salvar_json(ARQUIVO_CHAMADOS, {"chamados": chamados})


def criar_chamado(usuario, departamento, equipamento, descricao, horario_inicio):
    departamento = departamento.strip()
    equipamento = equipamento.strip()
    descricao = descricao.strip()
    horario_inicio = horario_inicio.strip()
    if not all((departamento, equipamento, descricao, horario_inicio)):
        return False, "Preencha todos os campos.", None
    chamados = carregar_chamados()
    ids = [int(c.get("id", 0)) for c in chamados if str(c.get("id", "0")).isdigit()]
    novo_id = max(ids or [0]) + 1
    chamado = {
        "id": novo_id,
        "departamento": departamento,
        "nome_solicitante": usuario.get("nome", ""),
        "email_solicitante": usuario.get("email", ""),
        "equipamento": equipamento,
        "descricao": descricao,
        "horario_inicio": horario_inicio,
        "data_abertura": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "status": "Aberto",
        "tecnico": TECNICO_PADRAO["email"],
        "descricao_finalizacao": "",
        "data_finalizacao": "",
    }
    chamados.append(chamado)
    salvar_chamados(chamados)
    return True, f"Chamado #{novo_id} criado com sucesso!", chamado


def chamados_do_usuario(usuario):
    email = usuario.get("email", "").lower()
    return [c for c in carregar_chamados() if c.get("email_solicitante", "").lower() == email]


def departamentos():
    return sorted(set(c.get("departamento", "") for c in carregar_chamados() if c.get("departamento")))


def finalizar_chamado(id_chamado, descricao_finalizacao, tecnico):
    descricao_finalizacao = descricao_finalizacao.strip()
    if not descricao_finalizacao:
        return False, "Descreva o que ocorreu e o que foi feito antes de finalizar."
    chamados = carregar_chamados()
    for chamado in chamados:
        if str(chamado.get("id")) == str(id_chamado):
            if chamado.get("status") == "Finalizado":
                return False, "Este chamado já está finalizado."
            chamado["status"] = "Finalizado"
            chamado["descricao_finalizacao"] = descricao_finalizacao
            chamado["data_finalizacao"] = datetime.now().strftime("%d/%m/%Y %H:%M")
            chamado["tecnico"] = tecnico.get("email", TECNICO_PADRAO["email"])
            salvar_chamados(chamados)
            return True, "Chamado finalizado com sucesso!"
    return False, "Chamado não encontrado."


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
carregar_env()
