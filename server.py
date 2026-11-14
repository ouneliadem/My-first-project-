from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parent
QUIZ_FILE = ROOT / "allcode"


class QuizHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        if urlsplit(path).path in ("/", "/allcode"):
            return str(QUIZ_FILE)
        return super().translate_path(path)

    def guess_type(self, path):
        if Path(path).name == "allcode":
            return "text/html; charset=utf-8"
        return super().guess_type(path)


if __name__ == "__main__":
    print("Quiz web server starting", flush=True)
    handler = lambda *args, **kwargs: QuizHandler(*args, directory=str(ROOT), **kwargs)
    server = ThreadingHTTPServer(("127.0.0.1", 8000), handler)
    print("Quiz web server ready at http://127.0.0.1:8000/", flush=True)
    server.serve_forever()
