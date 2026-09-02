from datetime import datetime

from dados import carregar_json, salvar_json

ARQUIVO_HISTORICO = "historico.json"


def registrar_evento(email_usuario, tipo, descricao):
    dados = carregar_json(ARQUIVO_HISTORICO, {"eventos": []})
    eventos = dados.get("eventos", []) if isinstance(dados, dict) else []

    eventos.append({
        "email_usuario": email_usuario.lower(),
        "tipo": tipo,
        "descricao": descricao,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
    })

    salvar_json(ARQUIVO_HISTORICO, {"eventos": eventos})


def historico_do_usuario(email_usuario):
    dados = carregar_json(ARQUIVO_HISTORICO, {"eventos": []})
    eventos = dados.get("eventos", []) if isinstance(dados, dict) else []
    return [e for e in eventos if e.get("email_usuario", "").lower() == email_usuario.lower()]
