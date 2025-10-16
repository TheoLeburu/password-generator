import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import pyperclip
from password_generator import PasswordGenerator
from password_evaluator import PasswordEvaluator


class PasswordGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Password Generator")
        self.root.geometry("600x700")
        self.root.resizable(True, True)

        self.generator = PasswordGenerator()
        self.evaluator = PasswordEvaluator()

        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        style = ttk.Style()
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
        style.configure("Title.TLabel", background="#f0f0f0", font=("Arial", 16, "bold"))
        style.configure("Strength.TLabel", font=("Arial", 12, "bold"))
        style.configure("TButton", font=("Arial", 10))
        style.configure("TCheckbutton", background="#f0f0f0")

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        title_label = ttk.Label(main_frame, text="Secure Password Generator", style="Title.TLabel")
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        ttk.Label(main_frame, text="Password Length:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.length_var = tk.IntVar(value=12)
        length_scale = ttk.Scale(main_frame, from_=6, to=32, variable=self.length_var,
                                 orient=tk.HORIZONTAL, command=self.update_length_label)
        length_scale.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)

        self.length_label = ttk.Label(main_frame, text="12")
        self.length_label.grid(row=1, column=2, padx=(10, 0), pady=5)

        ttk.Label(main_frame, text="Character Types:").grid(row=2, column=0, sticky=tk.W, pady=10)

        options_frame = ttk.Frame(main_frame)
        options_frame.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        self.lower_var = tk.BooleanVar(value=True)
        self.upper_var = tk.BooleanVar(value=True)
        self.digit_var = tk.BooleanVar(value=True)
        self.symbol_var = tk.BooleanVar(value=True)

        ttk.Checkbutton(options_frame, text="Lowercase (a-z)", variable=self.lower_var).grid(row=0, column=0,
                                                                                             sticky=tk.W)
        ttk.Checkbutton(options_frame, text="Uppercase (A-Z)", variable=self.upper_var).grid(row=0, column=1,
                                                                                             sticky=tk.W)
        ttk.Checkbutton(options_frame, text="Digits (0-9)", variable=self.digit_var).grid(row=1, column=0, sticky=tk.W)
        ttk.Checkbutton(options_frame, text="Symbols (!@#$)", variable=self.symbol_var).grid(row=1, column=1,
                                                                                             sticky=tk.W)

        ttk.Label(main_frame, text="Number of Passwords:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.count_var = tk.IntVar(value=1)
        count_combo = ttk.Combobox(main_frame, textvariable=self.count_var, values=[1, 5, 10, 20], state="readonly")
        count_combo.grid(row=3, column=1, sticky=tk.W, pady=5)

        generate_btn = ttk.Button(main_frame, text="Generate Passwords", command=self.generate_passwords)
        generate_btn.grid(row=4, column=0, columnspan=3, pady=20)

        ttk.Label(main_frame, text="Generated Passwords:").grid(row=5, column=0, sticky=tk.W, pady=(10, 5))

        self.password_text = scrolledtext.ScrolledText(main_frame, width=50, height=4, font=("Courier", 10))
        self.password_text.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)

        copy_btn = ttk.Button(main_frame, text="Copy to Clipboard", command=self.copy_to_clipboard)
        copy_btn.grid(row=7, column=0, columnspan=3, pady=5)

        ttk.Label(main_frame, text="Password Strength Evaluation:").grid(row=8, column=0, sticky=tk.W, pady=(20, 5))

        self.eval_entry = ttk.Entry(main_frame, font=("Arial", 11), width=40)
        self.eval_entry.grid(row=9, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        self.eval_entry.bind('<KeyRelease>', self.evaluate_password)

        eval_btn = ttk.Button(main_frame, text="Evaluate", command=self.evaluate_password)
        eval_btn.grid(row=9, column=2, padx=(10, 0), pady=5)

        self.strength_label = ttk.Label(main_frame, text="Enter a password to evaluate", style="Strength.TLabel")
        self.strength_label.grid(row=10, column=0, columnspan=3, sticky=tk.W, pady=(10, 5))

        self.feedback_text = scrolledtext.ScrolledText(main_frame, width=50, height=6, font=("Arial", 9))
        self.feedback_text.grid(row=11, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)

        main_frame.columnconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

    def update_length_label(self, value):
        self.length_label.config(text=str(int(float(value))))

    def generate_passwords(self):
        try:
            length = self.length_var.get()
            count = self.count_var.get()

            if not any([self.lower_var.get(), self.upper_var.get(),
                        self.digit_var.get(), self.symbol_var.get()]):
                messagebox.showerror("Error", "Please select at least one character type")
                return

            passwords = self.generator.generate_multiple_passwords(
                count, length,
                self.lower_var.get(),
                self.upper_var.get(),
                self.digit_var.get(),
                self.symbol_var.get()
            )

            self.password_text.delete(1.0, tk.END)
            for i, password in enumerate(passwords, 1):
                self.password_text.insert(tk.END, f"{i:2d}. {password}\n")

            if passwords:
                self.eval_entry.delete(0, tk.END)
                self.eval_entry.insert(0, passwords[0])
                self.evaluate_password()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate passwords: {str(e)}")

    def copy_to_clipboard(self):
        password = self.password_text.get(1.0, tk.END).strip()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Success", "Password copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No password to copy")

    def evaluate_password(self, event=None):
        password = self.eval_entry.get().strip()

        if not password:
            self.strength_label.config(text="Enter a password to evaluate", foreground="black")
            self.feedback_text.delete(1.0, tk.END)
            return

        result = self.evaluator.evaluate_strength(password)

        self.strength_label.config(text=f"Strength: {result['strength']}",
                                   foreground=result['color'])

        self.feedback_text.delete(1.0, tk.END)
        for feedback in result['feedback']:
            self.feedback_text.insert(tk.END, f"• {feedback}\n")

        self.feedback_text.insert(tk.END, f"\nScore: {result['score']}/{result['max_score']}")
        if result['entropy'] > 0:
            self.feedback_text.insert(tk.END, f"\nEstimated Entropy: {result['entropy']} bits")