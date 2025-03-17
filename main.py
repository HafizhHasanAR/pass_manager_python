from tkinter import * # → Untuk membuat GUI.
import string
from tkinter import messagebox
from random import shuffle, choice, randint
import pyperclip # → Untuk menyalin password ke clipboard secara otomatis.
import os
import random
import json




def search_password():
    """Mencari dan menampilkan password berdasarkan input website"""
    website = website_entry.get().strip().lower()  # Ambil input & ubah ke huruf kecil

    if not website:
        messagebox.showwarning("Warning", "Please enter a website name!")
        return

    # Cari lokasi file password_manager_master.json
    data_file_path = find_data_json("password_manager_master.json")

    if not data_file_path:
        messagebox.showwarning("Warning", "File 'password_manager_master.json' not found!")
        return

    try:
        with open(data_file_path, "r") as data_file: # Buka file JSON
            data = json.load(data_file)
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Error reading JSON file. The file may be corrupted.")
        return

    # Konversi semua kunci (nama website) ke lowercase untuk pencarian
    matched_key = next((key for key in data if key.lower() == website), None)

    if matched_key:
        email = data[matched_key]["email"]
        password = data[matched_key]["password"]
        messagebox.showinfo("Password", f"Email: {email}\nPassword: {password}")
        pyperclip.copy(password)  # Salin password ke clipboard
    else:
        messagebox.showwarning("Warning", f"Data for '{website}' not found!")

    website_entry.delete(0, END)

# ---------------------------- FIND password_manager_master.json FILE ------------------------------- #

def find_data_json(filename="password_manager_master.json"):
    """Mencari file JSON di semua drive Windows jika tidak ditemukan di direktori saat ini"""

    # Cek apakah file sudah ada di direktori saat ini
    if os.path.exists(filename):
        return filename

    # Deteksi semua drive yang tersedia
    drives = [f"{d}:/" for d in string.ascii_uppercase if os.path.exists(f"{d}:/")]

    print(f"🔍 Searching for '{filename}' in all drives... (this may take time)")

    for drive in drives:
        print(f"📂 Scanning drive: {drive}")

        try:
            for root, dirs, files in os.walk(drive): # Iterasi semua file di drive
                if filename in files:
                    full_path = os.path.join(root, filename) # Path lengkap file
                    print(f"✅ File found: {full_path}")
                    return full_path  # Kembalikan path file
        except PermissionError:
            print(f"⚠️ Access Denied: {drive} (Skipping)")

    print(f"❌ '{filename}' not found in any drive!")
    return None


# ---------------------------- OPEN password_manager_master.json FILE ------------------------------- #

def open_data_file():
    """Membuka file password_manager_master.json jika ditemukan"""
    data_file_path = find_data_json()
    
    if data_file_path:
        os.startfile(data_file_path)  # Membuka file dengan aplikasi default
    else:
        messagebox.showwarning("File Not Found", "File 'password_manager_master.json' not found in any drive!")

        

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
    
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showwarning(title="Oops", message="Please don't leave any fields empty!")
    else:
        try:
            with open("password_manager_master.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("password_manager_master.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open("password_manager_master.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)
            show_success_message()

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
Label(text="Powered by Hafizh Hasan", font=("Arial", 10, "italic")).grid(row=6, column=1, columnspan=2, sticky="se", padx=5, pady=5)

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


find_file_button = Button(text="Find Data File", width=36, command=open_data_file)
find_file_button.grid(row=5, column=1, columnspan=2, pady=10)

search_password_button = Button(text="Search", width=10, command=search_password)
search_password_button.grid(row=1, column=2, padx=5, pady=5)

window.mainloop() # → Membuat window menjadi aktif.

