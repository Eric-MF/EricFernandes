"""Servidor de teste do site. Igual ao `python3 -m http.server`, mas manda o navegador
conferir se há versão nova a cada visita, para mudanças no CSS aparecerem sem limpar o cache.

Uso: python3 _ferramentas/servidor.py [porta] [endereço]
"""
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer


class SemCache(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()


porta = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
endereco = sys.argv[2] if len(sys.argv) > 2 else "127.0.0.1"
ThreadingHTTPServer((endereco, porta), SemCache).serve_forever()
