import subprocess
import os


def _run_git(command: str) -> str:
    """Внутренняя утилита для безопасного выполнения git-команд (без запроса пользователя)."""
    try:
        result = subprocess.run(
            f"git {command}",
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return result.stdout.strip() if result.stdout else "Успешно."
        return f"Git ошибка: {result.stderr.strip()}"
    except Exception as e:
        return f"Критическая ошибка Git: {e}"


def git_status() -> str:
    """Возвращает текущий статус репозитория (измененные файлы, ветка)."""
    if not os.path.exists(".git"):
        return "Ошибка: Это не git-репозиторий. Сначала нужно выполнить 'git init' или добавить URL."
    return _run_git("status -s")


def git_init_or_clone(url: str = None) -> str:
    """Инициализирует новый репозиторий или клонирует существующий."""
    if os.path.exists(".git"):
        return "Git уже инициализирован в этой директории."

    if url and url.strip():
        return _run_git(f"clone {url} .")
    else:
        return _run_git("init")


def git_commit_all(message: str) -> str:
    """Добавляет все измененные файлы и делает коммит с указанным сообщением."""
    if not os.path.exists(".git"):
        return "Ошибка: Не найден .git. Сначала инициализируй репозиторий."

    status = _run_git("status -s")
    if not status or "Git ошибка" in status:
        return "Нет изменений для коммита."

    add_result = _run_git("add .")
    if "Git ошибка" in add_result:
        return f"Ошибка при git add: {add_result}"

    safe_message = message.replace('"', '\\"')
    commit_result = _run_git(f'commit -m "{safe_message}"')

    return f"Коммит успешно создан:\n{commit_result}"

GIT_STATUS_SCHEMA = {
    'type': 'function',
    'function': {
        'name': 'git_status',
        'description': 'Посмотреть статус git (измененные файлы, не добавленные файлы). Используй это перед коммитом, чтобы понять, что изменилось.',
        'parameters': {'type': 'object', 'properties': {}},
    },
}

GIT_INIT_SCHEMA = {
    'type': 'function',
    'function': {
        'name': 'git_init_or_clone',
        'description': 'Инициализировать пустой git-репозиторий в текущей папке ИЛИ склонировать по URL.',
        'parameters': {
            'type': 'object',
            'properties': {
                'url': {'type': 'string', 'description': 'URL репозитория (оставь пустым для локального git init)'}
            }
        },
    },
}

GIT_COMMIT_SCHEMA = {
    'type': 'function',
    'function': {
        'name': 'git_commit_all',
        'description': 'Добавить ВСЕ измененные файлы (git add .) и создать коммит (git commit -m). ВСЕГДА сначала вызывай git_status, чтобы проанализировать изменения и написать хорошее сообщение.',
        'parameters': {
            'type': 'object',
            'properties': {
                'message': {'type': 'string', 'description': 'Осмысленное сообщение коммита (что было сделано)'}
            },
            'required': ['message'],
        },
    },
}