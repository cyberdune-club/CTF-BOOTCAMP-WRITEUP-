FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc make libc6 libc6-dev libc6-dbg socat patchelf \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /challenge
COPY main.c /challenge/main.c
COPY Makefile /challenge/Makefile
COPY run.sh /challenge/run.sh
COPY entrypoint.sh /challenge/entrypoint.sh
COPY banner.txt /challenge/banner.txt
COPY flag.txt /flag.txt

RUN chmod +x /challenge/run.sh /challenge/entrypoint.sh && make
RUN chmod 755 /challenge/hft && chmod 444 /flag.txt && chown root:root /challenge/hft && chown root:root /flag.txt

EXPOSE 31344
CMD ["/challenge/run.sh"]
