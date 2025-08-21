import tkinter as tk
from tkinter import messagebox
import json

def create_student_login_page(root, go_back, show_dashboard_callback=None):
    bg_color = '#273b7a'

    # Load icons
    student_login_icon = tk.PhotoImage(file='icons/login_student.png')
    locked_icon = tk.PhotoImage(file='icons/locked_img.png')
    unlocked_icon = tk.PhotoImage(file='icons/unlocked.png')

    # Create frame
    frame = tk.Frame(root, highlightbackground=bg_color, highlightthickness=1)

    # Show/hide password function
    def show_hide_password():
        if password_ent['show'] == "*":
            password_ent.config(show='')
            show_hide_btn.config(image=unlocked_icon)
        else:
            password_ent.config(show="*")
            show_hide_btn.config(image=locked_icon)

    # Heading
    heading_lb = tk.Label(frame, text="Student Portal Login",
                          font=('bold', 18), bg=bg_color, fg='white')
    heading_lb.place(x=0, y=0, width=1200)

    # Back button
    back_btn = tk.Button(frame, text="←", font=('bold', 20), bd=0,
                         fg=bg_color, command=go_back)
    back_btn.place(x=12, y=40)

    # Student icon
    student_icon_lb = tk.Label(frame, image=student_login_icon, bd=0)
    student_icon_lb.place(x=550, y=65)

    # Student Name
    name_lb = tk.Label(frame, text="Student Name:", font=('bold', 15), fg=bg_color, bd=0)
    name_lb.place(x=480, y=180)
    name_ent = tk.Entry(frame, font=('bold', 15), justify=tk.CENTER,
                        highlightcolor=bg_color, highlightbackground='gray', highlightthickness=2)
    name_ent.place(x=480, y=215)

    # Password
    password_lb = tk.Label(frame, text="Password:", font=('bold', 15), fg=bg_color, bd=0)
    password_lb.place(x=480, y=255)
    password_ent = tk.Entry(frame, font=('bold', 15), justify=tk.CENTER,
                            highlightcolor=bg_color, highlightbackground='gray',
                            highlightthickness=2, show="*")
    password_ent.place(x=480, y=290)

    # Show/hide password button
    show_hide_btn = tk.Button(frame, image=locked_icon, bd=0, command=show_hide_password)
    show_hide_btn.place(x=720, y=290)

    # -----------------
    # Login Function
    # -----------------
    def login_action():
        username = name_ent.get().strip()
        password = password_ent.get().strip()

        try:
            with open("admin.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            messagebox.showerror("Error", "No student records found.")
            return

        for student in data.get("students", []):
            full_name = f"{student['first_name']} {student['last_name']}"
            if full_name.lower() == username.lower() and student["password"] == password:
                messagebox.showinfo("Success", f"Welcome {full_name}!")
                if show_dashboard_callback:
                    show_dashboard_callback(student["id"])  # ✅ pass ID to dashboard
                return

        messagebox.showerror("Login Failed", "Invalid Name or Password")

    # Login button
    login_btn = tk.Button(frame, text="Login", font=('bold', 15),
                          bg=bg_color, fg='white', command=login_action)
    login_btn.place(x=520, y=350, width=140, height=35)

    frame.pack_propagate(False)
    frame.configure(width=1200, height=720)

    # Keep image references
    frame.images = [student_login_icon, locked_icon, unlocked_icon]

    return frame
