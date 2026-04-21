import subprocess


def execute_command(command: str) -> str:
    """Выполняет bash/cmd команду, предварительно спросив разрешения у пользователя."""

    print(f"\n\033[41m\033[97m [ОПАСНОСТЬ] \033[0m Агент хочет выполнить команду терминала:")
    print(f"\033[93m> {command}\033[0m")

    while True:
        choice = input("\033[96mРазрешить выполнение? (y - да / n - нет): \033[0m").strip().lower()
        if choice in ['y', 'yes', 'д', 'да']:
            print("\033[90m[Выполняю...]\033[0m")
            break
        elif choice in ['n', 'no', 'н', 'нет']:
            return "Системное сообщение: Пользователь ЗАПРЕТИЛ выполнение этой команды. Придумай другой способ или сообщи пользователю, что не можешь продолжить."
        else:
            print("Пожалуйста, введите 'y' или 'n'.")

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=15
        )

        output = ""
        if result.stdout:
            output += f"STDOUT:\n{result.stdout}\n"
        if result.stderr:
            output += f"STDERR:\n{result.stderr}\n"

        if result.returncode == 0:
            return output if output else "Команда выполнена успешно (без вывода)."
        else:
            return f"Команда завершилась с ошибкой (код {result.returncode}).\n{output}"

    except subprocess.TimeoutExpired:
        return "Ошибка: Превышен таймаут выполнения (15 секунд)."
    except Exception as e:
        return f"Критическая ошибка выполнения: {str(e)}"


EXECUTE_CMD_SCHEMA = {
    'type': 'function',
    'function': {
        'name': 'execute_command',
        'description': 'Выполнить команду в системном терминале. ВАЖНО: выполнение будет приостановлено до получения согласия от пользователя.',
        'parameters': {
            'type': 'object',
            'properties': {
                'command': {
                    'type': 'string',
                    'description': 'Команда для выполнения (например: "python test.py")'
                }
            },
            'required': ['command'],
        },
    },
}