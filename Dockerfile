# ===== Comandos para ejecutar docker
# clear; docker rm UPY; docker build -t upy . && docker run --name UPY -p 504:504 upy
# ==========

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 501

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:501", "app:app"]
