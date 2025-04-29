FROM python:3.10-slim

RUN apt-get update && apt-get install -y wget curl unzip

# Install EPANET2 CLI
RUN wget https://github.com/OpenWaterAnalytics/epanet/releases/download/v2.2/epanet2_2.2_linux.zip -O epanet.zip && \
    unzip epanet.zip && \
    chmod +x bin/epanet2 && \
    mv bin/epanet2 /usr/local/bin/epanet2

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]