import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

class ATM:
    def __init__(self, root, username):
        self.root = root
        self.root.title("ATM Interface")
        self.root.geometry("400x350")
        self.root.resizable("False","False")
        self.root.configure(bg="#2c3e50")

        self.username = username
        self.users = self.load_users()  # Load users and balances from the JSON file
        self.balance = self.users[self.username]["balance"]  # Load the current user's balance

        # Create and place widgets
        self.label = tk.Label(root, text="ATM Interface", font=("Arial", 20, "bold"), bg="#2c3e50", fg="#ecf0f1")
        self.label.pack(pady=20)

        self.balance_label = tk.Label(root, text=f"Balance: ₹{self.balance}", font=("Arial", 16), bg="#2c3e50", fg="#ecf0f1")
        self.balance_label.pack(pady=10)

        self.button_frame = tk.Frame(root, bg="#2c3e50")
        self.button_frame.pack(pady=20)

        self.deposit_button = tk.Button(self.button_frame, text="Deposit", font=("Arial", 14), command=self.deposit, bg="#27ae60", fg="#ecf0f1", width=10)
        self.deposit_button.grid(row=0, column=0, padx=10, pady=5)

        self.withdraw_button = tk.Button(self.button_frame, text="Withdraw", font=("Arial", 14), command=self.withdraw, bg="#c0392b", fg="#ecf0f1", width=10)
        self.withdraw_button.grid(row=0, column=1, padx=10, pady=5)

        self.transfer_button = tk.Button(self.button_frame, text="Transfer", font=("Arial", 14), command=self.transfer, bg="#f39c12", fg="#ecf0f1", width=10)
        self.transfer_button.grid(row=1, column=0, padx=10, pady=5)

        self.exit_button = tk.Button(root, text="Exit", font=("Arial", 14), command=root.quit, bg="#34495e", fg="#ecf0f1", width=10)
        self.exit_button.pack(pady=10)

    def load_users(self):
        """Load users and their balances from a json file."""
        if os.path.exists("users.json"):
            with open("users.json", "r") as file:
                return json.load(file)
        return {}

    def save_users(self):
        """Save updated user balances to the json file."""
        with open("users.json", "w") as file:
            json.dump(self.users, file)

    def update_balance(self):
        """Update the displayed balance and save to JSON."""
        self.balance_label.config(text=f"Balance: ₹{self.balance}")
        self.users[self.username]["balance"] = self.balance  # Update the current user's balance
        self.save_users()

    def deposit(self):
        amount = self.get_amount("Deposit Amount")
        if amount:
            self.balance += amount
            self.update_balance()

    def withdraw(self):
        amount = self.get_amount("Withdraw Amount")
        if amount:
            if amount > self.balance:
                messagebox.showerror("Error", "Insufficient funds!")
            else:
                self.balance -= amount
                self.update_balance()

    def transfer(self):
        """Transfer money to another user's account."""
        recipient = simpledialog.askstring("Transfer", "Enter recipient's username:")
        
        if recipient and recipient != self.username:
            if recipient in self.users:
                amount = self.get_amount(f"Amount to transfer to {recipient}")
                if amount:
                    if amount > self.balance:
                        messagebox.showerror("Error", "Insufficient funds!")
                    else:
                        self.balance -= amount
                        self.users[recipient]["balance"] += amount
                        self.update_balance()
                        messagebox.showinfo("Success", f"₹{amount} transferred to {recipient}.")
            else:
                messagebox.showerror("Error", "Recipient does not exist!")
        else:
            messagebox.showerror("Error", "Invalid recipient!")

    def get_amount(self, prompt):
        """Get amount input from the user."""
        amount_str = simpledialog.askstring("Input", prompt)
        if amount_str:
            try:
                amount = float(amount_str)
                if amount <= 0:
                    raise ValueError
                return amount
            except ValueError:
                messagebox.showerror("Error", "Invalid amount!")
        return None

class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("500x350")
        self.root.resizable("False","False")
        self.root.configure(bg="#2c3e50")

        # Load users from json file
        self.users = self.load_users()

        self.username_label = tk.Label(root, text="Username:", font=("Arial", 14), bg="#2c3e50", fg="#ecf0f1")
        self.username_label.pack(pady=10)
        self.username_entry = tk.Entry(root, font=("Arial", 14))
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(root, text="Password:", font=("Arial", 14), bg="#2c3e50", fg="#ecf0f1")
        self.password_label.pack(pady=10)
        self.password_entry = tk.Entry(root, font=("Arial", 14), show="*")
        self.password_entry.pack(pady=5)

        self.login_button = tk.Button(root, text="Login", font=("Arial", 14), command=self.login, bg="#27ae60", fg="#ecf0f1", width=10)
        self.login_button.pack(pady=10)

        self.register_button = tk.Button(root, text="Register", font=("Arial", 14), command=self.register, bg="#2980b9", fg="#ecf0f1", width=10)
        self.register_button.pack(pady=10)

    def load_users(self):
        """Load users from a json file."""
        if os.path.exists("users.json"):
            with open("users.json", "r") as file:
                return json.load(file)
        return {}

    def save_users(self):
        """Save users to the json file."""
        with open("users.json", "w") as file:
            json.dump(self.users, file)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if "password" in self.users[username] and self.users[username]["password"] == password:
            messagebox.showinfo("Success", "Login successful!")
            self.root.destroy()
            main(username)
        else:
            messagebox.showerror("Error", "Invalid username or password!")

    def register(self):
        username = simpledialog.askstring("Register", "Enter new username:")
        password = simpledialog.askstring("Register", "Enter new password:", show="*")

        if username and password:
            if username in self.users:
                messagebox.showerror("Error", "Username already exists!")
            else:
                self.users[username] = {"password": password, "balance": 0}
                self.save_users()
                messagebox.showinfo("Success", "Registration successful! Please log in.")
        else:
            messagebox.showerror("Error", "Registration failed! Please try again.")

def main(username):
    root = tk.Tk()
    atm = ATM(root, username)
    root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    login_page = LoginPage(root)
    root.mainloop()
