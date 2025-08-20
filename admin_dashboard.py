import customtkinter as ctk
from tkinter import messagebox
import json, os

FILE = "admin.json"

# ---------------- Data Layer ----------------
DEFAULT_DB = {
    "admin": {"first_name": "Admin", "last_name": "User", "password": ""},
    "students": [],
    "courses": [],
    "leave_student": [],    # {id, student_id, reason, status: -1/0/1}
}

def load_json():
    if not os.path.exists(FILE):
        with open(FILE, "w") as f:
            json.dump(DEFAULT_DB, f, indent=4)
    with open(FILE, "r") as f:
        data = json.load(f)
    for k, v in DEFAULT_DB.items():
        if k not in data:
            data[k] = v
    return data

def save_json(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

def next_id(items):
    return (max((it.get("id", 0) for it in items), default=0) + 1) if items else 1

# ---------------- Utilities ----------------
class FormRow(ctk.CTkFrame):
    def __init__(self, master, label, **entry_kwargs):
        super().__init__(master, fg_color="transparent")
        ctk.CTkLabel(self, text=label, width=120, anchor="w").pack(side="left", padx=(0, 8))
        self.var = ctk.StringVar()
        self.entry = ctk.CTkEntry(self, textvariable=self.var, **entry_kwargs)
        self.entry.pack(side="left", fill="x", expand=True)

    def get(self): return self.var.get().strip()
    def set(self, val): self.var.set(val or "")

class ComboRow(ctk.CTkFrame):
    def __init__(self, master, label, values):
        super().__init__(master, fg_color="transparent")
        ctk.CTkLabel(self, text=label, width=120, anchor="w").pack(side="left", padx=(0, 8))
        self.var = ctk.StringVar()
        self.combo = ctk.CTkComboBox(self, variable=self.var, values=values)
        self.combo.pack(side="left", fill="x", expand=True)

    def get(self): return self.var.get()
    def set(self, val): self.var.set(val)

# ---------------- Base Pages ----------------
class BasePage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app

    def toast(self, msg, kind="info"):
        if kind == "info": messagebox.showinfo("Info", msg)
        elif kind == "error": messagebox.showerror("Error", msg)
        else: messagebox.showwarning("Notice", msg)

# ---------------- Dashboard ----------------
class DashboardPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        wrap = ctk.CTkFrame(self, fg_color="transparent")
        wrap.pack(fill="both", expand=True, padx=16, pady=16)

        ctk.CTkLabel(wrap, text="Administrative Dashboard",
                     font=ctk.CTkFont(size=20, weight="bold")).pack(anchor="w")
        self.stats_lbl = ctk.CTkLabel(wrap, font=ctk.CTkFont(size=14))
        self.stats_lbl.pack(anchor="w", pady=(8, 16))

        grid = ctk.CTkFrame(wrap, fg_color="transparent")
        grid.pack(fill="x")
        buttons = [
            ("Manage Students", lambda: app.show_page("students")),
            ("Manage Courses", lambda: app.show_page("courses")),
            ("Leaves", lambda: app.show_page("leaves")),
            ("Admin Profile", lambda: app.show_page("profile")),
        ]
        for i, (text, cmd) in enumerate(buttons):
            b = ctk.CTkButton(grid, text=text, command=cmd)
            b.grid(row=i//2, column=i%2, padx=6, pady=6, sticky="ew")
        grid.grid_columnconfigure(0, weight=1)
        grid.grid_columnconfigure(1, weight=1)

        self.refresh()

    def refresh(self):
        d = self.app.data
        lines = [
            f"Total Students: {len(d['students'])}",
            f"Total Courses: {len(d['courses'])}",
        ]
        self.stats_lbl.configure(text="\n".join(lines))

# ---------------- Students ----------------
class StudentsPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        ctk.CTkLabel(self, text="Manage Students",
                     font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", padx=12, pady=8)
        self.table = ctk.CTkScrollableFrame(self, height=500)
        self.table.pack(fill="both", expand=True, padx=12, pady=12)
        ctk.CTkButton(self, text="Add Student", command=self.add_student).pack(pady=6)
        self.refresh()

    def refresh(self):
        for w in self.table.winfo_children(): w.destroy()
        headers = ["ID", "First", "Last", "Email", "Gender", "Course"]
        for j, h in enumerate(headers):
            ctk.CTkLabel(self.table, text=h, font=ctk.CTkFont(weight="bold")).grid(row=0, column=j, padx=4, pady=2)
        for i, st in enumerate(self.app.data["students"], start=1):
            vals = [st.get("id"), st.get("first_name"), st.get("last_name"),
                    st.get("email",""), st.get("gender",""), self.app.get_course_name(st.get("course_id"))]
            for j, v in enumerate(vals):
                ctk.CTkLabel(self.table, text=v).grid(row=i, column=j, padx=4, pady=2)

    def add_student(self):
        win = ctk.CTkToplevel(self)
        win.title("Add Student")
        frm = ctk.CTkFrame(win)
        frm.pack(padx=12, pady=12)
        r_fn = FormRow(frm, "First name:"); r_ln = FormRow(frm, "Last name:")
        r_mail = FormRow(frm, "Email:"); r_gender = ComboRow(frm, "Gender:", ["Male", "Female", "Other"])
        r_course = ComboRow(frm, "Course:", [c.get("name") for c in self.app.data["courses"]])
        for w in (r_fn, r_ln, r_mail, r_gender, r_course): w.pack(fill="x", pady=4)
        def save():
            if not r_fn.get() or not r_mail.get():
                self.toast("First name and Email required", "error"); return
            new = {"id": next_id(self.app.data["students"]),
                   "first_name": r_fn.get(), "last_name": r_ln.get(),
                   "email": r_mail.get(), "gender": r_gender.get(),
                   "course_id": self.app.get_course_id_by_name(r_course.get())}
            self.app.data["students"].append(new); save_json(self.app.data)
            win.destroy(); self.refresh(); self.app.refresh_dashboard()
        ctk.CTkButton(frm, text="Save", command=save).pack(pady=6)

# ---------------- Leaves ----------------
class LeavesPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        tabs = ctk.CTkTabview(self)
        tabs.pack(fill="both", expand=True)
        self.student_tab = tabs.add("Student Leaves")

        self.student_frame = ctk.CTkScrollableFrame(self.student_tab)
        self.student_frame.pack(fill="both", expand=True, padx=12, pady=12)
        self.refresh()

    def refresh(self):
        for w in self.student_frame.winfo_children(): w.destroy()
        headers = ["ID","Student","Reason","Status"]
        for j,h in enumerate(headers):
            ctk.CTkLabel(self.student_frame,text=h,font=ctk.CTkFont(weight="bold")).grid(row=0,column=j,padx=4,pady=2)
        for i,lv in enumerate(self.app.data["leave_student"], start=1):
            vals = [lv.get("id"), self.app.get_student_name(lv.get("student_id")),
                    lv.get("reason"), self._status_text(lv.get("status",0))]
            for j,v in enumerate(vals):
                ctk.CTkLabel(self.student_frame,text=v).grid(row=i,column=j,padx=4,pady=2)

    def _status_text(self,s): return {1:"Approved",-1:"Rejected"}.get(s,"Pending")

# ---------------- Profile ----------------
class ProfilePage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        ctk.CTkLabel(self, text="View / Edit Profile",
                     font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", padx=12, pady=8)
        form = ctk.CTkFrame(self, fg_color="transparent")
        form.pack(fill="x", padx=12, pady=8)
        self.fname = FormRow(form, "First name:")
        self.lname = FormRow(form, "Last name:")
        self.passw = FormRow(form, "Password:", show="*")
        for w in (self.fname, self.lname, self.passw): w.pack(fill="x", pady=4)
        ctk.CTkButton(self, text="Save", command=self.save).pack(anchor="w", padx=12, pady=8)
        self.refresh()

    def refresh(self):
        a = self.app.data.get("admin", {})
        self.fname.set(a.get("first_name")); self.lname.set(a.get("last_name"))
        self.passw.set(a.get("password",""))

    def save(self):
        a = self.app.data.get("admin", {})
        a["first_name"] = self.fname.get() or a.get("first_name")
        a["last_name"] = self.lname.get() or a.get("last_name")
        if self.passw.get(): a["password"] = self.passw.get()
        self.app.data["admin"] = a; save_json(self.app.data)
        self.app.toast("Profile updated")

# ---------------- Main Application ----------------
class AdminApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Student Management System - Admin")
        self.geometry("1200x720")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.data = load_json()

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, fg_color="#273b7a", corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.main = ctk.CTkFrame(self, fg_color="white", corner_radius=0)
        self.main.pack(side="right", fill="both", expand=True)

        ctk.CTkLabel(self.sidebar, text="Menu",
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color="white").pack(padx=12, pady=(12,6))
        self._btn("Dashboard", lambda: self.show_page("dashboard"))
        self._btn("Students", lambda: self.show_page("students"))
        self._btn("Courses", lambda: self.show_page("courses"))
        self._btn("Leaves", lambda: self.show_page("leaves"))
        self._btn("Admin Profile", lambda: self.show_page("profile"))
        ctk.CTkButton(self.sidebar, text="Reload DB",
                      fg_color="red", text_color="white",
                      command=self.reload_db).pack(fill="x", padx=12, pady=8)

        # Pages
        self.pages = {
            "dashboard": DashboardPage(self.main, self),
            "students": StudentsPage(self.main, self),
            "courses": StudentsPage(self.main, self),  # TODO: implement CoursesPage same as StudentsPage
            "leaves": LeavesPage(self.main, self),
            "profile": ProfilePage(self.main, self),
        }
        for p in self.pages.values(): p.pack_forget()
        self.show_page("dashboard")

    def _btn(self, text, cmd):
        b = ctk.CTkButton(self.sidebar, text=text, command=cmd,
                          fg_color="transparent", text_color="white",
                          hover_color="#1c2b5a")
        b.pack(fill="x", padx=12, pady=2)

    def show_page(self, key):
        for p in self.pages.values(): p.pack_forget()
        self.pages[key].pack(fill="both", expand=True)
        if hasattr(self.pages[key],'refresh'): self.pages[key].refresh()

    def refresh_dashboard(self): self.pages["dashboard"].refresh()
    def reload_db(self):
        self.data = load_json()
        for p in self.pages.values():
            if hasattr(p,'refresh'): p.refresh()
        self.toast("Database reloaded from file")
    def toast(self,msg,kind="info"):
        if kind=="info": messagebox.showinfo("Info",msg)
        elif kind=="error": messagebox.showerror("Error",msg)
        else: messagebox.showwarning("Notice",msg)

    def get_course_name(self, course_id):
        c = next((c for c in self.data["courses"] if c.get("id")==course_id), None)
        return c.get("name") if c else ""
    def get_course_id_by_name(self, name):
        c = next((c for c in self.data["courses"] if c.get("name")==name), None)
        return c.get("id") if c else None
    def get_student_name(self, student_id):
        s = next((s for s in self.data["students"] if s.get("id")==student_id), None)
        return f"{s.get('first_name','')} {s.get('last_name','')}".strip() if s else ""

if __name__ == "__main__":
    app = AdminApp()
    app.mainloop()
