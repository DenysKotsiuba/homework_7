import pickle
from classes import *


COMMANDS_LIST = ["hello", "add record", "add phone", "change", "delete", "phone", "find", "show all", "birthday"]
CLOSE_COMMANDS_LIST = ["good bye", "close", "exit"]


def main():
    while True:

        user_text = input("Enter command: ")
        a = parser(user_text)

        if not a:
            continue
        
        command, user_information = parser(user_text)

        if command in CLOSE_COMMANDS_LIST:
            print("Good bye!")
            CONTACTS.write_data()
            break

        get_handler(command)(user_information)


def input_error(function):

    def wrapper(*args):
        try:
            result = function(*args)
            return result
        except ValueError:
            print(f"You've entered wrong command. Chose one of those: {', '.join(COMMANDS_LIST)}, {', '.join(CLOSE_COMMANDS_LIST)}.")
        except IndexError:
            print("Enter user name and phone number.")
        except KeyError:
            print("This user name doesn't exist.") 
        except NameError:
            print("Enter user name.")
        except PhoneError as e:
            print(e)
        except BirthdayError as e:
            print(e)
        
    return wrapper

        
@input_error
def parser(user_text):
    command, *user_information = user_text.split()
    command = command.lower()
    if command in ["show", "good", "add"] and len(user_information) > 0:
        command = f"{command} {user_information[0]}"
        user_information = user_information[1:]
        
    if command not in (COMMANDS_LIST + CLOSE_COMMANDS_LIST):
        raise ValueError
    
    return command, user_information


def get_handler(command):
    return COMMANDS[command]


@input_error
def add_record(user_information):
    if user_information[0] not in CONTACTS:
        name = Name(user_information[0].capitalize())
        phone = Phone()
        phone.value = user_information[1]
        birthday = Birthday()
        birthday.value = user_information[2] if len(user_information) > 2 else None
        record = Record(name, phone, birthday)
        CONTACTS.add_record(record)
    else:
        print("This contact exists.")


@input_error
def add_phone_to_record(user_information):
    CONTACTS[user_information[0]].add_phone(user_information[1])


@input_error
def change(user_information):
    if len(user_information) < 3:
        print("Enter user name, old phone, new phone.")
    else:
        CONTACTS[user_information[0]].edit_phone(user_information[1], user_information[2])


@input_error
def delete_phone_from_record(user_information):
    CONTACTS[user_information[0]].delete_phone(user_information[1])


def find_all(user_information):
    users = []

    if user_information:

        for key, value in CONTACTS.items():
            phones_values = map(lambda x: x.value, value.phones)
            phones = ''.join(phones_values)
            user_data = f"{key}{phones}{value.birthday.value}"
            if user_data.find(' '.join(user_information)) != -1:
                users.append(key)
        
        if users:
            print(", ".join(users))
        else:
            print("No matches.")

    else:
        print("Enter substring.")


def greeting(*args):
    print("How can I help you?")


@input_error
def next_birthday(user_information):
    if user_information:
        CONTACTS[user_information[0]].days_to_birthday()
    else:
        raise NameError


@input_error
def phone(user_information):
    if user_information:
        print(f"{CONTACTS[user_information[0]].phones}"[1:-1])
    else:
        raise NameError


def show_all(*args):
    for page in CONTACTS.iterator(int(input())):
        print(', '.join(page))


COMMANDS = {
    'add record': add_record,
    'add phone': add_phone_to_record,
    'birthday': next_birthday,
    'change': change,
    'delete': delete_phone_from_record,
    'find': find_all,
    'hello': greeting,
    'phone': phone,
    'show all': show_all,
}


CONTACTS = AddressBook().read_data()

main()