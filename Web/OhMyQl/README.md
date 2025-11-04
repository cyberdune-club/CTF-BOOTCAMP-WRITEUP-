# CYBERDUNE • OhMyQL (GraphQL + SQLite) — Challenge

**Port:** `31349`  
**Flag format:** `CYBERDUNE{...}`  
**Default flag (can override via env `FLAG`):** `CYBERDUNE{f~cDBvyQ5TzHqRmOxIMRSrZ-H~3jEpVLt6VH!F5WMs3j}`

## Run (Node.js)

```bash
cd cyberdune-ohmyql
npm install
npm run start
# Server runs on http://127.0.0.1:31349
```

## Run (Docker)

```bash
docker build -t cyberdune-ohmyql .
docker run --rm -it -p 31349:31349 -e FLAG="CYBERDUNE{f~cDBvyQ5TzHqRmOxIMRSrZ-H~3jEpVLt6VH!F5WMs3j}" -e JWT_SECRET="87e3b34d320efd4cfd9504b08166fab8" cyberdune-ohmyql
```

## Endpoints

- `GET /` — flashy red/black landing page
- `POST /graphql` — GraphQL endpoint (no GraphiQL), context via `Authorization: Bearer <JWT>`
- `GET /admin` — returns flag only if JWT has `flagOwner: true`

## Intention

- The database is **empty** (table `users(username,password,flagowner)`), but the `getUser()` lookup is **SQL-injection** vulnerable.
- The `login` mutation signs the JWT with the **provided** username (not DB’s), and `setFlagOwner` requires the header-JWT username to match the mutation argument.
- Therefore: UNION-based SQLi --> login as faux user --> use that JWT to call `setFlagOwner` with the **same** username string --> receive a new JWT with `flagOwner=true` --> `GET /admin`.
