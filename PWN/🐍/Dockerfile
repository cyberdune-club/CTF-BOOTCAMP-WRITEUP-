# Use a small Debian image with build tools
FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

# install build deps, socat and unzip (if you want to copy a zip)
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    build-essential gcc make socat unzip curl ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# create working dir
WORKDIR /opt/cyberdune

# copy all challenge files into container
# Make sure your directory contains chall.c, flag.txt, Makefile, etc.
COPY . /opt/cyberdune

# build the binary (Makefile should exist)
# The flags match what we used previously: disable stack protector, no-pie
RUN if [ -f Makefile ]; then make; else \
      gcc -g -O0 chall.c -o heap0 -fno-stack-protector -z execstack -no-pie ; \
    fi \
 && chmod +x heap0

# Expose port for the challenge
EXPOSE 31340

# create a non-privileged user (optional but keeps container safer)
RUN useradd -m -s /bin/bash ctf || true
# ensure files are owned properly
RUN chown -R ctf:ctf /opt/cyberdune
USER ctf
WORKDIR /opt/cyberdune

# Entrypoint: run socat to listen on all interfaces and exec heap0 per connection
# Use shell form to allow signal handling and logs to stdout
ENTRYPOINT ["sh", "-c", "exec socat TCP-LISTEN:31340,bind=0.0.0.0,reuseaddr,fork EXEC:./heap0"]
