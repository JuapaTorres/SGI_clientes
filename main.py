import tkinter as tk
from src.gui import InterfazCliente

def main():
    root = tk.Tk()
    app = InterfazCliente(root)
    root.mainloop()

if __name__ == "__main__":
    main()