import asyncio
import os
from contextlib import aclosing
from dotenv import load_dotenv
from pydantic import ValidationError
from schemas import ChatMessage, ModelConfig
from manager import AsyncLLMManager
from clients import LLMError, CONTROLLED_ERRORS, describe_error


async def main():
    load_dotenv()
    try:
        provider = os.getenv('LLM_PROVIDER', 'openai')
        model = os.getenv('OPENAI_MODEL' if provider == 'openai' else 'ANTHROPIC_MODEL', '')
        config = ModelConfig(provider=provider, model=model,
                             temperature=os.getenv('LLM_TEMPERATURE', '0.5'),
                             max_tokens=os.getenv('LLM_MAX_TOKENS', '256'),
                             timeout=os.getenv('LLM_TIMEOUT', '30'))
        messages = [ChatMessage(role='system', content='Responde brevemente en español.'),
                    ChatMessage(role='user', content='¿Qué es la entropía?')]
        async with AsyncLLMManager(config) as manager:
            print(f'Proveedor: {config.provider} | Modelo: {config.model}')
            print('\n--- GENERACIÓN NORMAL ---')
            response = await manager.generate(messages)
            print(response.content if response.error is None else f'Error: {response.error}')
            print('\n--- STREAMING ---')
            try:
                async with aclosing(manager.stream(messages)) as chunks:
                    async for chunk in chunks:
                        print(chunk, end='', flush=True)
            except LLMError as exc:
                print(f'\nError de streaming: {exc}')
            print('\nFin de la prueba.')
    except (*CONTROLLED_ERRORS, ValidationError) as exc:
        print(f'Error controlado: {describe_error(exc)}')


if __name__ == '__main__':
    asyncio.run(main())
