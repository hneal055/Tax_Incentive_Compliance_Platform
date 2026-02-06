import socket
import time
import urllib.request
from urllib.error import URLError, HTTPError

def check_service(name, host, port, path="/"):
    url = f"http://{host}:{port}{path}"
    print(f"Checking {name} at {url}...")
    
    # TCP Socket Check
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    try:
        start_socket = time.time()
        result = s.connect_ex((host, port))
        socket_time = (time.time() - start_socket) * 1000
        if result == 0:
            print(f"  [PASS] Port {port} is open (TCP Latency: {socket_time:.2f}ms)")
        else:
            print(f"  [FAIL] Port {port} is closed.")
            return
    except Exception as e:
        print(f"  [FAIL] Port check error: {e}")
        return
    finally:
        s.close()
    
    # HTTP Request Check
    try:
        start_http = time.time()
        req = urllib.request.Request(url, method='HEAD')
        with urllib.request.urlopen(req, timeout=5) as response:
            http_time = (time.time() - start_http) * 1000
            print(f"  [PASS] HTTP {response.getcode()} OK (Response Time: {http_time:.2f}ms)")
    except HTTPError as e:
        print(f"  [FAIL] HTTP Error: {e.code} {e.reason}")
    except URLError as e:
        print(f"  [FAIL] Connection failed: {e.reason}")
    except Exception as e:
        print(f"  [FAIL] Unexpected error: {e}")

print("\n=== Network Performance Evaluation ===\n")
check_service("Backend API", "127.0.0.1", 8000, "/api/v1/productions")
print("-" * 30)
check_service("Frontend dev server", "127.0.0.1", 5173, "/")
print("\n======================================")
