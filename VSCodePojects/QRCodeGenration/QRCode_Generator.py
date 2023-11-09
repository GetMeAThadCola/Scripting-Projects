import tkinter as tk
from tkinter import messagebox, filedialog
import qrcode
from PIL import Image, ImageTk

def generate_and_display_qr_code():
    url = url_entry.get()
    if url:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        img = img.resize((300, 300))  # Resize the image to display

        img_tk = ImageTk.PhotoImage(img)
        qr_label.config(image=img_tk)
        qr_label.image = img_tk

        save_button = tk.Button(root, text="Save QR Code", command=lambda: save_qr_code(img))
        save_button.pack()
    else:
        messagebox.showerror("Error", "Please enter a URL.")

def save_qr_code(img):
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])

    if file_path:
        img.save(file_path)
        messagebox.showinfo("QR Code Saved", "QR code saved successfully.")

root = tk.Tk()
root.title("QR Code Generator")

url_label = tk.Label(root, text="Enter URL:")
url_label.pack()
url_entry = tk.Entry(root)
url_entry.pack()

generate_button = tk.Button(root, text="Generate and Display QR Code", command=generate_and_display_qr_code)
generate_button.pack()

qr_label = tk.Label(root)
qr_label.pack()

root.mainloop()
