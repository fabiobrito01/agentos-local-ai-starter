"""Servidor web local e privado para conversar com modelos do Ollama."""
import json, os, urllib.request
from http.server import HTTPServer, SimpleHTTPRequestHandler

OLLAMA=os.getenv("OLLAMA_URL","http://127.0.0.1:11434")
MODEL=os.getenv("OLLAMA_MODEL","llama3.2")
class Handler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/api/chat": self.send_error(404); return
        try:
            body=json.loads(self.rfile.read(int(self.headers.get("Content-Length","0"))))
            payload=json.dumps({"model":body.get("model",MODEL),"messages":body["messages"],"stream":False}).encode()
            req=urllib.request.Request(f"{OLLAMA}/api/chat",payload,{"Content-Type":"application/json"})
            with urllib.request.urlopen(req,timeout=120) as res: data=res.read()
            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers(); self.wfile.write(data)
        except Exception as exc:
            self.send_response(502); self.send_header("Content-Type","application/json"); self.end_headers(); self.wfile.write(json.dumps({"error":str(exc)}).encode())
if __name__=="__main__":
    os.chdir(os.path.join(os.path.dirname(__file__),"web")); print("AgentOS Local AI: http://127.0.0.1:8787"); HTTPServer(("127.0.0.1",8787),Handler).serve_forever()
