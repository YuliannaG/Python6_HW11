"""Парсер команд. Часть которая отвечает за разбор введенных пользователем строк,
выделение из строки ключевых слов и модификаторов команд."""


def normalize(raw_user_input: str) -> dict:
    user_input = raw_user_input.lower().strip()
    user_command: dict = {'command': None, 'name': None, 'phone': [], 'birthday': None}

    if user_input in ['hello', 'show all', 'good buy', 'close', 'exit']:
        user_command['command'] = user_input
    else:
        user_input_list = user_input.split()
        user_command['command'] = user_input_list[0]
        user_command['name'] = user_input_list[1]
        if len(user_input_list) > 2:
            if "/" in user_input_list[2]:
                user_command['birthday'] = user_input_list[2]
            else:
                user_command['phone'].append(user_input_list[2])
        if len(user_input_list) > 3:
            user_command['phone'].append(user_input_list[3])

    return user_command


if __name__ == '__main__':
    ...
