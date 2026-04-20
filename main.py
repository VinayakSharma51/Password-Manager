import json
import random
import pyperclip
from tkinter import *
from tkinter import messagebox


FONT_STYLE = ("Arial", 10, "bold")


# PASSWORD GENERATOR
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = []

    for char in range(random.randint(8, 10)):
        password_list.append(random.choice(letters))

    for num in range(random.randint(2, 4)):
        password_list.append(random.choice(numbers))

    for sym in range(random.randint(2, 4)):
        password_list.append(random.choice(symbols))

    random.shuffle(password_list)

    password = "".join(password_list)

    password_input.delete(0, END)
    password_input.insert(0, password)
    pyperclip.copy(password)

# SAVE PASSWORD
def save():
    website = website_input.get().title()
    email = username_input.get()
    password = password_input.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")

    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \n"
                                                              f"Email: {email} \n"
                                                              f"Password: {password} \n"
                                                              f"Is it ok to save?")

        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    data = json.load(data_file)             # Reading old data
            except (FileNotFoundError, json.JSONDecodeError):
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                data.update(new_data)                       # Updating old data with new data
                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)    # Saving updated data
            finally:
                website_input.delete(0, END)
                password_input.delete(0, END)


# SEARCH WEBSITE
def search_website():
    website = website_input.get().title()

    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found!")
    else:
        if website in data:
            messagebox.showinfo(
                title=website,
                message=f"Email: {data[website]["email"]}\n"
                        f"Password: {data[website]["password"]}"
            )
        else:
            messagebox.showinfo(title="Not Found", message=f"No records for '{website} exists.'")


# UI SETUP
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_image)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website:", font=FONT_STYLE, pady=3)
website_label.grid(column=0, row=1)
username_label = Label(text="Email/Username:", font=FONT_STYLE, pady=3)
username_label.grid(column=0, row=2)
password_label = Label(text="Password:", font=FONT_STYLE, pady=3)
password_label.grid(column=0, row=3)

# Entries
website_input = Entry(width=35)
website_input.grid(column=1, row=1)
website_input.focus()
username_input = Entry(width=55)
username_input.grid(column=1, row=2, columnspan=2)
username_input.insert(0, "vinayaksharma@gmail.com")
password_input = Entry(width=35)
password_input.grid(column=1, row=3)

# Buttons
search_website_btn = Button(
    text="Search",
    font=("Arial", 9, "bold"),
    width=16,
    bd=1,
    relief="groove",
    highlightthickness=0,
    bg=window.cget("bg"),
    activebackground=window.cget("bg"),
    fg="gray25",
    cursor="hand2",
    highlightbackground="gray80",
    command=search_website
)
search_website_btn.grid(column=2, row=1, columnspan=2)

generate_password_btn = Button(
    text="Generate Password",
    font=("Arial", 9, "bold"),
    bd=1,
    relief="groove",
    highlightthickness=0,
    bg=window.cget("bg"),
    activebackground=window.cget("bg"),
    fg="gray25",
    cursor="hand2",
    highlightbackground="gray80",
    command=generate_password
)
generate_password_btn.grid(column=2, row=3, columnspan=2)

add_btn = Button(
    text="Add",
    font=FONT_STYLE,
    width=41,
    bd=1,
    relief="groove",
    highlightthickness=0,
    bg=window.cget("bg"),
    activebackground=window.cget("bg"),
    fg="gray20",
    cursor="hand2",
    highlightbackground="gray80",
    command=save
)
add_btn.grid(column=1, row=4, columnspan=2)

window.mainloop()
