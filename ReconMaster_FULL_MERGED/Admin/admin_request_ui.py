import tkinter as tk
from tkinter import messagebox
from admin_request_backend import send_admin_request

def start_ui(user="tester"):
    root = tk.Tk()
    root.title("Admin Hilfe / Anfrage")

    tk.Label(root, text="Deine Email:").grid(row=0, column=0)
    email_entry = tk.Entry(root, width=40)
    email_entry.grid(row=0, column=1)

    tk.Label(root, text="Kategorie:").grid(row=1, column=0)
    category_var = tk.StringVar(value="help")
    tk.OptionMenu(root, category_var, "help", "bug", "feedback").grid(row=1, column=1)

    tk.Label(root, text="Nachricht:").grid(row=2, column=0)
    message_text = tk.Text(root, height=10, width=40)
    message_text.grid(row=2, column=1)

    tk.Label(root, text="Land (ISO-Code z.B. DE):").grid(row=3, column=0)
    country_entry = tk.Entry(root, width=10)
    country_entry.insert(0, "DE")
    country_entry.grid(row=3, column=1)

    def send():
        email = email_entry.get()
        message = message_text.get("1.0", tk.END).strip()
        category = category_var.get()
        country = country_entry.get().upper()

        if not email or not message:
            messagebox.showerror("Fehler", "Email und Nachricht müssen ausgefüllt sein!")
            return

        send_admin_request(user, email, message, category, country)
        messagebox.showinfo("Erfolg", "Anfrage wurde gesendet!")
        email_entry.delete(0, tk.END)
        message_text.delete("1.0", tk.END)

    tk.Button(root, text="Senden", command=send).grid(row=4, column=1)
    root.mainloop()
