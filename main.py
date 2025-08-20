import customtkinter as ctk
from tkinter import messagebox
from welcome_page import create_welcome_page
from student_login_page import create_student_login_page
from admin_login_page import create_admin_login_page
from add_account_page import create_add_student_page
from student_dashboard import StudentApp
from admin_dashboard import AdminApp
import json


def show_frame(frame):
    frame.tkraise()


# ------------------ DASHBOARD LAUNCHERS ------------------
def launch_student_dashboard(student_id):
    root.destroy()  # close login window
    app = StudentApp(student_id=student_id)  # open student dashboard
    app.mainloop()


def launch_admin_dashboard():
    root.destroy()  # close login window
    app = AdminApp()  # open admin dashboard
    app.mainloop()


# ------------------ MAIN WINDOW ------------------
ctk.set_appearance_mode("light")   # can also be "dark"
ctk.set_default_color_theme("blue")  # blue / green / dark-blue

root = ctk.CTk()
root.geometry("1440x800")
root.title("Student Management System")
root.resizable(False, False)

container = ctk.CTkFrame(root, corner_radius=0)
container.pack(fill="both", expand=True)


# ------------------ Pages ------------------
welcome_page_fm = create_welcome_page(
    container,
    show_student_login=lambda: show_frame(student_login_page_fm),
    show_admin_login=lambda: show_frame(admin_login_page_fm),
    show_sign_up=lambda: show_frame(add_student_page_fm)
)

add_student_page_fm = create_add_student_page(
    container,
    lambda: show_frame(welcome_page_fm)
)

student_login_page_fm = create_student_login_page(
    container,
    lambda: show_frame(welcome_page_fm),
    show_dashboard_callback=launch_student_dashboard
)


# ----------- Admin login logic ------------
def admin_login_action(id_number_ent, password_ent):
    try:
        with open("admin.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        messagebox.showerror("Error", "admin.json not found!")
        return

    admin = data.get("admin", {})

    entered_id = id_number_ent.get().strip()
    entered_pw = password_ent.get().strip()

    if entered_id == admin.get("first_name") and entered_pw == admin.get("password"):
        messagebox.showinfo("Success", "Welcome Admin!")
        launch_admin_dashboard()
    else:
        messagebox.showerror("Login Failed", "Invalid Admin ID or Password")


admin_login_page_fm = create_admin_login_page(
    container,
    lambda: show_frame(welcome_page_fm),
    login_callback=admin_login_action
)


# ------------------ Register all frames ------------------
for frame in (
    welcome_page_fm,
    student_login_page_fm,
    admin_login_page_fm,
    add_student_page_fm,
):
    frame.grid(row=10, column=5, sticky="nsew")

# ------------------ Start ------------------
show_frame(welcome_page_fm)
root.mainloop()
