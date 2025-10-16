import re
from typing import Dict


class PasswordEvaluator:
    def __init__(self):
        self.common_passwords = {
            '123456', 'password', '12345678', 'qwerty', '123456789',
            '12345', '1234', '111111', '1234567', 'dragon',
            '123123', 'baseball', 'abc123', 'football', 'monkey',
            'letmein', 'shadow', 'master', '666666', 'qwertyuiop'
        }

    def evaluate_strength(self, password: str) -> Dict[str, any]:
        if not password:
            return self._create_result("Very Weak", 0, "Password is empty")

        score = 0
        feedback = []

        length = len(password)
        if length >= 12:
            score += 3
        elif length >= 8:
            score += 2
        elif length >= 6:
            score += 1
        else:
            feedback.append("Password is too short (minimum 6 characters recommended)")

        has_lowercase = bool(re.search(r'[a-z]', password))
        has_uppercase = bool(re.search(r'[A-Z]', password))
        has_digits = bool(re.search(r'\d', password))
        has_symbols = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))

        if has_lowercase:
            score += 1
        if has_uppercase:
            score += 1
        if has_digits:
            score += 1
        if has_symbols:
            score += 2

        if password.lower() in self.common_passwords:
            score = 0
            feedback.append("This is a very common password")

        if self._has_sequential_chars(password):
            score -= 1
            feedback.append("Contains sequential characters")

        if self._has_repeated_chars(password):
            score -= 1
            feedback.append("Contains repeated character patterns")

        charset_size = 0
        if has_lowercase: charset_size += 26
        if has_uppercase: charset_size += 26
        if has_digits: charset_size += 10
        if has_symbols: charset_size += 32

        if charset_size > 0:
            entropy = length * (charset_size.bit_length())
        else:
            entropy = 0

        if score >= 8:
            strength = "Very Strong"
            color = "#00ff00"
        elif score >= 6:
            strength = "Strong"
            color = "#7cfc00"
        elif score >= 4:
            strength = "Good"
            color = "#ffa500"
        elif score >= 2:
            strength = "Weak"
            color = "#ff4500"
        else:
            strength = "Very Weak"
            color = "#ff0000"

        if score >= 6:
            if length >= 12:
                feedback.append("✓ Good length")
            if has_lowercase and has_uppercase:
                feedback.append("✓ Mixed case letters")
            if has_digits:
                feedback.append("✓ Contains numbers")
            if has_symbols:
                feedback.append("✓ Contains symbols")

        return self._create_result(strength, score, feedback, color, entropy)

    def _has_sequential_chars(self, password: str) -> bool:
        for i in range(len(password) - 2):
            if (ord(password[i + 1]) == ord(password[i]) + 1 and
                    ord(password[i + 2]) == ord(password[i]) + 2):
                return True
        return False

    def _has_repeated_chars(self, password: str) -> bool:
        return bool(re.search(r'(.)\1{2,}', password))

    def _create_result(self, strength: str, score: int, feedback, color: str = "#000000", entropy: int = 0) -> Dict[
        str, any]:
        if isinstance(feedback, str):
            feedback = [feedback]
        return {
            'strength': strength,
            'score': score,
            'max_score': 10,
            'feedback': feedback,
            'color': color,
            'entropy': entropy
        }