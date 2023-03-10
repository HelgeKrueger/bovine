import base64
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlencode

host_name = "127.0.0.1"
server_port = 8080


class MyServer(BaseHTTPRequestHandler):
    path = None

    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><body>All Done</body></html>", "utf-8"))

        content_len = int(self.headers.get("Content-Length"))
        post_body = self.rfile.read(content_len)

        MyServer.path = post_body


if __name__ == "__main__":
    url_to_open = "https://wallet.hello.coop/authorize?" + urlencode(
        {
            "client_id": "XXX",
            "nonce": "xxx",
            "redirect_uri": f"http://{host_name}:{server_port}",
            "response_mode": "form_post",
            "response_type": "id_token",
            "scope": "openid+email",
        }
    ).replace("%2B", "+")

    print(url_to_open)

    web_server = HTTPServer((host_name, server_port), MyServer)
    try:
        web_server.handle_request()
    except KeyboardInterrupt:
        pass

    id_token = MyServer.path.decode("utf-8").split("=")[1]
    token = id_token.split(".")[1]
    result = base64.urlsafe_b64decode(token + "=" * divmod(len(token), 4)[1]).decode(
        "utf-8"
    )

    print(json.dumps(json.loads(result), indent=2))

    import IPython

    IPython.embed()

    web_server.server_close()
    print("Server stopped.")
