# STUDENT ACADEMIC PORTAL (Salone EduPortal)

Salone EduPortal is a **student academic management system** built with Python.  
It is divided into two main layers:

- **GUI Layer** — handles the user interface using `tkinter`.
- **Logic & Data Layer** — manages authentication, academic records, attendance, and finance operations.

---

## GUI Layer (User Interface)

Implemented with **tkinter** and **ttk**, it provides:

- **Login Screens** for students and administrators  
- **Navigation Sidebars** with custom icons for dashboard, courses, results, attendance, and finance  
- **Reusable Widgets** such as styled entries, progress bars, badges, and stat cards  
- **Dialogs** for inline editing of student, course, and finance records  
- **Scrollable Frames** for displaying long lists of data  
- Consistent **color palette** and **typography** for a modern, accessible interface  

---

## Logic & Data Layer

Handles backend operations and in‑memory data storage:

### Data Stores
- **USERS** — student accounts with GPA, ID, major, and year  
- **ADMINS** — administrator accounts with roles and emails  
- **COURSES, RESULTS, ATTENDANCE, TRANSACTIONS** — academic and financial records  

### Core Functions
- `authenticate()` and `authenticate_admin()` — login validation  
- `register_user()` — new student account creation  
- Summaries: `course_load_summary()`, `attendance_summary()`, `finance_summary()`  
- Utilities: `grade_color()`, `tint()`, `format_leones()`  

### Admin CRUD Operations
- Manage students: add, update, delete  
- Manage courses, results, attendance, and transactions  
- Input validation + updates to in‑memory data stores  

---

## Features

  - Student portal for viewing GPA, courses, attendance, and tuition balance  
  - Admin portal for managing student records, courses, grades, and finances  
  - Clean, responsive GUI with reusable components  
  - Demo accounts included:  
  - Student → `demo/demo123`  
  - Admin → `admin/admin123`  



## Getting Started

1. Clone the repository  
2. Ensure **Python 3.x** is installed  
3. Run the GUI layer file:  
   ```bash
   python gui_layer.py

##Authors
 -Osman Junior Kamara
 -precious Aminata Sandy 
 -Alpha C.K Allieu