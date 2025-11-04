from node:20-slim 

RUN apt-get update && \
    apt-get -y install socat 

RUN adduser ctf
USER ctf
WORKDIR /app

Run npm init -y
Run npm install md5 

COPY main.js .
COPY flag.txt .

CMD socat -T 20 TCP-LISTEN:31345,reuseaddr,fork EXEC:'node main.js'
