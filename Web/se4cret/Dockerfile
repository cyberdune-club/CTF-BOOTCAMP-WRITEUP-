# Lightweight CTF web challenge with an admin bot
# Uses Puppeteer's official image so headless Chrome works without extra deps
FROM ghcr.io/puppeteer/puppeteer:latest

WORKDIR /app

# Copy package manifests and install first (better layer caching)
COPY package.json package-lock.json* ./
RUN npm install --omit=dev

# Copy the application
COPY . .

# Environment
ENV PORT=31347
# Allow override of FLAG at runtime, but fall back to file /app/flag.txt
ENV FLAG=

EXPOSE 31347

# Healthcheck (optional)
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s CMD node -e "require('http').get('http://127.0.0.1:31347/health', res => process.exit(res.statusCode===200?0:1)).on('error',()=>process.exit(1))"

CMD ["node","server.js"]
