FROM python:3.11-slim

WORKDIR /app

# Install network diagnostic tools (realistic for a monitoring station)
RUN apt-get update && apt-get install -y --no-install-recommends \
    tcpdump iputils-ping iproute2 curl net-tools procps \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
