from tkinter import *
from tkinter import messagebox
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
import random

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

NR_LETTERS = 5
NR_NUMBERS = 5
NR_SYMBOLS = 3


# ---------------------------- GENERATE PASSWORD ------------------------------- #
def generate_password():
    char_list = random.sample(letters, NR_LETTERS)
    char_list += random.sample(numbers, NR_NUMBERS)
    char_list += random.sample(symbols, NR_SYMBOLS)
    random.shuffle(char_list)
    password = ''.join(char_list)
    entry_password.insert(END, password)

    # copy password to clipboard using the cross-platform pyperclip module
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_data_to_file():
    website = entry_website.get()
    email = entry_email.get()
    password = entry_password.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    # empty fields are not acceptable
    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showerror(title="ERROR", message="All fields should be filled out")

    else:
        try:
            with open("my_text.json", mode="r") as my_file:
                data = json.load(my_file)
        except FileNotFoundError:
            with open("my_text.json", mode="w") as my_file:
                json.dump(new_data, my_file, indent=4)
        else:
            data.update(new_data)
            with open("my_text.json", mode="w") as my_file:
                json.dump(data, my_file, indent=4)
        finally:
            clear_inputs()


def read_from_JSON():
    try:
        with open("my_text.json", mode="r") as my_file:
            data = json.load(my_file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No Data File Found")
        return None
    else:
        return data


def clear_inputs():
    entry_website.delete(0, END)
    entry_password.delete(0, END)


# ---------------------------- SEARCH AFTER EXISTING WEBSITE ------------------------------- #
def search_website():
    searched_website = entry_website.get()
    data_from_file = read_from_JSON()

    try:
        messagebox.showinfo(title=searched_website, message=f'Email: {data_from_file[searched_website].get("password")}'
                                                            f'\n\n'
                                                            f'Password: {data_from_file[searched_website].get("password")}')
    except KeyError:
        messagebox.showinfo(title="Info", message="Website not found")
    else:
        pass


# ---------------------------- UI SETUP ------------------------------- #
win = Tk()
win.title("Password Manager")
win.config(padx=20, pady=20, bg="white")

canvas = Canvas(width=200, height=200, bg="white", highlightthickness=0)
lock_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_image)
canvas.grid(column=1, row=0)

label_website = Label(text="Website", bg="white", pady=3)
label_website.grid(column=0, row=1)
entry_website = Entry(width=32)
entry_website.grid(column=1, row=1)
entry_website.focus()
button_search = Button(text="Search", bg="white", width=14, command=search_website)
button_search.grid(column=2, row=1)

label_password = Label(text="Password", bg="white", pady=1)
label_password.grid(column=0, row=3)
entry_password = Entry(width=32)
entry_password.grid(column=1, row=3)
button_generate = Button(text="Generate Password", pady=1, bg="white", command=generate_password)
button_generate.grid(column=2, row=3)

label_email = Label(text="Email", bg="white", pady=1)
label_email.grid(column=0, row=2)
entry_email = Entry(width=50)
entry_email.grid(column=1, row=2, columnspan=2)
entry_email.insert(END, "myemail@ggg.com")

button_add = Button(text="Add", width=42, padx=5, pady=1, bg="white", command=add_data_to_file)
button_add.grid(column=1, row=4, columnspan=3)

win.mainloop()
