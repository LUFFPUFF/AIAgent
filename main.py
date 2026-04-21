from config.prompts import SYSTEM_PROMPT_TEMPLATE
from core.provider import OllamaProvider
from schemas.chat import ChatContext
from tools.editor import replace_in_file, REPLACE_FILE_SCHEMA
from utils.logger import ConsoleLogger
from core.tools import ToolRegistry
from tools.file_system import list_directory, LIST_DIR_SCHEMA, read_file, READ_FILE_SCHEMA, write_file, \
    WRITE_FILE_SCHEMA
from tools.terminal import execute_command, EXECUTE_CMD_SCHEMA
from core.orchestrator import AgentOrchestrator
from utils.scanner import ProjectScanner

from tools.git_agent import (
    git_status, GIT_STATUS_SCHEMA,
    git_init_or_clone, GIT_INIT_SCHEMA,
    git_commit_all, GIT_COMMIT_SCHEMA
)


def main():
    provider = OllamaProvider()
    logger = ConsoleLogger()
    context = ChatContext()

    registry = ToolRegistry()
    registry.register(list_directory, LIST_DIR_SCHEMA)
    registry.register(read_file, READ_FILE_SCHEMA)
    registry.register(write_file, WRITE_FILE_SCHEMA)
    registry.register(execute_command, EXECUTE_CMD_SCHEMA)
    registry.register(replace_in_file, REPLACE_FILE_SCHEMA)
    registry.register(git_status, GIT_STATUS_SCHEMA)
    registry.register(git_init_or_clone, GIT_INIT_SCHEMA)
    registry.register(git_commit_all, GIT_COMMIT_SCHEMA)

    models = provider.list_models()
    if not models:
        return
    selected_model = "gemma4:latest" if "gemma4:latest" in models else models[0]

    logger.info("Сканирование проекта...")
    scanner = ProjectScanner(root_dir=".")
    project_tree = scanner.get_project_tree()

    formatted_prompt = SYSTEM_PROMPT_TEMPLATE.format(project_tree=project_tree)
    context.add_message("system", formatted_prompt)

    orchestrator = AgentOrchestrator(provider, registry, selected_model)

    logger.success(f"Агент-разработчик запущен (Модель: {selected_model}).")
    print("-" * 50)

    while True:
        try:
            user_input = input("\033[92m> \033[0m")
            if user_input.lower() in ['exit', 'quit']:
                break
            if not user_input.strip():
                continue

            context.add_message("user", user_input)
            orchestrator.process_request(context)

        except KeyboardInterrupt:
            print("\n")
            break


if __name__ == "__main__":
    main()