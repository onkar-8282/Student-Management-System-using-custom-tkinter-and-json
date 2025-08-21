import tkinter as tk

def create_admin_login_page(root, go_back, login_callback):
    bg_color = '#273b7a'

    # Load icons
    admin_login_icon = tk.PhotoImage(file='icons/admin_img.png')
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
    heading_lb = tk.Label(frame, text="Admin Portal Login",
                          font=('bold', 18), bg=bg_color, fg='white')
    heading_lb.place(x=0, y=0, width=1200)

    # Back button
    back_btn = tk.Button(frame, text="←", font=('bold', 20), bd=0,
                         fg=bg_color, command=go_back)
    back_btn.place(x=12, y=40)

    # Admin icon
    admin_icon_lb = tk.Label(frame, image=admin_login_icon, bd=0)
    admin_icon_lb.place(x=550, y=65)

    # Admin ID
    id_number_lb = tk.Label(frame, text="Admin ID Number:", font=('bold', 15),
                            fg=bg_color, bd=0)
    id_number_lb.place(x=480, y=180)
    id_number_ent = tk.Entry(frame, font=('bold', 15), justify=tk.CENTER,
                             highlightcolor=bg_color, highlightbackground='gray', highlightthickness=2)
    id_number_ent.place(x=480, y=215)

    # Password
    password_lb = tk.Label(frame, text="Password:", font=('bold', 15),
                           fg=bg_color, bd=0)
    password_lb.place(x=480, y=255)
    password_ent = tk.Entry(frame, font=('bold', 15), justify=tk.CENTER,
                            highlightcolor=bg_color, highlightbackground='gray',
                            highlightthickness=2, show="*")
    password_ent.place(x=480, y=290)

    # Show/hide password button
    show_hide_btn = tk.Button(frame, image=locked_icon, bd=0,
                              command=show_hide_password)
    show_hide_btn.place(x=720, y=290)

    # Login button (calls login_callback from main.py)
    login_btn = tk.Button(
        frame,
        text="Login",
        font=('bold', 15),
        bg=bg_color,
        fg='white',
        command=lambda: login_callback(id_number_ent, password_ent)
    )
    login_btn.place(x=520, y=350, width=140, height=35)

    # Configure frame size
    frame.pack_propagate(False)
    frame.configure(width=1200, height=720)

    # Keep image references
    frame.images = [admin_login_icon, locked_icon, unlocked_icon]

    return frame
