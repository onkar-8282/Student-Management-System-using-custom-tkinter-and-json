import tkinter as tk
from tkinter import messagebox
import json

def create_add_student_page(root, show_welcome):
    bg_color = "#273b7a"

    frame = tk.Frame(root, highlightbackground=bg_color, highlightthickness=1)

    # ------------------ Heading ------------------
    heading = tk.Label(
        frame,
        text="Create Student Account",
        font=('bold', 18),
        bg=bg_color,
        fg="white",
        anchor="center"
    )
    heading.pack(fill="x")   # ✅ full width bar

    # ------------------ First Name ------------------
    tk.Label(frame, text="First Name:", font=('bold', 13), bg="white").place(x=140, y=160)
    fname_entry = tk.Entry(frame, font=(13))
    fname_entry.place(x=270, y=160, width=200)

    # ------------------ Password ------------------
    tk.Label(frame, text="Password:", font=('bold', 13), bg="white").place(x=140, y=220)
    pw_entry = tk.Entry(frame, font=(13), show="*")
    pw_entry.place(x=270, y=220, width=200)

    # ------------------ Sign Up Action ------------------
    def signup_action():
        new_student = {
            "id": fname_entry.get().strip().lower(),
            "first_name": fname_entry.get().strip(),
            "password": pw_entry.get().strip()
        }

        try:
            with open("students.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {"students": []}

        data["students"].append(new_student)

        with open("students.json", "w") as f:
            json.dump(data, f, indent=4)

        messagebox.showinfo("Success", "Student Registered Successfully")
        show_welcome()

    signup_btn = tk.Button(frame, text="Sign Up", font=('bold', 13),
                           bg=bg_color, fg="white", command=signup_action)
    signup_btn.place(x=220, y=300, width=120)

    # ------------------ Back Button ------------------
    back_btn = tk.Button(frame, text="← Back", font=('bold', 11),
                         command=show_welcome, bd=0, bg="white", fg=bg_color)
    back_btn.place(x=10, y=10)

    frame.pack_propagate(False)
    frame.configure(width=550, height=570, bg="white")
    return frame
