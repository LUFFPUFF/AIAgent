from core.provider import ILLMProvider
from schemas.chat import ChatContext
from core.tools import ToolRegistry
from utils.logger import ConsoleLogger, ProgressSpinner

class AgentOrchestrator:
    def __init__(self, provider: ILLMProvider, registry: ToolRegistry, model: str):
        self.provider = provider
        self.registry = registry
        self.model = model
        self.logger = ConsoleLogger()
        self.max_iterations = 5

    def process_request(self, context: ChatContext):
        """Основной цикл (Chain of Thought). Агент может вызывать инструменты несколько раз подряд."""
        iteration = 0

        while iteration < self.max_iterations:
            iteration += 1

            with ProgressSpinner("Agent is thinking"):
                content, tool_calls = self.provider.chat_with_tools(
                    model=self.model,
                    messages=context.messages,
                    tools=self.registry.get_schemas()
                )

            if tool_calls:
                context.add_message("assistant", content, tool_calls=tool_calls)

                for call in tool_calls:
                    result = self.registry.call(call.name, call.arguments)
                    context.add_message("tool", result)

                self.logger.info("Агент обрабатывает полученные данные...")
                continue

            else:
                context.add_message("assistant", content)
                self.logger.print_agent_header()
                self.logger.print_chunk(content + "\n")
                break

        if iteration == self.max_iterations:
            self.logger.info("Достигнут лимит раздумий агента.")