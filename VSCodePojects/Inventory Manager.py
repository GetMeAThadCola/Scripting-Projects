import tkinter as tk
from tkinter import ttk
import sqlite3

# Create a SQLite database or connect to an existing one
conn = sqlite3.connect('inventory.db')
cursor = conn.cursor()

# Create an inventory table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        location TEXT NOT NULL,
        serial_number TEXT,
        device_type TEXT,
        brand TEXT,
        notes TEXT,
        assigned TEXT NOT NULL
    )
''')
conn.commit()

# Create a Tkinter window
root = tk.Tk()
root.title("Inventory Manager")

# Define functions for adding, deleting, and searching items
def add_item():
    name = entry_name.get()
    location = entry_location.get()
    serial_number = entry_serial_number.get()
    device_type = entry_device_type.get()
    brand = entry_brand.get()
    notes = entry_notes.get()
    assigned = entry_assignment.get()

    # Insert the item data into the database
    cursor.execute('''
        INSERT INTO inventory (name, location, serial_number, device_type, brand, notes, assigned)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (name, location, serial_number, device_type, brand, notes, assigned))
    conn.commit()
    clear_fields()
    update_display()

def delete_item():
    selected_item = listbox.curselection()
    if selected_item:
        item_id = listbox.get(selected_item[0]).split(',')[0].split(': ')[1]
        cursor.execute('DELETE FROM inventory WHERE id = ?', (item_id,))
        conn.commit()
        update_display()

def search_item():
    criteria = entry_search.get()
    cursor.execute('''
        SELECT * FROM inventory WHERE name LIKE ? OR location LIKE ? OR assigned LIKE ?
    ''', (f"%{criteria}%", f"%{criteria}%", f"%{criteria}%"))
    items = cursor.fetchall()
    display_search_results(items)

def clear_fields():
    entry_name.delete(0, tk.END)
    entry_location.delete(0, tk.END)
    entry_serial_number.delete(0, tk.END)
    entry_device_type.delete(0, tk.END)
    entry_brand.delete(0, tk.END)
    entry_notes.delete(0, tk.END)
    entry_assignment.delete(0, tk.END)

def update_display():
    cursor.execute('SELECT * FROM inventory')
    items = cursor.fetchall()
    display_search_results(items)

def display_search_results(items):
    listbox.delete(0, tk.END)
    for item in items:
        listbox.insert(tk.END, f"ID: {item[0]}, Name: {item[1]}, Location: {item[2]}, Serial: {item[3]}, Type: {item[4]}, Brand: {item[5]}, Notes: {item[6]}, Assigned: {item[7]}")

# Create GUI components
frame = ttk.Frame(root)
frame.pack(padx=10, pady=10)

label = ttk.Label(frame, text="Inventory Manager", font=("Helvetica", 16), background="green", foreground="white")
label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

label_name = ttk.Label(frame, text="Name:", foreground="black")
label_name.grid(row=1, column=0, sticky="w")
entry_name = ttk.Entry(frame)
entry_name.grid(row=1, column=1)

label_location = ttk.Label(frame, text="Location:", foreground="black")
label_location.grid(row=2, column=0, sticky="w")
entry_location = ttk.Entry(frame)
entry_location.grid(row=2, column=1)

label_serial_number = ttk.Label(frame, text="Serial Number:", foreground="black")
label_serial_number.grid(row=3, column=0, sticky="w")
entry_serial_number = ttk.Entry(frame)
entry_serial_number.grid(row=3, column=1)

label_device_type = ttk.Label(frame, text="Device Type:", foreground="black")
label_device_type.grid(row=4, column=0, sticky="w")
entry_device_type = ttk.Entry(frame)
entry_device_type.grid(row=4, column=1)

label_brand = ttk.Label(frame, text="Brand:", foreground="black")
label_brand.grid(row=5, column=0, sticky="w")
entry_brand = ttk.Entry(frame)
entry_brand.grid(row=5, column=1)

label_notes = ttk.Label(frame, text="Notes:", foreground="black")
label_notes.grid(row=6, column=0, sticky="w")
entry_notes = ttk.Entry(frame)
entry_notes.grid(row=6, column=1)

label_assignment = ttk.Label(frame, text="Assignment (yes/no):", foreground="black")
label_assignment.grid(row=7, column=0, sticky="w")
entry_assignment = ttk.Entry(frame)
entry_assignment.grid(row=7, column=1)

add_button = ttk.Button(frame, text="Add Item", command=add_item)
add_button.grid(row=8, column=0, pady=10)

delete_button = ttk.Button(frame, text="Delete Item", command=delete_item)
delete_button.grid(row=8, column=1, pady=10)

label_search = ttk.Label(frame, text="Search:", foreground="black")
label_search.grid(row=9, column=0, sticky="w")
entry_search = ttk.Entry(frame)
entry_search.grid(row=9, column=1)

search_button = ttk.Button(frame, text="Search Inventory", command=search_item)
search_button.grid(row=9, column=2, pady=10)

listbox = tk.Listbox(frame, width=80, height=10)
listbox.grid(row=10, column=0, columnspan=3, padx=10, pady=10)

# Update the display to show all items in the beginning
update_display()

# Run the Tkinter main loop
root.mainloop()

# Close the database connection when done
conn.close()
