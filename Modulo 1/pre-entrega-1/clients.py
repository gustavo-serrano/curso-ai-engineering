from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
import os
import openai
import anthropic
import httpx
from schemas import ChatMessage, ModelConfig


class LLMError(Exception):
    """Error controlado de configuración o del proveedor."""


class BaseLLMClient(ABC):
    def __init__(self, config: ModelConfig):
        self.config = config

    @abstractmethod
    async def generate(self, messages: list[ChatMessage]) -> str:
        ...

    @abstractmethod
    def stream(self, messages: list[ChatMessage]) -> AsyncIterator[str]:
        ...

    async def close(self):
        await self.client.close()


class OpenAIClient(BaseLLMClient):
    def __init__(self, config):
        super().__init__(config)
        key = os.getenv('OPENAI_API_KEY')
        if not key:
            raise LLMError('Falta OPENAI_API_KEY')
        self.client = openai.AsyncOpenAI(api_key=key, timeout=config.timeout, max_retries=2)

    def _params(self, messages):
        return dict(model=self.config.model,
                    messages=[m.model_dump() for m in messages],
                    temperature=self.config.temperature,
                    max_completion_tokens=self.config.max_tokens)

    async def generate(self, messages):
        response = await self.client.chat.completions.create(**self._params(messages))
        return response.choices[0].message.content or ''

    async def stream(self, messages):
        response = await self.client.chat.completions.create(**self._params(messages), stream=True)
        async with response:
            async for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content


class AnthropicClient(BaseLLMClient):
    def __init__(self, config):
        super().__init__(config)
        if config.temperature > 1:
            raise LLMError('Anthropic admite temperatura entre 0 y 1')
        key = os.getenv('ANTHROPIC_API_KEY')
        if not key:
            raise LLMError('Falta ANTHROPIC_API_KEY')
        self.client = anthropic.AsyncAnthropic(api_key=key, timeout=config.timeout, max_retries=2)

    def _params(self, messages):
        # Anthropic recibe las instrucciones system por separado.
        system = '\n'.join(m.content for m in messages if m.role == 'system')
        chat = [m.model_dump() for m in messages if m.role != 'system']
        return dict(model=self.config.model, messages=chat, system=system,
                    temperature=self.config.temperature, max_tokens=self.config.max_tokens)

    async def generate(self, messages):
        response = await self.client.messages.create(**self._params(messages))
        return ''.join(block.text for block in response.content if block.type == 'text')

    async def stream(self, messages):
        async with self.client.messages.stream(**self._params(messages)) as stream:
            async for text in stream.text_stream:
                yield text


def describe_error(exc: Exception) -> str:
    if isinstance(exc, (openai.AuthenticationError, anthropic.AuthenticationError)):
        return 'API key inválida o no autorizada.'
    if isinstance(exc, (openai.RateLimitError, anthropic.RateLimitError)):
        return 'Límite de peticiones o cuota alcanzado.'
    if isinstance(exc, (TimeoutError, openai.APITimeoutError, anthropic.APITimeoutError, httpx.TimeoutException)):
        return 'Tiempo de espera agotado.'
    if isinstance(exc, (openai.APIConnectionError, anthropic.APIConnectionError, httpx.TransportError)):
        return 'Error de conexión con el proveedor.'
    if isinstance(exc, (openai.APIError, anthropic.APIError)):
        return 'El proveedor rechazó la solicitud o presentó un error.'
    return str(exc)


CONTROLLED_ERRORS = (LLMError, TimeoutError, openai.APIError, anthropic.APIError, httpx.TransportError)
