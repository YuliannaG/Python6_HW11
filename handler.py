"""Функции обработчики команд -- набор функций, которые ещё называют handler,
они отвечают за непосредственное выполнение команд."""
from collections import UserDict



class Field():
    ...


class Name(Field):

    def __init__(self, name: str):
        self.name = name


    def __repr__(self):
        return f'{self.name}'


class Phone(Field):
    def __init__(self, phone: str):
        self.phone = phone


    def __repr__(self):
        return f'{self.phone}'


class Record(UserDict):

    def __init__(self, name: Name, phone: Phone = None):
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)

    def __repr__(self):
        return f'{self.name.name}: {[p.phone for p in self.phones]}'

    def add_phone(self, phone: Phone):
        if phone.phone not in [p.phone for p in self.phones]:
            self.phones.append(phone)
            return phone

    def delete_phone(self, phone: Phone):
        for p in self.phones:
            if p.phone == phone.phone:
                self.phones.remove(p)
                return phone

    def change_phone(self, phone: Phone, new_phone: Phone):
        if self.delete_phone(phone):
            self.add_phone(new_phone)
            return phone, new_phone


class AddressBook(UserDict):

    # def __init__(self):
    #     self.data = {}

    def add_record(self, record: Record):
        self.data[record.name.name] = record


contacts_dict = AddressBook()


def func_hello(*args):
    return "How can I help you?"


def add_contact(name, phone, *args):
    name_a = Name(name)
    phone_a = Phone(phone)
    record_new = Record(name_a, phone_a)
    record_lookup = contacts_dict.get(name)
    if isinstance(record_lookup, Record):
        record_lookup.add_phone(Phone(phone))
        return f'New contact added for {name.capitalize()}'
    contacts_dict.add_record(record_new)
    return f'Contact {name.capitalize()} added'

def change_contact(name, phone, new_phone):
    record = contacts_dict.get(name)
    print(record)
    print(record.phones)
    print(contacts_dict[name].phones)
    if isinstance(record, Record):
        for p in record.phones:
            if str(p) == phone:
                record.change_phone(Phone(phone), Phone(new_phone))
                return f'Contact {name.capitalize()} changed number {phone} to number {new_phone}'
        return f'Contact {name.capitalize()} has no number {phone} on file. Number was not changed.'
    return f'Sorry, phone book has no entry with name {name}'


def phone_contact(name, *args):
    return f"{name.capitalize()}'s numbers are {contacts_dict[name].phones}"


def show_all(*args):
    # for k,v in contacts_dict.items():
    #     return '{:^10}{:^10}'.format(k, v)
    return contacts_dict


def func_exit(*args):
    return 'Good bye!'


if __name__ == '__main__':
    name = 'maria'
    phone = '44'
    add_contact(name,phone)
    name = 'maria'
    phone = '44'
    new_phone = '88'
    change_contact(name, phone, new_phone)



