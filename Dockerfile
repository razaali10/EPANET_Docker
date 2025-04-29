FROM python:3.10-slim

# Install build dependencies
RUN apt-get update && apt-get install -y \
    wget curl unzip build-essential cmake git

# Clone and build EPANET from source
RUN git clone https://github.com/OpenWaterAnalytics/EPANET.git && \
    cd EPANET && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make && \
    cp bin/runepanet /usr/local/bin/epanet2

# Set working directory
WORKDIR /app

# Copy and install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy FastAPI application
COPY app.py .

# Expose API port
EXPOSE 5000

# Run FastAPI app using Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]



