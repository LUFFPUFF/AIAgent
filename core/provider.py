import ollama
from abc import ABC, abstractmethod
from typing import Generator, List, Optional, Dict, Any, Tuple
from schemas.chat import Message, ToolCall


class ILLMProvider(ABC):
    @abstractmethod
    def generate_stream(self, model: str, messages: List[Message]) -> Generator[str, None, None]:
        pass

    @abstractmethod
    def list_models(self) -> List[str]:
        pass

    @abstractmethod
    def chat_with_tools(self, model: str, messages: List[Message], tools: List[Dict]) -> Tuple[str, List[ToolCall]]:
        """Отвечает целиком, так как Tool Calling в Ollama пока плохо работает со stream=True"""
        pass


class OllamaProvider(ILLMProvider):
    def __init__(self):
        self._client = ollama.Client(timeout=None)

    def list_models(self) -> List[str]:
        try:
            response = self._client.list()
            return [m.model for m in response.models]
        except:
            return []

    def generate_stream(self, model: str, messages: List[Message]) -> Generator[str, None, None]:
        formatted_messages = [{'role': m.role, 'content': m.content} for m in messages]

        try:
            stream = self._client.chat(
                model=model,
                messages=formatted_messages,
                stream=True
            )
            for chunk in stream:
                if 'message' in chunk and 'content' in chunk['message']:
                    yield chunk['message']['content']
        except Exception as e:
            yield f"\n[CRITICAL ERROR]: {e}"

    def chat_with_tools(self, model: str, messages: List[Message], tools: List[Dict]) -> Tuple[str, List[ToolCall]]:
        formatted_messages = []
        for m in messages:
            msg = {'role': m.role, 'content': m.content}
            if m.tool_calls:
                msg['tool_calls'] = [{'function': {'name': tc.name, 'arguments': tc.arguments}} for tc in m.tool_calls]
            formatted_messages.append(msg)

        response = self._client.chat(
            model=model,
            messages=formatted_messages,
            tools=tools,
            stream=False
        )

        msg = response['message']
        content = msg.get('content', '')

        tool_calls = []
        if 'tool_calls' in msg:
            for tc in msg['tool_calls']:
                tool_calls.append(ToolCall(
                    name=tc['function']['name'],
                    arguments=tc['function']['arguments']
                ))

        return content, tool_calls