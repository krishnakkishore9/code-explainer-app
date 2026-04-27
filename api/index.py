from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<h1>Code Explainer App</h1><p>Streamlit is starting... If it does not load, please use Streamlit Community Cloud for a more stable experience.</p>')
        return
