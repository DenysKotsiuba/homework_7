import pickle
from collections import UserDict
from datetime import datetime
from re import fullmatch


class AddressBook(UserDict):
    
    def add_record(self, record):
        self.data[record.name.value] = record

    def iterator(self, n):
        start = 0
        data = list(map(lambda x: f"{x[0]}: {str(x[1].phones)[1:-1]}", self.data.items()))
        
        while start < len(self.data):
            yield data[start: start+n]
            start += n


    def read_data(self):
        try:
            with open('data.bin', 'rb') as file:
                contacts = pickle.load(file)
        except FileNotFoundError as e:
            contacts = self
        except EOFError as e:
            contacts = self
        finally:
            return contacts


    def write_data(self):
        with open('data.bin', 'wb') as file:
            pickle.dump(self, file)


class Field:

    def __init__(self, value=None):
       self._value = value

    def __repr__(self):
        return str(self.value)

    def __str__(self):
        return str(self.value)

    @property
    def value(self):
        return self._value
   
    @value.setter
    def value(self, value):
        self._value = value        


class Birthday(Field):
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):   
        if value == None or fullmatch(r'\d{1,2}/\d{1,2}/\d{4}', value):
            self._value = value
        else:
            raise BirthdayError("Enter the birthday date according to the specified template: XX/XX/XXXX.")
        

class BirthdayError(Exception):
    pass


class Name(Field):
    pass


class Phone(Field):

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if fullmatch(r"\+\d{3}\(\d{2}\)\d{3}-\d{2}-\d{2}", value):
            self._value = value
        else:
            raise PhoneError("Enter the phone number according to the specified template: +380(XX)XXX-XX-XX.")
        

class PhoneError(Exception):
    pass


class Record:

    def __init__(self, name, phone, birthday=None):
        self.name = name
        self.phones = [phone]
        self.birthday = birthday

    def add_phone(self, phone):
        for phone_object in self.phones:

            if phone_object.value == phone:
                print(f"Phone number {phone} exists.")
                break

        else:
            new_phone = Phone()
            new_phone.value = phone
            self.phones.append(new_phone)

    def days_to_birthday(self):
        if self.birthday.value:

            birthday = datetime.strptime(self.birthday.value, '%d/%m/%Y').date()
            today = datetime.now().date()
            this_year_birthday = birthday.replace(year=today.year)

            if today > this_year_birthday:
                next_year_birthday = birthday.replace(year=today.year+1)
                days = next_year_birthday - today
                print(str(days).split(',')[0])
                
                return days.days

            days = this_year_birthday - today 
            print(str(days).split(',')[0])

            return days.days
        
        else:
            print("Birthday date not specified.")

    def delete_phone(self, phone):
        for phone_object in self.phones:

            if phone_object.value == phone:
                self.phones.remove(phone_object)
                break

        else:
            print(f"Phone number {phone} doesn't exist. Enter existing phone number.")

    def edit_phone(self, phone, new_phone):
        for phone_object in self.phones:

            if phone_object.value == phone:
                phone_object.value = new_phone
                break

        else:
            print(f"Phone number {phone} doesn't exist. Enter existing phone number.") 


if __name__ == '__main__':
    a = 2
    name = Name('Bill')
    phone = Phone('1234567890')
    rec = Record(name, phone)
    ab = AddressBook()
    ab.add_record(rec)
    assert isinstance(ab['Bill'], Record)
    assert isinstance(ab['Bill'].name, Name)
    assert isinstance(ab['Bill'].phones, list)
    assert isinstance(ab['Bill'].phones[0], Phone)
    assert ab['Bill'].phones[0].value == '1234567890'
    print('All Ok)')
