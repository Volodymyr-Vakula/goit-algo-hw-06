from collections import UserDict

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
            raise ValueError("Phone number must be 10 digits long")
        if not value.isdigit():
            raise ValueError("Phone number must contain digits only")
        super().__init__(value)

class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
    
    # Method to add a new phone number
    def add_phone(self, phone: str):
        phone = Phone(phone)
        if phone.value not in [ph.value for ph in self.phones]:
            self.phones.append(phone)
    
    # Method to remove a phone number
    def remove_phone(self, phone: str):
        self.phones = [ph for ph in self.phones if ph.value != phone]
    
    # Method to edit an existing phone number
    def edit_phone(self, old_phone: str, new_phone: str):
        if old_phone in [ph.value for ph in self.phones]:
            self.remove_phone(old_phone)
            self.add_phone(new_phone)
        else:
            raise ValueError("Phone number to be edited is missing from the list")

    # Method to find a phone number
    def find_phone(self, phone: str) -> Phone | None:
        for ph in self.phones:
            if phone == ph.value:
                return ph
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
