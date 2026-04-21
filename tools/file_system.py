import os


def list_directory(path: str = ".") -> str:
    """Возвращает список файлов и папок в указанной директории."""
    try:
        if not os.path.exists(path):
            return f"Директория {path} не существует."

        items = os.listdir(path)
        if not items:
            return f"Директория {path} пуста."

        return "\n".join(f"- {item}" for item in items)
    except Exception as e:
        return f"Ошибка доступа к {path}: {str(e)}"


def read_file(path: str) -> str:
    """Читает содержимое файла."""
    try:
        if not os.path.exists(path):
            return f"Ошибка: Файл {path} не найден."
        if not os.path.isfile(path):
            return f"Ошибка: {path} не является файлом."

        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            return f"Содержимое файла {path}:\n```\n{content}\n```"
    except Exception as e:
        return f"Ошибка при чтении {path}: {str(e)}"

def write_file(path: str, content: str) -> str:
    """Создает или перезаписывает файл."""
    try:
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Успешно: файл {path} создан/перезаписан."
    except Exception as e:
        return f"Ошибка при записи {path}: {str(e)}"

LIST_DIR_SCHEMA = {
    'type': 'function',
    'function': {
        'name': 'list_directory',
        'description': 'Посмотреть список файлов и папок в директории.',
        'parameters': {
            'type': 'object',
            'properties': {
                'path': {
                    'type': 'string',
                    'description': 'Путь к директории (например: ".", "./src")'
                }
            },
            'required': ['path'],
        },
    },
}

READ_FILE_SCHEMA = {
    'type': 'function',
    'function': {
        'name': 'read_file',
        'description': 'Прочитать содержимое конкретного файла. Используй это, чтобы анализировать код.',
        'parameters': {
            'type': 'object',
            'properties': {
                'path': {
                    'type': 'string',
                    'description': 'Путь к файлу (например: "src/main.py")'
                }
            },
            'required': ['path'],
        },
    },
}

WRITE_FILE_SCHEMA = {
    'type': 'function',
    'function': {
        'name': 'write_file',
        'description': 'Создать или перезаписать файл. Используй для написания кода.',
        'parameters': {
            'type': 'object',
            'properties': {
                'path': {'type': 'string', 'description': 'Путь к файлу (например: "workspace/app.py")'},
                'content': {'type': 'string', 'description': 'Полный исходный код или текст для записи'}
            },
            'required': ['path', 'content'],
        },
    },
}