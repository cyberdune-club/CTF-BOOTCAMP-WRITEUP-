# OhMyQL — Walkthrough (Inspired)

This challenge mirrors FlagYard’s “OhMyQL” idea. Key steps:

- `/admin` requires a valid JWT where `flagOwner === true`.
- `login(username,password)` fetches a row with `getUser(username)` — but that function is **SQLi vulnerable** via string interpolation.
- The table is empty; a plain SELECT returns nothing. Use **UNION SELECT** to fabricate a row:
  ```sql
  SELECT * FROM users WHERE username = '' UNION SELECT 'admin','admin',1;
  ```
- The login resolver **signs the JWT with the provided username** (the injection string), not the username returned by the DB row.
- Then call:
  ```graphql
  mutation setFlagOwner($u: String!){ setFlagOwner(username: $u) }
  ```
  with `Authorization: Bearer <your first token>` and variables `{ "u": "<the EXACT username you used in login>" }`.
- You’ll receive a second JWT with `flagOwner: true` — send it to `/admin` and recover the flag.

See `scripts/solve.py` for an automated exploit.
