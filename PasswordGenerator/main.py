import tkinter as tk
from password_gui import PasswordGeneratorGUI

def main():
    try:
        root = tk.Tk()
        app = PasswordGeneratorGUI(root)
        root.mainloop()
    except Exception as e:
        print(f"Failed to start application: {e}")

if __name__ == "__main__":
    main()