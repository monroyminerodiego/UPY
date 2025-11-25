import time, json
from kafka import KafkaProducer # type: ignore
from kafka.errors import NoBrokersAvailable # type: ignore

# Configuración basada en tu docker-compose.yml
KAFKA_BROKER = 'kafka_visualization:9092'
TOPIC_NAME = 'clicks'

class ClickProducer:
    def __init__(self):
        self.producer = None
        self._connect()

    def _connect(self):
        """Intenta conectar con Kafka con reintentos."""
        retries = 0
        max_retries = 15
        while retries < max_retries:
            try:
                print(f"[Producer] Intentando conectar al broker {KAFKA_BROKER}...")
                self.producer = KafkaProducer(
                    bootstrap_servers=[KAFKA_BROKER],
                    value_serializer=lambda x: json.dumps(x).encode('utf-8'),
                    acks='all'
                )
                print("[Producer] ¡Conexión exitosa!")
                return
            except NoBrokersAvailable:
                print("[Producer] Kafka no listo. Reintentando en 2s...")
                time.sleep(2)
                retries += 1
        print("[Producer] Error: No se pudo conectar a Kafka.")

    def send_click(self, click_type):
        """
        Envía un evento de clic a Kafka.
        click_type: 'cheers' | 'fuck'
        """
        if not self.producer:
            self._connect()
        
        if self.producer:
            data = {
                'type': click_type,
                'timestamp': time.time()
            }
            try:
                # Enviamos al tópico único 'clicks'
                self.producer.send(TOPIC_NAME, value=data)
                self.producer.flush() 
                print(f"[Producer] Mensaje enviado: {data}")
                return True
            except Exception as e:
                print(f"[Producer] Error enviando: {e}")
                return False
        return False

# Instancia global
click_producer = ClickProducer()