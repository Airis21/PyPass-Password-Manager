from Package.modules import passgen, save_login, ui_setup as ui
import pyperclip

FONT = ("arial", 10, "bold")
DEFAULT_EMAIL = "email@gmail.com"


def on_generate_password():
    length = ui.get_pass_len()
    use_numbers = ui.include_numbers()
    use_symbols = ui.include_symbols()
    gen_pass = generator.generate_password(length=length, use_numbers=use_numbers, use_symbols=use_symbols)
    ui.set_password(gen_pass)
    pyperclip.copy(gen_pass)

def on_save_command():
    username = ui.get_username_entry()
    website = ui.get_web_entry()
    password = ui.get_password()
    save_manager.save_password(website=website, username=username, password=password)
    ui.clear_fields()


if __name__ == "__main__":
    ui = ui.MainWindow(DEFAULT_EMAIL)
    generator = passgen.PassGen()
    save_manager = save_login.SaveLogin()

    ui.create_labels(FONT)
    ui.create_menu()
    ui.create_buttons(gen_command=on_generate_password, save_command=on_save_command)

    ui.main_loop()
