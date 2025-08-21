import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
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
    # Backfill missing keys if schema grew
    for k, v in DEFAULT_DB.items():
        if k not in data:
            data[k] = v
    return data


def save_json(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


def next_id(items):
    return (max((it.get("id", 0) for it in items), default=0) + 1) if items else 1


# ---------------- Small utilities ----------------
class FormRow(ttk.Frame):
    def __init__(self, master, label, **entry_kwargs):
        super().__init__(master)
        ttk.Label(self, text=label, width=18).pack(side=tk.LEFT, padx=(0, 8))
        self.var = tk.StringVar()
        self.entry = ttk.Entry(self, textvariable=self.var, **entry_kwargs)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def get(self):
        return self.var.get().strip()

    def set(self, val):
        self.var.set(val or "")


class ComboRow(ttk.Frame):
    def __init__(self, master, label, values):
        super().__init__(master)
        ttk.Label(self, text=label, width=18).pack(side=tk.LEFT, padx=(0, 8))
        self.var = tk.StringVar()
        self.combo = ttk.Combobox(self, textvariable=self.var, values=values, state="readonly")
        self.combo.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def get(self):
        return self.var.get()

    def set(self, val):
        self.var.set(val)


class BoolRow(ttk.Frame):
    def __init__(self, master, label):
        super().__init__(master)
        self.var = tk.BooleanVar(value=False)
        ttk.Checkbutton(self, text=label, variable=self.var).pack(side=tk.LEFT)

    def get(self):
        return self.var.get()

    def set(self, val):
        self.var.set(bool(val))


# ---------------- Base Pages ----------------
class BasePage(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

    def toast(self, msg, kind="info"):
        if kind == "info":
            messagebox.showinfo("Info", msg)
        elif kind == "error":
            messagebox.showerror("Error", msg)
        else:
            messagebox.showwarning("Notice", msg)


class ListPage(BasePage):
    """Generic list + toolbar page using ttk.Treeview."""
    COLUMNS = []    # Override: [(key, heading, width)]
    TITLE = ""

    def __init__(self, parent, app):
        super().__init__(parent, app)
        # Header
        head = ttk.Frame(self)
        head.pack(fill=tk.X, pady=(6, 4))
        ttk.Label(head, text=self.TITLE, font=("Segoe UI", 16, "bold")).pack(side=tk.LEFT)
        ttk.Button(head, text="Refresh", command=self.refresh).pack(side=tk.RIGHT)

        # Toolbar
        bar = ttk.Frame(self)
        bar.pack(fill=tk.X, pady=(0, 6))
        ttk.Button(bar, text="Add", command=self.add_dialog).pack(side=tk.LEFT, padx=2)
        ttk.Button(bar, text="Edit", command=self.edit_dialog).pack(side=tk.LEFT, padx=2)
        ttk.Button(bar, text="Delete", command=self.delete_selected).pack(side=tk.LEFT, padx=2)

        # Tree
        self.tree = ttk.Treeview(self, columns=[c[0] for c in self.COLUMNS], show="headings")
        for key, heading, width in self.COLUMNS:
            self.tree.heading(key, text=heading)
            self.tree.column(key, width=width, anchor=tk.W)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.refresh()

    # ---- Data API to override ----
    def items(self):
        return []

    def to_row(self, item):
        return []

    def add_dialog(self):
        pass

    def edit_dialog(self):
        sel = self.get_selected()
        if not sel:
            self.toast("Select a row to edit")
            return
        self._edit_dialog(sel)

    def _edit_dialog(self, item):
        pass

    def delete_selected(self):
        sel = self.get_selected()
        if not sel:
            self.toast("Select a row to delete")
            return
        if messagebox.askyesno("Confirm", "Delete selected item?"):
            self._delete(sel)
            save_json(self.app.data)
            self.refresh()

    def _delete(self, item):
        pass

    # ---- Helpers ----
    def get_selected(self):
        cur = self.tree.focus()
        if not cur:
            return None
        # Treeview iid is set to the item's id (string). Look up matching item in items().
        try:
            sel_id = int(cur)
        except Exception:
            return None
        for it in self.items():
            if it.get("id") == sel_id:
                return it
        return None

    def refresh(self):
        # Clear tree
        try:
            self.tree.delete(*self.tree.get_children())
        except Exception:
            pass

        for it in self.items():
            values = self.to_row(it)
            # use the object's id as the iid so we can look it up later
            iid = str(it.get("id"))
            try:
                self.tree.insert("", tk.END, iid=iid, values=values)
            except Exception:
                # fallback: insert without iid
                self.tree.insert("", tk.END, values=values)


# ---------------- Specific Pages ----------------
class DashboardPage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        wrap = ttk.Frame(self)
        wrap.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)

        ttk.Label(wrap, text="Administrative Dashboard", font=("Segoe UI", 30, "bold")).pack(anchor=tk.W)
        self.stats_lbl = ttk.Label(wrap, font=("Segoe UI", 18))
        self.stats_lbl.pack(anchor=tk.W, pady=(8, 16))

        grid = ttk.Frame(wrap)
        grid.pack(fill=tk.X)
        buttons = [
            ("Manage Students", lambda: app.show_page("students")),
            ("Manage Courses", lambda: app.show_page("courses")),
            ("Leaves", lambda: app.show_page("leaves")),
            ("Admin Profile", lambda: app.show_page("profile")),
        ]
        for i, (text, cmd) in enumerate(buttons):
            b = ttk.Button(grid, text=text, command=cmd)
            b.grid(row=i//2, column=i%2, padx=6, pady=6, sticky="ew")
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)

        self.refresh()

    def refresh(self):
        d = self.app.data
        lines = [
            f"Total Students: {len(d['students'])}",
            f"Total Courses: {len(d['courses'])}",
            f"Total Number of Students who have applied for Leave: {len(d['leave_student'])}",
        ]
        self.stats_lbl.config(text="\n".join(lines))


# ---- Courses ----
class CoursePage(ListPage):
    TITLE = "Manage Courses"
    COLUMNS = [("id", "ID", 60), ("name", "Course Name", 260)]

    def items(self):
        return self.app.data["courses"]

    def to_row(self, it):
        return (it.get("id"), it.get("name"))

    def add_dialog(self):
        win = tk.Toplevel(self)
        win.title("Add Course")
        r_name = FormRow(win, "Name:")
        r_name.pack(fill=tk.X, padx=12, pady=6)

        def save():
            name = r_name.get()
            if not name:
                self.toast("Enter name", "error"); return
            new = {"id": next_id(self.app.data["courses"]), "name": name}
            self.app.data["courses"].append(new)
            save_json(self.app.data)
            win.destroy(); self.refresh(); self.app.refresh_dashboard()
        ttk.Button(win, text="Save", command=save).pack(pady=8)

    def _edit_dialog(self, item):
        win = tk.Toplevel(self)
        win.title("Edit Course")
        r_name = FormRow(win, "Name:"); r_name.set(item.get("name")); r_name.pack(fill=tk.X, padx=12, pady=6)
        def save():
            item["name"] = r_name.get() or item["name"]
            save_json(self.app.data); win.destroy(); self.refresh(); self.app.refresh_dashboard()
        ttk.Button(win, text="Update", command=save).pack(pady=8)

    def _delete(self, item):
        # prevent deletion if any student or subject is linked
        used = any(s.get("course_id") == item["id"] for s in self.app.data["students"]) or \
               any(sj.get("course_id") == item["id"] for sj in self.app.data["subjects"])
        if used:
            self.toast("Course in use by students/subjects", "error"); return
        self.app.data["courses"] = [c for c in self.app.data["courses"] if c["id"] != item["id"]]

# ---- Students ----
class StudentPage(ListPage):
    TITLE = "Manage Students"
    COLUMNS = [("id", "ID", 60), ("first_name", "First Name", 120), ("last_name", "Last Name", 120),
               ("email", "Email", 220), ("gender", "Gender", 80), ("course", "Course", 140)]

    def items(self):
        return self.app.data["students"]

    def to_row(self, it):
        course_name = self.app.get_course_name(it.get("course_id"))
        return (it.get("id"), it.get("first_name"), it.get("last_name"), it.get("email"), it.get("gender"), course_name)

    def add_dialog(self):
        win = tk.Toplevel(self); win.title("Add Student")
        f = ttk.Frame(win); f.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)
        r_fn = FormRow(f, "First name:"); r_ln = FormRow(f, "Last name:")
        r_mail = FormRow(f, "Email:"); r_gender = ComboRow(f, "Gender:", ["Male", "Female", "Other"])
        r_course = ComboRow(f, "Course:", [c.get("name") for c in self.app.data["courses"]])
        for w in (r_fn, r_ln, r_mail, r_gender, r_course):
            w.pack(fill=tk.X, pady=4)
        def save():
            if not r_fn.get() or not r_mail.get():
                self.toast("First name and Email are required", "error"); return
            new = {
                "id": next_id(self.app.data["students"]),
                "first_name": r_fn.get(), "last_name": r_ln.get(),
                "course_id": self.app.get_course_id_by_name(r_course.get()),
            }
            self.app.data["students"].append(new); save_json(self.app.data)
            win.destroy(); self.refresh(); self.app.refresh_dashboard(); self.toast("Student added")
        ttk.Button(f, text="Save", command=save).pack(pady=8)

    def _edit_dialog(self, it):
        win = tk.Toplevel(self); win.title("Edit Student")
        f = ttk.Frame(win); f.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)
        r_fn = FormRow(f, "First name:"); r_fn.set(it.get("first_name"))
        r_ln = FormRow(f, "Last name:"); r_ln.set(it.get("last_name"))
        r_mail = FormRow(f, "Email:"); r_mail.set(it.get("email"))
        r_gender = ComboRow(f, "Gender:", ["Male", "Female", "Other"]); r_gender.set(it.get("gender"))
        r_course = ComboRow(f, "Course:", [c.get("name") for c in self.app.data["courses"]])
        r_course.set(self.app.get_course_name(it.get("course_id")))
        for w in (r_fn, r_ln, r_mail, r_gender, r_course): w.pack(fill=tk.X, pady=4)
        def save():
            it["first_name"] = r_fn.get() or it["first_name"]
            it["last_name"]  = r_ln.get() or it["last_name"]
            it["email"]      = r_mail.get() or it["email"]
            it["gender"]     = r_gender.get() or it.get("gender")
            it["course_id"] = self.app.get_course_id_by_name(r_course.get())
            save_json(self.app.data); win.destroy(); self.refresh(); self.toast("Updated")
        ttk.Button(f, text="Update", command=save).pack(pady=8)

    def _delete(self, it):
        self.app.data["students"] = [s for s in self.app.data["students"] if s["id"] != it["id"]]

# ---- Leaves ----
class LeavePage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        ttk.Label(self, text="Student How Have Apply For Leaves", font=("Segoe UI", 30, "bold")).pack(anchor=tk.W, padx=12, pady=8)

        self.student_tree = ttk.Treeview(self, columns=("id","student","reason","status"), show="headings")
        for c, t, w in (("id","ID",100),("student","Student",350),("reason","Reason",500),("status","Status",150)):
            self.student_tree.heading(c, text=t)
            self.student_tree.column(c, width=w)
        self.student_tree.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        stbar = ttk.Frame(self); stbar.pack(fill=tk.X, padx=8, pady=4)
        ttk.Button(stbar, text="Approve", command=lambda: self._set_student_status(1)).pack(side=tk.LEFT)
        ttk.Button(stbar, text="Reject", command=lambda: self._set_student_status(-1)).pack(side=tk.LEFT, padx=6)

        self.refresh()


    def refresh(self):
        self.student_tree.delete(*self.student_tree.get_children())
        for lv in self.app.data["leave_student"]:
            self.student_tree.insert("", tk.END, iid=str(lv.get("id")), values=(lv.get("id"), self.app.get_student_name(lv.get("student_id")), lv.get("reason"), self._status_text(lv.get("status",0))))

    def _status_text(self, s):
        return {1:"Approved", -1:"Rejected"}.get(s, "Pending")

    def _set_student_status(self, s):
        cur = self.student_tree.focus()
        if not cur: return
        lid = int(self.student_tree.item(cur, "values")[0])
        lv = next((l for l in self.app.data["leave_student"] if l.get("id") == lid), None)
        if lv: lv["status"] = s; save_json(self.app.data); self.refresh()

# ---- Admin Profile ----
class ProfilePage(BasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        ttk.Label(self, text="View / Edit Profile", font=("Segoe UI", 30, "bold")).pack(anchor=tk.W, padx=12, pady=8)
        form = ttk.Frame(self); form.pack(fill=tk.X, padx=12, pady=8)
        self.fname = FormRow(form, "First name:")
        self.lname = FormRow(form, "Last name:")
        self.passw = FormRow(form, "Password:")
        for w in (self.fname, self.lname, self.passw): w.pack(fill=tk.X, pady=4)
        ttk.Button(self, text="Save", command=self.save).pack(anchor=tk.W, padx=12, pady=8 )
        self.refresh()

    def refresh(self):
        a = self.app.data.get("admin", {})
        self.fname.set(a.get("first_name")); self.lname.set(a.get("last_name"))
        self.passw.set(a.get("password", ""))

    def save(self):
        a = self.app.data.get("admin", {})
        a["first_name"] = self.fname.get() or a.get("first_name")
        a["last_name"]  = self.lname.get() or a.get("last_name")
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

        # Main content frame
        self.main = ctk.CTkFrame(self, fg_color="white", corner_radius=0)
        self.main.pack(side="right", fill="both", expand=True)

        # --- Sidebar ---
        ctk.CTkLabel(
            self.sidebar,
            text="Menu",
            font=("Segoe UI", 16, "bold"),
            text_color="white"
        ).pack(padx=12, pady=(12,6))

        self.sidebar_buttons = {}  # store buttons for highlight

        self.sidebar_buttons["dashboard"] = self._btn("Dashboard", lambda: self.show_page("dashboard"))
        self.sidebar_buttons["students"] = self._btn("Students", lambda: self.show_page("students"))
        self.sidebar_buttons["courses"] = self._btn("Courses", lambda: self.show_page("courses"))
        self.sidebar_buttons["leaves"] = self._btn("Leaves", lambda: self.show_page("leaves"))
        self.sidebar_buttons["profile"] = self._btn("Admin Profile", lambda: self.show_page("profile"))

        # Separator (thin line)
        ctk.CTkFrame(self.sidebar, height=2, fg_color="white").pack(fill="x", padx=12, pady=8)

        self.sidebar_buttons["reload"] = self._btn("Reload DB", self.reload_db)

        # --- Sidebar bottom (Log out) ---
        self.sidebar_bottom = ctk.CTkFrame(self.sidebar, fg_color="#273b7a")
        self.sidebar_bottom.pack(side="bottom", fill="x", pady=8)

        self.sidebar_buttons["logout"] = ctk.CTkButton(
            self.sidebar_bottom,
            text="Log Out",
            command=self.logout,
            fg_color="#c62828",      # red background
            hover_color="#e53935",   # brighter red on hover
            text_color="white",
            anchor="w"
        )
        self.sidebar_buttons["logout"].pack(fill="x", padx=12, pady=4)

        # Pages
        self.pages = {
            "dashboard": DashboardPage(self.main, self),
            "courses": CoursePage(self.main, self),
            "students": StudentPage(self.main, self),
            "leaves": LeavePage(self.main, self),
            "profile": ProfilePage(self.main, self),
        }
        for p in self.pages.values():
            p.pack_forget()
        self.show_page("dashboard")

        # Style (kept for ttk parts if you use them elsewhere)
        self.style = ttk.Style(self)
        try:
            self.style.theme_use("clam")
        except:
            pass

    # Sidebar button helper (customtkinter only)
    def _btn(self, text, command):
        btn = ctk.CTkButton(
            self.sidebar,
            text=text,
            command=command,
            fg_color="#394d9c",    # normal button color
            hover_color="#4a63c3", # hover effect
            text_color="white",
            anchor="w"
        )
        btn.pack(fill="x", padx=12, pady=4)
        return btn

    def show_page(self, key):
        # hide all pages
        for k, p in self.pages.items():
            p.pack_forget()
        # show selected page
        self.pages[key].pack(fill=tk.BOTH, expand=True)
        if hasattr(self.pages[key], 'refresh'):
            self.pages[key].refresh()

        # update sidebar highlight
        for k, b in self.sidebar_buttons.items():
            if k == key:
                b.configure(fg_color="#1a237e")  # active page color
            elif k not in ("reload", "logout"):
                b.configure(fg_color="#394d9c")  # reset others

    def refresh_dashboard(self):
        self.pages["dashboard"].refresh()

    def reload_db(self):
        self.data = load_json()
        for p in self.pages.values():
            if hasattr(p, 'refresh'):
                p.refresh()
        self.toast("Database reloaded from file")

    def logout(self):
        from tkinter import messagebox
        if messagebox.askyesno("Confirm Logout", "Are you sure you want to log out?"):
            self.destroy()

            try:
                login = LoginApp()   
                login.mainloop()
            except:
                pass

    def toast(self, msg, kind="info"):
        if kind == "info":
            messagebox.showinfo("Info", msg)
        elif kind == "error":
            messagebox.showerror("Error", msg)
        else:
            messagebox.showwarning("Notice", msg)

    # ---- Lookup helpers ----
    def get_course_name(self, course_id):
        c = next((c for c in self.data["courses"] if c.get("id") == course_id), None)
        return c.get("name") if c else ""

    def get_course_id_by_name(self, name):
        c = next((c for c in self.data["courses"] if c.get("name") == name), None)
        return c.get("id") if c else None

    def get_student_name(self, student_id):
        s = next((s for s in self.data["students"] if s.get("id") == student_id), None)
        if not s: return ""
        return f"{s.get('first_name','')} {s.get('last_name','')}".strip()

    def get_student_display(self, s):
        return f"{s.get('first_name','')} {s.get('last_name','')} (ID:{s.get('id')})".strip()

    def get_student_id_by_display(self, disp):
        try:
            return int(disp.split("ID:")[-1].rstrip(")"))
        except:
            return None
    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to log out?"):
            self.destroy()


if __name__ == "__main__":
    app = AdminApp()
    app.mainloop()