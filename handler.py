"""Функции обработчики команд -- набор функций, которые ещё называют handler,
они отвечают за непосредственное выполнение команд."""
from collections import UserDict, defaultdict
from datetime import datetime, timedelta
import re


class Field:
    def __init__(self, value):
        self._value = None # если у нас наследование и в дочерних классах предвидится минимум переопределений используем _ одинарное подчеркивание (протектед)
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):
    # Working option:
    # def __init__(self, name: str):
    #     self.name = name
    #
    # def __repr__(self):
    #     return f'{self.name}'

    # def __repr__(self):
    #     return f'{self.name}'


    # проверяет значение по регулярке но выводит в виде handler.Name object at 0X3782658723
    # def __init__(self, name: str):
    #     super().__init__(name)

    @Field.value.setter
    def value(self, name):
        if re.match (r"[a-zA-Z]+", name): # Было не корректное выражение
            self._value = name
            #Field.value.fset(self, name) # А что єто за конструкция????)))
        else:
            raise ValueError('Name format is incorrect.')


class Phone(Field):

    # def __init__(self, phone: str = None):
    #     self.phone = phone

    def __repr__(self):
        return f'{self._value}'


    # def __init__(self, phone: str):
    #     super().__init__(phone)
    #
    @Field.value.setter
    def value(self, phone):
        if re.match (r"^[\+]\d{11}\d?", phone):
            self._value = phone
            #Field.value.fset(self, phone)
        else:
            raise ValueError('Phone format is incorrect.')


class Birthday(Field):

    # def __init__(self, birthday: str): # в классе не должно быть поле None, если так, то класс не создаётся
    #     try:
    #         birthday = datetime.strptime(birthday, "%Y/%m/%d").date()
    #         self.birthday = birthday
    #     except TypeError or ValueError:
    #         return
    
    @Field.value.setter
    def value(self, value):
        try:
            birthday = datetime.strptime(value, "%Y/%m/%d").date()
            self._value = birthday
        except TypeError or ValueError:
            raise ValueError("Data mus be in 'YYYY/MM/DD' format.")

    def __repr__(self):
        return f'{self._value}'


    #  непонятно как в инициализацию ввести конвертацию в дату

    # def __init__(self, birthday: str = None):
    #     super().__init__(birthday)
    #
    # @Field.value.setter
    # def value(self, birthday):
    #     if re.match (r"^[0-1]\d/[0-1]\d/[1|2][0|9]\d\d", birthday):
    #         Field.value.fset(self, birthday)
    #     else:
    #         raise ValueError('Birthday format is incorrect. please enter yyyy/mm/dd')


class Record(UserDict):

    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None):
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)
        #if birthday: # можно без проверки, просто поле будет None
        self.birthday = birthday
        #else:
        #    self.birthday = ""

    def __repr__(self):
        if self.birthday:
            return f'{self.name.value}: {[p.value for p in self.phones]}, DOB {self.birthday}'
        return f'{self.name.value}: {[p.value for p in self.phones]}'

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
        self.data[record.name.value] = record

    def __iter__(self): # Должен быть не магический __iter__, а физический iterator(self, pages):
        data = self.data
        items = list(data.items())
        for i in range(len(items) // 2):
            _tmp = items[2 * i: 2 * (i + 1)]
            yield _tmp


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
    # выводит только первую пару:( единственную запись тоже не выводит
    while True:
        try:
            element = next(iter(contacts_dict))
            return element
        except StopIteration:
            break


def func_exit(*args, **kwargs):
    return 'Good bye!'


if __name__ == '__main__':
    ab = AddressBook()
    ab.add_record(Record(Name("Bill"), Phone("+380971234567"), Birthday('1990/06/15')))
    while True:
        try:
            name = Name(input("Type contact name >>> "))
            phone = Phone(input("Tupe contact telephone >>> "))
            ab.add_record(Record(name, phone))
            break
        except ValueError as e:
            print(e)
    print(ab)
