### Context
``` Instrucciones Adicionales
El objetivo de esta actividad es construir una Tubería ETL (Extract, Transform, Load) funcional utilizando Apache Airflow para procesar un conjunto de datos y crear un dashboard que ofrezca insights para resolver o comprender un problema social o ambiental.

Fase 1: Selección del Dataset y Justificación del Problema
Tarea: Elige un dataset público de tamaño mediano O genera datos sintéticos.
Ejemplos de datasets:
 * Calidad del aire
 * Uso del transporte público
 * Niveles de ruido de la ciudad
 * Consumo de agua
 * Avistamientos de vida silvestre
 * Producción de energía renovable
 * Datasets del Banco Mundial
 * Portales de datos abiertos del gobierno

Requisitos de la Justificación (1 Párrafo):
Debes incluir una justificación breve (1 párrafo) que responda a estas preguntas clave:
 * Relevancia: ¿Por qué es importante este dataset a nivel social, ambiental o económico?
 * Problema: ¿Qué problema podría mejorarse al analizar estos datos?
 * Beneficiarios: ¿Quién se beneficia de los insights obtenidos (ciudades, comunidades, naturaleza, salud, etc.)?

Fase 2: Construcción de la Tubería ETL con Airflow
Tarea: Crear un DAG (Directed Acyclic Graph) de Airflow completamente funcional.
Componentes Obligatorios del DAG
| Componente | Descripción |
|---|---|
| Extract | Descargar el dataset elegido O generar datos sintéticos usando Python dentro de una tarea. |
| Transform | Incluir Limpieza (manejo de valores perdidos, duplicados, formato de tipos) y Agregación o Creación de Features (nuevas características). |
| Load | Guardar el dataset limpio y transformado en uno de los siguientes: una carpeta local, una Base de Datos Postgres, o un bucket de almacenamiento en la nube (si está permitido). |
| Scheduling | Añadir un intervalo de programación (diario, por hora, semanal, etc.). Puede ser real o simulado para la clase. |
| Error Handling | Utilizar al menos uno de: try/except dentro de un PythonOperator, o las configuraciones de reintento de Airflow. |
| Scaling Consideration | Agregar una mejora de escalabilidad como: Procesamiento por chunks, uso de formatos de datos eficientes (como Parquet), tareas paralelas, o filtrado de datos crudos de alto volumen antes del procesamiento. |
| Failure Notifications | Incluir notificaciones de fallo a nivel de tarea (el logging o registro es suficiente). |

Fase 3: Creación del Dashboard
Tarea: Crear un dashboard sencillo usando la salida final de la tubería ETL.
Herramientas Permitidas:
 * Power BI
 * Looker Studio
 * Tableau Public
 * Python (Plotly/Matplotlib)
 * Excel / Sheets (solo si los datos limpios son manejables)

Requisitos del Dashboard:
 * Debe contener al menos 2 gráficos y 1 KPI (Key Performance Indicator).
 * Debe usar SOLO los datos limpios/transformados provenientes de la ETL.
 * Debe apoyar claramente la justificación declarada en la Fase 1.

Requisitos de Explicación:
Debes estar preparado para explicar:
 * Propósito de los Gráficos: ¿Por qué elegiste esos gráficos específicos?
 * Impacto: ¿Cómo ayuda este dashboard a solucionar o comprender el problema del mundo real que identificaste?
```

### Prompt
