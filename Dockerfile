FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget curl unzip build-essential cmake git

# Clone EPANET repository and build EPANET CLI
RUN git clone https://github.com/OpenWaterAnalytics/EPANET.git && \
    cd EPANET && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make && \
    cp bin/epanet2 /usr/local/bin/epanet2

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
