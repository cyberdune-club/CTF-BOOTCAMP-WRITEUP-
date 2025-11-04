# Hints

1. **Recon:** The site looks modern, but `/graphql` is where the logic lives.
2. **DB State:** There are *no* users initially. So a plain login won’t work.
3. **SQLi:** `getUser()` concatenates the username into the SQL query.
4. **UNION:** Return your own row from nowhere: `('admin','admin',1)`.
5. **JWT Trap:** The login token is signed with the **provided** username value (not the actual DB row's username).
6. **Flag Owner:** `setFlagOwner(username)` compares the token’s `username` with your mutation argument. Make them **identical**.
7. **Finale:** Use the upgraded token on `/admin`.
