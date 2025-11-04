FROM node:20-alpine

WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install --production || npm install --production --legacy-peer-deps
COPY . .

ENV PORT=31349
EXPOSE 31349
CMD ["npm","run","start"]
