import secrets
import string
from typing import List


class PasswordGenerator:
    def __init__(self):
        self.character_sets = {
            'lowercase': string.ascii_lowercase,
            'uppercase': string.ascii_uppercase,
            'digits': string.digits,
            'symbols': string.punctuation
        }

    def generate_password(self, length: int, use_lowercase: bool, use_uppercase: bool,
                          use_digits: bool, use_symbols: bool) -> str:
        if length < 4:
            raise ValueError("Password length must be at least 4 characters")

        character_pool = ""
        if use_lowercase:
            character_pool += self.character_sets['lowercase']
        if use_uppercase:
            character_pool += self.character_sets['uppercase']
        if use_digits:
            character_pool += self.character_sets['digits']
        if use_symbols:
            character_pool += self.character_sets['symbols']

        if not character_pool:
            raise ValueError("At least one character type must be selected")

        password_chars = []
        if use_lowercase:
            password_chars.append(secrets.choice(self.character_sets['lowercase']))
        if use_uppercase:
            password_chars.append(secrets.choice(self.character_sets['uppercase']))
        if use_digits:
            password_chars.append(secrets.choice(self.character_sets['digits']))
        if use_symbols:
            password_chars.append(secrets.choice(self.character_sets['symbols']))

        remaining_length = length - len(password_chars)
        for _ in range(remaining_length):
            password_chars.append(secrets.choice(character_pool))

        secrets.SystemRandom().shuffle(password_chars)
        return ''.join(password_chars)

    def generate_multiple_passwords(self, count: int, length: int, use_lowercase: bool,
                                    use_uppercase: bool, use_digits: bool, use_symbols: bool) -> List[str]:
        passwords = []
        for _ in range(count):
            passwords.append(self.generate_password(length, use_lowercase, use_uppercase, use_digits, use_symbols))
        return passwords