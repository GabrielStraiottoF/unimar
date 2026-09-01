import os
from pathlib import Path


class AssistenteFoundry:
    """Integra o aplicativo ao modelo configurado no Azure AI Foundry."""

    def __init__(self):
        self.client = None
        self.modelo = None
        self._carregar_env()

    @staticmethod
    def _carregar_env():
        caminho = Path(__file__).resolve().parent / ".env"
        if not caminho.exists():
            return

        try:
            for linha in caminho.read_text(encoding="utf-8").splitlines():
                linha = linha.strip()
                if not linha or linha.startswith("#") or "=" not in linha:
                    continue
                chave, valor = linha.split("=", 1)
                os.environ.setdefault(chave.strip(), valor.strip().strip('"').strip("'"))
        except OSError:
            pass

    def iniciar(self):
        endpoint = os.getenv("FOUNDRY_ENDPOINT", "").strip()
        chave = os.getenv("FOUNDRY_API_KEY", "").strip()
        modelo = os.getenv("FOUNDRY_MODEL", "").strip()

        if not endpoint or not chave or not modelo:
            raise ValueError(
                "Configure FOUNDRY_ENDPOINT, FOUNDRY_API_KEY e FOUNDRY_MODEL no .env."
            )

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
        texto = texto.strip()
        if not texto:
            raise ValueError("Digite uma pergunta antes de enviar.")

        if self.client is None:
            self.iniciar()

        resposta = self.client.chat.completions.create(
            model=self.modelo,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Você é o Assistente de Estudos do UNIMAR Study. "
                        "Ajude estudantes a entender conteúdos, organizar estudos, "
                        "planejar tarefas e desenvolver projetos escolares. "
                        "Explique de forma clara, objetiva e adequada para estudantes."
                    ),
                },
                {"role": "user", "content": texto},
            ],
        )

        return resposta.choices[0].message.content
