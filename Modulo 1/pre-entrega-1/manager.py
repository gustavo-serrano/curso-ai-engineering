import asyncio
from collections.abc import AsyncIterator
from contextlib import aclosing
from pydantic import TypeAdapter, ValidationError
from schemas import ChatMessage, ModelConfig, ModelResponse
from clients import OpenAIClient, AnthropicClient, LLMError, CONTROLLED_ERRORS, describe_error


class AsyncLLMManager:
    def __init__(self, config: ModelConfig):
        self.config = config
        providers = {'openai': OpenAIClient, 'anthropic': AnthropicClient}
        self.client = providers[config.provider](config)

    def _validate(self, messages):
        validated = TypeAdapter(list[ChatMessage]).validate_python(messages)
        if not any(m.role == 'user' for m in validated):
            raise LLMError('Se requiere al menos un mensaje user.')
        return validated

    async def generate(self, messages: list[ChatMessage]) -> ModelResponse:
        try:
            async with asyncio.timeout(self.config.timeout):
                text = await self.client.generate(self._validate(messages))
            return ModelResponse(provider=self.config.provider, model=self.config.model, content=text)
        except (*CONTROLLED_ERRORS, ValidationError) as exc:
            return ModelResponse(provider=self.config.provider, model=self.config.model,
                                 error=describe_error(exc))

    async def stream(self, messages: list[ChatMessage]) -> AsyncIterator[str]:
        try:
            async with aclosing(self.client.stream(self._validate(messages))) as chunks:
                # Plazo total para esperar fragmentos, sin dejar un timeout activo durante yield.
                deadline = asyncio.get_running_loop().time() + self.config.timeout
                while True:
                    try:
                        async with asyncio.timeout_at(deadline):
                            chunk = await anext(chunks)
                    except StopAsyncIteration:
                        break
                    yield chunk
        except (*CONTROLLED_ERRORS, ValidationError) as exc:
            raise LLMError(describe_error(exc)) from exc

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.client.close()
