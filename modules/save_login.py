from tkinter import messagebox
import os
import json

DOCS_PATH = os.path.expanduser("~/Documents")

class SaveLogin:
    def __init__(self):
        """Uses or creates a data_file.json inside the current user's documents folder"""
        self.data_file = os.path.join(DOCS_PATH,"data.json")

    def save_password(self, website: str, username: str, password: str) -> None:
        """Saves entries to data_file.json
        requires user entry fields - website, username, password
        creates message boxes for detected empty fields and for confirming saving data
        """
        # User input
        website, username, password = website.strip(), username.strip(), password.strip()


        # Validation
        if len(website) == 0 or len(password) == 0:
            messagebox.showinfo(title="Error", message="Website or Password fields cannot be empty.")
            return
        else:
            # Confirmation message
            is_ok = messagebox.askokcancel(title="Confirmation",
                                   message=f"You are saving: \n\nLocation: {website} \nUsername: {username} "
                                           f"\nPassword: {password}  \n\nIs this ok?")

            # Prep json data structure
            nested_data = {
                website: {
                    "username": username,
                    "password": password,
                }
            }

            if is_ok:
                try:
                    # Read existing data
                    with open(file=self.data_file, mode="r") as data:
                        js_data = json.load(data)
                except FileNotFoundError:
                    # If no data, create a new empty dict
                    js_data = {}

                    # Update dict with new data
                js_data.update(nested_data)

                    # Write to file with indentation
                with open(file=self.data_file, mode="w") as data:
                    json.dump(js_data, data, indent=4)

# Test case
# save_manager = SaveLogin("test.json")
# save_pass = save_manager.save_password("web","user","pass")