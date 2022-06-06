"""Функции обработчики команд -- набор функций, которые ещё называют handler,
они отвечают за непосредственное выполнение команд."""
from collections import UserDict, defaultdict
from datetime import datetime, timedelta
import re

class Field():
   ...

class Name(Field):
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f'{self.name}'

    # def __init__(self, name: str):
    #     self.__name = name
    #
    # def __repr__(self):
    #     return f'{self.__name}'
    #
    # @property
    # def value(self):
    #     return self.__name
    #
    # @value.setter
    # def value(self, name):
    #     if re.match (r"[a-z,A-Z]*", name):
    #         self.__name = name
    #     else:
    #         raise ValueError('Name format is incorrect.')

class Phone(Field):

    def __init__(self, phone: str = None):
        self.phone = phone

    def __repr__(self):
        return f'{self.phone}'

    # def __init__(self, phone: str = None):
    #     self.__phone = phone
    #
    # def __repr__(self):
    #     return f'{self.__phone}'
    #
    # @property
    # def value(self):
    #     return self.__phone
    #
    # @value.setter
    # def value(self, phone):
    #     if re.match (r"^[\+]\d{11}\d?", phone):
    #         self.__phone = phone
    #     else:
    #         raise ValueError('Phone format is incorrect.')


class Birthday(Field):

    def __init__(self, birthday: str = None):
        try:
            birthday = datetime.strptime(birthday, "%Y/%m/%d").date()
            self.birthday = birthday
        except TypeError or ValueError:
            self.birthday = birthday

    def __repr__(self):
        return f'{self.birthday}'

    # def __init__(self, birthday: str = None):
    #     try:
    #         self.__birthday = datetime.strptime(birthday, "%d/%m/%Y")
    #         return self.__birthday
    #     except TypeError or ValueError:
    #         self.__birthday = birthday
    #
    # def __repr__(self):
    #     return f'{self.__birthday}'
    #
    # @property
    # def value(self):
    #     return self.__birthday
    #
    # @value.setter
    # def value(self, birthday):
    #     if re.match (r"^[0-1]\d/[0-1]\d/[1|2][0|9]\d\d", birthday):
    #         self.__birthday = birthday
    #     else:
    #         raise ValueError('Birthday format is incorrect. please enter dd/mm/yyyy')

class Record(UserDict):

    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None):
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)
        if birthday:
            self.birthday = birthday
        else:
            self.birthday = ""


    def __repr__(self):
        return f'{self.name.name}: {[p.phone for p in self.phones]}, DOB {self.birthday}'

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

    def add_birthday(self, birthday: Birthday):
        if birthday:
            self.birthday = birthday

    def days_to_birthday(self):
        delta1 = datetime(datetime.now().year, self.birthday.birthday.month, self.birthday.birthday.day)
        delta2 = datetime(datetime.now().year + 1, self.birthday.birthday.month, self.birthday.birthday.day)
        result = ((delta1 if delta1 > datetime.now() else delta2) - datetime.now()).days
        return f'Birthday is in {result} days.'



class AddressBook(UserDict):

    def add_record(self, record: Record):
        self.data[record.name.name] = record

    # AddressBook реализует метод iterator, которые возвращает генератор
    # по записям AddressBook и за одну итерацию возвращает представление
    # для N записей.
    def iterator(self):
        ...

contacts_dict = AddressBook()


def func_hello(*args, **kwargs):
    return "How can I help you?"


def add_contact(name, phone = None, birthday = None):
    name_a = Name(name)
    phone_a = Phone(phone[0] if phone else None)
    birthday_a = Birthday(birthday)
    record_new = Record(name_a, phone_a, birthday_a)
    record_lookup = contacts_dict.get(name)
    if isinstance(record_lookup, Record):
        if phone:
            record_lookup.add_phone(Phone(phone[0]))
            return f'New phone number added for {name.capitalize()}'
        if birthday:
            record_lookup.add_birthday(Birthday(birthday))
            return f'Birthday information updated for {name.capitalize()}'
    contacts_dict.add_record(record_new)
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
        if record_lookup.birthday.birthday is None:
            return "No birthday data available"
        else:
            result_bd = record_lookup.days_to_birthday()
            return f"{name.capitalize()}'s birthday is {contacts_dict[name].birthday}. {result_bd}"
    return "No personal record available"
def show_all(*args, **kwargs):
    # for k,v in contacts_dict.items():
    #     return '{:^10}{:^10}'.format(k, v)
    return contacts_dict


def func_exit(*args, **kwargs):
    return 'Good bye!'


if __name__ == '__main__':
    contacts_dict = {}
    name = 'maria'
    phone = '44'
    date = '1987/12/12'
    date_norm = datetime.strptime(date, "%Y/%m/%d")
    print(date_norm)
    # print(add_contact(name,phone))
    # print(contacts_dict)
    print(add_contact(name, date))
    print(contacts_dict)
    # name = 'maria'
    # phone = '44'
    # new_phone = '88'
    # change_contact(name, phone, new_phone)
    # print(datetime.strptime("2011/12/10", "%Y/%m/%d"))
    # birthday = Birthday('2011/12/10')
    # record = Record(name, phone, birthday)
    # result = record.days_to_birthday()
    # print(result)
    # record_no = Record(name, phone)
    # print(record_no.days_to_birthday())


