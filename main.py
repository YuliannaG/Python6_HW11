"""Цикл запрос-ответ. Эта часть приложения отвечает за получения от пользователя данных
и возврат пользователю ответа от функции-handlerа."""
from parser import normalize
from handler import *


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            print('Please, enter command, name and phone number')
    return inner


COMMANDS = {func_hello: 'hello', show_all: 'show all', add_contact: 'add', change_contact: 'change',
            phone_contact: 'phone', func_exit: ['good buy', 'close', 'exit']}


@input_error
def output_func(user_command):
    command = user_command['command']
    name_command = user_command['name']
    phone_command = user_command['phone']
    for k, v in COMMANDS.items():
        if command in v:
            return k(name_command, *phone_command)


def main():
    while True:
        user_input = input('>>>')
        user_command = normalize(user_input)
        result = output_func(user_command)
        print(result)
        if result == 'Good bye!':
            break


if __name__ == '__main__':
    main()
