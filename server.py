
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
import os

ROOT = Path(__file__).resolve().parent
QUIZ_FILE = ROOT / "allcode"


def _is_quiz_route(path: str) -> bool:
    normalized = urlsplit(path).path.rstrip("/")
    return normalized in ("", "/allcode")


class QuizHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        if _is_quiz_route(path):
            return str(QUIZ_FILE)
        return super().translate_path(path)

    def guess_type(self, path):
        if Path(path).name == "allcode" or _is_quiz_route(path):
            return "text/html; charset=utf-8"
        return super().guess_type(path)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    server = ThreadingHTTPServer(
        ("0.0.0.0", port),
        lambda *args, **kwargs: QuizHandler(
            *args, directory=str(ROOT), **kwargs
        )
    )
    print(f"Server running on port {port}", flush=True)
    server.serve_forever()
