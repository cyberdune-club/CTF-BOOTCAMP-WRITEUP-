#!/usr/bin/env python3
import socket
import threading

HOST = "0.0.0.0"
PORT = 31338
TIMEOUT_SECONDS = 10

# read flag from file
with open("flag.txt", "r") as f:
    FLAG = f.read().strip()

# helper to send line
def send_line(conn, msg):
    conn.sendall((msg + "\n").encode())

def handle_client(conn, addr):
    conn.settimeout(TIMEOUT_SECONDS)
    try:
        rounds = 3
        for m in range(1, rounds + 1):
            data = b''
            # read until newline
            while not data.endswith(b"\n"):
                chunk = conn.recv(4096)
                if not chunk:
                    raise ConnectionError("client closed")
                data += chunk

            # strip and parse
            line = data.strip().decode(errors='ignore')
            try:
                x = int(line)
            except Exception:
                send_line(conn, "Not allowed Answer!")
                conn.close()
                return

            if x == m:
                send_line(conn, "============================")
                send_line(conn, "Keep Going!")
                send_line(conn, "============================")
                continue
            else:
                send_line(conn, "============================")
                send_line(conn, "Wrong Answer!")
                send_line(conn, "============================")
                conn.close()
                return

        # all rounds passed
        send_line(conn, FLAG)
        conn.close()

    except socket.timeout:
        try:
            send_line(conn, "============================")
            send_line(conn, "Timeout: session terminated")
            send_line(conn, "============================")
        except Exception:
            pass
        conn.close()
        return

    except Exception as e:
        try:
            conn.close()
        except Exception:
            pass
        return

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(5)
        print(f"Listening on {HOST}:{PORT} ...")
        while True:
            conn, addr = s.accept()
            print("Connection from", addr)
            t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            t.start()

if __name__ == '__main__':
    main()

