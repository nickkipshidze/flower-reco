from http.server import BaseHTTPRequestHandler
import json, os, sys, cgi, io, PIL.Image
import __main__

BASE_DIR = os.path.dirname(sys.argv[0]) if os.path.dirname(sys.argv[0]) != "" else "."

class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            response = open(f"{BASE_DIR}/static/index.html", "r").read().encode()
            
        elif self.path == "/static/style.css":
            self.send_response(200)
            self.send_header("Content-type", "text/css")
            response = open(f"{BASE_DIR}/static/style.css", "r").read().encode()
            
        elif self.path == "/static/script.js":
            self.send_response(200)
            self.send_header("Content-type", "text/javascript")
            response = open(f"{BASE_DIR}/static/script.js", "r").read().encode()
            
        else:
            self.send_response(404)
            response = "404 Not Found".encode()

        self.end_headers()
        self.wfile.write(response)
            
    def do_POST(self):
        if self.path == "/upload":
            ctype, pdict = cgi.parse_header(self.headers.get("Content-Type"))
            if ctype == "multipart/form-data":
                pdict["boundary"] = bytes(pdict["boundary"], "utf-8")
                pdict["CONTENT-LENGTH"] = int(self.headers.get("Content-Length"))
                form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={"REQUEST_METHOD": "POST"}, keep_blank_values=True)
                if "file" in form:
                    file_item = form["file"]
                    if file_item.file:
                        image_data = file_item.file.read()
                        image = PIL.Image.open(io.BytesIO(image_data))
                        response = __main__.predict(image)
                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()
                        self.wfile.write(response.encode())
                        return
                else:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b"Invalid form data (file)")
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Invalid form data (mime type)")
                
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write("404 Not Found".encode())