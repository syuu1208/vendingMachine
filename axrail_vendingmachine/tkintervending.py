import tkinter as tk
from tkinter import PhotoImage, messagebox
from decimal import Decimal

# possible notes/coins in  100x cents
ringgit = [10000, 5000, 2000, 1000, 500, 100, 50, 20, 10, 5, 1]

class VendingMachine:
    def __init__(self, root):
        self.root = root
        self.root.title("Vending Machine")

        self.items = {
            'cola': 150,
            'juice': 100,
            'water': 125,
            'coffee': 200
        }

        # initiate balance to 0
        self.balance = tk.DoubleVar()
        self.balance.set(0.0)

        self.images = {
            'cola': self.resize_image('soft-drink.png', 50, 50),
            'juice': self.resize_image('juice-box.png', 50, 50),
            'water': self.resize_image('water.png', 50, 50),
            'coffee': self.resize_image('coffee-cup.png', 50, 50)
        }

        # embed image for each drink
        for item, image in self.images.items():
            button = tk.Button(root, image=image, command=lambda i=item, p=self.items[item]: self.select_item(i, p))
            button.image = image
            button.pack()

            # price label
            price_label = tk.Label(root, text=f"RM{self.items[item]/100:.2f}")
            price_label.pack()

        # balance label
        self.label_balance = tk.Label(root, text="Current balance: RM0.00", width=20)
        self.label_balance.pack()

        # reads money input
        self.entry_money = tk.Entry(root)
        self.entry_money.pack()

        # insert money button
        self.button_insert = tk.Button(root, text="Insert Money", command=self.insert_money)
        self.button_insert.pack()

    # resize all the images into (50,50)
    def resize_image(self, filename, width, height):
        original_image = PhotoImage(file=filename)
        resized_image = original_image.subsample(int(original_image.width() / width), int(original_image.height() / height))
        return resized_image

    # update balance. decimal module used for precision
    def insert_money(self):
        try:
            amount = Decimal(self.entry_money.get()) * 100 
            self.balance.set(Decimal(self.balance.get()) + amount)
            self.label_balance.config(text=f"Current Balance: RM{self.balance.get() / 100:.2f}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid number.")

    # select drink then update change
    def select_item(self, item, price):
        if self.balance.get() >= price:
            self.balance.set(self.balance.get() - price)
            self.change()
        else:
            messagebox.showerror("Insufficient funds", "Please insert more money.")

    # refresh balance and display change
    def change(self):
        change_amount = self.balance.get()
        available_notes = ringgit
        returned_notes = self.give_change(change_amount, available_notes)

        # check if there is any change 
        if returned_notes:
            self.balance.set(0.0)
            self.label_balance.config(text="Current balance: RM0.00")

            message = "Change:\n"
            for note in returned_notes:
                message += f"RM{note / 100:.2f}\n" 
            messagebox.showinfo("Change: ", message)

        else: 
            self.balance.set(0.0)
            self.label_balance.config(text="Current balance: RM0.00")

    # calculate to get the least number of notes/coincs
    def give_change(self, amount, available_notes):
        returned_notes = []
        for note in available_notes:
            while amount >= note:
                amount -= note
                returned_notes.append(note)
        return returned_notes


def main():
    root = tk.Tk()
    VendingMachine(root)
    root.mainloop()


if __name__ == "__main__":
    main()
