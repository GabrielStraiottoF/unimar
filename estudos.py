from datetime import datetime

from dados import carregar_json, salvar_json
from historico import registrar_evento

ARQUIVO_TAREFAS = "tarefas.json"
ARQUIVO_PROJETOS = "projetos.json"


def _proximo_id(lista):
    ids = []
    for item in lista:
        try:
            ids.append(int(item.get("id", 0)))
        except (TypeError, ValueError):
            continue
    return max(ids or [0]) + 1


def carregar_tarefas():
    dados = carregar_json(ARQUIVO_TAREFAS, {"tarefas": []})
    return dados.get("tarefas", []) if isinstance(dados, dict) else []


def salvar_tarefas(tarefas):
    salvar_json(ARQUIVO_TAREFAS, {"tarefas": tarefas})


def tarefas_do_usuario(email_usuario):
    return [t for t in carregar_tarefas() if t.get("email_usuario", "").lower() == email_usuario.lower()]


def criar_tarefa(email_usuario, titulo, descricao, prioridade, prazo="", projeto_id=None):
    titulo = titulo.strip()
    descricao = descricao.strip()
    prazo = prazo.strip()

    if not titulo:
        return False, "Informe o título da tarefa.", None

    if prioridade not in {"Baixa", "Média", "Alta"}:
        prioridade = "Média"

    tarefas = carregar_tarefas()
    tarefa = {
        "id": _proximo_id(tarefas),
        "email_usuario": email_usuario.lower(),
        "titulo": titulo,
        "descricao": descricao,
        "prioridade": prioridade,
        "prazo": prazo,
        "concluida": False,
        "projeto_id": projeto_id,
        "data_criacao": datetime.now().strftime("%d/%m/%Y %H:%M"),
    }
    tarefas.append(tarefa)
    salvar_tarefas(tarefas)
    registrar_evento(email_usuario, "tarefa_criada", f'Tarefa criada: "{titulo}"')
    return True, "Tarefa criada com sucesso!", tarefa


def concluir_tarefa(email_usuario, id_tarefa):
    tarefas = carregar_tarefas()

    for tarefa in tarefas:
        if str(tarefa.get("id")) != str(id_tarefa):
            continue
        if tarefa.get("email_usuario", "").lower() != email_usuario.lower():
            continue
        if tarefa.get("concluida"):
            return False, "Esta tarefa já está concluída."

        tarefa["concluida"] = True
        tarefa["data_conclusao"] = datetime.now().strftime("%d/%m/%Y %H:%M")
        salvar_tarefas(tarefas)
        registrar_evento(email_usuario, "tarefa_concluida", f'Tarefa concluída: "{tarefa.get("titulo", "")}"')
        return True, "Tarefa concluída!"

    return False, "Tarefa não encontrada."


def excluir_tarefa(email_usuario, id_tarefa):
    tarefas = carregar_tarefas()
    novas = []
    removida = None

    for tarefa in tarefas:
        if str(tarefa.get("id")) == str(id_tarefa) and tarefa.get("email_usuario", "").lower() == email_usuario.lower():
            removida = tarefa
        else:
            novas.append(tarefa)

    if removida is None:
        return False, "Tarefa não encontrada."

    salvar_tarefas(novas)
    registrar_evento(email_usuario, "tarefa_excluida", f'Tarefa excluída: "{removida.get("titulo", "")}"')
    return True, "Tarefa excluída."


def carregar_projetos():
    dados = carregar_json(ARQUIVO_PROJETOS, {"projetos": []})
    return dados.get("projetos", []) if isinstance(dados, dict) else []


def salvar_projetos(projetos):
    salvar_json(ARQUIVO_PROJETOS, {"projetos": projetos})


def projetos_do_usuario(email_usuario):
    return [p for p in carregar_projetos() if p.get("email_usuario", "").lower() == email_usuario.lower()]


def criar_projeto(email_usuario, nome, descricao):
    nome = nome.strip()
    descricao = descricao.strip()

    if not nome:
        return False, "Informe o nome do projeto.", None

    projetos = carregar_projetos()
    projeto = {
        "id": _proximo_id(projetos),
        "email_usuario": email_usuario.lower(),
        "nome": nome,
        "descricao": descricao,
        "data_criacao": datetime.now().strftime("%d/%m/%Y %H:%M"),
    }
    projetos.append(projeto)
    salvar_projetos(projetos)
    registrar_evento(email_usuario, "projeto_criado", f'Projeto criado: "{nome}"')
    return True, "Projeto criado com sucesso!", projeto


def progresso_projeto(email_usuario, projeto_id):
    tarefas = [
        t for t in tarefas_do_usuario(email_usuario)
        if str(t.get("projeto_id")) == str(projeto_id)
    ]
    total = len(tarefas)
    concluidas = sum(1 for t in tarefas if t.get("concluida"))
    percentual = round((concluidas / total) * 100) if total else 0
    return total, concluidas, percentual
