import sys

def calculate(num1, operator, num2):
    try:
        # Проверка, что переданы 4 аргумента (имя скрипта + 3 значения)
        if len(sys.argv) != 4:
            print("Использование: python calc.py <число1> <оператор> <число2>")
            sys.exit(1)

        # Парсинг аргументов
        try:
            n1 = float(sys.argv[1])
            op = sys.argv[2]
            n2 = float(sys.argv[3])
        except ValueError:
            print("Ошибка: Первые и третье значения должны быть числами.")
            sys.exit(1)

        result = None
        if op == '+':
            result = n1 + n2
        elif op == '-':
            result = n1 - n2
        elif op == '*':
            result = n1 * n2
        else:
            print("Ошибка: Недопустимый оператор. Используйте '+', '-', или '*'.")
            sys.exit(1)

        print(f"Результат: {result}")

    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    calculate(None, None, None)