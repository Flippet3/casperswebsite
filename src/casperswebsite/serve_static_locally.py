from casperswebsite.general_tools import get_root_folder
import http.server
import socketserver
import os

PORT = 8080
static_folder = os.path.join(get_root_folder(), "compiled")
os.chdir(static_folder)

Handler = http.server.SimpleHTTPRequestHandler

def serve_static():
    # Call fuser -k 8080/tcp before serving, to kill anything using the port (works on Linux).
    try:
        os.system(f"fuser -k {PORT}/tcp")
    except Exception as e:
        print(f"Warning: Could not run fuser to kill processes on port 8080: {e}")
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving static files at http://localhost:{PORT}/ from {static_folder}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down the server.")
            httpd.server_close()

if __name__ == "__main__":
    serve_static()