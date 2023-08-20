#!/usr/bin/env python3
# This code belongs to HUNTER CARBONE
print("THIS CODE IS PROPERTY OF HUNTER CARBONE")

import hashlib
import os
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

def calculate_hash(filename, algorithm):
    hash_function = getattr(hashlib, algorithm)()
    with open(filename, "rb") as f:
        while chunk := f.read(8192):
            hash_function.update(chunk)
    return hash_function.hexdigest()

def compare_files():
    global file1, file2, chosen_algorithm

    if not file1 or not file2:
        result_label.config(text="Please select both files.")
        return

    hash_file1 = calculate_hash(file1, chosen_algorithm)
    hash_file2 = calculate_hash(file2, chosen_algorithm)

    if hash_file1 == hash_file2:
        result_label.config(text="Identical files")
    else:
        result_label.config(text="There are differences")

    prev_hash_choice = messagebox.askyesno("Previous Hash", "Do you want to provide a previous hash for comparison?")
    if prev_hash_choice:
        prev_hash = simpledialog.askstring("Previous Hash", "Enter the previous hash value:")
        if prev_hash == hash_file1:
            result_label.config(text=f"Previous hash matches hash of {file1}")
        elif prev_hash == hash_file2:
            result_label.config(text=f"Previous hash matches hash of {file2}")
        else:
            result_label.config(text="Previous hash does not match either file")

    verbose_choice = messagebox.askyesno("Verbose Mode", "Do you want to enable verbose mode?")
    if verbose_choice:
        verbose_result.set(f"Hash of {file1}: {hash_file1}\nHash of {file2}: {hash_file2}")

    log_choice = messagebox.askyesno("Log Results", "Do you want to save the results to a log file?")
    if log_choice:
        log_file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        with open(log_file, "a") as f:
            f.write(f"Comparison between {file1} and {file2}\n")
            f.write(f"Hash of {file1}: {hash_file1}\n")
            f.write(f"Hash of {file2}: {hash_file2}\n")

            if hash_file1 != hash_file2:
                f.write("There are differences\n")
            else:
                f.write("Identical files\n")

        result_label.config(text=f"Results saved to {log_file}")

        # Clear GUI and exit
        root.quit()

def select_file_1():
    global file1
    file1 = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
    if file1:
        file1_label.config(text=f"Selected file: {os.path.basename(file1)}")

def select_file_2():
    global file2
    file2 = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
    if file2:
        file2_label.config(text=f"Selected file: {os.path.basename(file2)}")

def select_algorithm(value):
    global chosen_algorithm
    chosen_algorithm = value

def main():
    global root, file1_label, file2_label, result_label, verbose_result

    root = tk.Tk()
    root.title("File Integrity Checker")

    algorithm_var = tk.StringVar()
    chosen_algorithm = None

    algorithm_label = tk.Label(root, text="Choose a hash algorithm:")
    algorithm_label.pack()

    algorithms = [
        ("MD5", "md5"),
        ("SHA-1", "sha1"),
        ("SHA-256", "sha256"),
        ("SHA-512", "sha512")
    ]

    for text, value in algorithms:
        tk.Radiobutton(root, text=text, variable=algorithm_var, value=value, command=lambda v=value: select_algorithm(v)).pack()

    file1_button = tk.Button(root, text="Select File 1", command=select_file_1)
    file1_button.pack()

    file1_label = tk.Label(root, text="Selected file: None")
    file1_label.pack()

    file2_button = tk.Button(root, text="Select File 2", command=select_file_2)
    file2_button.pack()

    file2_label = tk.Label(root, text="Selected file: None")
    file2_label.pack()

    compare_button = tk.Button(root, text="Compare Files", command=compare_files)
    compare_button.pack()

    result_label = tk.Label(root, text="")
    result_label.pack()

    verbose_result = tk.StringVar()
    verbose_label = tk.Label(root, textvariable=verbose_result)
    verbose_label.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
