import os


def replace_in_file(path: str, target_snippet: str, new_snippet: str) -> str:
    """
    Находит точный фрагмент кода в файле и заменяет его на новый.
    Идеально для изменения нескольких строк без перезаписи всего файла.
    """
    try:
        if not os.path.exists(path):
            return f"Ошибка: Файл {path} не найден."

        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        if target_snippet not in content:
            return (
                f"Ошибка: Искомый фрагмент не найден в {path}.\n"
                "Подсказка: Убедись, что отступы, переносы строк и символы "
                "в target_snippet совпадают с оригиналом на 100%."
            )

        new_content = content.replace(target_snippet, new_snippet, 1)

        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return f"Успех: Блок кода в файле {path} успешно обновлен."

    except Exception as e:
        return f"Ошибка при редактировании {path}: {str(e)}"


REPLACE_FILE_SCHEMA = {
    'type': 'function',
    'function': {
        'name': 'replace_in_file',
        'description': 'Заменить конкретный блок кода в файле. ВСЕГДА используй это вместо write_file для изменения существующих файлов, чтобы не переписывать файл целиком.',
        'parameters': {
            'type': 'object',
            'properties': {
                'path': {
                    'type': 'string',
                    'description': 'Путь к файлу'
                },
                'target_snippet': {
                    'type': 'string',
                    'description': 'Точный кусок существующего кода, который нужно заменить (включая отступы)'
                },
                'new_snippet': {
                    'type': 'string',
                    'description': 'Новый код, который будет вставлен на это место'
                }
            },
            'required': ['path', 'target_snippet', 'new_snippet'],
        },
    },
}