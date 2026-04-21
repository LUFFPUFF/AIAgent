from typing import Dict, Any, Callable, List
from utils.logger import ConsoleLogger

class ToolRegistry:
    def __init__(self):
        self._functions: Dict[str, Callable] = {}
        self._schemas: List[Dict[str, Any]] = []
        self.logger = ConsoleLogger()

    def register(self, func: Callable, schema: Dict[str, Any]):
        """Регистрирует функцию и ее JSON-схему для Ollama."""
        name = schema['function']['name']
        self._functions[name] = func
        self._schemas.append(schema)
        self.logger.info(f"Инструмент '{name}' зарегистрирован.")

    def get_schemas(self) -> List[Dict[str, Any]]:
        return self._schemas

    def call(self, name: str, arguments: Dict[str, Any]) -> str:
        """Выполняет функцию по имени и возвращает результат в виде строки."""
        if name not in self._functions:
            return f"Ошибка: Инструмент {name} не найден."

        try:
            self.logger.info(f"Агент вызывает инструмент: {name}({arguments})")
            result = self._functions[name](**arguments)
            return str(result)
        except Exception as e:
            return f"Ошибка при выполнении {name}: {str(e)}"