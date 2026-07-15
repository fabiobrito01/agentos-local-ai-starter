# AgentOS Local AI Starter

Assistente de IA local, privado e sem telemetria, com interface web e integração direta com [Ollama](https://ollama.com/).

## Começar

```bash
ollama pull llama3.2
python app.py
```

Abra `http://127.0.0.1:8787`. Configure outro modelo com `OLLAMA_MODEL` e outro servidor com `OLLAMA_URL`.

## Segurança

O servidor escuta apenas em `127.0.0.1`. Não o exponha à internet sem autenticação e HTTPS.

Projeto AgentOStudio · Licença MIT.
