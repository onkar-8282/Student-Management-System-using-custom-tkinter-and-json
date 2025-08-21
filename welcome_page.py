import tkinter as tk
import customtkinter as ctk

def create_welcome_page(root, show_student_login, show_admin_login, show_sign_up):
    bg_color = "#273b7a"

    student_login_icon = tk.PhotoImage(file='icons/login_student.png')
    admin_login_icon = tk.PhotoImage(file='icons/admin_img.png')
    add_student_icon = tk.PhotoImage(file='icons/add_student_img.png')

    frame = tk.Frame(root, highlightbackground=bg_color, highlightthickness=1)

    # Heading
    heading = tk.Label(frame, text="Student Management\nSystem", font=('bold', 18),
                       bg=bg_color, fg='white')
    heading.place(x=0, y=0, width=550)

    # Student Login
    student_login_btn = tk.Button(frame, text="Student Login", font=('bold', 15),
                                  bd=0, bg=bg_color, fg='white', command=show_student_login)
    student_login_btn.place(x=180, y=125, width=260)
    student_login_img = tk.Button(frame, image=student_login_icon, bd=0,
                                  command=show_student_login)
    student_login_img.place(x=60, y=100)

    # Admin Login
    admin_login_btn = tk.Button(frame, text="Admin Login", font=('bold', 15),
                                bd=0, bg=bg_color, fg='white', command=show_admin_login)
    admin_login_btn.place(x=180, y=250, width=260)
    admin_login_img = tk.Button(frame, image=admin_login_icon, bd=0,
                                command=show_admin_login)
    admin_login_img.place(x=60, y=225)

    # Sign Up
    add_student_btn = tk.Button(frame, text="Sign Up", font=('bold', 15),
                                bd=0, bg=bg_color, fg='white', command=show_sign_up)
    add_student_btn.place(x=180, y=375, width=260)
    add_student_img = tk.Button(frame, image=add_student_icon, bd=0,
                                command=show_sign_up)
    add_student_img.place(x=60, y=350)

    frame.pack_propagate(False)
    frame.configure(width=550, height=570)
    frame.place( x = 25 , y = 59)
    # Keep image references
    frame.images = [student_login_icon, admin_login_icon, add_student_icon]

    return frame

