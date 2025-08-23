import tkinter as tk
from tkinter import messagebox, ttk
import json, os

def create_add_student_page(root, go_back):
    bg_color = '#273b7a'
    branch_list = ['CO', 'IT', 'EE', 'ME', 'CE', 'ET']

    # Load icons
    locked_icon = tk.PhotoImage(file='icons/locked_img.png')
    unlocked_icon = tk.PhotoImage(file='icons/unlocked.png')

    student_gender = tk.StringVar(value="Male")

    frame = tk.Frame(root, highlightbackground=bg_color, highlightthickness=1)

    # Heading
    heading = tk.Label(frame, text="Enter Your Information", font=('bold', 18),
                       bg=bg_color, fg='white')
    heading.place(x=0, y=0, width=1200)

    # Show/hide password function
    def show_hide_password():
        if account_password_ent['show'] == "*":
            account_password_ent.config(show='')
            show_hide_btn.config(image=unlocked_icon)
        else:
            account_password_ent.config(show="*")
            show_hide_btn.config(image=locked_icon)

    # --- Form Fields ---
    id_no_ent = tk.Entry(frame, font=('bold', 15),
                                 highlightcolor=bg_color, highlightbackground='gray', highlightthickness=2)
    tk.Label(frame, text="Enter Your Student Id Number :", font=('bold', 12)).place(x=400, y=70)
    id_no_ent.place(x=620, y=70, width=200)

    #student_name_ent = tk.Entry(frame, font=('bold', 15),
    #                            highlightcolor=bg_color, highlightbackground='gray', highlightthickness=2)
    # First Name
    student_first_name_ent = tk.Entry(frame, font=('bold', 15),
                                      highlightcolor=bg_color, highlightbackground='gray', highlightthickness=2)
    tk.Label(frame, text="Enter First Name:", font=('bold', 12)).place(x=400, y=120)
    student_first_name_ent.place(x=620, y=120, width=200)

    # Last Name
    student_last_name_ent = tk.Entry(frame, font=('bold', 15),
                                     highlightcolor=bg_color, highlightbackground='gray', highlightthickness=2)
    tk.Label(frame, text="Enter Last Name:", font=('bold', 12)).place(x=400, y=170)
    student_last_name_ent.place(x=620, y=170, width=200)

    tk.Label(frame, text="Select Your Gender:", font=('bold', 12)).place(x=400, y=220)
    tk.Radiobutton(frame, text="Male", font=('bold', 12), variable=student_gender, value="Male").place(x=620, y=220)
    tk.Radiobutton(frame, text="Female", font=('bold', 12), variable=student_gender, value="Female").place(x=620, y=240)
    tk.Radiobutton(frame, text="Others", font=('bold', 12), variable=student_gender, value="Others").place(x=620, y=260)

    # Branch Selection
    tk.Label(frame, text="Select Course:", font=('bold', 12)).place(x=400, y=300)
    course_cmb = ttk.Combobox(frame, values=branch_list, font=('bold', 12), state="readonly")
    course_cmb.place(x=620, y=300, width=200)
    course_cmb.set(branch_list[0])

    # Email
    student_email_ent = tk.Entry(frame, font=('bold', 15),
                                 highlightcolor=bg_color, highlightbackground='gray', highlightthickness=2)
    tk.Label(frame, text="Enter Your Email:", font=('bold', 12)).place(x=400, y=360)
    student_email_ent.place(x=620, y=360, width=300)

    # Password
    account_password_ent = tk.Entry(frame, font=('bold', 15),
                                    highlightcolor=bg_color, highlightbackground='gray', highlightthickness=2, show="*")
    tk.Label(frame, text="Password:", font=('bold', 12)).place(x=400, y=410)
    account_password_ent.place(x=620, y=410, width=190)

    show_hide_btn = tk.Button(frame, image=locked_icon, bd=0, command=show_hide_password, bg='white')
    show_hide_btn.place(x=820, y=408)

    # --- Submit Function ---
    def submit_student(id_no=None):
        id_no = id_no_ent.get().strip()
        first_name = student_first_name_ent.get().strip()
        last_name = student_last_name_ent.get().strip()
        gender = student_gender.get()
        course = course_cmb.get().strip()
        email = student_email_ent.get().strip()
        password = account_password_ent.get().strip()

        # Validation
        if not id_no or not first_name or not last_name or not course or not email or not password:
            messagebox.showerror("Error", "All fields are required!")
            return

        if "@" not in email or "." not in email:
            messagebox.showerror("Error", "Invalid email format!")
            return

        # Load existing data
        if os.path.exists("admin.json"):
            with open("admin.json", "r") as f:
                data = json.load(f)
        else:
            data = {"students": []}

        # Check duplicate enrollment
        for s in data["students"]:
            if s["id"] == id_no:
                messagebox.showerror("Error", "ID number already exists!")
                return

        # Add new student
        new_student = {
            "id": id_no,
            "first_name": first_name,
            "last_name": last_name,
            "gender": gender,
            "Course": course,
            "email": email,
            "password": password,  # store hashed password
        }
        data["students"].append(new_student)

        # Save back
        with open("admin.json", "w") as f:
            json.dump(data, f, indent=4)

        messagebox.showinfo("Success", f"Student {first_name} added successfully!")

        # Clear form after success
        id_no_ent.delete(0, tk.END)
        student_first_name_ent.delete(0, tk.END)
        student_last_name_ent.delete(0, tk.END)
        student_email_ent.delete(0, tk.END)
        account_password_ent.delete(0, tk.END)
        course_cmb.current(0)
        student_gender.set("Male")

        go_back()  # return to welcome page after success

    # --- Buttons ---
    home_btn = tk.Button(frame, text="Home", font=('bold', 15), bd=0, bg='red', fg='white', command=go_back)
    home_btn.place(x=570, y=505, width=80, height=35)

    submit_btn = tk.Button(frame, text="Submit", font=('bold', 15), bd=0, bg='green', fg='white',
                           command=submit_student)
    submit_btn.place(x=700, y=505, width=80, height=35)

    frame.pack_propagate(False)
    frame.configure(width=1200, height=720)

    # Keep image references
    frame.images = [locked_icon, unlocked_icon]

    return frame
