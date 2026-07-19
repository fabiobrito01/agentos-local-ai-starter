"""Servidor web local e privado para conversar com modelos do Ollama."""
import json
import os
import urllib.request
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

OLLAMA = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434").rstrip("/")
MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
MAX_BODY = int(os.getenv("AGENTOS_MAX_BODY", "1048576"))


def valid_messages(value):
    return isinstance(value, list) and 0 < len(value) <= 200 and all(
        isinstance(item, dict)
        and item.get("role") in {"system", "user", "assistant"}
        and isinstance(item.get("content"), str)
        and 0 < len(item.get("content")) <= 100_000
        for item in value
    )


class Handler(SimpleHTTPRequestHandler):
    def _json(self, status, data):
        payload = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        if self.path == "/api/health":
            try:
                with urllib.request.urlopen(f"{OLLAMA}/api/tags", timeout=3) as response:
                    self._json(200, {"ok": response.status == 200, "ollama": OLLAMA, "default_model": MODEL})
            except Exception as exc:
                self._json(503, {"ok": False, "error": str(exc), "ollama": OLLAMA})
            return
        if self.path == "/api/models":
            try:
                with urllib.request.urlopen(f"{OLLAMA}/api/tags", timeout=5) as response:
                    self._json(200, json.loads(response.read()))
            except Exception as exc:
                self._json(502, {"error": str(exc)})
            return
        super().do_GET()

    def do_POST(self):
        if self.path != "/api/chat":
            self._json(404, {"error": "rota não encontrada"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > MAX_BODY:
                self._json(413, {"error": "requisição vazia ou grande demais"})
                return
            body = json.loads(self.rfile.read(length))
            if not valid_messages(body.get("messages")):
                self._json(400, {"error": "messages deve conter role e content válidos"})
                return
            options = {}
            if "temperature" in body:
                temperature = float(body["temperature"])
                if not 0 <= temperature <= 2:
                    self._json(400, {"error": "temperature deve estar entre 0 e 2"})
                    return
                options["temperature"] = temperature
            payload = json.dumps({"model": body.get("model") or MODEL, "messages": body["messages"], "stream": False, "options": options}).encode()
            request = urllib.request.Request(f"{OLLAMA}/api/chat", payload, {"Content-Type": "application/json"})
            with urllib.request.urlopen(request, timeout=120) as response:
                self._json(200, json.loads(response.read()))
        except Exception as exc:
            self._json(502, {"error": str(exc)})


if __name__ == "__main__":
    os.chdir(os.path.join(os.path.dirname(__file__), "web"))
    print("AgentOS Local AI: http://127.0.0.1:8787")
    ThreadingHTTPServer(("127.0.0.1", 8787), Handler).serve_forever()
