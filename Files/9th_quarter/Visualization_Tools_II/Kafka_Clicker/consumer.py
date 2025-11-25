import threading, time, json
from kafka import KafkaConsumer # type: ignore
from kafka.errors import NoBrokersAvailable # type: ignore

# Configuración
KAFKA_BROKER = 'kafka_visualization:9092'
TOPIC_NAME = 'clicks'

class ClickConsumer:
    def __init__(self):
        self.consumer = None
        self.running = True
        self.lock = threading.Lock()
        
        # Estado acumulado
        self.total_cheers = 0
        self.total_fuck = 0
        
        # Historial para Time Series
        self.recent_events = [] 

        # Hilo background
        self.thread = threading.Thread(target=self._run_consumer_loop, daemon=True)
        self.thread.start()

    def _connect(self):
        while self.running:
            try:
                print(f"[Consumer] Buscando broker en {KAFKA_BROKER}...")
                self.consumer = KafkaConsumer(
                    TOPIC_NAME,
                    bootstrap_servers=[KAFKA_BROKER],
                    auto_offset_reset='earliest',
                    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                    # Usamos un group_id fijo para no perder mensajes si reiniciamos
                    group_id='click-dashboard-group-v1' 
                )
                print("[Consumer] ¡Conectado y escuchando!")
                return True
            except NoBrokersAvailable:
                print("[Consumer] Broker no disponible. Reintentando en 3s...")
                time.sleep(3)
        return False

    def _run_consumer_loop(self):
        if not self._connect(): return

        print("[Consumer] Loop de escucha iniciado.")
        
        last_cleanup = time.time()

        try:
            # timeout_ms permite que el loop no se bloquee eternamente y podamos hacer limpieza
            for message in self.consumer:
                if not self.running: break
                
                data = message.value
                c_type = data.get('type')
                ts = data.get('timestamp')

                with self.lock:
                    if c_type == 'cheers': self.total_cheers += 1
                    elif c_type == 'fuck': self.total_fuck += 1
                    
                    self.recent_events.append({'type': c_type, 'timestamp': ts})

                # Limpieza automática cada 30 segundos (incluso si nadie ve el dashboard)
                if time.time() - last_cleanup > 30:
                    self._cleanup_old_data()
                    last_cleanup = time.time()

        except Exception as e:
            print(f"[Consumer] Error en loop: {e}")

    def _cleanup_old_data(self):
        """Elimina eventos de hace más de 3 minutos para liberar RAM"""
        limit_time = time.time() - 180 
        with self.lock:
            # Mantenemos solo los recientes
            initial_len = len(self.recent_events)
            self.recent_events = [e for e in self.recent_events if e['timestamp'] >= limit_time]
            # print(f"[Consumer] Limpieza: {initial_len} -> {len(self.recent_events)} eventos.")

    def get_data(self):
        current_time = time.time()
        window_start = current_time - 120 # Ventana de 2 minutos

        with self.lock:
            # Filtramos para enviar solo lo necesario al front
            valid_events = [e for e in self.recent_events if e['timestamp'] >= window_start]
            
            response = {
                'totals': {
                    'cheers': self.total_cheers,
                    'fuck': self.total_fuck
                },
                'recent_history': valid_events,
                'server_time': current_time
            }
        return response

click_consumer = ClickConsumer()