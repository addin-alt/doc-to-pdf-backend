# Base image
FROM ubuntu:22.04

# Install LibreOffice + Python
RUN apt update && apt install -y \
    libreoffice \
    python3 \
    python3-pip

WORKDIR /app
COPY . .

RUN pip3 install -r requirements.txt

CMD ["python3", "app.py"]
