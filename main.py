from tkinter import * # → Untuk membuat GUI.
from tkinter import messagebox
from random import shuffle, choice, randint
import pyperclip # → Untuk menyalin password ke clipboard secara otomatis.
import os
import random




# search password manager

def search():
    website = website_entry.get().strip() # → Mengambil inputan di website_entry.

    if not website:
        messagebox.showwarning(title="Oops", message="Please enter a website name.")
        return

    try:
        with open("data.txt", "r") as data_file:
            for line in data_file:
                parts = line.strip().split(" | ") # → Membagi data berdasarkan " | ".
                if len(parts) == 3 and parts[0].lower() == website.lower(): # → Cek apakah website yang dicari ada di file.
                    email, password = parts[1], parts[2]
                    messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
                    pyperclip.copy(password)  # Salin password ke clipboard
                    return

        messagebox.showwarning(title="Not Found", message=f"No details for {website} found.")

    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No Data File Found")
    except Exception as e:
        messagebox.showerror(title="Error", message=f"An unexpected error occurred.\nError: {e}")
    




# ---------------------------- OPEN FILE ------------------------------- #

def open_file():
    try:
        if os.path.exists("data.txt"):  # Cek apakah file ada
            os.system("notepad.exe data.txt")  # Buka dengan Notepad di Windows
        else:
            messagebox.showwarning("Warning", "File 'data.txt' not found!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open file.\nError: {e}")

# ---------------------------- SHOW SUCCESS MESSAGE ------------------------------- #

def show_success_message():
    success_popup = Toplevel(window)  # Buat window kecil
    success_popup.title("Success")
    success_popup.geometry("250x100")  # Atur ukuran popup
    success_popup.resizable(False, False)

    Label(success_popup, text="Data saved successfully!", font=("Arial", 10)).pack(pady=20)

    # Tutup otomatis dalam 1 detik
    window.after(1000, success_popup.destroy)

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_symbols = [random.choice(symbols) for _ in range(random.randint(2, 4))]
    password_numbers = [random.choice(numbers) for _ in range(random.randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)  

    password= "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)





# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    website = website_entry.get().strip()
    email = email_entry.get().strip()
    password = password_entry.get().strip()

    if not website or not password:
        messagebox.showwarning(title="Oops", message="Please fill in all fields.")
        return

    is_ok = messagebox.askokcancel(
        title=website, 
        message=f"These are the details entered:\nEmail: {email}\nPassword: {password}\nSave?"
    )

    if is_ok:
        try:
            with open("data.txt", "a") as data_file:
                data_file.write(f"{website} | {email} | {password}\n") # → Menulis data ke file.
            show_success_message()
            website_entry.delete(0, END) # → Menghapus inputan di website_entry.
            email_entry.delete(0, END) # → Menghapus inputan di email_entry.
            password_entry.delete(0, END) # → Menghapus inputan di password_entry.
        except Exception as e:
            messagebox.showerror(title="Error", message=f"Failed to save data.\nError: {e}")

# ---------------------------- UI SETUP ------------------------------- #

window = Tk() # → Membuat window baru.
window.title("Password Manager")
window.config(padx=50, pady=50)

# Logo
canvas = Canvas(width=200, height=200, highlightthickness=0)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1, pady=10)

# Labels
Label(text="Website:").grid(row=1, column=0, sticky="e", padx=5, pady=5) # → Sticky="e" → Membuat label ke kanan.
Label(text="Email/Username:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
Label(text="Password:").grid(row=3, column=0, sticky="e", padx=5, pady=5)

# Entries
website_entry = Entry(width=33)
website_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
website_entry.focus()

email_entry = Entry(width=33)
email_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")


password_entry = Entry(width=21)
password_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

# Buttons
generate_password_button = Button(text="Generate", width=10, command=generate_password) # → Command → Menjalankan fungsi generate_password.
generate_password_button.grid(row=3, column=2, padx=5, pady=5)

add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2, pady=10)

open_file_button = Button(text="Open File", width=36, command=open_file)
open_file_button.grid(row=5, column=1, columnspan=2, pady=10)

search_password_button = Button(text="Search", width=10, command=search)
search_password_button.grid(row=1, column=2, padx=5, pady=5)

window.mainloop() # → Membuat window menjadi aktif.

