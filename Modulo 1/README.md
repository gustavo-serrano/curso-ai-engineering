# Orquestador concurrente de modelos de IA

## Curso AI Engineering - Coderhouse

**Módulo 1 — La interfaz base: conexión y abstracción de LLMs**

## Descripción

Este proyecto simula un backend que consulta múltiples modelos de inteligencia artificial mediante una arquitectura asíncrona en Python.

El objetivo es implementar concurrencia, resiliencia y control de flujo utilizando la biblioteca estándar asyncio.

## Tecnologías utilizadas

- Python 3.12.3
- asyncio
- logging
- Visual Studio Code
- Git y GitHub

## Funcionalidades

### 1. Concurrencia

Simulación de llamadas a tres modelos de inteligencia artificial:

- GPT-4: latencia de 1 segundo.
- Claude 3: latencia de 1,5 segundos.
- Llama: latencia de 3 segundos.

Las consultas se ejecutan concurrentemente mediante `asyncio.gather()`.

### 2. Resiliencia

Implementación de un tiempo límite de 2 segundos mediante `asyncio.timeout()`.

Se captura la excepción `TimeoutError`, permitiendo que el programa continúe su ejecución.

### 3. Control de flujo

Implementación de `asyncio.Semaphore(2)` para limitar a dos la cantidad de llamadas concurrentes sobre un total de diez solicitudes simuladas.

## Requisitos

- Python 3.12 o superior.
- No requiere dependencias externas.
- No requiere claves de API.

## Ejecución

```bash
python main.py
```

## Resultados obtenidos

| Prueba | Tiempo aproximado | Resultado |
|---|---|---|
| Concurrencia | 3 segundos | Correcto |
| Timeout | 2 segundos | Excepción controlada |
| Semáforo | 5 segundos | Correcto |

## Conceptos aplicados

- Programación asíncrona.
- Corrutinas.
- Event Loop.
- Concurrencia.
- Manejo de excepciones.
- Timeouts.
- Semáforos.
- Logging.

## Contexto académico

Ejercicio práctico desarrollado durante el módulo 1 del curso AI Engineering de Coderhouse.

Las llamadas a los modelos son simuladas y no realizan conexiones reales a servicios externos.