import customtkinter as ctk
from tkinter import ttk, messagebox
import json, os

FILE = "admin.json"


# ---------------- JSON Helpers ----------------
def load_json():
    if not os.path.exists(FILE):
        data = {
            "students": [],
            "leave_student": [],
            "notifications": [],
            "courses": []
        }
        save_json(data)
        return data
    with open(FILE, "r") as f:
        return json.load(f)


def save_json(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


# ---------------- Base Page ----------------
def toast(msg, kind="info"):
    if kind == "info":
        messagebox.showinfo("Info", msg)
    elif kind == "error":
        messagebox.showerror("Error", msg)
    else:
        messagebox.showwarning("Notice", msg)


class BasePage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="white")
        self.app = app


# ---------------- Pages ----------------
class DashboardPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        ctk.CTkLabel(self, text="Dashboard",
                     font=ctk.CTkFont(size=30, weight="bold"),
                     text_color="black").pack(anchor="w", padx=16, pady=12)
        self.details_label = ctk.CTkLabel(self, font=ctk.CTkFont(size=20),
                                          text_color="black", justify="left")
        self.details_label.pack(anchor="w", padx=16, pady=8)
        self.refresh()

    def refresh(self):
        s = self.app.student
        details = f"""
ID: {s.get("id", "N/A")}
First Name: {s.get("first_name", "")}
Last Name: {s.get("last_name", "")}
Email: {s.get("email", "")}
Gender: {s.get("gender", "")}
Course: {self.app.get_course_name(s.get("course_id"))}
"""
        self.details_label.configure(text=details)


class LeavePage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        ctk.CTkLabel(self, text="Apply Leave",
                     font=ctk.CTkFont(size=18, weight="bold"),
                     text_color="black").pack(anchor="w", padx=16, pady=12)

        self.txt = ctk.CTkTextbox(self, height=100, width=500)
        self.txt.pack(padx=16, pady=8)

        ctk.CTkButton(self, text="Submit Leave", command=self.submit,
                      fg_color="green", text_color="white").pack(padx=16, pady=8)

        # Treeview (still ttk)
        self.tree = ttk.Treeview(self, columns=("id", "reason", "status"), show="headings", height=5)
        for c, w in (("id", 50), ("reason", 260), ("status", 120)):
            self.tree.heading(c, text=c.title())
            self.tree.column(c, width=w)
        self.tree.pack(fill="both", expand=True, padx=16, pady=8)
        self.refresh()

    def submit(self):
        reason = self.txt.get("1.0", "end").strip()
        if not reason:
            return toast("Enter reason", "error")

        existing_ids = [lv["id"] for lv in self.app.data.get("leave_student", [])]
        new_id = max(existing_ids or [0]) + 1

        new = {
            "id": new_id,
            "student_id": self.app.student["id"],
            "reason": reason,
            "status": 0
        }
        self.app.data.setdefault("leave_student", []).append(new)
        save_json(self.app.data)
        self.txt.delete("1.0", "end")
        self.refresh()
        toast("Leave applied")
        return None

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        for lv in self.app.data.get("leave_student", []):
            if lv.get("student_id") != self.app.student["id"]:
                continue
            st = {0: "Pending", 1: "Approved", -1: "Rejected"}.get(lv.get("status"), "Pending")
            self.tree.insert("", "end", values=(lv["id"], lv["reason"], st))


class ProfilePage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        ctk.CTkLabel(self, text="View/Edit Profile",
                     font=ctk.CTkFont(size=18, weight="bold"),
                     text_color="black").grid(row=0, column=0, columnspan=2, padx=16, pady=12, sticky="w")

        self.fn = ctk.CTkEntry(self, width=200)
        self.ln = ctk.CTkEntry(self, width=200)
        self.email = ctk.CTkEntry(self, width=200)

        labels = ["First Name:", "Last Name:", "Email:"]
        entries = [self.fn, self.ln, self.email]

        for i, (lbl, ent) in enumerate(zip(labels, entries), start=1):
            ctk.CTkLabel(self, text=lbl, text_color="black").grid(row=i, column=0, sticky="w", padx=16, pady=4)
            ent.grid(row=i, column=1, sticky="ew", padx=16, pady=4)

        self.columnconfigure(1, weight=1)
        ctk.CTkButton(self, text="Save Profile", command=self.save,
                      fg_color="blue", text_color="white").grid(row=5, column=0, columnspan=2, pady=12)
        self.refresh()

    def refresh(self):
        s = self.app.student
        self.fn.delete(0, "end"); self.fn.insert(0, s.get("first_name", ""))
        self.ln.delete(0, "end"); self.ln.insert(0, s.get("last_name", ""))
        self.email.delete(0, "end"); self.email.insert(0, s.get("email", ""))

    def save(self):
        s = self.app.student
        s["first_name"] = self.fn.get()
        s["last_name"] = self.ln.get()
        s["email"] = self.email.get()
        save_json(self.app.data)
        toast("Profile updated")
        self.refresh()


class NotificationPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        ctk.CTkLabel(self, text="Notifications",
                     font=ctk.CTkFont(size=18, weight="bold"),
                     text_color="black").pack(anchor="w", padx=16, pady=12)

        self.txtbox = ctk.CTkTextbox(self, height=400, width=600)
        self.txtbox.configure(state="disabled")
        self.txtbox.pack(fill="both", expand=True, padx=16, pady=12)
        self.refresh()

    def refresh(self):
        self.txtbox.configure(state="normal")
        self.txtbox.delete("1.0", "end")
        for n in self.app.data.get("notifications", []):
            recipients = n.get("student_id")
            if recipients is not None and recipients != self.app.student["id"]:
                continue
            msg = f"{n.get('time','')} - {n.get('message','')}\n"
            self.txtbox.insert("end", msg)
        self.txtbox.configure(state="disabled")


# ---------------- Main Student App ----------------
class StudentApp(ctk.CTk):
    def __init__(self, student_id):
        super().__init__()
        self.title("Student Management System - Student")
        self.geometry("1200x720")
        self.data = load_json()

        # Find student by ID
        student = None
        for s in self.data.get("students", []):
            if s["id"] == student_id:
                student = s
                break

        if not student:
            messagebox.showerror("Error", "Student not found!")
            self.destroy()
            return

        self.student = student

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0 , fg_color="#273b7a")
        self.sidebar.pack(side="left", fill="y")
        ctk.CTkLabel(self.sidebar, text="Menu",
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color="white").pack(padx=12, pady=12)

        # keep track of sidebar buttons
        self.buttons = {}
        self.active_page = None

        self._btn("Dashboard", "dashboard")
        self._btn("Leaves", "leaves")
        self._btn("Profile", "profile")
        self._btn("Notifications", "notifications")

        # Logout stays separate (always red)
        ctk.CTkButton(self.sidebar, text="Logout",
                      fg_color="red", text_color="white",
                      hover_color="#b30000", command=self.logout).pack(fill="x", padx=12, pady=20)

        # Main pages
        self.main = ctk.CTkFrame(self, fg_color="white")
        self.main.pack(side="right", fill="both", expand=True)

        self.pages = {
            "dashboard": DashboardPage(self.main, self),
            "leaves": LeavePage(self.main, self),
            "profile": ProfilePage(self.main, self),
            "notifications": NotificationPage(self.main, self),
        }
        for p in self.pages.values():
            p.pack_forget()
        self.show_page("dashboard")

    # updated _btn
    def _btn(self, text, key):
        btn = ctk.CTkButton(self.sidebar, text=text, width=180,
                            fg_color="#273b7a", text_color="white",
                            hover_color="#1e2f5a", corner_radius=0,
                            anchor="w", height=40,
                            command=lambda: self.show_page(key))
        btn.pack(padx=0, pady=2, fill="x")
        self.buttons[key] = btn

    # updated show_page with highlight
    def show_page(self, key):
        for p in self.pages.values():
            p.pack_forget()
        self.pages[key].pack(fill="both", expand=True)
        if hasattr(self.pages[key], "refresh"):
            self.pages[key].refresh()

        # reset all buttons
        for k, b in self.buttons.items():
            b.configure(fg_color="#273b7a")
        # highlight active
        if key in self.buttons:
            self.buttons[key].configure(fg_color="#1e2f5a")
        self.active_page = key

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to log out?"):
            self.destroy()

    def get_course_name(self, course_id):
        for c in self.data.get("courses", []):
            if c.get("id") == course_id:
                return c.get("name", "N/A")
        return "N/A"


# ---------------- Testing ----------------
if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    try:
        app = StudentApp(student_id=1)
        app.mainloop()
    except Exception as e:
        print("Application closed:", e)
