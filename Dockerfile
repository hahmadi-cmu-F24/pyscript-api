FROM python:3.11-bullseye

# Install dependencies for building nsjail
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    pkg-config \
    libprotobuf-dev \
    libnl-route-3-dev \
    libcap-dev \
    libssl-dev \
    protobuf-compiler \
    libprotobuf-c-dev \
    flex \
    bison \
    && rm -rf /var/lib/apt/lists/*

# Build and install nsjail
RUN git clone https://github.com/google/nsjail.git /tmp/nsjail && \
    cd /tmp/nsjail && make && \
    mv nsjail /usr/local/bin/ && \
    rm -rf /tmp/nsjail

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["flask", "--app", "app", "run", "--host=0.0.0.0", "--port=8080"]
