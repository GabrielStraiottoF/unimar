import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PASTA_DADOS = BASE_DIR / "dados"


def garantir_pasta_dados():
    """Cria a pasta de dados quando o programa é executado pela primeira vez."""
    PASTA_DADOS.mkdir(exist_ok=True)


def carregar_json(nome_arquivo, padrao):
    """Carrega um JSON e retorna o valor padrão se ele não existir ou estiver inválido."""
    garantir_pasta_dados()
    caminho = PASTA_DADOS / nome_arquivo

    try:
        with caminho.open("r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return padrao


def salvar_json(nome_arquivo, dados):
    """Salva dados em JSON usando UTF-8 e indentação legível."""
    garantir_pasta_dados()
    caminho = PASTA_DADOS / nome_arquivo

    with caminho.open("w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)
