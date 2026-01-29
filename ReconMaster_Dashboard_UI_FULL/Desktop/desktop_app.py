import threading
import socket
import os
import time

import webview
import uvicorn

from Controller.server import app

def _pick_free_port() -> int:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port

def _run_server(port: int):
    uvicorn.run(app, host="127.0.0.1", port=port, log_level="warning")

def main():
    port_env = os.environ.get("RM_PORT", "").strip()
    port = int(port_env) if port_env.isdigit() else _pick_free_port()

    t = threading.Thread(target=_run_server, args=(port,), daemon=True)
    t.start()
    time.sleep(0.4)

    webview.create_window("ReconMaster", f"http://127.0.0.1:{port}/", width=1280, height=760)
    webview.start()

if __name__ == "__main__":
    main()
