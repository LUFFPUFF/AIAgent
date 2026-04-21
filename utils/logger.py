import sys
import time
import threading
import itertools

class ConsoleLogger:
    @staticmethod
    def info(message: str):
        print(f"\033[94m[INFO]\033[0m {message}")

    @staticmethod
    def success(message: str):
        print(f"\033[92m[SUCCESS]\033[0m {message}")

    @staticmethod
    def print_agent_header():
        print(f"\033[93m[AGENT]:\033[0m ", end="", flush=True)

    @staticmethod
    def print_chunk(content: str):
        print(content, end="", flush=True)


class ProgressSpinner:
    def __init__(self, message="Thinking"):
        self.message = message
        self._stop_event = threading.Event()
        self._thread = None
        self.spinner_cycle = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])

    def _spin(self):
        while not self._stop_event.is_set():
            sys.stdout.write(f"\r\033[93m{next(self.spinner_cycle)}\033[0m {self.message}...")
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write('\r' + ' ' * (len(self.message) + 10) + '\r')
        sys.stdout.flush()

    def __enter__(self):
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._spin)
        self._thread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._stop_event.set()
        self._thread.join()