#! /usr/bin/env python3
import asyncio

from my_app.performer import perform_operation


def main():
    identifier: str = input("Введите номер заявки: ")
    # Инициализация asyncio loop
    loop = asyncio.get_event_loop()
    # Запуск асинхронной операции

    result = loop.run_until_complete(perform_operation(str(identifier)))
    print(result)


if __name__ == "__main__":
    main()
