# 📈 Kafka Real-Time Clicker & Dashboard

**Autor**: Diego Monroy 

Este módulo implementa un sistema de streaming de datos en tiempo real utilizando **Apache Kafka**, **Flask** y **Chart.js**. El objetivo es visualizar la interacción de usuarios (votos positivos/negativos) con una latencia mínima mediante una arquitectura Productor-Consumidor.

## 🧠 Arquitectura del Sistema

El flujo de datos sigue un patrón de mensajería asíncrona para desacoplar la generación de eventos de su procesamiento.

```mermaid
graph LR
    A["Usuario (Clicker UI)"] -->|HTTP POST| B("Flask Endpoint")
    B -->|"Producer.py"| C{"Kafka Cluster"}
    C -->|"Topic: clicks"| D["Consumer.py (Background Thread)"]
    D -->|"Aggregates Data"| E[("Memoria RAM")]
    F["Usuario (Dashboard UI)"] -->|"HTTP GET / Polling"| E
    E -->|"JSON Data"| F
````

### Componentes

1.  **Producer (`producer.py`)**:

      * Conecta al broker de Kafka (`kafka_visualization:9092`).
      * Serializa los eventos (Cheers/Hate) a JSON.
      * Maneja reintentos de conexión automáticos si el broker no está listo.

2.  **Consumer (`consumer.py`)**:

      * Corre en un **hilo en segundo plano (Daemon Thread)** dentro de la app de Flask para no bloquear el servidor web.
      * Escucha el tópico `clicks`.
      * Mantiene un estado en memoria (`total_cheers`, `total_fuck`, `recent_events`) y limpia datos antiguos (\>3 min) para optimizar RAM.

3.  **Frontend**:

      * **Clicker**: Interfaz simple para enviar eventos.
      * **Dashboard**: Utiliza `Chart.js` para renderizar una serie de tiempo en vivo, agrupando eventos en ventanas de 2 segundos (Binning).


## 🛠️ Stack Tecnológico

  * **Backend**: Python 3.11, Flask, Kafka-Python.
  * **Broker**: Apache Kafka + Zookeeper (Containerizados).
  * **Frontend**: HTML5, CSS3, Javascript (Fetch API), Chart.js.
  * **Infraestructura**: Docker & Docker Compose.


## 🚀 Instalación y Ejecución

Este módulo es parte del proyecto `web_upy`. Asegúrate de estar en la raíz del proyecto para levantar los servicios.

### 1\. Estructura de Servicios (Docker Compose)

El sistema depende de que los siguientes contenedores estén activos:

  * `web_upy`: Servidor Flask (Puerto 501).
  * `kafka_visualization`: Broker de Kafka (Puerto 9092).
  * `zookeeper_visualization`: Coordinador (Puerto 2181).

### 2\. Comandos de Despliegue

```bash
# Desde la raíz ~/UPY/
docker-compose up -d --build
```

### 3\. Verificar Logs

Para asegurar que el consumidor conectó correctamente:

```bash
docker logs -f web_upy
```

*Deberías ver:* `[Consumer] ¡Conectado y escuchando!`


## 🔗 Endpoints y Rutas

### Vistas (Frontend)

| Ruta | Descripción |
| :--- | :--- |
| `/visualization-tools-ii/kafka-clicker` | Interfaz para generar clicks (Productor). |
| `/visualization-tools-ii/kafka-dashboard` | Dashboard de visualización en vivo (Consumidor). |

### API (Backend)

| Método | Endpoint | Payload | Descripción |
| :--- | :--- | :--- | :--- |
| `POST` | `.../kafka/click` | `{"type": "cheers"}` | Envía un evento al tópico de Kafka. |
| `GET` | `.../kafka/data` | N/A | Retorna el conteo total y el historial reciente (2 min). |


## ⚙️ Detalles de Implementación

### Configuración del Broker

El sistema espera encontrar a Kafka en la red interna de Docker:

  * **Host**: `kafka_visualization`
  * **Port**: `9092`
  * **Topic**: `clicks`

### Manejo de Fallos

  * **Reconexión**: Tanto el `producer` como el `consumer` tienen lógica de `retry` (bucle `while` con `time.sleep`) para esperar a que Kafka termine de iniciar antes de lanzar errores.
  * **Mocks**: Si la librería `kafka-python` falla al importar, la aplicación Flask no se rompe, simplemente deshabilita las rutas de Kafka.


## 📂 Estructura de Archivos

```text
Kafka_Clicker/
├── clicker.html      # UI para enviar eventos
├── dashboard.html    # UI para visualizar métricas
├── producer.py       # Lógica de envío a Kafka
├── consumer.py       # Lógica de lectura y agregación
└── README.md         # Documentación
```



