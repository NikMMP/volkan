# from PIL import Image, ImageTk
# import tkinter as tk
from pathlib import Path
import os
import pickle
import re
import time
import sys
import shutil
from collections import UserDict
from datetime import date, timedelta
from termcolor import colored
import colorama
from abc import abstractmethod, ABCMeta

import functools
import os
from pathlib import Path

# from notes import CLINotes
colorama.init()

dir_path = os.path.dirname(__file__)


class Notes:

    @staticmethod
    def add_note(note, tag, text):
        filename = note + ".txt"
        full_path = os.path.join(Path().resolve(), "notes", filename)
        create_dict_note = {
            "note": note,
            "tag": tag,
            "text": "\n"+text
        }

        if not os.path.isfile(full_path):

            with open(full_path, 'w', encoding="utf8") as file:
                for k, v in create_dict_note.items():
                    file.writelines(f"{k}: {v}\n")
                    print(file)
            return f"Your new note with name '{note}' is created in folder 'notes'"

        return f"Note with name '{note}' is already exist in folder 'notes'"

    @staticmethod
    def read_note(note):
        filename = note + ".txt"
        full_path = os.path.join(Path().resolve(), "notes", filename)
        note = ""
        tag = ""
        text = ""

        if os.path.isfile(full_path):
            with open(full_path, 'r', encoding="utf8") as file:
                note_data = file.readlines()
                for i, l in enumerate(note_data):
                    if i == 0:
                        note = l.replace('\n', '')
                    elif i == 1:
                        tag = l.replace('\n', '')
                    else:
                        text += l
            return f"{note}\n{tag}\n{text.strip()}"
        return f"Note with name '{note}' was not found in folder 'notes'"

    @staticmethod
    def update_note(note, tag, text):
        filename = note + ".txt"
        full_path = os.path.join(Path().resolve(), "notes", filename)

        if os.path.isfile(full_path):
            with open(full_path, "w", encoding='utf8') as file:
                file.writelines(f"note: {note}\n")
                file.writelines(f"{tag}\n")
                file.writelines(text)
            return f"Note '{note}' was updated successfully!"

        return f"Note with name '{note}' was not found in folder 'notes'"

    @staticmethod
    def delete_note(note):
        filename = note + ".txt"
        full_path = os.path.join(Path().resolve(), "notes", filename)

        if os.path.isfile(full_path):
            os.remove(full_path)
            return f"Your note with name '{note}' was deleted from folder 'notes'"
        else:
            return f"Note with name '{note}' was not found in folder 'notes'"

    @staticmethod
    def show_all_note():
        folder = os.path.join(Path().resolve(), "notes")
        create_list_notes = []

        for filename in os.listdir(folder):
            create_list_notes.append(filename)

        if len(create_list_notes) == 0:
            return f"Your notebook is still empty.\nPlease add your first note"
        else:
            first_string = "Your notebook has the following notes:\n"
            note_lines = "\n".join(str(record)
                                   for record in list(create_list_notes))
            return first_string + note_lines

    @staticmethod
    def find_by_tag_note(tag):
        folder = os.path.join(Path().resolve(), "notes")
        create_list_notes = []

        for filename in os.listdir(folder):
            note_to_do = Notes.read_note(filename.split('.')[0])
            tags = note_to_do.split('\n')[1].split()
            if tag in tags:
                create_list_notes.append(filename)

        if len(create_list_notes) == 0:
            return f"I can't find any note by this tag.\nPlease enter a valid note's tag for search."

        first_string = "I found the following notes by your tag:\n"
        note_names = "\n".join(str(record)
                               for record in list(create_list_notes))
        return first_string + note_names

    @staticmethod
    def find_by_name_note(note):
        folder = os.path.join(Path().resolve(), "notes")
        create_list_notes = []

        for filename in os.listdir(folder):
            if note in filename.split('.')[0]:
                create_list_notes.append(filename)

        if len(create_list_notes) == 0:
            return f"I can't find any note that contain this name.\nPlease enter a valid note's name for search."

        first_string = "I found  the following notes by searching name:\n"
        note_names = "\n".join(str(record)
                               for record in list(create_list_notes))
        return first_string + note_names


# >>>>> here start class CLI <<<<<
NOTES = Notes()


def is_exist(note):
    filename = note + ".txt"
    full_path = os.path.join(Path().resolve(), "notes", filename)
    if os.path.exists(full_path):
        return True
    return False


def command_error_handler(func):
    @functools.wraps(func)
    def wrapper(*args):
        try:
            return func(*args)
        except (ValueError, KeyError, Exception) as err:
            return str(err)

    return wrapper


class CLINotes:

    @staticmethod
    def help_handler():
        return ("""
    You can use the following commands for your notebook:
    - add note -> to create new note and save into folder 'notes';
    - read note -> to open indicated note and read text inside;
    - delete note -> to delete indicated note from the folder;
    - find by tag -> to find all notes that are matched with this tag;
    - find by name -> to find notes that are matched with this name;
    - show all -> to show list of notes that were saved in folder;
    - add tag -> to include additional tag to existing note;
    - add text -> to include additional text to existing note;
    - change tag -> to change existing tag in note (recommend to read note first);
    - change text -> to change existing text in note (recommend to read note first);
    - delete tag -> to delete existing tag in note (recommend to read note first);
    - delete text -> to delete existing text in note (recommend to read note first);
    """)

    @command_error_handler
    def add_note_handler(self=None):
        note = input("Enter note: ")
        if note == "":
            return f"You haven't enter, try again please"

        elif is_exist(note):
            return f"Note with name '{note}' is already exist in folder 'notes'"

        else:
            tag = input("Please enter tags (start with #, space to divide): ")
            text = input("Please enter text for note: ")
            return NOTES.add_note(note, tag, text)

    @command_error_handler
    def read_note_handler(self=None):
        note = input(
            "Please enter note which want to you read (without '.txt'): ")

        if note != "":
            return NOTES.read_note(note)
        return "Note is missed. Please try again"

    @command_error_handler
    def delete_note_handler(self=None):
        note = input("Enter note which want to delete it (without '.txt'): ")

        if note != "":
            return NOTES.delete_note(note)
        return "Name of note is missed. Please try again"

    @command_error_handler
    def find_tag_handler(self=None):
        tag = input("Please enter 1 tag to find notes (start with #): ")

        if tag != "":
            return NOTES.find_by_tag_note(tag)
        return "Tag for search is missed. Please try again"

    @command_error_handler
    def find_note_handler(self=None):

        note = input("To find note (without '.txt'): ")
        if note != "":
            return NOTES.find_by_name_note(note)

        return "Search is missed. Please try again"

    @command_error_handler
    def show_all_handler(self=None):
        return NOTES.show_all_note()

    @command_error_handler
    def add_tag_handler(self=None):
        note = input("Note to update info (without '.txt'): ")

        if is_exist(note):
            tag = input(
                "Please use first tag to add to this note (start with #): ")
            note_to_read = NOTES.read_note(note)
            old_tag = ""
            old_text = ""

            for i, item in enumerate(note_to_read.split('\n'), start=0):
                if i == 1:
                    old_tag = item + " "

            for i, item in enumerate(note_to_read.split('\n')[2:], start=0):
                old_text += item + '\n'

            return NOTES.update_note(note, old_tag + tag, old_text)
        raise ValueError(
            f"Note with name '{note}' does not exist in notebook.")

    @command_error_handler
    def add_text_handler(self=None):
        note = input("Enter note to update info (without '.txt'): ")

        if is_exist(note):
            text = input("Please write text to add to the current note: ")
            note_to_do = NOTES.read_note(note)
            old_tag = ''
            old_text = ''

            for i, item in enumerate(note_to_do.split('\n'), start=0):
                if i == 1:
                    old_tag = item

            for i, item in enumerate(note_to_do.split('\n')[2:], start=0):
                old_text += item + '\n'

            return NOTES.update_note(note, old_tag, old_text + text)
        raise ValueError(
            f"Note with name '{note}' does not exist in notebook.")

    @command_error_handler
    def change_tag_handler(self=None):
        note = input(
            "Please enter name of note to update info (without '.txt'): ")

        if is_exist(note):
            note_to_do = NOTES.read_note(note)
            tag_list = note_to_do.split('\n')[1]
            new_tag = ''
            new_text = ''

            for i, item in enumerate(tag_list.split(), start=0):
                print(i, item)
            tag_index = int(
                input("Please enter index of tag that you want to change: "))
            tag = input(
                "Please write new tag to add instead old to the current note: ")

            for i, item in enumerate(tag_list.split(), start=0):
                if i == tag_index:
                    item = tag
                new_tag += item + ' '

            for i, item in enumerate(note_to_do.split('\n')[2:], start=0):
                new_text += item + '\n'

            return NOTES.update_note(note, new_tag, new_text)

        raise ValueError(
            f"Note with name '{note}' does not exist in notebook.")

    @command_error_handler
    def change_text_handler(self=None):
        note = input(
            "Please enter name of note to update info (without '.txt'): ")

        if is_exist(note):
            note_to_do = NOTES.read_note(note)
            new_tag = ''
            new_text = ''

            for i, item in enumerate(note_to_do.split('\n')[2:], start=0):
                print(i, item)

            text_index = int(
                input("Please enter index of text that you want to change: "))
            text = input(
                "Please write new text to add instead old to the current note: ")

            for i, item in enumerate(note_to_do.split('\n'), start=0):
                if i == 1:
                    new_tag = item

            for i, item in enumerate(note_to_do.split('\n')[2:], start=0):

                if i == text_index:
                    item = text
                new_text += item + '\n'

                return NOTES.update_note(note, new_tag, new_text)

            raise ValueError(
                f"Note with name '{note}' does not exist in notebook.")

    @command_error_handler
    def delete_tag_handler(self=None):
        note = input(
            "Please enter name of note to update info (without '.txt'): ")

        if is_exist(note):
            note_to_do = NOTES.read_note(note)
            tag_list = note_to_do.split('\n')[1]
            new_tag = ''
            new_text = ''

            for i, item in enumerate(tag_list.split(), start=0):
                print(i, item)
            tag_index = int(
                input("Please enter index of tag that you want to delete: "))

            for i, item in enumerate(tag_list.split(), start=0):
                if i == tag_index:
                    item = ""
                new_tag += item + ' '

            for i, item in enumerate(note_to_do.split('\n')[2:], start=0):
                new_text += item + '\n'

            return NOTES.update_note(note, new_tag.strip(), new_text)

        raise ValueError(
            f"Note with name '{note}' does not exist in notebook.")

    @command_error_handler
    def delete_text_handler(self=None):
        note = input(
            "Please enter name of note to update info (without '.txt'): ")

        if is_exist(note):
            note_to_do = NOTES.read_note(note)
            tag_list = note_to_do.split('\n')[1]
            new_tag = ''
            new_text = ''

            for i, item in enumerate(note_to_do.split('\n')[2:], start=0):
                print(i, item)
            text_index = int(
                input("Please enter index of text that you want to delete: "))

            for i, item in enumerate(tag_list.split('\n'), start=0):
                if i == 0:
                    new_tag = item

            for i, item in enumerate(note_to_do.split('\n')[2:], start=0):
                if i == text_index:
                    item = ''
                new_text += item + '\n'

            return NOTES.update_note(note, new_tag, new_text.strip())

        raise ValueError(
            f"Note with name '{note}' does not exist in notebook.")

    commands_dict = {
        "help": help_handler,

        "add note": add_note_handler,
        "read note": read_note_handler,
        "delete note": delete_note_handler,

        "find by tag": find_tag_handler,
        "find by name": find_note_handler,
        "show all": show_all_handler,

        "add tag": add_tag_handler,
        "add text": add_text_handler,
        "change tag": change_tag_handler,
        "change text": change_text_handler,
        "delete tag": delete_tag_handler,
        "delete text": delete_text_handler,
    }

    @staticmethod
    def run_notes():
        folder = os.path.join(Path().resolve(), "notes")

        if not os.path.exists(folder):
            os.mkdir(folder)

        print("Hello! I'm here to assist you with your notes in your notebook.")
        print("You could enter exact commands if you already know them.\n"
              "Or please use:\n"
              "  help -> to see whole list of commands\n"
              "  exit -> to finish work with your notebook")

        while True:
            command = input("You haven't entered command: ").lower().strip()

            if command == "exit":
                return "\nThanks, see you soon!!!\n"

            if command in CLINotes.commands_dict.keys():
                handler = CLINotes.commands_dict[command]
                answer = handler()
                print(answer)

            else:
                commands_list = []
                for k in CLINotes.commands_dict.keys():
                    for item in k.split():
                        if command in item:
                            commands_list.append(k)
                            break

                if commands_list:
                    print("What you have mean entered these commands: ")
                    print(*commands_list, sep=", ")
                else:
                    print(
                        "Incorrect input.\nPlease check and enter correct command (or 'help' or 'exit').")


# class Logo_Image:
#     def __init__(self, title="Volkan", geometry="300x400", image="Volkan.png", button_img="button.png"):
#         self.window = tk.Tk()
#         self.window.title(title)
#         self.window.geometry(geometry)
#         self.window.resizable(width=False, height=False)
#         print(os.getcwd())
#         self.canvas = tk.Canvas(self.window, width=600, height=400)
#         self.canvas.place(x=-1, y=-1)
#         self.img = Image.open(os.path.join(dir_path, image))

#         self.resized_image = self.img.resize((300, 400), Image.ANTIALIAS)
#         self.bgImage = ImageTk.PhotoImage(self.resized_image)
#         self.bg = self.canvas.create_image(
#             0, 0, image=self.bgImage, anchor=tk.NW)

#         self.img1 = Image.open(os.path.join(dir_path, button_img))
#         self.resized_button = self.img1.resize((100, 30), Image.ANTIALIAS)
#         self.bgBtn = ImageTk.PhotoImage(self.resized_button)

#         self.button = self.canvas.create_image(150, 365, image=self.bgBtn)
#         self.command = lambda: self.click_button_event()
#         self.canvas.tag_bind(self.button, "<Button-1>",
#                              self.click_button_event)

#     def run(self):
#         self.window.mainloop()

#     def click_button_event(self, event):
#         self.window.destroy()


NOT_DEFINED = "not defined"
ADRESSBOOK = "book.bin"
TELEPHONE = r"[+]380[(][0-9]{2}[)][0-9]{3}[-][0-9]{2}[-][0-9]{2} | [+]380[(][0-9]{2}[)][0-9]{3}[-][0-9]{1}[-][0-9]{3}"


class Widget:
    @abstractmethod
    def __init__(self, device):
        pass

    @abstractmethod
    def send_message(self, msg: str):
        pass


class Terminal(Widget):
    def __init__(self, stream):
        self.stream = stream

    def send_message(self, msg: str):
        self.stream.write(">> " + msg)


OUTPUT_DEVICE = Terminal(sys.stdout)
OUTPUT_DEVICE_NAME = "console"


class AddressBook(UserDict):

    outputdevice = Terminal(sys.stdout)
    outputdvicename = "console"

    def __init__(self, device=Terminal(sys.stdout), devicename="console"):
        self.outputdevice = device
        self.outputdvicename = devicename
        self.data = {}

    def __getstate__(self):
        attributes = self.__dict__.copy()
        return attributes

    def __setstate__(self, value):
        self.__dict__ = value

    def save_to_file(self, filename):
        with open(filename, "wb") as fh:
            pickle.dump(self.data, fh)

    def read_from_file(self, filename):
        with open(filename, "rb") as fh:
            self.data = pickle.load(fh)

    def iterator(self, n=1):  # n indicates number of record to take for each iteration
        recorded = 0
        output = []
        for record in self.data:
            if (recorded < n):
                output.append(self.data[record])
                recorded += 1
            else:  # recorded == n
                yield output
                recorded = 1
                output = [self.data[record]]
        yield output

    def add_record(self, record):  # adding record type Record into the dictionary
        self.data[record.name.value] = record

    def print(self):
        outputline = ""
        for name in self.data:
            outputline += self.data[name].print()
        self.outputdevice.send_message(outputline)
        return f"output was sent to the device: {self.outputdvicename}"

    def find_name(self, strname):
        for record in self.data:
            if strname == record:
                return self.data[record]
        return Record(Name(NOT_DEFINED))

    def remove(self, name):
        self.data.pop(name)

    def len(self):
        return len(self.data)


# contact_book = AddressBook()


class Record:  # responsible for the record manipulation

    def __init__(self, name):
        self.name = name  # type of Name
        self.phone = []  # list of phones
        self.email = []  # list of e-mails
        self.birthday = Birthday()
        self.add = Address()

    def set_birthday(self, s):
        self.birthday.day = check_birthday(s)

    def days_to_birthday(self):
        today = date.today()
        result = self.birthday.day
        if result != "":
            inputdate = result.split("/")
            birthday = date(year=int(inputdate[0]), month=int(
                inputdate[1]), day=int(inputdate[2]))
            thisbirthday = date(
                year=today.year, month=birthday.month, day=birthday.day)
            if today.month > birthday.month:  # birthday has passed
                nextbirthday = date(year=today.year + 1,
                                    month=birthday.month, day=birthday.day)
            else:  # still will be
                nextbirthday = date(
                    year=today.year, month=birthday.month, day=birthday.day)
            delta = nextbirthday - today
            return delta.days
        else:
            return "No date of birth defined yet"

    def add_phone(self, phone):
        self.phone.append(phone)
        return (f"add phone: {phone.value} for {self.name.value}")

    def find_phone(self, phone):
        for ph in self.phone:
            if ph.value == phone:
                return ph
        return Phone()

    def find_email(self, email):
        for ph in self.email:
            if ph.value == email:
                return ph
        return Email()

    def remove_phone(self, strphone):
        try:
            phone = self.find_phone(strphone)
            self.phone.remove(phone)
            return f"{phone.value} removed"
        except ValueError:
            return f"can not remove phone {strphone}: does not exist"

    def add_email(self, email):
        self.email.append(email)
        return (f"add email: {email.value}")

    def remove_email(self, stremail):
        try:
            email = self.find_email(stremail)
            self.email.remove(email)
            return f"{email.value} removed"
        except ValueError:
            return f"can not remove email {stremail}: does not exist"

    def print_phones(self):
        # output = "Phones: "
        output = ""
        for phone in self.phone:
            output += phone.value + " "
        return output

    def print_emails(self):
        # print("Emails: ")
        output = ""
        for email in self.email:
            output += email.value + " "
        return output

    def edit_address(self, newaddress):
        self.add.update(newaddress)

    def print_address(self):
        return self.add.value

    def create_output_line(self, index):
        output = []
        if index == 0:
            output.append(self.name.value)
            if len(self.phone) > 0:
                output.append(self.phone[0].value)
            else:
                output.append("")

            if len(self.email) > 0:
                output.append(self.email[0].value)
            else:
                output.append("")

            if self.birthday.day != "":
                output.append(self.birthday.day)
            else:
                output.append("")

            if self.add.value != NOT_DEFINED:
                output.append(self.add.value)
            else:
                output.append("")
        else:
            output = [""]
            if len(self.phone) > index:
                output.append(self.phone[index].value)
            else:
                output.append("")

            if len(self.email) > index:
                output.append(self.email[index].value)
            else:
                output.append("")
            output.append("")
            output.append("")
        return output

    def print(self):
        m1 = len(self.phone)
        m2 = len(self.email)
        if m1 > m2:
            m = m1
        else:
            m = m2
        outputline = ""
        # print("-" * 160)
        outputline += "-" * 160 + "\n"
        for i in range(m):
            output = self.create_output_line(i)
            # print(output)
            # print(" {:^20} | {:^20}| {:^20} | {:^20} | {:^20} ".format(
            #    output[0], output[1], output[2], output[3], output[4]))
            outputline += " {:^20} | {:^20}| {:^20} | {:^20} | {:^20} ".format(
                output[0], output[1], output[2], output[3], output[4])+"\n"

        return outputline

    def edit_birthday(self, new):
        self.birthday.update(new)


class Field:  # defines general fields properties TBD
    def __init__(self, value):
        self.value = value

    def update(self, newvalue):
        self.value = newvalue


class Name(Field):  # mandatory field
    def __init__(self, value):
        self.value = value


class Phone(Field):  # nonmandatory field
    def __init__(self, phone=NOT_DEFINED):
        self.__value = phone

    @ property  # define getter
    def value(self):
        return self.__value

    @ value.setter  # define setter
    def value(self, val):
        match = re.fullmatch(
            r"[+]?[1-9]{1,2}(\([1-9]{3}\)|[1-9]{3})[1-9]{3}[-]?[0-9]{2}[-]?[0-9]{2}", val)
        if not match:
            raise ValueError(">> Phone number is not  correct.\n")
        else:
            self.__value = val


class Email(Field):  # nonmandatory field
    def __init__(self, email=NOT_DEFINED):
        self.__value = email

    @ property  # getter
    def value(self):
        return self.__value

    @ value.setter  # setter
    def value(self, val):
        match = re.fullmatch(
            r"[a-zA-Z\.\-_0-9]+@[a-zA-Z0-9]+[\.][a-zA-Z]{2}", val)
        if not match:
            raise ValueError(">> Email name is not correct. \n")
        else:
            self.__value = val


class Birthday:
    # will keep it in format yyyy/mm/dd
    def __init__(self):
        self.__birthday = ""

    @ property  # define getter
    def day(self):
        return self.__birthday

    @ day.setter  # define setter
    def day(self, val):
        match = re.fullmatch(r"^[1-9][0-9]{3}\/[0-9]{2}\/[0-9]{2}", val)
        if not match:
            raise ValueError(">> Date is not  correct date.\n")
        else:
            self.__birthday = val

    def update(self, newbirth):
        self.__birthday = newbirth.day


class Address(Field):
    def __init__(self, add=NOT_DEFINED):
        self.value = add


def do_something():
    output = """ here we created the following classes:\n
    - AdressBook \n
    - Record \n
    - Field \n
    - Name \n
    - Phone \n
    - Email \n
    and added some functionality which will be developed in the next H/Ws"""
    print(output)


def output(list):  # list of records
    s = ""
    for record in list:
        s += record.name.value + " "
    return s


def check_birthday(val):
    match = re.fullmatch(r"^[1-9][0-9]{3}\/[0-9]{2}\/[0-9]{2}", val)
    while not match:
        print(">> Please input correct date. Typically it is yyyy/mm/dd")
        val = input(">> ").lower()
        match = re.fullmatch(r"^[1-9][0-9]{3}\/[0-9]{2}\/[0-9]{2}", val)
    return val


exit_list = ["good bye", "close", "exit", "close"]


# list of commands to use

HELLO_CMD = "hello"
ADD_CMD = "add"
CHANGE_CMD = "change"
PHONE_CMD = "phone"
SHOW_CMD = "show all"
HLP_CMD = "help"
SRCH_CMD = "search"
SORT_CMD = 'sort'
EDT_CMD = "edit"
RMV_CMD = "remove"
EMAIL_CMD = "email"
CONGRAT_CMD = "birthday"
NOTES_CMD = "notes"

COMMANDS = [HELLO_CMD, ADD_CMD, CHANGE_CMD,
            PHONE_CMD, SHOW_CMD, HLP_CMD, SRCH_CMD,
            EDT_CMD, RMV_CMD, EMAIL_CMD, CONGRAT_CMD, NOTES_CMD]


def parser(line):
    return re.sub("[^0-9a-zA-Z+()-]", " ", line).split()


GREETING = "How can I help you ? For the commands description please type help"
NOTHING = "There is nothing to execute"
UNDERSTOOD = "Understood"


def wait():
    print(">> Please wait....")
    time.sleep(2)


def check_number(num):
    match = re.fullmatch("^[0-9]+$", num)
    while not match:
        print(">> Please input correct number. It should include only digits")
        num = input(">> ").lower()
        match = re.fullmatch("^[0-9]+$", num)
    return num


def check_name(name):
    match = re.fullmatch("[a-zA-Z]+", name)
    while not match:
        print(">> Please input correct name. It should include only letters")
        name = input(">> ").lower()
        match = re.fullmatch("[a-zA-Z]+", name)
    return name


def check_phone(phone):
    match = re.fullmatch(
        r"[+]?[1-9]{1,2}(\([1-9]{3}\)|[1-9]{3})[1-9]{3}[-]?[0-9]{2}[-]?[0-9]{2}", phone)
    while not match:
        print(">> Please input correct phone. Typically it is +1(647)861-9006 or similar")
        phone = input(">> ").lower()
        match = re.fullmatch(
            r"[+]?[1-9]{1,2}(\([1-9]{3}\)|[1-9]{3})[1-9]{3}[-]?[0-9]{2}[-]?[0-9]{2}", phone)
    return phone


def add_process(words):
    command = words[0]
    if len(words) == 3:  # all required arguments were taken
        name = check_name(words[1])  # check the name
        print(">> " + "Check phone info for " + name)
        wait()
        phone = check_phone(words[2])  # check the phone
        print(">> " + "It is all right. Will add " + name + " " + phone)
        wait()
    elif len(words) == 2:  # one argument is missing - phone
        name = check_name(words[1])  # check the name
        print(">> " + "Need phone info for " + name)
        phone = check_phone("-1")  # check the phone
        print(">> " + "It is all right. Will add " + name + " " + phone)
        wait()
    else:  # all arguments were missing only add
        print(">> " + "Found command add in your request. Will need a name and a phone of the contact")
        name = check_name("-1")  # check the name
        print(">> " + "Need phone info for " + name)
        phone = check_phone("-1")  # check the phone
    return command + " " + name + " " + phone


def change_process(words):
    command = words[0]
    if len(words) == 3:  # all required arguments were taken
        name = check_name(words[1])  # check the name
        print(">> " + "Check phone info for " + name)
        wait()
        phone = check_phone(words[2])  # check the phone
        print(">> " + "It is all right. Will change " + name + " " + phone)
        wait()
    elif len(words) == 2:  # one argument is missing - phone
        name = check_name(words[1])  # check the name
        print(">> " + "Need phone info for " + name)
        phone = check_phone("-1")  # check the phone
        print(">> " + "It is all right. Will change " + name + " " + phone)
        wait()
    else:  # all arguments were missing only add
        print(">> " + "Found command change in your request. Will need name and a new phone of the contact")
        name = check_name("-1")  # check the name
        print(">> " + "Need phone info for " + name)
        phone = check_phone("-1")  # check the phone
    return command + " " + name + " " + phone


def phone_process(words):
    command = words[0]
    if len(words) == 2:  # all required arguments were taken
        name = check_name(words[1])  # check the name
        print(">> " + "It is all right. Will chase for the phone of " + name)
        wait()
    else:  # all arguments were missing only add
        print(">> " + "Found command phone in your request. Will need name of the contact")
        name = check_name("-1")  # check the name
    return command + " " + name


def email_process(words):
    command = words[0]
    if len(words) == 2:  # all required arguments were taken
        name = check_name(words[1])  # check the name
        print(">> " + "It is all right. Will chase for the email of " + name)
        wait()
    else:  # all arguments were missing only add
        print(">> " + "Found command email in your request. Will need name of the contact")
        name = check_name("-1")  # check the name
    return command + " " + name


def search_process(words):
    command = words[0]
    if len(words) < 2:
        what = ""
        while len(what) == 0:
            print(">> would you please enter what you looking for ?")
            what = input(">> ").lower()
    else:
        what = words[1]
    return command + " " + what


def edit_process(words):
    command = words[0]
    if len(words) < 2:
        name = check_name("-1")
    else:
        name = check_name(words[1])
    return command + " " + name


def remove_process(words):
    command = words[0]
    if len(words) < 2:
        name = check_name("-1")
    else:
        name = check_name(words[1])
    return command + " " + name


def birthday_process(words):
    command = words[0]
    if len(words) == 2:  # all required arguments were taken
        days = check_number(words[1])  # check the name
        print(">> " + "It is all right. Will chase for the names who will have birthday in " + days + "  days")
        wait()
    else:  # all arguments were missing only add
        print(">> " + "Found command birthday in your request. Will need number of days")
        days = check_number("-1")  # check the name
    return command + " " + days


PROCESS = {ADD_CMD: add_process,
           CHANGE_CMD: change_process,
           PHONE_CMD: phone_process,
           SRCH_CMD: search_process,
           EDT_CMD: edit_process,
           RMV_CMD: remove_process,
           EMAIL_CMD: email_process,
           CONGRAT_CMD: birthday_process
           }


def input_error(command_func):
    def inner(list):
        corrected_list = []
        for record in list:  # list of commands extracted from the user input
            # print(record)
            words = record.split()  # split the possible action
            command = words[0]  # it is always command
            corrected_list.append(PROCESS[command](words))
            # 33 print(corrected_list)
        return command_func(corrected_list)
    return inner


def nothing():
    return NOTHING


def greet(list=[]):
    return GREETING


@ input_error
def add_contact(list):  # list contains lists of possible actions to add
    # print(list)
    output = ""
    for record in list:
        words = record.split()
        # print(words)
        name = words[1]
        phone = words[2]
        # will add the contact into the address book
        title = Name(name)
        person = Record(title)
        person.add_phone(Phone(phone))
        contact_book.add_record(person)
        output += name + " "
    return "Added " + output + "into the contacts"


@ input_error
def change(list):  # list contains lists of possible actions to add
    # print(list)
    output = ""
    for record in list:
        words = record.split()
        name = words[1]
        found_record = contact_book.find_name(name)
        # print(found)
        if found_record.name.value != NOT_DEFINED:
            found_record.print()
            print(">> please specify which phone you would like to change?")
            old_phone = input(">> ").lower()
            old_phone = check_phone(old_phone)
            # remove old phone
            print(">> " + contact_book.get(name).remove_phone(old_phone))
            phone = words[2]
            contact_book.get(name).add_phone(Phone(phone))  # add new phone
            found_record.print()
            output += name + " "
        else:
            print(">> Sorry, there is no contact called " + name + ". Skipped")
    return "Phones were modified for: " + output


@ input_error
def phone(list):  # list contains lists of possible actions to add
    # print(list)
    for record in list:
        words = record.split()
        name = words[1]
        found_record = contact_book.find_name(name)
        # print(found)
        if found_record.name.value != NOT_DEFINED:
            print(f">> {name}:" + found_record.print_phones())
        else:
            print(">> Sorry, there is no contact called " + name + ". Skipped")
    return "Done"


@ input_error
def email(list):  # list contains lists of possible actions to add
    # print(list)
    for record in list:
        words = record.split()
        name = words[1]
        found_record = contact_book.find_name(name)
        # print(found)
        if found_record.name.value != NOT_DEFINED:
            print(f">> {name}:" + found_record.print_emails())
        else:
            print(">> Sorry, there is no contact called " + name + ". Skipped")
    return "Done"


def show(list=[]):
    # print("-" * 36)
    # print("{:^36}|".format("Current list of the contacts"))
    # print("-" * 36)
    # for contact in CONTACTS:
    #    print("{:^16} | {:^16} |".format(contact, CONTACTS[contact]))
    #    print("-" * 36)
    # contact_book.print()
    return contact_book.print()


def sorting(path):
    find = re.findall(r'[a-zA-Z:\\+\-()]*$', path[0])
    folder = find[0]
    img = ('JPEG', 'PNG', 'JPG', 'SVG')
    vid = ('AVI', 'MP4', 'MOV', 'MKV')
    doc = ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX')
    muz = ('MP3', 'OGG', 'WAV', 'AMR')
    arch = ('ZIP', 'GZ', 'TAR')

    Path(folder + '/' + 'images').mkdir(exist_ok=False)
    Path(folder + '/' + 'video').mkdir(exist_ok=True)
    Path(folder + '/' + 'documents').mkdir(exist_ok=True)
    Path(folder + '/' + 'audio').mkdir(exist_ok=True)
    Path(folder + '/' + 'archives').mkdir(exist_ok=True)

    for i in Path(folder).glob('**\*'):

        if i.name == 'images' or i.name == 'video' or i.name == 'documents' or i.name == 'audio' or i.name == 'archives':
            continue
        if i.is_dir():
            continue
        if i.suffix.upper()[1:] in img:
            Path(i).rename(folder + r'\\images' + '\\' + i.name)
        elif i.suffix.upper()[1:] in vid:
            Path(i).rename(folder + r'\\video' + '\\' + i.name)
        elif i.suffix.upper()[1:] in doc:
            Path(i).rename(folder + r'\\documents' + '\\' + i.name)
        elif i.suffix.upper()[1:] in muz:
            Path(i).rename(folder + r'\\audio' + '\\' + i.name)
        elif i.suffix.upper()[1:] in arch:
            try:
                shutil.unpack_archive(
                    Path(i), folder + r'\\archives' + '\\' + i.name)
            except:
                continue

    for empty in Path(folder).glob('**/*'):
        if empty.is_dir() and not list(empty.glob('*')):
            empty.rmdir()


def help(list=[]):

    output = """\n
* add - add a contact and a phone\n
* change - change a contact phone \n
* phone - list a phone of the contact \n
* email - list an email of the contact \n
* show all - list all the contacts \n
* remove - remove record \n
* edit - edit record (append phones, emails) \n
* search - search records according to input text \n
* birthday - output list of contacts having birthday in defined days period \n
* help - list menu of the commands \n"""
    OUTPUT_DEVICE.send_message(output)
    return f"output was sent to device {OUTPUT_DEVICE_NAME}"


@ input_error
def search(list):
    users = ""
    for record in list:
        words = record.split()
        what = words[1]
        for contact in contact_book.iterator():
            contact_record = contact[0]
            name = contact_record.name.value
            x = name.find(what)
            if x >= 0:
                users += name + " "
            else:
                for phone in contact_record.phone:
                    x = phone.value.find(what)
                    if x >= 0:
                        users += name + " "
        if len(users) == 0:
            return "nothing was found"
        else:
            return "users found: " + users


@ input_error
def edit(list):
    for record in list:
        words = record.split()
        name = words[1]  # read name
        record = contact_book.find_name(name)
        # print(record.name)
        if record.name.value == NOT_DEFINED:
            print(">> contact " + name + " does not exist. Skip")
        else:
            record.print()
            print(">> would you like to append phone ?[y/n]")
            reponse = input(">> ").lower()
            if reponse == "y":
                print(">> please input correct phone kind of +1(647)861-90-06")
                phone = input(">> ").lower()
                try:
                    newphone = Phone()
                    newphone.value = phone
                    record.add_phone(newphone)
                    wait()
                    record.print()
                except ValueError as msg:
                    print(msg)

            print(">> would you like to append email ?[y/n]")
            reponse = input(">> ").lower()
            if reponse == "y":

                print(">> please input e-mail kind of ali-mak@gmail.ca")
                email = input(">> ").lower()
                try:
                    newemail = Email()
                    newemail.value = email
                    record.add_email(newemail)
                    wait()
                    record.print()
                except ValueError as msg:
                    print(msg)

            print(">> would you like to edit adress ?[y/n]")
            reponse = input(">> ").lower()
            if reponse == "y":
                print(">> please input your full address")
                address = input(">> ").lower()
                record.edit_address(address)
                wait()
                record.print()

            print(">> would you like to input birthday? [y/n]")
            reponse = input(">> ").lower()
            if reponse == "y":
                print(">> please input date kind of yyyy/mm/dd")
                birthday = input(">> ").lower()
                try:
                    newday = Birthday()
                    newday.day = birthday
                    record.edit_birthday(newday)
                    wait()
                    record.print()
                except ValueError as msg:
                    print(msg)
    return "Done"


@ input_error
def remove(list):
    for record in list:
        words = record.split()
        name = words[1]  # read name
        record = contact_book.find_name(name)
        if record.name.value == NOT_DEFINED:
            print(">> contact " + name + " does not exist. Skip")
        else:
            record.print()
            print(
                ">> are are you sure that you want to remove this record completely? [y/n]")
            reponse = input(">> ").lower()
            if reponse == "y":
                contact_book.remove(name)

    return "Done"


@ input_error
def birthday(list):  # list contains lists of possible actions to add
    # print(list)
    if len(contact_book) == 0:
        return "contact book is empty"
    output = ""
    for record in list:
        words = record.split()
        days = int(words[1])
        for contact in contact_book.iterator():
            contact_record = contact[0]
            name = contact_record.name.value
            # print(date.today() + timedelta(days=58))
            if contact_record.days_to_birthday() == days:
                output += name + " "
    return "birthday have: " + output


def start_notes(list=[]):  # list contains lists of possible actions to add
    print(">> do you want to start working with notes ?[y/n]")
    reponse = input(">> ").lower()
    if reponse == "y":
        CLINotes.run_notes()
    return "continue with address book again"


def command_parser(line):
    return re.findall("add[ ]+[a-zA-Z]+[ ]+[+][1-9][(][0-9]{3}[)][0-9]{3}-[0-9]{4}", line)


PARSER = {
    HELLO_CMD: lambda x: re.findall(HELLO_CMD, x),
    ADD_CMD: lambda x: re.findall(ADD_CMD + "[ ]*[a-zA-Z0-9\+\-()]*[ ]*[a-zA-Z0-9\+\-()]*", x),
    CHANGE_CMD: lambda x: re.findall(CHANGE_CMD + "[ ]*[a-zA-Z0-9\+\-()]*[ ]*[a-zA-Z0-9\+\-()]*", x),
    PHONE_CMD: lambda x: re.findall(PHONE_CMD + "[ ]*[a-zA-Z0-9\+\-()]*", x),
    EMAIL_CMD: lambda x: re.findall(EMAIL_CMD + "[ ]*[a-zA-Z0-9\+\-()]*", x),
    SHOW_CMD: lambda x: re.findall(SHOW_CMD + "[ ]*[a-zA-Z0-9\+\-()]*", x),
    HLP_CMD: lambda x: re.findall(HLP_CMD, x),
    SRCH_CMD: lambda x: re.findall(SRCH_CMD + "[ ]*[a-zA-Z0-9\+\-()]*", x),
    EDT_CMD: lambda x: re.findall(EDT_CMD + "[ ]*[a-zA-Z0-9\+\-()]*", x),
    RMV_CMD: lambda x: re.findall(RMV_CMD + "[ ]*[a-zA-Z0-9\+\-()]*", x),
    CONGRAT_CMD: lambda x: re.findall(
        CONGRAT_CMD + "[ ]*[a-zA-Z0-9\+\-()]*", x),
    NOTES_CMD: lambda x: re.findall(NOTES_CMD, x)
}

RESPONSE = {
    HELLO_CMD: greet,
    ADD_CMD: add_contact,
    CHANGE_CMD: change,
    PHONE_CMD: phone,
    EMAIL_CMD: email,
    SHOW_CMD: show,
    HLP_CMD: help,
    SRCH_CMD: search,
    EDT_CMD: edit,
    RMV_CMD: remove,
    CONGRAT_CMD: birthday,
    NOTES_CMD: start_notes
}


start_command_note = {
    "notes": CLINotes.run_notes
}

contact_book = AddressBook()  # address book of contacts


def main():
    global contact_book

    # window = Logo_Image()
    # window.run()
    print("\n\n>> working directory: " + os.getcwd()+"\n\n")

    if (os.path.exists(ADRESSBOOK)):
        contact_book.read_from_file(ADRESSBOOK)
        print(colored(">> address book was succesfully read", "yellow"))
        # contact_book.print()
    else:
        out_address_book_not = colored(
            f">> address book {ADRESSBOOK} was not found", "red")
        print(out_address_book_not)

    while True:
        line = input(">> ").lower()
        if line in exit_list:
            print(">> Good bye!")
            break
        else:
            for word in COMMANDS:
                command_list = PARSER[word](line)
                if len(command_list):
                    handler = RESPONSE[word]
                    print(">> " + str(handler(command_list)))

    out_save = colored(">> address book saved to ", "yellow")
    out_address_book = colored(ADRESSBOOK, "red")
    print(out_save + out_address_book)
    contact_book.save_to_file(ADRESSBOOK)

    # start command for notes from class CLINotes
    # command = input("Enter notes for write them: ").strip()
    # if command == '':
    #     raise SystemError(
    #         "\nThank you for using Volkan.\nSee you later! Take care of yourself!\n")

    # if command in start_command_note.keys():
    #     handler = start_command_note[command]
    #     answer = handler()
    #     print(answer)

    # print("Incorrect input.\nPlease check and enter correct command -> help.")


# print(check_phone("+386478617006"))
# print(check_name("+1(647)861 wrwf"))
# line = "add Alisa +16478617006 show all"
# command_line = PARSER["add"](line)
# handler = RESPONSE["add"]
# print(handler(command_line))
# 3command_line = PARSER["show"](line)
# handler = RESPONSE["show"]
# print(handler(command_line))
# wait()
if __name__ == "__main__":
    main()
