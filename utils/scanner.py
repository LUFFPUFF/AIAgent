import os

class ProjectScanner:
    def __init__(self, root_dir: str = "."):
        self.root_dir = root_dir
        self.ignore_dirs = {'.venv', '__pycache__', '.git', '.idea', 'node_modules', 'test_folder'}

    def get_project_tree(self) -> str:
        """Создает текстовое дерево файлов проекта."""
        tree_str = "Структура проекта:\n"

        for root, dirs, files in os.walk(self.root_dir):
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs]

            level = root.replace(self.root_dir, '').count(os.sep)
            indent = ' ' * 4 * (level)

            basename = os.path.basename(root)
            if basename and basename != ".":
                tree_str += f"{indent}📁 {basename}/\n"

            subindent = ' ' * 4 * (level + 1)
            for f in files:
                tree_str += f"{subindent}📄 {f}\n"

        return tree_str