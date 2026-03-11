import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import qrcode
import pyttsx3

engine = pyttsx3.init()
qr_data = ""
qr_history = []

# Generate qr-code
def generate_qr():
    global qr_data
    data = entry.get().strip()

    if not data:
        messagebox.showerror("Input Error", "Please enter some text or URL!")
        return

    if data not in qr_history:
        qr_history.append(data)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=5,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="#FF0000", back_color="white").convert("RGB")
# Adding logo
    logo_path = "pngegg.png"
    try:
        logo = Image.open(logo_path)
        logo = logo.convert("RGBA")
        logo_width = qr_img.size[0] // 6
        logo_height = qr_img.size[1] // 6
        logo = logo.resize((logo_width, logo_height))
        position = ((qr_img.size[0] - logo_width) // 2, (qr_img.size[1] - logo_height) // 2)
        qr_img.paste(logo, position, logo)
    except FileNotFoundError:
        print("Logo file not found, proceeding without logo.")

    qr_img_tk = ImageTk.PhotoImage(qr_img)
    label.config(image=qr_img_tk)
    label.image = qr_img_tk
    qr_data = data

# History tracking
def show_history():
    history_window = tk.Toplevel(root)
    history_window.title("QR Code History")
    history_window.geometry("300x400")

    history_listbox = tk.Listbox(history_window, height=15, width=40)
    history_listbox.pack(pady=20)

    for item in qr_history:
        history_listbox.insert(tk.END, item)

    def on_select(event):
        selected_data = history_listbox.get(history_listbox.curselection())
        entry.delete(0, tk.END)
        entry.insert(tk.END, selected_data)

    history_listbox.bind("<<ListboxSelect>>", on_select)
    clear_history_button = ttk.Button(history_window, text="Clear History", command=clear_history)
    clear_history_button.pack(pady=10)

# Reading qr-code
def read_qr_data():
    if qr_data:
        engine.say(qr_data)
        engine.runAndWait()
    else:
        messagebox.showinfo("No Data", "No QR Code generated yet!")

# Clearing entry
def clear_entry():
    entry.delete(0, tk.END)
    label.config(image="")
    global qr_data
    qr_data = ""
    messagebox.showinfo("Cleared", "Input and QR code cleared successfully!")

# Clearing history
def clear_history():
    global qr_history
    qr_history.clear()
    messagebox.showinfo("History Cleared", "QR Code history cleared successfully!")

# Making GUI
root = tk.Tk()
root.title("QR Code Generator")
root.geometry("400x500")

# Adding Background
image_path = "backgroundImage.jpg"
bg_image = Image.open(image_path)
bg_image = bg_image.resize((1400, 1400))
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Add heading
heading = ttk.Label(root, text="QR Code Generator", font=("Arial", 20, "bold"),width=20,foreground="white", background="#032956", anchor="center")
heading.pack(pady=20)

# Making Entry box
entry = ttk.Entry(root, width=40, font=("Arial", 14), justify="center")
entry.pack(pady=5, ipady=5)

# Making custom style for Buttons
style = ttk.Style()
style.configure("Rounded.TButton", font=("Arial", 10, "bold"), padding=8)

# Adding Buttons
generate_button = ttk.Button(root, text="Generate QR Code", style="Rounded.TButton", command=generate_qr)
generate_button.pack(pady=10)

tts_button = ttk.Button(root, text="Read QR Data", style="Rounded.TButton", command=read_qr_data)
tts_button.pack(pady=10)

history_button = ttk.Button(root, text="Show History", style="Rounded.TButton", command=show_history)
history_button.pack(pady=10)

clear_button = ttk.Button(root, text="Clear", style="Rounded.TButton", command=clear_entry)
clear_button.pack(pady=10)

# Adding labels
label = ttk.Label(root, background="#032956")
label.pack(pady=10)

root.mainloop()