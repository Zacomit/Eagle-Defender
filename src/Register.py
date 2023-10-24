import tkinter as tk
from tkinter import filedialog
import re
from PIL import Image, ImageTk
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
import os

# Global variables
second_page_frame = None
private_key = None
public_key = None
rsa_private_key = None

# Function to handle the registration button on the first page
def continue_to_page2():
    # Validate the username and password before moving to the second page
    username = username_entry.get()
    password = password_entry.get()

    # Regular expressions to validate the username and password
    username_pattern = r"^(?!.*[\W_])(?!.*\d.*\d.*\d.*\d.*\d)(?!.*\b(?:ass|clit|fag|fuck|shit)\b)[A-Za-z0-9]{1,15}$"
    password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,}$"

    if re.match(username_pattern, username) and re.match(password_pattern, password):
        # Both fields are valid; you can continue to the second page
        username_label.pack_forget()
        username_entry.pack_forget()
        password_frame.pack_forget()
        age_label.pack_forget()
        age_entry.pack_forget()
        email_label.pack_forget()
        email_entry.pack_forget()
        select_image_button.pack_forget()
        register_button.pack_forget()
        image_label.pack_forget()

        # Show the second page
        show_page2()
    else:
        # At least one of the fields doesn't meet the constraints
        tk.messagebox.showerror("Error", "Please check that the fields meet the constraints.")

# Function to show the second page
def show_page2():
    global question_entries, second_page_frame

    if second_page_frame:
        second_page_frame.pack_forget()

    second_page_frame = tk.Frame(window)
    second_page_frame.pack(pady=10)

    second_page_label = tk.Label(second_page_frame, text="Second Page")
    second_page_label.pack(pady=10)

    questions = [
        "First pet",
        "First teacher",
        "Country you want to live in",
        "Childhood nickname",
        "Favorite football team"
    ]

    for question_text in questions:
        question_label = tk.Label(second_page_frame, text=question_text)
        question_label.pack(pady=10)
        question_entry = tk.Entry(second_page_frame)
        question_entry.pack(pady=10)
        question_entries.append(question_entry)

    next_to_page3_button = tk.Button(second_page_frame, text="Continue to Third Page", command=show_page3)
    next_to_page3_button.pack(pady=10)

# Function to show the third page
def show_page3():
    global question_entries, second_page_frame

    if second_page_frame:
        second_page_frame.pack_forget()

    questions = [
        "Card Number",
        "Expiration Date",
        "Security Code (CVV)"
    ]

    for question_text in questions:
        question_label = tk.Label(window, text=question_text)
        question_label.pack(pady=10)
        question_entry = tk.Entry(window)
        question_entry.pack(pady=10)
        question_entries.append(question_entry)

    # Add an image on the third page
    image = Image.open("images/promo.jpg")
    image = image.resize((500, 600))  # Adjust the image size as needed
    image = ImageTk.PhotoImage(image)

    image_label = tk.Label(window, image=image)
    image_label.image = image  # Make sure to keep a reference to the image object
    image_label.pack(pady=10)

    save_button = tk.Button(window, text="Save Data", command=save_data)
    save_button.pack(pady=10)

# Function to return to the first page
def return_to_page1():
    for entry in question_entries:
        entry.pack_forget()
    second_page_frame.pack_forget()

    username_label.pack(pady=10)
    username_entry.pack(pady=10)
    password_frame.pack(pady=10)
    age_label.pack(pady=10)
    age_entry.pack(pady=10)
    email_label.pack(pady=10)
    email_entry.pack(pady=10)
    select_image_button.pack(pady=10)
    register_button.pack(pady=10)
    image_label.pack(pady=10)

# Function to select a profile picture
def select_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
    if file_path:
        image_label.config(text="Selected Image: " + file_path)

def toggle_password_visibility():
    if password_entry.cget("show") == "":
        password_entry.config(show="\u25CA")
        show_password_button.config(image=show_eye_icon)
    else:
        password_entry.config(show="")
        show_password_button.config(image=hide_eye_icon)

def save_data():
    # Get the data from the form
    username = username_entry.get()
    password = password_entry.get()
    age = age_entry.get()
    email = email_entry.get()

    selected_questions = [
        "Card Number",
        "Expiration Date",
        "Security Code (CVV)"
    ]

    question_answers = {}
    for question, entry in zip(selected_questions, question_entries):
        question_answers[question] = entry.get()

    # Save the data to a temporary file
    with open('temp_user_data.txt', 'w') as file:
        file.write(f"Username: {username}\n")
        file.write(f"Password: {password}\n")
        file.write(f"Age: {age}\n")
        file.write(f"Email: {email}\n")
        file.write("Security Questions:\n")
        for question in selected_questions:
            file.write(f"- {question}: {question_answers.get(question, '')}\n")

    # Encrypt the data with the RSA public key
    with open('temp_user_data.txt', 'rb') as file:
        data_to_encrypt = file.read()
        encrypted_data = public_key.encrypt(
            data_to_encrypt,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    # Save the encrypted data to a file
    with open('user_data_encrypted.bin', 'wb') as encrypted_file:
        encrypted_file.write(encrypted_data)

    # Remove the temporary file
    os.remove('temp_user_data.txt')
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)
public_key = private_key.public_key()

window = tk.Tk()
window.title("Registration Form")
window.attributes('-fullscreen', True)

username_label = tk.Label(window, text="Username:")
username_label.pack(pady=10)
username_entry = tk.Entry(window)
username_entry.pack(pady=10)

password_frame = tk.Frame(window)
password_frame.pack(pady=10)

password_label = tk.Label(password_frame, text="Password:")
password_label.pack(side="left")
password_entry = tk.Entry(password_frame, show="*")
password_entry.pack(side="left")

show_eye_icon = Image.open("images/ojo1.png")
show_eye_icon.thumbnail((20, 20))
show_eye_icon = ImageTk.PhotoImage(show_eye_icon)

hide_eye_icon = Image.open("images/ojo2.png")
hide_eye_icon.thumbnail((20, 20))
hide_eye_icon = ImageTk.PhotoImage(hide_eye_icon)

show_password_button = tk.Button(password_frame, image=show_eye_icon, command=toggle_password_visibility)
show_password_button.pack(side="right")

age_label = tk.Label(window, text="Age:")
age_label.pack(pady=10)
age_entry = tk.Entry(window)
age_entry.pack(pady=10)

email_label = tk.Label(window, text="Email:")
email_label.pack(pady=10)
email_entry = tk.Entry(window)
email_entry.pack(pady=10)

image_label = tk.Label(window, text="Selected Image: ")
image_label.pack(pady=10)

select_image_button = tk.Button(window, text="Select Profile Image", command=select_image)
select_image_button.pack(pady=10)

register_button = tk.Button(window, text="Continue", command=continue_to_page2)
register_button.pack(pady=10)

question_entries = []

window.mainloop()