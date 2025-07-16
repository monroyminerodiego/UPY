# ===== Comandos para ejecutar docker
# clear; docker rm UPY; docker build -t upy . && docker run --name UPY -p 10000:10000 upy
# ==========

# Imagen base oficial de Python
FROM python:3.11-slim

# Crear y usar directorio de trabajo
WORKDIR /app

# Copiar dependencias y código
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Exponer puerto Flask
EXPOSE 10000

# Comando para correr la app
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:10000", "app:app"]
