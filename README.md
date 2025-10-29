# 🎓 Student Management System
A desktop-based student management application built using Python’s Tkinter (CustomTkinter) for the GUI and JSON for lightweight data storage.
This project provides a clean and interactive interface for managing students and admin data without needing a full database.

---

## 🧩 Features

- 🔐 Admin Login Panel – Secure access for administrators.
- 🧑‍🎓 Student Login Panel – Separate interface for students.
- 🗂️ Manage Student Data – Add, update, or delete student accounts.
- 💾 JSON-Based Storage – All user data stored in simple .json files.
- 🎨 Modern GUI – Built using CustomTkinter for an improved visual experience.
- 🧱 Modular Design – Clean separation between UI components and logic.
  
---

## 🛠️ Tech Stack

| Component | Technology |
|------------|-------------|
| **Language** | Python |
| **GUI Library** | Tkinter / CustomTkinter |
| **Data Storage** | JSON |
| **OS Compatibility** | Windows / macOS / Linux |


---

### 📁 Folder Structure
```pgsql
Student-Management-System-using-custom-tkinter-and-json/
│
├── main.py                  # Entry point of the application
├── welcome_page.py          # Welcome window
├── admin_login_page.py      # Admin login logic
├── student_login_page.py    # Student login logic
├── admin_dashboard.py       # Admin dashboard
├── student_dashboard.py     # Student dashboard
├── add_account_page.py      # Form for adding new student accounts
├── admin.json               # JSON file storing admin credentials
├── icons/                   # Folder for icons/images
└── README.md                # Project documentation

```

## ⚙️ Installation & Setup
Prerequisites
- Python 3.x installed on your system
- Tkinter (usually included by default with Python)
  
### 1️⃣ Clone this Repository
```bash
git clone https://github.com/onkar-8282/Student-Management-System-using-custom-tkinter-and-json.git
cd Student-Management-System-using-custom-tkinter-and-json
```
### 2️⃣ Install Required Libraries
```bash
pip install customtkinter
```
### 3️⃣ Run the Application
```bash
python main.py
```

## 🧭 Usage Guide

1. **Launch the app** using:
   ```bash
   python main.py
   ```
2. **From the welcome page, select either Admin or Student login**
3. **Admin can:**
   - View all registered students.
   - Add new student accounts.
   - Update or delete existing records.
4. **Students can:**
   - Log in using their credentials.
   - Access their profile and related details.
     
### 🧠 Future Enhancements

- Switch to an SQL database (e.g., SQLite or MySQL)
- Add password hashing for secure authentication
- Include attendance and grade tracking modules
- Improve dashboard design and add themes
- Integrate email or notification system
