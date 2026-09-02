# UNIMAR Study

Aplicativo desktop em Python + Tkinter para ajudar estudantes a organizar tarefas, projetos e histórico de estudos.

## Objetivo

O UNIMAR Study transforma uma rotina de estudos espalhada em um espaço simples para acompanhar atividades e evolução.

## Funcionalidades

- cadastro e login de usuários;
- tarefas com prioridade, descrição e prazo;
- conclusão e exclusão de tarefas;
- projetos escolares;
- acompanhamento percentual dos projetos;
- histórico das ações do usuário;
- assistente de estudos com Azure AI Foundry, quando configurado.

## Conteúdo do bootcamp aplicado

O projeto utiliza diretamente conceitos das Aulas 1 e 2: GUI, widgets, `Tk`, `mainloop`, `Entry`, `Button`, `Label`, `Frame`, `pack`, `grid`, `Checkbutton`, `Radiobutton`, `BooleanVar`, `StringVar`, `Text`, `messagebox`, `command`, `bind` e organização da janela com classe baseada em `tk.Tk`.

## Como executar

1. Instale Python 3.10+.
2. Instale as dependências: `pip install -r requirements.txt`.
3. Execute: `python main.py`.

Os dados locais são criados automaticamente na pasta `dados/`.

## Assistente de estudos

Crie um `.env` a partir do `.env.example` e configure as variáveis do Azure AI Foundry. O aplicativo continua funcionando sem a IA; apenas a tela do assistente ficará indisponível até a configuração.

## Segurança e escopo

As contas são locais e os dados são armazenados em JSON porque o objetivo é demonstrar os conceitos do bootcamp. Em um sistema real, autenticação e persistência deveriam usar infraestrutura apropriada.
