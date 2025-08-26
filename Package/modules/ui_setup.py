from tkinter import *
from tkinter import messagebox
from custom_hovertip import CustomTooltipLabel
import os
import sys
import json

DOCS_PATH = os.path.expanduser("~/Documents")

class MainWindow:
    def __init__(self, default_email):
        """Main window and img canvas"""
        self.window = Tk()
        self.window.title("PyPass Password Manager")
        self.window.minsize(width=550, height=400)
        self.window.config(padx=50, pady=50)

        self.length_var = IntVar(value=12)  # default pass length
        self.symbols_var = IntVar(value=1) # default include symbols
        self.numbers_var = IntVar(value=1) # default include numbers

        self.data_file = os.path.join(DOCS_PATH,"data.json")

        self.canvas = Canvas(width=200, height=200, highlightthickness=0)
        self.canvas.grid(row=0, column=0,columnspan=3)
        try:
            # Bundled path uses _MEIPASS Temp
            self.image = os.path.join(sys._MEIPASS, "logo.png")
            self.logo_img = PhotoImage(file=self.image)
            self.canvas.create_image(100, 100, image=self.logo_img)
        except AttributeError:
            # Local/relative path for running in PyCharm IDE
            self.image = "assets/logo.png"
            self.logo_img = PhotoImage(file=self.image)
            self.canvas.create_image(100, 100, image=self.logo_img)
        except TclError:
            # If no image bundled or found when running locally
            messagebox.showinfo(title="Warning", message="No logo found!")

        self.password_entry = Entry(width=32)
        self.password_entry.grid(row=3, column=1,sticky="w")

        self.website_entry = Entry(width=51)
        self.website_entry.grid(row=1, column=1, columnspan=2, sticky="w")
        self.website_entry.focus()

        self.default_email = "email@gmail.com"
        self.email_username_entry = Entry(width=51)
        self.email_username_entry.insert(0,string=default_email)
        self.email_username_entry.grid(row=2, column=1, columnspan=2, sticky="w")


    def set_password(self, gen_pass: str) -> None:
        """Wipes password entry field and inserts a newly generated password"""
        self.password_entry.delete(0, END)
        self.password_entry.insert(0, string=gen_pass)

    def clear_fields(self) -> None:
        """Clears website/password fields and sets focus to the website entry"""
        self.website_entry.delete(0, END)
        self.password_entry.delete(0, END)
        self.website_entry.focus()

    def get_password(self) -> str:
        return self.password_entry.get()

    def get_web_entry(self) -> str:
        return self.website_entry.get()

    def get_username_entry(self) -> str:
        return self.email_username_entry.get()

    def main_loop(self) -> None:
        self.window.mainloop()

    def create_menu(self) -> None:
        """Creates the top level menu on the main window"""
        menu_font = ("",10,"bold")
        menu_bar = Menu(self.window,font=menu_font)
        self.window.config(menu=menu_bar)

        file_menu = Menu(menu_bar, tearoff=False, font=menu_font)
        file_menu.add_command(label="Options", command=self.options_menu)
        file_menu.add_command(label="Open Vault", command=self.vault)

        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.window.destroy)

        menu_bar.add_cascade(label="File", menu=file_menu, underline=0, font=("",20,"bold"))

    def options_menu(self):
        """Creates an options window with a scale and checkboxes for:
        password length, use numbers, use symbols
        """
        options_window = Toplevel(self.window)
        options_window.title("Options")
        options_window.grab_set()
        options_window.focus_set()
        options_window.minsize(width=220,height=200)
        options_window.config(padx=12)

        check_boxes_label = Label(options_window, text="Include Symbols/Numbers?")
        check_boxes_label.grid(row=0, column=0, pady=10, columnspan=2)

        check_boxes_symbols = Checkbutton(options_window, text="!#$%*&", variable=self.symbols_var)
        check_boxes_symbols.grid(row=1, column=0, padx=5)

        check_boxes_numbers = Checkbutton(options_window, text="123456", variable=self.numbers_var)
        check_boxes_numbers.grid(row=1, column=1, padx=5)

        pass_len_label = Label(options_window, text="Set generated password length")
        pass_len_label.grid(row=2, column=0, pady=10, columnspan=2)

        pass_len_select = Scale(options_window, orient="horizontal", from_=8, to=24, variable=self.length_var, length=150)
        pass_len_select.grid(row=3, column=0, pady=10, columnspan=2)

    def vault(self):
        """Displays json data in a vault window with formatting"""
        vault_window = Toplevel(self.window)
        vault_window.title("My Vault")
        vault_window.grab_set()
        vault_window.focus_set()
        vault_window.minsize(width=300,height=400)
        sb = Scrollbar(vault_window)
        sb.pack(side="right", fill="y")

        data_text = Text(vault_window)
        data_text.pack()
        data_text.config(yscrollcommand=sb.set)
        sb.config(command=data_text.yview)

        try:
            with open(file=self.data_file, mode="r") as data:
                content = data.read()
                parsed_json = json.loads(content)
                pretty_json = json.dumps(parsed_json, indent=2)
                data_text.insert(END, pretty_json)
        except FileNotFoundError:
            data_text.insert(END,"No data found")

    def get_pass_len(self) -> int:
        return self.length_var.get()

    def include_numbers(self) -> bool:
        return bool(self.numbers_var.get())

    def include_symbols(self) -> bool:
        return bool(self.symbols_var.get())


    @staticmethod
    def create_labels(font: tuple[str, int, str]) -> None:
        """Creates text labels on the main window
         to the left of the website, email and password entry fields
         """
        website_label = Label(text="Website:", font=font)
        website_label.grid(row=1, column=0)

        email_username_label = Label(text="Username:", font=font)
        email_username_label.grid(row=2, column=0)

        password_label = Label(text="Password:", font=font)
        password_label.grid(row=3, column=0)


    @staticmethod
    def create_buttons(gen_command, save_command) -> None:
        """Creates the gen password and add(save) buttons on the main window"""
        generate_password_button = Button(text="Generate Password", command=gen_command)
        generate_password_button.grid(row=3, column=2)

        CustomTooltipLabel(anchor_widget=generate_password_button,
                           text="Gen password copies to clipboard", hover_delay=0)

        add_button = Button(text="Add to My Vault", width=43, command=save_command)
        add_button.grid(row=4, column=1, columnspan=2)
