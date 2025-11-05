FROM ubuntu:20.04

# Install necessary packages
RUN apt-get update && apt-get install -y \
    gcc \
    make \
    libc6-dev \
    socat \
    && rm -rf /var/lib/apt/lists/*

# Create challenge user
RUN useradd -m -s /bin/bash ctf

# Copy challenge files
WORKDIR /challenge
COPY vuln.c .
COPY Makefile .
COPY flag.txt .

# Build the binary
RUN make vuln

# Set permissions
RUN chown root:ctf flag.txt
RUN chmod 640 flag.txt
RUN chown root:ctf vuln
RUN chmod 755 vuln

# Switch to ctf user
USER ctf

# Expose port
EXPOSE 1337

# Run the challenge with timeout
CMD timeout 180 socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"./vuln"