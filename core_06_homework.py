from typing import Callable
from functools import wraps
from collections import UserDict

# Decorator to silently handle phone validation
def phone_validation(func: Callable):
    """
    Handles silently any kind of ValueError for phone number input

    Parameters:
        func (callable): function operating with phone input
    """
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return None
    return inner

class Field:
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value: str):
        if len(value) != 10:
            raise ValueError(f"Phone number {value} is not 10 digits long")
        super().__init__(value)

class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
    
    # Method to add a new phone number
    @phone_validation
    def add_phone(self, phone: str):
        phone = Phone(phone)
        if phone.value not in [ph.value for ph in self.phones]:
            self.phones.append(phone)
    
    # Method to remove an existing phone number
    @phone_validation
    def remove_phone(self, phone: str):
        phone = Phone(phone)
        self.phones = [ph for ph in self.phones if ph.value != phone.value]
    
    # Method to edit an existing phone number
    @phone_validation
    def edit_phone(self, old_phone: str, new_phone: str):
        old_phone = Phone(old_phone)
        new_phone = Phone(new_phone)
        self.phones = [ph if ph.value != old_phone.value else new_phone for ph in self.phones]

    # Method to find a phone number
    @phone_validation
    def find_phone(self, phone: str) -> Phone | None:
        phone = Phone(phone)
        if phone.value in [ph.value for ph in self.phones]:
            return phone
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):

    # Method to add a record
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    # Method to find a record
    def find(self, name: str) -> Phone | None:
        if name in self.data:
            return self.data[name]
        return None
    
    # Method to delete an existing record
    def delete(self, name: str):
        if name in self.data:
            self.data.pop(name)

    def __str__(self):
        return "\n".join(record.__str__() for record in self.data.values())
