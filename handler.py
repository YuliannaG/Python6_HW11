"""Функции обработчики команд -- набор функций, которые ещё называют handler,
они отвечают за непосредственное выполнение команд."""
from collections import UserDict
from datetime import datetime
import re


class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):

    @Field.value.setter
    def value(self, name):
        if re.match (r"[a-zA-Z]+", name):
            self._value = name
        else:
            raise ValueError

    def __repr__(self):
        return f'{self._value}'


class Phone(Field):

    @Field.value.setter
    def value(self, phone):
        if re.match (r"^[\+]\d{11}\d?", phone):
            self._value = phone
        else:
            raise ValueError

    def __repr__(self):
        return f'{self._value}'


class Birthday(Field):

    @Field.value.setter
    def value(self, value):
        if value:
            try:
                birthday = datetime.strptime(value, "%Y/%m/%d").date()
                self._value = birthday
            except TypeError or ValueError:
                raise ValueError
        else:
            self._value = ""

    def __repr__(self):
        return f'{self._value}'


class Record(UserDict):

    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None):
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)
        self.birthday = birthday

    def __repr__(self):
        if self.birthday:
            return f'{self.name.value}: {[p.value for p in self.phones]}, DOB {self.birthday}'
        return f'{self.name.value}: {[p.value for p in self.phones]}'

    def add_phone(self, phone: Phone):
        if phone._value not in [p._value for p in self.phones]:
            self.phones.append(phone)
            return phone

    def delete_phone(self, phone: Phone):
        for p in self.phones:
            if p._value == phone._value:
                self.phones.remove(p)
                return phone

    def change_phone(self, phone: Phone, new_phone: Phone):
        if self.delete_phone(phone):
            self.add_phone(new_phone)
            return phone, new_phone

    def days_to_birthday(self):
        delta1 = datetime(datetime.now().year, self.birthday._value.month, self.birthday._value.day)
        delta2 = datetime(datetime.now().year + 1, self.birthday._value.month, self.birthday._value.day)
        result = ((delta1 if delta1 > datetime.now() else delta2) - datetime.now()).days
        return f'Birthday is in {result} days.'

i = 2

class AddressBook(UserDict):

    def iterator(self, num: int = 2):
        data = self.data
        items = list(data.items())
        for i in range(len(items) // num): #range is number of filled pages in the address book with num records on 1 page
            if i == (len(items) // num):
                _tmp = items[num * i:len(items)]
            _tmp = items[num * i: (num * i) + num]  #records on any one page
            yield _tmp

    def __repr__(self):
        return f'{self.data}'


contacts_dict = AddressBook()


def func_hello(*args, **kwargs):
    return "How can I help you?"


def add_contact(name, phone = None, birthday = None):
    name_a = Name(name)
    phone_a = Phone(phone[0]) if phone else None
    birthday_a = Birthday(birthday)
    record_new = Record(name_a, phone_a, birthday_a)
    record_lookup = contacts_dict.get(name)
    if isinstance(record_lookup, Record):
        if phone:
            record_lookup.add_phone(Phone(phone[0]))
            return f'New phone number added for {name.capitalize()}'
        if birthday:
            record_lookup.birthday = birthday
            return f'Birthday information updated for {name.capitalize()}'
    contacts_dict.data[record_new.name.value] = record_new
    return f'Information record for {name.capitalize()} added'


def change_contact(name, phone: list, *args, **kwargs):
    record = contacts_dict.get(name)
    if isinstance(record, Record):
        for p in record.phones:
            if str(p) == phone[0]:
                record.change_phone(Phone(phone[0]), Phone(phone[1]))
                return f'Contact {name.capitalize()} changed number {phone[0]} to number {phone[1]}'
        return f'Contact {name.capitalize()} has no number {phone[0]} on file. Number was not changed.'
    return f'Sorry, phone book has no entry with name {name}'


def phone_contact(name, *args, **kwargs):
    return f"{name.capitalize()}'s numbers are {contacts_dict[name].phones}"


def birthday_contact(name, *args, **kwargs):
    record_lookup = contacts_dict.get(name)
    if isinstance(record_lookup, Record):
        if record_lookup.birthday._value is None:
            return "No birthday data available"
        else:
            result_bd = record_lookup.days_to_birthday()
            return f"{name.capitalize()}'s birthday is {contacts_dict[name].birthday}. {result_bd}"
    return "No personal record available"


def show_all(*args, **kwargs):
    iter = contacts_dict.iterator(2)
    result = ""
    for i in iter:
        result += f'{i}\n'
    return result


def func_exit(*args, **kwargs):
    return 'Good bye!'


if __name__ == '__main__':
    ...
