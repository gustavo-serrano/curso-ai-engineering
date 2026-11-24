
# Pre-entrega 1 — Unified Async LLM Client

## Curso AI Engineering — Coderhouse

Módulo 1: La interfaz base — conexión y abstracción de LLMs.

## Descripción

Cliente unificado de modelos de inteligencia artificial para OpenAI y
Anthropic, desarrollado con Python 3.12+, programación asíncrona,
streaming y validación de datos mediante Pydantic.

El objetivo del proyecto es permitir el intercambio de proveedores
de inteligencia artificial bajo una interfaz común, sin modificar
la lógica principal de la aplicación.

## Funcionalidades

- Intercambiabilidad entre OpenAI y Anthropic.
- Programación asíncrona mediante async/await.
- Generación de respuestas completas.
- Streaming mediante generadores asíncronos.
- Validación de mensajes y configuración con Pydantic.
- Manejo controlado de excepciones.
- Gestión de errores de red y límites de cuota.
- Configuración de tiempos máximos de espera (timeouts).
- Gestión segura de credenciales mediante variables de entorno.
- Pruebas automatizadas de validación.

## Tecnologías utilizadas

- Python 3.12.3
- asyncio
- OpenAI SDK
- Anthropic SDK
- Pydantic
- python-dotenv
- httpx
- unittest
- Visual Studio Code
- Git y GitHub

## Estructura del proyecto

```text
pre-entrega-1/
├── schemas.py
├── clients.py
├── manager.py
├── main.py
├── test_schemas.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Instalación (Windows CMD)

Desde esta carpeta, con el entorno virtual del módulo activado:

```cmd
python -m pip install -r requirements.txt
copy .env.example .env
```

Si no existe un entorno virtual, crearlo mediante:

```cmd
python -m venv .venv
```

Activarlo:

```cmd
.venv\Scripts\activate.bat
```

## Configuración

Editar el archivo `.env` localmente.

Ejemplo de configuración:

```dotenv
LLM_PROVIDER=openai

OPENAI_API_KEY=
ANTHROPIC_API_KEY=

OPENAI_MODEL=gpt-4o-mini
ANTHROPIC_MODEL=

LLM_TEMPERATURE=0.5
LLM_MAX_TOKENS=256
LLM_TIMEOUT=30
```

Para utilizar OpenAI:

- Seleccionar `LLM_PROVIDER=openai`.
- Completar `OPENAI_API_KEY`.
- Configurar `OPENAI_MODEL`.

Para utilizar Anthropic:

- Seleccionar `LLM_PROVIDER=anthropic`.
- Completar `ANTHROPIC_API_KEY`.
- Configurar `ANTHROPIC_MODEL` con un modelo disponible en la cuenta.

Solo se necesita la clave del proveedor seleccionado.

La suscripción a ChatGPT y el consumo de la API tienen sistemas
de facturación independientes.

### Variables de entorno

| Variable | Responsabilidad |
|---|---|
| LLM_PROVIDER | Selecciona OpenAI o Anthropic. |
| OPENAI_API_KEY | Credencial privada de OpenAI. |
| ANTHROPIC_API_KEY | Credencial privada de Anthropic. |
| OPENAI_MODEL | Identificador del modelo de OpenAI. |
| ANTHROPIC_MODEL | Identificador del modelo de Anthropic. |
| LLM_TEMPERATURE | Temperatura entre 0 y 2. Anthropic limita a 1. El modelo seleccionado debe admitir este parámetro. |
| LLM_MAX_TOKENS | Límite positivo de tokens de salida. |
| LLM_TIMEOUT | Tiempo máximo de espera en segundos. |

## Ejecución

```cmd
python main.py
```

El programa realiza la pregunta:

"¿Qué es la entropía?"

La consulta se ejecuta en dos modalidades:

1. Generación normal: recibe la respuesta completa.
2. Streaming: recibe fragmentos de texto conforme llegan desde la API.

Las consultas son reales y están sujetas a la disponibilidad,
los permisos, las cuotas y los costos del proveedor seleccionado.

Para probar el segundo proveedor, modificar el archivo `.env`
y ejecutar nuevamente el programa.

## Arquitectura

### schemas.py

Define los modelos de datos mediante Pydantic:

- ChatMessage: estructura de los mensajes de entrada.
- ModelConfig: configuración y validación de parámetros del modelo.
- ModelResponse: estructura de las respuestas.

### clients.py

Implementa el contrato abstracto BaseLLMClient y los clientes:

- OpenAIClient.
- AnthropicClient.

Utiliza los SDK oficiales en sus versiones asíncronas:

- AsyncOpenAI.
- AsyncAnthropic.

Las instrucciones de tipo system se envían por separado a Anthropic.
Se admite conversación textual con al menos un mensaje user.

### manager.py

Implementa AsyncLLMManager, encargado de:

- Seleccionar el proveedor.
- Validar la configuración.
- Gestionar las consultas.
- Controlar los tiempos de espera.
- Manejar excepciones.
- Cerrar las conexiones.

### main.py

Script principal que permite comprobar el funcionamiento
del cliente en modo normal y streaming.

Utiliza un único asyncio.run() como punto de entrada.

### test_schemas.py

Contiene las pruebas automatizadas de validación de los
esquemas definidos con Pydantic.

## Manejo de errores y resiliencia

El método generate() retorna un ModelResponse con el contenido
generado o un error controlado.

El método stream() entrega fragmentos de texto mediante yield
y async for.

Si ocurre un error durante el streaming, se genera una excepción
LLMError que es capturada por el script principal, evitando
mezclar mensajes de error con el texto generado.

Un fallo durante el streaming puede dejar texto parcial
previamente mostrado.

Los SDK tienen configurados hasta dos reintentos para errores
transitorios compatibles, sujetos al plazo del manager.

No se reintenta manualmente un stream parcial.

La cancelación de una llamada local no garantiza que el proveedor
detenga inmediatamente el procesamiento remoto.

El timeout y los reintentos no constituyen un mecanismo
de limitación de peticiones por minuto.

## Pruebas automatizadas

Para ejecutar las pruebas locales:

```cmd
python -m unittest test_schemas -v
```

Estas pruebas no requieren API Keys, conexión a Internet
ni saldo disponible en los proveedores.

### Resultados obtenidos

```text
test_invalid_config ... ok
test_invalid_message ... ok
test_valid_config ... ok

Ran 3 tests in 0.001s

OK
```

| Prueba | Resultado |
|---|---|
| Validación de configuración inválida | Correcto |
| Validación de mensaje inválido | Correcto |
| Validación de configuración válida | Correcto |

Total: 3 pruebas superadas.

## Prueba de integración con OpenAI

Se ejecutó el programa utilizando una API Key de OpenAI
y el modelo gpt-4o-mini.

Resultado obtenido:

```text
Proveedor: openai | Modelo: gpt-4o-mini

--- GENERACIÓN NORMAL ---
Error: Límite de peticiones o cuota alcanzado.

--- STREAMING ---

Error de streaming: Límite de peticiones o cuota alcanzado.

Fin de la prueba.
```

La cuenta de API no dispone actualmente de créditos.

El programa gestionó correctamente el error de cuota tanto
en la generación normal como en el streaming, permitiendo
finalizar la ejecución sin interrupciones inesperadas.

## Estado de validación

| Funcionalidad | Estado |
|---|---|
| Entorno Python 3.12 | Verificado |
| Instalación de dependencias | Verificado |
| Importación de librerías | Verificado |
| Validación con Pydantic | Verificado |
| Selección del proveedor OpenAI | Verificado |
| Manejo de errores de cuota | Verificado |
| Continuidad del programa ante errores | Verificado |
| Cliente asíncrono de OpenAI | Implementado |
| Cliente asíncrono de Anthropic | Implementado |
| Streaming | Implementado |
| Manejo de errores de red | Implementado |
| Generación real de respuestas | Pendiente de validación |
| Streaming real de respuestas | Pendiente de validación |
| Integración real con Anthropic | Pendiente de validación |

La generación efectiva de respuestas y el streaming con OpenAI
no pudieron validarse debido a la falta de créditos disponibles.

La integración con Anthropic está implementada, pero no fue
probada con credenciales reales.

Para completar estas pruebas se requiere una API Key válida,
permisos adecuados y cuota disponible en el proveedor seleccionado.

## Seguridad

Las credenciales se almacenan mediante variables de entorno.

El archivo `.env` contiene información privada y no debe
publicarse en GitHub.

El archivo `.env.example` funciona como plantilla de configuración
y no contiene credenciales reales.

El archivo `.gitignore` excluye el entorno virtual, las credenciales
y los archivos temporales de Python.

## Conceptos de AI Engineering aplicados

| Concepto | Responsabilidad |
|---|---|
| Abstracción | Define una interfaz común entre proveedores. |
| Herencia | Permite implementar clientes especializados. |
| Polimorfismo | Permite intercambiar proveedores bajo un mismo contrato. |
| async/await | Permite ejecutar operaciones no bloqueantes. |
| Event Loop | Coordina las operaciones asíncronas. |
| Streaming | Entrega fragmentos de respuesta progresivamente. |
| yield | Produce resultados de manera incremental. |
| async for | Recorre iteradores asíncronos. |
| Pydantic | Valida los datos de entrada y configuración. |
| Timeout | Limita el tiempo de espera de una operación. |
| Retry | Reintenta operaciones ante errores transitorios. |
| Rate Limit | Restringe el consumo de la API por unidad de tiempo. |
| Manejo de excepciones | Evita interrupciones inesperadas del programa. |
| Variables de entorno | Separa la configuración y credenciales del código. |
| unittest | Permite realizar pruebas automatizadas. |

## Conclusión

El proyecto implementa una arquitectura unificada para la
integración de diferentes proveedores de inteligencia artificial,
aplicando principios de abstracción, asincronía, validación
de datos y resiliencia.

La implementación permite seleccionar el proveedor mediante
configuración, sin modificar la lógica principal de la aplicación.

Las pruebas locales y el manejo de errores de cuota fueron
verificados correctamente. Las pruebas de generación real quedan
sujetas a la disponibilidad de créditos y credenciales.

## Contexto académico

Pre-entrega 1 del curso AI Engineering de Coderhouse.

Módulo 1 — La interfaz base: conexión y abstracción de LLMs.
