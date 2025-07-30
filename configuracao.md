# Agendamento Automático no Windows (Task Scheduler)

Este guia explica como configurar a automação para rodar automaticamente no Windows usando o Agendador de Tarefas.

## 1. Crie o arquivo `run_automation.bat`

Crie um arquivo chamado `run_automation.bat` na raiz do projeto com o seguinte conteúdo:

```bat
@echo off
REM Script para rodar a automação de emendas com ambiente virtual ativado
cd /d %~dp0
call venv\Scripts\activate.bat
python src\main.py
```

> Certifique-se de que o ambiente virtual está criado na pasta `venv` na raiz do projeto.

## 2. Configure o Agendador de Tarefas do Windows

1. Abra o **Agendador de Tarefas** (Task Scheduler).
2. Clique em **Criar Tarefa**.
3. Na aba **Ações**, clique em **Nova...** e configure:
   - **Ação:** Iniciar um programa
   - **Programa/script:** Caminho completo para o `run_automation.bat` (ex: `C:\Users\SeuUsuario\Desktop\amendments-automation\run_automation.bat`)
   - **Argumentos:** (deixe vazio)
   - **Iniciar em:** Caminho da pasta do projeto (ex: `C:\Users\SeuUsuario\Desktop\amendments-automation`)
4. Defina o **gatilho** (quando a tarefa será executada) conforme desejado.
5. Salve a tarefa.

Pronto! O Windows executará a automação no horário agendado, ativando o ambiente virtual corretamente.

---

> Dica: Teste o `.bat` manualmente antes de agendar para garantir que tudo está funcionando.
