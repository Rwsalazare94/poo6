import tkinter as tk
from tkinter import messagebox
import os

CONTACT_FILE = "contacts.txt"

def read_contacts():
    contacts = []
    if os.path.exists(CONTACT_FILE):
        with open(CONTACT_FILE, "r") as file:
            for line in file:
                parts = line.strip().split("!")
                if len(parts) == 2:  # Asegurar que la línea es válida
                    name, number = parts
                    contacts.append((name, number))
    return contacts

def create_contact():
    name = entry_name.get().strip()
    number = entry_number.get().strip()

    if name == "" or number == "":
        messagebox.showwarning("Error", "Los campos no pueden estar vacíos.")
        return

    contacts = read_contacts()
    for contact in contacts:
        if contact[0] == name or contact[1] == number:
            messagebox.showwarning("Error", "El contacto ya existe.")
            return

    with open(CONTACT_FILE, "a") as file:
        file.write(f"{name}!{number}\n")

    messagebox.showinfo("Éxito", "Contacto agregado.")
    clear_fields()
    read_contact_list()

def read_contact_list():
    contacts = read_contacts()
    listbox_contacts.delete(0, tk.END)  # Limpiar la lista
    for contact in contacts:
        listbox_contacts.insert(tk.END, f"{contact[0]} - {contact[1]}")

def update_contact():
    name = entry_name.get().strip()
    number = entry_number.get().strip()

    if name == "" or number == "":
        messagebox.showwarning("Error", "Los campos no pueden estar vacíos.")
        return

    contacts = read_contacts()
    updated = False

    with open(CONTACT_FILE, "w") as file:
        for contact in contacts:
            if contact[0] == name:
                file.write(f"{name}!{number}\n")
                updated = True
            else:
                file.write(f"{contact[0]}!{contact[1]}\n")

    if updated:
        messagebox.showinfo("Éxito", "Contacto actualizado.")
    else:
        messagebox.showwarning("Error", "El contacto no existe.")

    clear_fields()
    read_contact_list()

def delete_contact():
    name = entry_name.get().strip()

    if name == "":
        messagebox.showwarning("Error", "El nombre no puede estar vacío.")
        return

    contacts = read_contacts()
    deleted = False

    with open(CONTACT_FILE, "w") as file:
        for contact in contacts:
            if contact[0] == name:
                deleted = True
            else:
                file.write(f"{contact[0]}!{contact[1]}\n")

    if deleted:
        messagebox.showinfo("Éxito", "Contacto eliminado.")
    else:
        messagebox.showwarning("Error", "El contacto no existe.")

    clear_fields()
    read_contact_list()

def clear_fields():
    entry_name.delete(0, tk.END)
    entry_number.delete(0, tk.END)

def load_selected_contact(event):
    try:
        selected = listbox_contacts.get(listbox_contacts.curselection())  # Obtener selección
        name, number = selected.split(" - ")
        entry_name.delete(0, tk.END)
        entry_name.insert(0, name)
        entry_number.delete(0, tk.END)
        entry_number.insert(0, number)
    except:
        pass

# Crear ventana
root = tk.Tk()
root.title("Agenda de Contactos")
root.geometry("350x350")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(pady=10)

label_name = tk.Label(frame, text="Nombre:")
label_name.grid(row=0, column=0, padx=5, pady=5)
entry_name = tk.Entry(frame, width=30)
entry_name.grid(row=0, column=1, padx=5, pady=5)

label_number = tk.Label(frame, text="Número:")
label_number.grid(row=1, column=0, padx=5, pady=5)
entry_number = tk.Entry(frame, width=30)
entry_number.grid(row=1, column=1, padx=5, pady=5)

button_create = tk.Button(frame, text="Crear", command=create_contact, width=12)
button_create.grid(row=2, column=0, padx=5, pady=5)

button_read = tk.Button(frame, text="Mostrar", command=read_contact_list, width=12)
button_read.grid(row=2, column=1, padx=5, pady=5)

button_update = tk.Button(frame, text="Actualizar", command=update_contact, width=12)
button_update.grid(row=3, column=0, padx=5, pady=5)

button_delete = tk.Button(frame, text="Eliminar", command=delete_contact, width=12)
button_delete.grid(row=3, column=1, padx=5, pady=5)

listbox_contacts = tk.Listbox(root, width=45, height=10)
listbox_contacts.pack(padx=10, pady=10)
listbox_contacts.bind("<<ListboxSelect>>", load_selected_contact)

read_contact_list()
root.mainloop()
