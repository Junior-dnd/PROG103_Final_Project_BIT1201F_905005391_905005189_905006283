# Salone EduPortal — Logic & Data Layer

import random


# ─────────────────────────────────────────────
#  DATA STORES
# ─────────────────────────────────────────────
USERS = {
    "demo": {
        "fullname": "Amara Koroma",
        "password": "demo123",
        "gpa":      "3.85",
        "id":       "SEP-2024-0042",
        "major":    "Computer Science",
        "year":     "3rd Year",
        "email":    "amara.koroma@unimak.edu.sl",
    }
}

ADMINS = {
    "admin": {
        "fullname": "Dr. Samuel Conteh",
        "password": "admin123",
        "role":     "System Administrator",
        "email":    "s.conteh@unimak.edu.sl",
    }
}

# (code, name, lecturer, credit_hours, accent_color)
COURSES = [
    ["CSC101", "Programming Fundamentals",  "Dr. Bangura",  3, "#16a34a"],
    ["CSC102", "Database Systems",          "Dr. Conteh",   3, "#2563eb"],
    ["CSC103", "Computer Networking",       "Prof. Sesay",  3, "#d97706"],
    ["CSC104", "Web Development",           "Dr. Kamara",   3, "#7c3aed"],
    ["CSC105", "Software Engineering",      "Prof. Turay",  3, "#dc2626"],
    ["CSC106", "AI & Machine Learning",     "Dr. Koroma",   3, "#0891b2"],
]

# (code, name, grade, score, semester)
RESULTS = [
    ["CSC101", "Programming Fundamentals",  "A",  95, "Semester 1 2024"],
    ["CSC102", "Database Systems",          "B+", 88, "Semester 1 2024"],
    ["CSC103", "Computer Networking",       "A",  92, "Semester 1 2024"],
    ["CSC104", "Web Development",           "A-", 91, "Semester 2 2023"],
    ["CSC105", "Software Engineering",      "B",  85, "Semester 2 2023"],
]

# (code, name, classes_attended, classes_total)
ATTENDANCE = [
    ["CSC101", "Programming Fundamentals",  22, 24],
    ["CSC102", "Database Systems",          21, 24],
    ["CSC103", "Computer Networking",       24, 24],
    ["CSC104", "Web Development",           20, 24],
    ["CSC105", "Software Engineering",      23, 24],
]

# (date, description, amount_in_leones, status) — status is "paid" or "due"
TRANSACTIONS = [
    ["15 Aug 2024", "Tuition Instalment 1", 3_500_000, "paid"],
    ["01 Oct 2024", "Tuition Instalment 2", 3_500_000, "paid"],
    ["15 Dec 2024", "Tuition Instalment 3", 1_000_000, "due"],
]


# ─────────────────────────────────────────────
#  PURE HELPER FUNCTIONS
# ─────────────────────────────────────────────
def grade_color(grade):
    """Map a letter grade to a semantic hex color."""
    if grade.startswith("A"):
        return "#16a34a"
    if grade.startswith("B"):
        return "#2563eb"
    return "#d97706"


def tint(hex_color, amount=0.85):
    """Return a light pastel version of hex_color, blended toward white."""
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    r = int(r + (255 - r) * amount)
    g = int(g + (255 - g) * amount)
    b = int(b + (255 - b) * amount)
    return f"#{r:02x}{g:02x}{b:02x}"


def format_leones(amount):
    """Format an integer amount of Leones as 'Le 3,500,000'."""
    return f"Le {amount:,}"


# ─────────────────────────────────────────────
#  DERIVED SUMMARIES
# ─────────────────────────────────────────────
def course_load_summary():
    count = len(COURSES)
    total_credits = sum(cr for _, _, _, cr, _ in COURSES)
    return count, total_credits


def attendance_summary():
    attended = sum(a for _, _, a, _ in ATTENDANCE)
    total = sum(t for _, _, _, t in ATTENDANCE)
    missed = total - attended
    pct = round(attended / total * 100) if total else 0
    return pct, attended, missed


def course_attendance_status(attended, total):
    pct = int(attended / total * 100) if total else 0
    if pct >= 90:
        return pct, "success"
    if pct >= 75:
        return pct, "warning"
    return pct, "danger"


def finance_summary():
    total = sum(amt for _, _, amt, _ in TRANSACTIONS)
    paid = sum(amt for _, _, amt, status in TRANSACTIONS if status == "paid")
    balance = total - paid
    pct_paid = round(paid / total * 100, 1) if total else 0
    return total, paid, balance, pct_paid


# ─────────────────────────────────────────────
#  AUTHENTICATION & REGISTRATION
# ─────────────────────────────────────────────
def authenticate(username, password):
    """Check student credentials. Returns (success, error_message)."""
    username = username.strip()
    if username in USERS and USERS[username]["password"] == password:
        return True, None
    return False, "Invalid username or password. Please try again."


def authenticate_admin(username, password):
    """Check admin credentials. Returns (success, error_message)."""
    username = username.strip()
    if username in ADMINS and ADMINS[username]["password"] == password:
        return True, None
    return False, "Invalid admin credentials. Please try again."


def get_user(username):
    return USERS.get(username)


def get_admin(username):
    return ADMINS.get(username)


def register_user(fullname, username, password):
    """Validate and create a new student account."""
    fullname = fullname.strip()
    username = username.strip()
    if not fullname or not username or not password:
        return False, "incomplete"
    if username in USERS:
        return False, "taken"
    if len(password) < 6:
        return False, "weak"
    USERS[username] = {
        "fullname": fullname,
        "password": password,
        "gpa":      "0.00",
        "id":       f"SEP-2024-{random.randint(1000, 9999)}",
        "major":    "Undeclared",
        "year":     "1st Year",
        "email":    f"{username}@unimak.edu.sl",
    }
    return True, None


# ─────────────────────────────────────────────
#  ADMIN CRUD OPERATIONS
# ─────────────────────────────────────────────

# ── Students ────────────────────────────────
def admin_get_all_students():
    """Return list of (username, info_dict) for all students."""
    return list(USERS.items())


def admin_update_student(username, field, value):
    """Update a single field on a student record."""
    if username not in USERS:
        return False, "Student not found."
    USERS[username][field] = value
    return True, None


def admin_delete_student(username):
    if username not in USERS:
        return False, "Student not found."
    del USERS[username]
    return True, None


def admin_add_student(fullname, username, password, major, year, gpa):
    fullname = fullname.strip()
    username = username.strip()
    if not fullname or not username or not password:
        return False, "incomplete"
    if username in USERS:
        return False, "taken"
    if len(password) < 6:
        return False, "weak"
    USERS[username] = {
        "fullname": fullname,
        "password": password,
        "gpa":      gpa or "0.00",
        "id":       f"SEP-2024-{random.randint(1000, 9999)}",
        "major":    major or "Undeclared",
        "year":     year or "1st Year",
        "email":    f"{username}@unimak.edu.sl",
    }
    return True, None


# ── Courses ─────────────────────────────────
COURSE_COLORS = [
    "#16a34a", "#2563eb", "#d97706",
    "#7c3aed", "#dc2626", "#0891b2",
    "#db2777", "#ea580c", "#65a30d",
]

def admin_add_course(code, name, lecturer, credits):
    code = code.strip().upper()
    if any(c[0] == code for c in COURSES):
        return False, "Course code already exists."
    color = COURSE_COLORS[len(COURSES) % len(COURSE_COLORS)]
    COURSES.append([code, name, lecturer, int(credits), color])
    return True, None


def admin_update_course(index, code, name, lecturer, credits):
    if index < 0 or index >= len(COURSES):
        return False, "Invalid course index."
    color = COURSES[index][4]
    COURSES[index] = [code.strip().upper(), name, lecturer, int(credits), color]
    return True, None


def admin_delete_course(index):
    if index < 0 or index >= len(COURSES):
        return False, "Invalid course index."
    COURSES.pop(index)
    return True, None


# ── Results ─────────────────────────────────
def admin_add_result(code, name, grade, score, semester):
    RESULTS.append([code.strip().upper(), name, grade, int(score), semester])
    return True, None


def admin_update_result(index, code, name, grade, score, semester):
    if index < 0 or index >= len(RESULTS):
        return False, "Invalid result index."
    RESULTS[index] = [code.strip().upper(), name, grade, int(score), semester]
    return True, None


def admin_delete_result(index):
    if index < 0 or index >= len(RESULTS):
        return False, "Invalid result index."
    RESULTS.pop(index)
    return True, None


# ── Attendance ──────────────────────────────
def admin_add_attendance(code, name, attended, total):
    ATTENDANCE.append([code.strip().upper(), name, int(attended), int(total)])
    return True, None


def admin_update_attendance(index, code, name, attended, total):
    if index < 0 or index >= len(ATTENDANCE):
        return False, "Invalid attendance index."
    ATTENDANCE[index] = [code.strip().upper(), name, int(attended), int(total)]
    return True, None


def admin_delete_attendance(index):
    if index < 0 or index >= len(ATTENDANCE):
        return False, "Invalid attendance index."
    ATTENDANCE.pop(index)
    return True, None


# ── Finance ─────────────────────────────────
def admin_add_transaction(date, description, amount, status):
    TRANSACTIONS.append([date, description, int(amount), status])
    return True, None


def admin_update_transaction(index, date, description, amount, status):
    if index < 0 or index >= len(TRANSACTIONS):
        return False, "Invalid transaction index."
    TRANSACTIONS[index] = [date, description, int(amount), status]
    return True, None


def admin_delete_transaction(index):
    if index < 0 or index >= len(TRANSACTIONS):
        return False, "Invalid transaction index."
    TRANSACTIONS.pop(index)
    return True, None