#!/usr/bin/env python3
# challenge.py
from Crypto.Util.number import long_to_bytes, bytes_to_long, inverse
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from fastecdsa.curve import P256 as EC
from fastecdsa.point import Point
import os, random, hashlib, json
import socketserver, socket
from secret import FLAG

class SignService:
    def __init__(self):
        self.G = Point(EC.gx, EC.gy, curve=EC)
        self.order = EC.q
        self.p = EC.p
        self.a = EC.a
        self.b = EC.b
        self.privkey = random.randrange(1, self.order - 1)
        self.pubkey = (self.privkey * self.G)
        self.key = os.urandom(16)
        self.iv = os.urandom(16)
        # INTENTIONAL VULN: reuse same ephemeral nonce k for all signatures
        self._fixed_k = random.randrange(1, self.order - 1)

    def generate_key(self):
        self.privkey = random.randrange(1, self.order - 1)
        self.pubkey = (self.privkey * self.G)

    def ecdsa_sign(self, message, privkey):
        z = int(hashlib.sha256(message).hexdigest(), 16)
        k = self._fixed_k                       # <-- insecure reuse
        r = (k*self.G).x % self.order
        s = (inverse(k, self.order) * (z + r*privkey)) % self.order
        return (r, s)

    def ecdsa_verify(self, message, r, s, pubkey):
        r %= self.order
        s %= self.order
        if s == 0 or r == 0:
            return False
        z = int(hashlib.sha256(message).hexdigest(), 16)
        s_inv = inverse(s, self.order)
        u1 = (z*s_inv) % self.order
        u2 = (r*s_inv) % self.order
        W = u1*self.G + u2*pubkey
        return W.x == r

    def aes_encrypt(self, plaintext):
        cipher = AES.new(self.key, AES.MODE_GCM, nonce=self.iv)
        ct, tag = cipher.encrypt_and_digest(plaintext)
        return tag + ct

    def aes_decrypt(self, ciphertext):
        tag, ct = ciphertext[:16], ciphertext[16:]
        cipher = AES.new(self.key, AES.MODE_GCM, nonce=self.iv)
        plaintext = cipher.decrypt_and_verify(ct, tag)
        return plaintext

    def get_flag(self):
        key = hashlib.sha256(long_to_bytes(self.privkey)).digest()[:16]
        cipher = AES.new(key, AES.MODE_ECB)
        encrypted_flag = cipher.encrypt(pad(FLAG.encode(), 16))
        return encrypted_flag

# Single SignService instance (stateful across connections)
S = SignService()

class ThreadedTCPRequestHandler(socketserver.StreamRequestHandler):
    def handle(self):
        # enforce per-connection timeout (60 seconds)
        self.request.settimeout(60)

        # send initial info as one JSON line
        signkey = S.aes_encrypt(long_to_bytes(S.privkey))
        info = {'pubkey': {'x': hex(S.pubkey.x), 'y': hex(S.pubkey.y)}, 'signkey': signkey.hex()}
        welcome = "Welcome to Fl1pper Zer0 – Signing Service!\n"
        try:
            self.wfile.write(welcome.encode())
            self.wfile.write((json.dumps(info) + "\n").encode())
        except Exception:
            return

        while True:
            try:
                line = self.rfile.readline()
                if not line:
                    break
                try:
                    inp = json.loads(line.decode().strip())
                except Exception:
                    self.wfile.write((json.dumps({'error': 'Invalid JSON'}) + "\n").encode())
                    continue

                if 'option' not in inp:
                    self.wfile.write((json.dumps({'error': 'You must send an option'}) + "\n").encode())

                elif inp['option'] == 'sign':
                    try:
                        msg = bytes.fromhex(inp['msg'])
                        signkey = bytes.fromhex(inp['signkey'])
                        sk = bytes_to_long(S.aes_decrypt(signkey))
                        r, s = S.ecdsa_sign(msg, sk)
                        self.wfile.write((json.dumps({'r': hex(r), 's': hex(s)}) + "\n").encode())
                    except Exception:
                        self.wfile.write((json.dumps({'error': 'sign failed'}) + "\n").encode())

                elif inp['option'] == 'verify':
                    try:
                        msg = bytes.fromhex(inp['msg'])
                        r = int(inp['r'], 16)
                        s = int(inp['s'], 16)
                        px = int(inp['px'], 16)
                        py = int(inp['py'], 16)
                        pub = Point(px, py, curve=EC)
                        verified = S.ecdsa_verify(msg, r, s, pub)
                        if verified:
                            self.wfile.write((json.dumps({'result': 'Success'}) + "\n").encode())
                        else:
                            self.wfile.write((json.dumps({'result': 'Invalid signature'}) + "\n").encode())
                    except Exception:
                        self.wfile.write((json.dumps({'error': 'verify failed'}) + "\n").encode())

                elif inp['option'] == 'generate_key':
                    try:
                        S.generate_key()
                        signkey = S.aes_encrypt(long_to_bytes(S.privkey))
                        self.wfile.write((json.dumps({'pubkey': {'x': hex(S.pubkey.x), 'y': hex(S.pubkey.y)}, 'signkey': signkey.hex()}) + "\n").encode())
                    except Exception:
                        self.wfile.write((json.dumps({'error': 'generate failed'}) + "\n").encode())

                elif inp['option'] == 'get_flag':
                    try:
                        encrypted_flag = S.get_flag()
                        self.wfile.write((json.dumps({'flag': encrypted_flag.hex()}) + "\n").encode())
                    except Exception:
                        self.wfile.write((json.dumps({'error': 'flag failed'}) + "\n").encode())

                elif inp['option'] == 'quit':
                    self.wfile.write(("Adios :)\n").encode())
                    break

                else:
                    self.wfile.write((json.dumps({'error': 'Invalid option'}) + "\n").encode())

            except socket.timeout:
                # connection idle too long — close gracefully
                try:
                    self.wfile.write((json.dumps({'error': 'Connection timeout (60s)'}) + "\n").encode())
                except Exception:
                    pass
                break
            except Exception:
                # any other error: close connection
                break

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

if __name__ == '__main__':
    HOST, PORT = '0.0.0.0', 31337
    print(f"Starting server on {HOST}:{PORT} ...")
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
        server.server_close()
