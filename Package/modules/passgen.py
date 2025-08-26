from random import randint, choice, shuffle

class PassGen:
    def __init__(self):
        self.letters: str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.numbers = "0123456789"
        self.symbols = "!@#$%^&*+"


    def generate_password(self, length: int = 12, use_numbers: bool = True, use_symbols: bool = True) -> str:
        """Generates and returns a random password from a selection of
         uppercase & lowercase letters, numbers and symbols.
         """
        chars = list(self.letters)

        if use_numbers:
            chars.extend(self.numbers)

        if use_symbols:
            chars.extend(self.symbols)

        password_list: list[str] = [choice(chars) for _ in range(length)]

        shuffle(password_list)

        return"".join(password_list)

#Test case
# generator = PassGen()
# password = generator.generate_password()
# print(password)
