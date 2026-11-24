
import asyncio
import logging


# ==========================================
# CONFIGURACIÓN DE LOGS
# ==========================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d | %(message)s",
    datefmt="%H:%M:%S"
)


# ==========================================
# 1. SIMULACIÓN DE MODELOS DE IA
# ==========================================

async def gpt_4_call():
    logging.info("GPT-4: iniciando consulta")
    await asyncio.sleep(1)
    logging.info("GPT-4: consulta finalizada")
    return "Respuesta de GPT-4"


async def claude_3_call():
    logging.info("Claude 3: iniciando consulta")
    await asyncio.sleep(1.5)
    logging.info("Claude 3: consulta finalizada")
    return "Respuesta de Claude 3"


async def local_llama_call():
    logging.info("Llama: iniciando consulta")
    await asyncio.sleep(3)
    logging.info("Llama: consulta finalizada")
    return "Respuesta de Llama"


# ==========================================
# 2. ORQUESTACIÓN CON GATHER
# ==========================================

async def prueba_concurrencia():

    logging.info("=== PRUEBA 1: CONCURRENCIA ===")

    resultados = await asyncio.gather(
        gpt_4_call(),
        claude_3_call(),
        local_llama_call()
    )

    logging.info(f"Resultados: {resultados}")


# ==========================================
# 3. RESILIENCIA CON TIMEOUT
# ==========================================

async def prueba_timeout():

    logging.info("=== PRUEBA 2: TIMEOUT ===")

    try:
        async with asyncio.timeout(2):

            resultados = await asyncio.gather(
                gpt_4_call(),
                claude_3_call(),
                local_llama_call()
            )

            logging.info(f"Resultados: {resultados}")

    except TimeoutError:
        logging.error(
            "Se superó el tiempo límite de 2 segundos"
        )

    logging.info("El programa continúa normalmente")


# ==========================================
# 4. CONTROL DE FLUJO CON SEMÁFORO
# ==========================================

async def llamada_controlada(numero, semaforo):

    async with semaforo:

        logging.info(f"Llamada {numero}: iniciada")

        await asyncio.sleep(1)

        logging.info(f"Llamada {numero}: finalizada")

        return f"Respuesta {numero}"


async def prueba_semaforo():

    logging.info("=== PRUEBA 3: SEMÁFORO ===")

    semaforo = asyncio.Semaphore(2)

    resultados = await asyncio.gather(
        *(
            llamada_controlada(numero, semaforo)
            for numero in range(1, 11)
        )
    )

    logging.info(f"Resultados: {resultados}")


# ==========================================
# 5. FUNCIÓN PRINCIPAL
# ==========================================

async def main():

    await prueba_concurrencia()

    await prueba_timeout()

    await prueba_semaforo()

    logging.info("Orquestador finalizado correctamente")


# ==========================================
# PUNTO DE ENTRADA
# ==========================================

if __name__ == "__main__":
    asyncio.run(main())
