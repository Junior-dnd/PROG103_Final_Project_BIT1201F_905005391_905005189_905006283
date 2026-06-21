
#Salone EduPortal — GUI Layer

import tkinter as tk
from tkinter import ttk, messagebox
import math

from logic import (
    COURSES, RESULTS, ATTENDANCE, TRANSACTIONS,
    grade_color, tint, format_leones,
    course_load_summary, attendance_summary,
    course_attendance_status, finance_summary,
    authenticate, authenticate_admin,
    get_user, get_admin, register_user,
    admin_get_all_students,
    admin_update_student, admin_delete_student, admin_add_student,
    admin_add_course, admin_update_course, admin_delete_course,
    admin_add_result, admin_update_result, admin_delete_result,
    admin_add_attendance, admin_update_attendance, admin_delete_attendance,
    admin_add_transaction, admin_update_transaction, admin_delete_transaction,
    USERS,
)


# ─────────────────────────────────────────────
#  DESIGN TOKENS
# ─────────────────────────────────────────────
C = {
    "sidebar":        "#111827",
    "sidebar_hover":  "#1f2937",
    "sidebar_active": "#1a3a2a",
    "sidebar_accent": "#16a34a",
    "green":          "#16a34a",
    "green_light":    "#22c55e",
    "green_dark":     "#14532d",
    "gold":           "#d97706",
    "gold_light":     "#fbbf24",
    "gold_pale":      "#fef9ee",
    "bg":             "#f9fafb",
    "card":           "#ffffff",
    "border":         "#e5e7eb",
    "input_bg":       "#f3f4f6",
    "text":           "#111827",
    "text_sub":       "#6b7280",
    "text_muted":     "#9ca3af",
    "white":          "#ffffff",
    "success":        "#16a34a",
    "warning":        "#d97706",
    "danger":         "#dc2626",
    "info":           "#2563eb",
    # Admin sidebar tones
    "admin_sidebar":        "#1e1b4b",
    "admin_sidebar_hover":  "#312e81",
    "admin_sidebar_active": "#1e3a5f",
    "admin_accent":         "#6366f1",
    "admin_dark":           "#0f0a3c",
}

FONT_HEADING  = ("Segoe UI", 22, "bold")
FONT_SUBHEAD  = ("Segoe UI", 14, "bold")
FONT_BODY     = ("Segoe UI", 10)
FONT_BODY_B   = ("Segoe UI", 10, "bold")
FONT_SMALL    = ("Segoe UI", 9)
FONT_SMALL_B  = ("Segoe UI", 9, "bold")
FONT_LABEL    = ("Segoe UI", 8)
FONT_TITLE    = ("Segoe UI", 13, "bold")
FONT_NAV      = ("Segoe UI", 10)
FONT_NAV_B    = ("Segoe UI", 10, "bold")
FONT_LOGO     = ("Segoe UI", 12, "bold")
FONT_LOGO_SUB = ("Segoe UI", 8)


# ─────────────────────────────────────────────
#  ICON PAINTER
# ─────────────────────────────────────────────
class Icon:
    @staticmethod
    def _canvas(parent, size=18, bg=None):
        c = tk.Canvas(parent, width=size, height=size,
                      bg=bg or parent.cget("bg"),
                      highlightthickness=0, bd=0)
        return c

    @staticmethod
    def dashboard(parent, size=18, color="#fff", bg=None):
        c = Icon._canvas(parent, size, bg)
        h = size // 2 - 1; pad = 2
        c.create_rectangle(pad, pad, h, h, fill=color, outline="")
        c.create_rectangle(h+2, pad, size-pad, h, fill=color, outline="")
        c.create_rectangle(pad, h+2, h, size-pad, fill=color, outline="")
        c.create_rectangle(h+2, h+2, size-pad, size-pad, fill=color, outline="")
        return c

    @staticmethod
    def book(parent, size=18, color="#fff", bg=None):
        c = Icon._canvas(parent, size, bg)
        p = 2
        c.create_rectangle(p+3, p, size-p, size-p, fill=color, outline="")
        c.create_rectangle(p, p, p+4, size-p, fill=color, outline="")
        c.create_line(p+3, p, p+3, size-p, fill=bg or parent.cget("bg"), width=1)
        return c

    @staticmethod
    def chart(parent, size=18, color="#fff", bg=None):
        c = Icon._canvas(parent, size, bg)
        p = 2; w = (size - 2*p) // 3
        heights = [size-p-4, size-p-9, size-p-6]
        for i, h in enumerate(heights):
            x0 = p + i*(w+1)
            c.create_rectangle(x0, h, x0+w-1, size-p, fill=color, outline="")
        c.create_line(p, p, p, size-p, fill=color, width=1)
        c.create_line(p, size-p, size-p, size-p, fill=color, width=1)
        return c

    @staticmethod
    def checkmark(parent, size=18, color="#fff", bg=None):
        c = Icon._canvas(parent, size, bg)
        cx, cy, r = size//2, size//2, size//2-2
        c.create_oval(cx-r, cy-r, cx+r, cy+r, outline=color, width=2)
        c.create_line(4, cy, cx-1, size-5, cx-1, size-5, size-4, 5,
                      fill=color, width=2, smooth=True)
        return c

    @staticmethod
    def wallet(parent, size=18, color="#fff", bg=None):
        c = Icon._canvas(parent, size, bg)
        p = 2
        c.create_rectangle(p, p+4, size-p, size-p, fill=color, outline="")
        c.create_rectangle(p, p+2, size-p-4, p+6, fill=color, outline="")
        c.create_oval(size-7, size//2-3, size-3, size//2+3,
                      fill=bg or parent.cget("bg"), outline=bg or parent.cget("bg"))
        return c

    @staticmethod
    def person(parent, size=18, color="#fff", bg=None):
        c = Icon._canvas(parent, size, bg)
        cx = size // 2; r = size // 5
        c.create_oval(cx-r, 2, cx+r, 2+r*2, fill=color, outline="")
        c.create_arc(2, size//2, size-2, size+4, start=0, extent=180,
                     fill=color, outline="")
        return c

    @staticmethod
    def gear(parent, size=18, color="#fff", bg=None):
        c = Icon._canvas(parent, size, bg)
        cx, cy = size/2, size/2
        r_out, r_in = size/2-2, size/4
        teeth, pts = 8, []
        for i in range(teeth*2):
            angle = math.pi * i / teeth
            r = r_out if i % 2 == 0 else r_out - 3
            pts += [cx + r*math.cos(angle), cy + r*math.sin(angle)]
        c.create_polygon(pts, fill=color, outline="")
        c.create_oval(cx-r_in, cy-r_in, cx+r_in, cy+r_in,
                      fill=bg or parent.cget("bg"), outline="")
        return c

    @staticmethod
    def logout(parent, size=18, color="#ef4444", bg=None):
        c = Icon._canvas(parent, size, bg)
        p = 3
        c.create_arc(p, p, size-p-4, size-p, start=30, extent=300,
                     outline=color, width=2, style="arc")
        arrow_x = size-p-1; mid = size//2
        c.create_line(mid, mid, arrow_x, mid, fill=color, width=2)
        c.create_line(arrow_x-3, mid-3, arrow_x, mid,
                      arrow_x-3, mid+3, fill=color, width=2)
        return c

    @staticmethod
    def attendance_icon(parent, size=18, color="#fff", bg=None):
        c = Icon._canvas(parent, size, bg)
        p = 2
        c.create_rectangle(p, p+3, size-p, size-p, outline=color, width=2)
        c.create_line(p+3, p, p+3, p+5, fill=color, width=2)
        c.create_line(size-p-3, p, size-p-3, p+5, fill=color, width=2)
        c.create_line(p, p+7, size-p, p+7, fill=color, width=1)
        c.create_line(5, 12, 8, 15, 13, 9, fill=color, width=2)
        return c

    @staticmethod
    def users(parent, size=18, color="#fff", bg=None):
        c = Icon._canvas(parent, size, bg)
        cx = size // 2; r = size // 6
        c.create_oval(cx-r-3, 2, cx+r-3, 2+r*2, fill=color, outline="")
        c.create_arc(0, size//2-2, size-6, size+2,
                     start=0, extent=180, fill=color, outline="")
        c.create_oval(cx+r, 2, cx+r*3, 2+r*2, fill=color, outline="")
        c.create_arc(6, size//2, size+2, size+6,
                     start=0, extent=180, fill=color, outline="")
        return c

    @staticmethod
    def shield(parent, size=18, color="#6366f1", bg=None):
        c = Icon._canvas(parent, size, bg)
        cx = size // 2
        pts = [cx, 2, size-3, 5, size-3, size//2+2,
               cx, size-2, 3, size//2+2, 3, 5]
        c.create_polygon(pts, fill=color, outline="")
        return c


# ─────────────────────────────────────────────
#  SCROLLABLE FRAME
# ─────────────────────────────────────────────
class ScrollFrame(tk.Frame):
    def __init__(self, parent, **kw):
        super().__init__(parent, **kw)
        bg = kw.get("bg", C["bg"])
        canvas = tk.Canvas(self, bg=bg, highlightthickness=0, bd=0)
        vsb = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.inner = tk.Frame(canvas, bg=bg)
        canvas.create_window((0, 0), window=self.inner, anchor="nw")
        canvas.configure(yscrollcommand=vsb.set)
        canvas.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        self.inner.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))


# ─────────────────────────────────────────────
#  REUSABLE WIDGETS
# ─────────────────────────────────────────────
def card(parent, **kw):
    kw.setdefault("bg", C["card"])
    kw.setdefault("relief", "flat")
    kw.setdefault("bd", 0)
    return tk.Frame(parent, **kw)


def divider(parent, color=None, pady=0):
    tk.Frame(parent, height=1, bg=color or C["border"]).pack(fill="x", pady=pady)


def label(parent, text, font=FONT_BODY, fg=None, bg=None, **kw):
    fg = fg or C["text"]
    bg = bg or (parent.cget("bg") if hasattr(parent, "cget") else C["card"])
    return tk.Label(parent, text=text, font=font, fg=fg, bg=bg, **kw)


def badge(parent, text, fg, bg_color):
    f = tk.Frame(parent, bg=bg_color, padx=8, pady=3)
    tk.Label(f, text=text, font=FONT_SMALL_B, fg=fg, bg=bg_color).pack()
    return f


def progress_bar(parent, value, width=300, height=8, fill_color=None, bg_color=None):
    fill_color = fill_color or C["green"]
    bg_color   = bg_color   or C["border"]
    pct = max(0, min(100, value)) / 100
    outer = tk.Canvas(parent, width=width, height=height,
                      highlightthickness=0, bd=0, bg=parent.cget("bg"))
    outer.create_rectangle(0, 0, width, height, fill=bg_color, outline="")
    outer.create_rectangle(0, 0, int(width*pct), height, fill=fill_color, outline="")
    return outer


def styled_entry(parent, textvariable, width=30, show=None):
    f = tk.Frame(parent, bg=C["input_bg"],
                 highlightbackground=C["border"], highlightthickness=1)
    kw = dict(textvariable=textvariable, font=FONT_BODY,
              bg=C["input_bg"], fg=C["text"], relief="flat",
              bd=0, width=width, insertbackground=C["text"])
    if show:
        kw["show"] = show
    e = tk.Entry(f, **kw)
    e.pack(padx=10, pady=8)
    return f, e


def primary_btn(parent, text, command, bg=None, fg=None, width=None):
    bg = bg or C["green"]
    fg = fg or C["white"]
    kw = dict(text=text, command=command, bg=bg, fg=fg,
              font=FONT_BODY_B, relief="flat",
              activebackground=C["green_dark"],
              activeforeground=C["white"],
              cursor="hand2", padx=16, pady=9)
    if width:
        kw["width"] = width
    return tk.Button(parent, **kw)


def stat_card(parent, title, value, sub, accent):
    f = card(parent, padx=18, pady=16)
    bar = tk.Frame(f, bg=accent, width=4)
    bar.pack(side="left", fill="y", padx=(0, 14))
    inner = tk.Frame(f, bg=C["card"])
    inner.pack(side="left", fill="both", expand=True)
    label(inner, value, font=("Segoe UI", 20, "bold"), fg=accent, bg=C["card"]).pack(anchor="w")
    label(inner, title, font=FONT_BODY_B, fg=C["text"], bg=C["card"]).pack(anchor="w")
    label(inner, sub, font=FONT_SMALL, fg=C["text_sub"], bg=C["card"]).pack(anchor="w")
    return f


# ─────────────────────────────────────────────
#  ADMIN NAV ITEM
# ─────────────────────────────────────────────
class AdminNavItem(tk.Frame):
    def __init__(self, parent, text, icon_fn, command, active=False):
        super().__init__(parent, bg=C["admin_sidebar"], cursor="hand2")
        self._active = active
        self._cmd = command
        self._text = text
        self._icon_fn = icon_fn
        self._build()
        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>",    self._on_enter)
        self.bind("<Leave>",    self._on_leave)

    def _build(self):
        for w in self.winfo_children():
            w.destroy()
        bg = C["admin_sidebar_active"] if self._active else C["admin_sidebar"]
        fg = "#a5b4fc" if self._active else "#9ca3af"
        acc = tk.Frame(self, bg=C["admin_accent"] if self._active else C["admin_sidebar"], width=3)
        acc.pack(side="left", fill="y")
        ico = self._icon_fn(self, size=16, color=fg, bg=bg)
        ico.configure(bg=bg)
        ico.pack(side="left", padx=(12, 8), pady=10)
        tk.Label(self, text=self._text,
                 font=FONT_NAV_B if self._active else FONT_NAV,
                 fg=fg, bg=bg, anchor="w").pack(side="left", fill="x", expand=True)
        self.configure(bg=bg)
        for child in self.winfo_children():
            child.bind("<Button-1>", self._on_click)
            child.bind("<Enter>",    self._on_enter)
            child.bind("<Leave>",    self._on_leave)

    def set_active(self, val):
        self._active = val
        self._build()

    def _on_click(self, e=None): self._cmd()
    def _on_enter(self, e=None):
        if not self._active:
            self.configure(bg=C["admin_sidebar_hover"])
            for w in self.winfo_children():
                try: w.configure(bg=C["admin_sidebar_hover"])
                except: pass
    def _on_leave(self, e=None):
        bg = C["admin_sidebar_active"] if self._active else C["admin_sidebar"]
        self.configure(bg=bg)
        for w in self.winfo_children():
            try: w.configure(bg=bg)
            except: pass


# ─────────────────────────────────────────────
#  SIDEBAR NAV ITEM (Student)
# ─────────────────────────────────────────────
class NavItem(tk.Frame):
    def __init__(self, parent, text, icon_fn, command, active=False):
        super().__init__(parent, bg=C["sidebar"], cursor="hand2", padx=0, pady=0)
        self._active = active
        self._cmd    = command
        self._text   = text
        self._icon_fn = icon_fn
        self._build()
        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>",    self._on_enter)
        self.bind("<Leave>",    self._on_leave)

    def _build(self):
        for w in self.winfo_children():
            w.destroy()
        bg = C["sidebar_active"] if self._active else C["sidebar"]
        fg = C["green_light"]    if self._active else "#9ca3af"
        acc = tk.Frame(self, bg=C["green"] if self._active else C["sidebar"], width=3)
        acc.pack(side="left", fill="y")
        ico = self._icon_fn(self, size=16, color=fg, bg=bg)
        ico.configure(bg=bg)
        ico.pack(side="left", padx=(12, 8), pady=10)
        tk.Label(self, text=self._text,
                 font=FONT_NAV_B if self._active else FONT_NAV,
                 fg=fg, bg=bg, anchor="w").pack(side="left", fill="x", expand=True)
        self.configure(bg=bg)
        for child in self.winfo_children():
            child.bind("<Button-1>", self._on_click)
            child.bind("<Enter>",    self._on_enter)
            child.bind("<Leave>",    self._on_leave)

    def set_active(self, val):
        self._active = val
        self._build()

    def _on_click(self, e=None): self._cmd()
    def _on_enter(self, e=None):
        if not self._active:
            self.configure(bg=C["sidebar_hover"])
            for w in self.winfo_children():
                try: w.configure(bg=C["sidebar_hover"])
                except: pass
    def _on_leave(self, e=None):
        bg = C["sidebar_active"] if self._active else C["sidebar"]
        self.configure(bg=bg)
        for w in self.winfo_children():
            try: w.configure(bg=bg)
            except: pass


# ─────────────────────────────────────────────
#  INLINE EDIT DIALOG HELPER
# ─────────────────────────────────────────────
class EditDialog(tk.Toplevel):
    """Generic modal dialog with labelled entry fields."""
    def __init__(self, parent, title, fields, on_save, prefill=None):
        super().__init__(parent)
        self.title(title)
        self.resizable(False, False)
        self.configure(bg=C["bg"])
        self.grab_set()
        self._vars = {}
        self._on_save = on_save

        hdr = tk.Frame(self, bg=C["admin_dark"], padx=20, pady=14)
        hdr.pack(fill="x")
        tk.Label(hdr, text=title, font=FONT_SUBHEAD,
                 fg=C["white"], bg=C["admin_dark"]).pack(anchor="w")

        body = card(self, padx=24, pady=20)
        body.pack(fill="both", expand=True, padx=16, pady=16)

        for key, lbl_txt, show in fields:
            tk.Label(body, text=lbl_txt.upper(),
                     font=("Segoe UI", 8, "bold"),
                     fg=C["text_sub"], bg=C["card"]).pack(anchor="w", pady=(8, 2))
            var = tk.StringVar(value=(prefill.get(key, "") if prefill else ""))
            self._vars[key] = var
            f, _ = styled_entry(body, var, width=34, show=show)
            f.pack(fill="x")

        btn_row = tk.Frame(body, bg=C["card"])
        btn_row.pack(fill="x", pady=(18, 0))
        primary_btn(btn_row, "Save", self._save, width=16).pack(side="left")
        tk.Button(btn_row, text="Cancel", font=FONT_BODY,
                  fg=C["text_sub"], bg=C["card"], relief="flat",
                  cursor="hand2", command=self.destroy).pack(side="left", padx=8)

        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        x = parent.winfo_rootx() + (parent.winfo_width()  - w) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - h) // 2
        self.geometry(f"+{x}+{y}")

    def _save(self):
        values = {k: v.get() for k, v in self._vars.items()}
        self._on_save(values)
        self.destroy()


# ─────────────────────────────────────────────
#  LOGIN SCREEN
# ─────────────────────────────────────────────
class LoginScreen(tk.Frame):
    def __init__(self, parent, on_login, on_register, on_admin_login):
        super().__init__(parent, bg=C["sidebar"])
        self._on_login       = on_login
        self._on_register    = on_register
        self._on_admin_login = on_admin_login
        self._username       = tk.StringVar()
        self._password       = tk.StringVar()
        self._err_var        = tk.StringVar()
        self._build()

    def _build(self):
        # ── Left panel ──────────────────────────────
        left = tk.Frame(self, bg=C["green_dark"], width=460)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        pad = tk.Frame(left, bg=C["green_dark"])
        pad.place(relx=0.5, rely=0.5, anchor="center")

        crest_canvas = tk.Canvas(pad, width=56, height=64,
                                 bg=C["green_dark"], highlightthickness=0)
        crest_canvas.pack(pady=(0, 18))
        pts = [28, 4, 52, 14, 52, 36, 28, 60, 4, 36, 4, 14]
        crest_canvas.create_polygon(pts, fill=C["gold"],
                                    outline=C["gold_light"], width=2)
        crest_canvas.create_line(28, 18, 28, 46, fill=C["green_dark"], width=3)
        crest_canvas.create_line(16, 32, 40, 32, fill=C["green_dark"], width=3)

        tk.Label(pad, text="SALONE EDUPORTAL",
                 font=("Segoe UI", 20, "bold"),
                 fg=C["white"], bg=C["green_dark"]).pack()
        tk.Label(pad, text="Student Academic Portal",
                 font=("Segoe UI", 11),
                 fg="#86efac", bg=C["green_dark"]).pack(pady=(4, 24))

        divider(pad, color="#166534", pady=0)
        tk.Frame(pad, height=24, bg=C["green_dark"]).pack()

        for line in [
            ("Academic Records",  "Track your GPA and semester results"),
            ("Course Management", "View enrolled courses and schedules"),
            ("Fee & Finance",     "Monitor tuition balance in Leones"),
        ]:
            row = tk.Frame(pad, bg=C["green_dark"])
            row.pack(fill="x", pady=6)
            dot = tk.Canvas(row, width=8, height=8,
                            bg=C["green_dark"], highlightthickness=0)
            dot.create_oval(1, 1, 7, 7, fill=C["gold"], outline="")
            dot.pack(side="left", padx=(0, 10), pady=2)
            inner = tk.Frame(row, bg=C["green_dark"])
            inner.pack(side="left")
            tk.Label(inner, text=line[0], font=FONT_BODY_B,
                     fg=C["white"], bg=C["green_dark"]).pack(anchor="w")
            tk.Label(inner, text=line[1], font=FONT_SMALL,
                     fg="#86efac", bg=C["green_dark"]).pack(anchor="w")

        # Admin portal button on left panel
        tk.Frame(pad, height=28, bg=C["green_dark"]).pack()
        divider(pad, color="#166534")
        tk.Frame(pad, height=14, bg=C["green_dark"]).pack()
        admin_btn = tk.Button(
            pad, text="Admin Portal  →",
            font=("Segoe UI", 9, "bold"),
            fg=C["gold_light"], bg="#1a3a2a",
            relief="flat", cursor="hand2",
            activeforeground=C["gold"],
            activebackground="#1a3a2a",
            padx=14, pady=8,
            command=self._on_admin_login)
        admin_btn.pack()
        tk.Label(pad, text="Staff & administrator access",
                 font=FONT_LABEL, fg="#6b7280",
                 bg=C["green_dark"]).pack(pady=(4, 0))

        # ── Right panel ─────────────────────────────
        right = tk.Frame(self, bg=C["card"])
        right.pack(side="right", fill="both", expand=True)

        form = tk.Frame(right, bg=C["card"])
        form.place(relx=0.5, rely=0.5, anchor="center", width=360)

        tk.Label(form, text="Sign In", font=("Segoe UI", 22, "bold"),
                 fg=C["text"], bg=C["card"]).pack(anchor="w")
        tk.Label(form, text="Enter your student credentials to continue.",
                 font=FONT_SMALL, fg=C["text_sub"],
                 bg=C["card"]).pack(anchor="w", pady=(4, 20))

        hint = tk.Frame(form, bg="#f0fdf4",
                        highlightbackground="#bbf7d0", highlightthickness=1)
        hint.pack(fill="x", pady=(0, 16))
        tk.Label(hint,
                 text="Demo login: username  demo   |   password  demo123",
                 font=FONT_SMALL, fg="#166534",
                 bg="#f0fdf4").pack(padx=12, pady=8)

        self._err_lbl = tk.Label(form, textvariable=self._err_var,
                                 font=FONT_SMALL, fg=C["danger"],
                                 bg=C["card"], wraplength=340, justify="left")
        self._err_lbl.pack(anchor="w", pady=(0, 4))

        tk.Label(form, text="USERNAME", font=("Segoe UI", 8, "bold"),
                 fg=C["text_sub"], bg=C["card"]).pack(anchor="w", pady=(8, 3))
        u_frame, self._u_entry = styled_entry(form, self._username, width=32)
        u_frame.pack(fill="x")

        tk.Label(form, text="PASSWORD", font=("Segoe UI", 8, "bold"),
                 fg=C["text_sub"], bg=C["card"]).pack(anchor="w", pady=(14, 3))
        p_frame, self._p_entry = styled_entry(form, self._password, width=32, show="*")
        p_frame.pack(fill="x")
        self._p_entry.bind("<Return>", lambda e: self._login())

        tk.Frame(form, height=8, bg=C["card"]).pack()
        primary_btn(form, "Sign In", self._login, width=32).pack(fill="x", ipady=2)

        tk.Frame(form, height=12, bg=C["card"]).pack()
        bottom = tk.Frame(form, bg=C["card"])
        bottom.pack()
        tk.Label(bottom, text="No account yet?",
                 font=FONT_SMALL, fg=C["text_sub"], bg=C["card"]).pack(side="left")
        tk.Button(bottom, text=" Create account",
                  font=("Segoe UI", 9, "bold"), fg=C["green"],
                  bg=C["card"], relief="flat", cursor="hand2",
                  activeforeground=C["green_dark"],
                  activebackground=C["card"],
                  command=self._on_register).pack(side="left")

    def _login(self):
        success, error = authenticate(self._username.get(), self._password.get())
        if success:
            self._err_var.set("")
            self._on_login(self._username.get().strip())
        else:
            self._err_var.set(error)


# ─────────────────────────────────────────────
#  ADMIN LOGIN SCREEN
# ─────────────────────────────────────────────
class AdminLoginScreen(tk.Frame):
    def __init__(self, parent, on_login, on_back):
        super().__init__(parent, bg=C["admin_dark"])
        self._on_login = on_login
        self._on_back  = on_back
        self._username = tk.StringVar()
        self._password = tk.StringVar()
        self._err_var  = tk.StringVar()
        self._build()

    def _build(self):
        # Left panel — admin branding
        left = tk.Frame(self, bg=C["admin_dark"], width=460)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        pad = tk.Frame(left, bg=C["admin_dark"])
        pad.place(relx=0.5, rely=0.5, anchor="center")

        # Shield icon
        sh = tk.Canvas(pad, width=64, height=72,
                       bg=C["admin_dark"], highlightthickness=0)
        sh.pack(pady=(0, 18))
        pts = [32, 4, 60, 16, 60, 42, 32, 68, 4, 42, 4, 16]
        sh.create_polygon(pts, fill=C["admin_accent"],
                          outline="#818cf8", width=2)
        sh.create_line(32, 22, 32, 52, fill=C["admin_dark"], width=3)
        sh.create_line(20, 37, 44, 37, fill=C["admin_dark"], width=3)
        sh.create_oval(26, 28, 38, 40, fill="#818cf8", outline="")

        tk.Label(pad, text="ADMIN PORTAL",
                 font=("Segoe UI", 20, "bold"),
                 fg=C["white"], bg=C["admin_dark"]).pack()
        tk.Label(pad, text="Staff & Administrator Access",
                 font=("Segoe UI", 11),
                 fg="#a5b4fc", bg=C["admin_dark"]).pack(pady=(4, 24))

        tk.Frame(pad, height=1, bg="#312e81", width=260).pack(fill="x")
        tk.Frame(pad, height=20, bg=C["admin_dark"]).pack()

        for line in [
            ("Student Management",  "Add, edit, and remove student records"),
            ("Academic Records",    "Manage courses, results, and attendance"),
            ("Finance Control",     "Edit tuition fees and payment records"),
        ]:
            row = tk.Frame(pad, bg=C["admin_dark"])
            row.pack(fill="x", pady=6)
            dot = tk.Canvas(row, width=8, height=8,
                            bg=C["admin_dark"], highlightthickness=0)
            dot.create_oval(1, 1, 7, 7, fill=C["admin_accent"], outline="")
            dot.pack(side="left", padx=(0, 10), pady=2)
            inner = tk.Frame(row, bg=C["admin_dark"])
            inner.pack(side="left")
            tk.Label(inner, text=line[0], font=FONT_BODY_B,
                     fg=C["white"], bg=C["admin_dark"]).pack(anchor="w")
            tk.Label(inner, text=line[1], font=FONT_SMALL,
                     fg="#a5b4fc", bg=C["admin_dark"]).pack(anchor="w")

        tk.Frame(pad, height=28, bg=C["admin_dark"]).pack()
        tk.Frame(pad, height=1, bg="#312e81", width=260).pack(fill="x")
        tk.Frame(pad, height=14, bg=C["admin_dark"]).pack()
        tk.Button(pad, text="← Student Login",
                  font=("Segoe UI", 9, "bold"),
                  fg="#a5b4fc", bg="#1e1b4b",
                  relief="flat", cursor="hand2",
                  activeforeground=C["white"],
                  activebackground="#1e1b4b",
                  padx=14, pady=8,
                  command=self._on_back).pack()

        # Right panel — form
        right = tk.Frame(self, bg=C["card"])
        right.pack(side="right", fill="both", expand=True)

        form = tk.Frame(right, bg=C["card"])
        form.place(relx=0.5, rely=0.5, anchor="center", width=360)

        tk.Label(form, text="Admin Sign In",
                 font=("Segoe UI", 22, "bold"),
                 fg=C["text"], bg=C["card"]).pack(anchor="w")
        tk.Label(form,
                 text="Enter your administrator credentials to continue.",
                 font=FONT_SMALL, fg=C["text_sub"],
                 bg=C["card"]).pack(anchor="w", pady=(4, 20))

        hint = tk.Frame(form, bg="#eef2ff",
                        highlightbackground="#c7d2fe", highlightthickness=1)
        hint.pack(fill="x", pady=(0, 16))
        tk.Label(hint,
                 text="Demo: username  admin   |   password  admin123",
                 font=FONT_SMALL, fg="#3730a3",
                 bg="#eef2ff").pack(padx=12, pady=8)

        self._err_lbl = tk.Label(form, textvariable=self._err_var,
                                 font=FONT_SMALL, fg=C["danger"],
                                 bg=C["card"], wraplength=340)
        self._err_lbl.pack(anchor="w", pady=(0, 4))

        tk.Label(form, text="USERNAME", font=("Segoe UI", 8, "bold"),
                 fg=C["text_sub"], bg=C["card"]).pack(anchor="w", pady=(8, 3))
        u_frame, self._u_entry = styled_entry(form, self._username, width=32)
        u_frame.pack(fill="x")

        tk.Label(form, text="PASSWORD", font=("Segoe UI", 8, "bold"),
                 fg=C["text_sub"], bg=C["card"]).pack(anchor="w", pady=(14, 3))
        p_frame, self._p_entry = styled_entry(form, self._password, width=32, show="*")
        p_frame.pack(fill="x")
        self._p_entry.bind("<Return>", lambda e: self._login())

        tk.Frame(form, height=8, bg=C["card"]).pack()
        tk.Button(form, text="Sign In as Admin",
                  font=FONT_BODY_B, bg=C["admin_accent"], fg=C["white"],
                  relief="flat", cursor="hand2",
                  activebackground="#4f46e5",
                  activeforeground=C["white"],
                  padx=16, pady=9, width=32,
                  command=self._login).pack(fill="x", ipady=2)

    def _login(self):
        success, error = authenticate_admin(
            self._username.get(), self._password.get())
        if success:
            self._err_var.set("")
            self._on_login(self._username.get().strip())
        else:
            self._err_var.set(error)


# ─────────────────────────────────────────────
#  REGISTER SCREEN
# ─────────────────────────────────────────────
class RegisterScreen(tk.Frame):
    def __init__(self, parent, on_back, on_register):
        super().__init__(parent, bg=C["bg"])
        self._on_back     = on_back
        self._on_register = on_register
        self._vars = {k: tk.StringVar()
                      for k in ("fullname", "username", "password")}
        self._build()

    def _build(self):
        outer = tk.Frame(self, bg=C["bg"])
        outer.place(relx=0.5, rely=0.5, anchor="center", width=440)

        hdr = tk.Frame(outer, bg=C["green_dark"], padx=24, pady=24)
        hdr.pack(fill="x")
        tk.Label(hdr, text="SALONE EDUPORTAL", font=FONT_LOGO,
                 fg=C["gold"], bg=C["green_dark"]).pack(anchor="w")
        tk.Label(hdr, text="New Student Registration",
                 font=FONT_SUBHEAD, fg=C["white"],
                 bg=C["green_dark"]).pack(anchor="w", pady=(4, 0))

        body = card(outer, padx=32, pady=28)
        body.pack(fill="x")

        fields = [
            ("FULL NAME", "fullname", "e.g. Amara Koroma", None),
            ("USERNAME",  "username", "e.g. amara_k",      None),
            ("PASSWORD",  "password", "Min. 6 characters", "*"),
        ]
        for label_txt, key, ph, show in fields:
            tk.Label(body, text=label_txt, font=("Segoe UI", 8, "bold"),
                     fg=C["text_sub"], bg=C["card"]).pack(anchor="w", pady=(10, 3))
            f, _ = styled_entry(body, self._vars[key], width=34, show=show)
            f.pack(fill="x")
            tk.Label(body, text=ph, font=FONT_SMALL,
                     fg=C["text_muted"], bg=C["card"]).pack(anchor="w")

        tk.Frame(body, height=10, bg=C["card"]).pack()
        primary_btn(body, "Create Account", self._submit, width=34).pack(fill="x", ipady=2)
        tk.Frame(body, height=6, bg=C["card"]).pack()
        tk.Button(body, text="Back to Sign In", font=FONT_BODY,
                  fg=C["text_sub"], bg=C["card"], relief="flat",
                  cursor="hand2", command=self._on_back).pack()

    def _submit(self):
        vals = {k: v.get() for k, v in self._vars.items()}
        success, error_kind = register_user(
            vals["fullname"], vals["username"], vals["password"])
        if not success:
            msgs = {"incomplete": ("Incomplete", "Please fill in all fields.", "warning"),
                    "taken":      ("Taken",       "That username is already registered.", "error"),
                    "weak":       ("Weak Password","Password must be at least 6 characters.", "warning")}
            t, m, kind = msgs[error_kind]
            (messagebox.showwarning if kind == "warning" else messagebox.showerror)(t, m, parent=self)
            return
        messagebox.showinfo("Registered",
            f"Account created for {vals['fullname'].strip()}.\nYou may now sign in.",
            parent=self)
        self._on_back()


# ─────────────────────────────────────────────
#  ADMIN DASHBOARD
# ─────────────────────────────────────────────
class AdminDashboard(tk.Frame):
    PAGES = [
        ("Overview",   Icon.dashboard),
        ("Students",   Icon.users),
        ("Courses",    Icon.book),
        ("Results",    Icon.chart),
        ("Attendance", Icon.attendance_icon),
        ("Finance",    Icon.wallet),
        ("Settings",   Icon.gear),
    ]

    def __init__(self, parent, username, on_logout):
        super().__init__(parent, bg=C["bg"])
        self._user      = username
        self._info      = get_admin(username)
        self._on_logout = on_logout
        self._active    = "Overview"
        self._nav_items = {}
        self._build()

    def _build(self):
        # ── Admin Sidebar ──────────────────────────────
        sb = tk.Frame(self, bg=C["admin_sidebar"], width=220)
        sb.pack(side="left", fill="y")
        sb.pack_propagate(False)

        logo_frame = tk.Frame(sb, bg=C["admin_dark"], pady=16)
        logo_frame.pack(fill="x")
        # Shield badge inline
        sh = tk.Canvas(logo_frame, width=20, height=22,
                       bg=C["admin_dark"], highlightthickness=0)
        sh.pack(side="left", padx=(16, 6))
        pts2 = [10, 2, 19, 6, 19, 14, 10, 20, 1, 14, 1, 6]
        sh.create_polygon(pts2, fill=C["admin_accent"], outline="")

        text_f = tk.Frame(logo_frame, bg=C["admin_dark"])
        text_f.pack(side="left")
        tk.Label(text_f, text="SALONE EDUPORTAL",
                 font=FONT_LOGO, fg="#e0e7ff",
                 bg=C["admin_dark"]).pack(anchor="w")
        tk.Label(text_f, text="Admin Portal",
                 font=FONT_LOGO_SUB, fg="#a5b4fc",
                 bg=C["admin_dark"]).pack(anchor="w", pady=(2, 0))

        tk.Frame(sb, bg="#312e81", height=1).pack(fill="x")
        tk.Frame(sb, bg=C["admin_sidebar"], height=10).pack()

        tk.Label(sb, text="MANAGEMENT",
                 font=("Segoe UI", 7, "bold"),
                 fg="#4b5563", bg=C["admin_sidebar"]).pack(
            anchor="w", padx=16, pady=(6, 4))

        for name, icon_fn in self.PAGES:
            item = AdminNavItem(sb, name, icon_fn,
                                command=lambda n=name: self._switch(n),
                                active=(name == self._active))
            item.pack(fill="x")
            self._nav_items[name] = item

        tk.Frame(sb, bg=C["admin_sidebar"]).pack(fill="y", expand=True)
        tk.Frame(sb, bg="#312e81", height=1).pack(fill="x")

        user_strip = tk.Frame(sb, bg=C["admin_sidebar"], pady=12)
        user_strip.pack(fill="x")

        av = tk.Canvas(user_strip, width=34, height=34,
                       bg=C["admin_sidebar"], highlightthickness=0)
        av.pack(side="left", padx=(14, 8))
        av.create_oval(1, 1, 33, 33, fill=C["admin_accent"], outline="")
        initials = "".join(p[0] for p in self._info["fullname"].split())[:2].upper()
        av.create_text(17, 17, text=initials,
                       font=("Segoe UI", 11, "bold"), fill="white")

        u_info = tk.Frame(user_strip, bg=C["admin_sidebar"])
        u_info.pack(side="left", fill="x", expand=True)
        tk.Label(u_info, text=self._info["fullname"].split()[0],
                 font=FONT_SMALL_B, fg=C["white"],
                 bg=C["admin_sidebar"]).pack(anchor="w")
        tk.Label(u_info, text=self._info["role"],
                 font=FONT_LABEL, fg="#6b7280",
                 bg=C["admin_sidebar"]).pack(anchor="w")

        tk.Button(sb, text="Sign Out",
                  font=FONT_SMALL_B, fg=C["danger"],
                  bg="#1e1b4b", relief="flat", cursor="hand2",
                  activeforeground="#fca5a5",
                  activebackground="#1e1b4b",
                  command=self._on_logout, pady=8).pack(
            fill="x", padx=12, pady=(0, 12))

        # ── Content area ──────────────────────────────
        self._content = tk.Frame(self, bg=C["bg"])
        self._content.pack(side="right", fill="both", expand=True)
        self._pages = {}
        self._load_page("Overview")

    def _switch(self, name):
        if name == self._active:
            return
        if self._active in self._pages:
            self._pages[self._active].pack_forget()
        self._nav_items[self._active].set_active(False)
        self._active = name
        self._nav_items[name].set_active(True)
        self._load_page(name)

    def _reload_page(self, name):
        """Destroy cached page and reload it fresh."""
        if name in self._pages:
            self._pages[name].pack_forget()
            self._pages[name].destroy()
            del self._pages[name]
        self._load_page(name)

    def _load_page(self, name):
        if name not in self._pages:
            builders = {
                "Overview":   self._page_overview,
                "Students":   self._page_students,
                "Courses":    self._page_courses,
                "Results":    self._page_results,
                "Attendance": self._page_attendance,
                "Finance":    self._page_finance,
                "Settings":   self._page_settings,
            }
            pg = builders[name]()
            self._pages[name] = pg
        self._pages[name].pack(fill="both", expand=True)

    def _page_header(self, parent, title, subtitle=None, accent=None):
        hdr = tk.Frame(parent, bg=C["bg"], pady=0)
        hdr.pack(fill="x", padx=28, pady=(24, 4))
        label(hdr, title, font=("Segoe UI", 18, "bold"),
              fg=C["text"], bg=C["bg"]).pack(anchor="w")
        if subtitle:
            label(hdr, subtitle, font=FONT_SMALL,
                  fg=C["text_sub"], bg=C["bg"]).pack(anchor="w", pady=(2, 0))
        tk.Frame(parent, bg=accent or C["admin_accent"], height=2).pack(
            fill="x", padx=28, pady=(8, 20))

    def _action_btn(self, parent, text, command, color=None):
        color = color or C["admin_accent"]
        return tk.Button(parent, text=text, command=command,
                         bg=color, fg=C["white"],
                         font=FONT_SMALL_B, relief="flat",
                         cursor="hand2", padx=10, pady=5,
                         activebackground="#4f46e5",
                         activeforeground=C["white"])

    # ── OVERVIEW ────────────────────────────────────
    def _page_overview(self):
        sf = ScrollFrame(self._content, bg=C["bg"])
        p = sf.inner
        self._page_header(p,
            f"Welcome, {self._info['fullname'].split()[0]}",
            f"{self._info['role']}  |  University of Makeni (UNIMAK)")

        stat_row = tk.Frame(p, bg=C["bg"])
        stat_row.pack(fill="x", padx=28, pady=(0, 20))

        stats = [
            ("Total Students",  str(len(USERS)),    "Registered accounts", C["admin_accent"]),
            ("Active Courses",  str(len(COURSES)),  f"{sum(c[3] for c in COURSES)} credit hours", C["green"]),
            ("Results Logged",  str(len(RESULTS)),  "Across all semesters", C["gold"]),
            ("Transactions",    str(len(TRANSACTIONS)), "Payment records", C["info"]),
        ]
        for i, (t, v, s, a) in enumerate(stats):
            sc = stat_card(stat_row, t, v, s, a)
            sc.grid(row=0, column=i, padx=(0, 12), sticky="nsew")
            stat_row.columnconfigure(i, weight=1)

        # Quick summary cards
        cols = tk.Frame(p, bg=C["bg"])
        cols.pack(fill="x", padx=28, pady=(0, 28))

        # Student list preview
        left_col = card(cols, padx=0, pady=0)
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 12))
        tk.Label(left_col, text="Registered Students",
                 font=FONT_TITLE, fg=C["text"],
                 bg=C["card"]).pack(anchor="w", padx=20, pady=(18, 12))
        divider(left_col)

        for uname, info in list(USERS.items())[:5]:
            row = tk.Frame(left_col, bg=C["card"])
            row.pack(fill="x", padx=20, pady=8)
            av = tk.Canvas(row, width=30, height=30,
                           bg=C["card"], highlightthickness=0)
            av.pack(side="left")
            av.create_oval(1, 1, 29, 29, fill=C["admin_accent"], outline="")
            initials = "".join(p2[0] for p2 in info["fullname"].split())[:2].upper()
            av.create_text(15, 15, text=initials,
                           font=("Segoe UI", 9, "bold"), fill="white")
            info_col = tk.Frame(row, bg=C["card"])
            info_col.pack(side="left", padx=10, fill="x", expand=True)
            tk.Label(info_col, text=info["fullname"],
                     font=FONT_BODY_B, fg=C["text"],
                     bg=C["card"]).pack(anchor="w")
            tk.Label(info_col, text=f"@{uname}  |  {info['major']}",
                     font=FONT_SMALL, fg=C["text_sub"],
                     bg=C["card"]).pack(anchor="w")
            tk.Label(row, text=f"GPA {info['gpa']}",
                     font=FONT_SMALL_B, fg=C["green"],
                     bg=C["card"]).pack(side="right")
            divider(left_col)

        # Finance overview
        right_col = card(cols, padx=20, pady=20, width=240)
        right_col.pack(side="right", fill="y")
        right_col.pack_propagate(False)

        tk.Label(right_col, text="FINANCE SUMMARY",
                 font=("Segoe UI", 7, "bold"),
                 fg=C["text_sub"], bg=C["card"]).pack(anchor="w")
        tk.Frame(right_col, height=8, bg=C["card"]).pack()
        total, paid, balance, pct = finance_summary()
        for val, lbl_txt, color in [
            (format_leones(total),   "Total Fees",  C["text"]),
            (format_leones(paid),    "Collected",   C["success"]),
            (format_leones(balance), "Outstanding", C["danger"]),
        ]:
            r = tk.Frame(right_col, bg=C["card"])
            r.pack(fill="x", pady=5)
            tk.Label(r, text=lbl_txt, font=FONT_SMALL,
                     fg=C["text_sub"], bg=C["card"]).pack(side="left")
            tk.Label(r, text=val, font=FONT_SMALL_B,
                     fg=color, bg=C["card"]).pack(side="right")
        tk.Frame(right_col, height=10, bg=C["card"]).pack()
        pb = progress_bar(right_col, int(pct), width=180,
                          height=8, fill_color=C["green"])
        pb.pack(anchor="w")
        tk.Label(right_col, text=f"{pct}% collected",
                 font=FONT_SMALL, fg=C["text_sub"],
                 bg=C["card"]).pack(anchor="w", pady=(4, 0))
        return sf

    # ── STUDENTS ────────────────────────────────────
    def _page_students(self):
        sf = ScrollFrame(self._content, bg=C["bg"])
        p = sf.inner
        self._page_header(p, "Student Management",
                          "Add, edit, and remove student accounts")

        # Toolbar
        tb = tk.Frame(p, bg=C["bg"])
        tb.pack(fill="x", padx=28, pady=(0, 14))
        self._action_btn(tb, "+ Add Student",
                         self._add_student).pack(side="left")

        tbl = card(p, padx=0, pady=0)
        tbl.pack(fill="x", padx=28, pady=(0, 28))

        hdr_bg = "#f9fafb"
        hdr = tk.Frame(tbl, bg=hdr_bg, pady=10)
        hdr.pack(fill="x")
        for col_text, w in [("STUDENT", 220), ("ID", 120), ("MAJOR", 160),
                             ("YEAR", 90), ("GPA", 70), ("ACTIONS", 120)]:
            tk.Label(hdr, text=col_text, font=("Segoe UI", 8, "bold"),
                     fg=C["text_sub"], bg=hdr_bg,
                     width=w//8, anchor="w").pack(
                side="left", padx=(20 if col_text=="STUDENT" else 4, 0))
        divider(tbl)

        for idx, (uname, info) in enumerate(USERS.items()):
            row_bg = C["card"] if idx % 2 == 0 else "#fafafa"
            row = tk.Frame(tbl, bg=row_bg, pady=8)
            row.pack(fill="x")

            # Name col
            nc = tk.Frame(row, bg=row_bg, width=220)
            nc.pack(side="left", padx=(20, 0))
            nc.pack_propagate(False)
            tk.Label(nc, text=info["fullname"],
                     font=FONT_BODY_B, fg=C["text"],
                     bg=row_bg, anchor="w").pack(fill="x")
            tk.Label(nc, text=f"@{uname}",
                     font=FONT_SMALL, fg=C["text_sub"],
                     bg=row_bg, anchor="w").pack(fill="x")

            for val, w in [(info["id"], 120), (info["major"], 160),
                           (info["year"], 90)]:
                tk.Label(row, text=val, font=FONT_SMALL,
                         fg=C["text_sub"], bg=row_bg,
                         width=w//8, anchor="w").pack(side="left", padx=4)

            gpa_color = C["success"] if float(info["gpa"]) >= 3.5 else (
                C["warning"] if float(info["gpa"]) >= 2.5 else C["danger"])
            tk.Label(row, text=info["gpa"], font=FONT_SMALL_B,
                     fg=gpa_color, bg=row_bg, width=8).pack(side="left", padx=4)

            # Actions
            act = tk.Frame(row, bg=row_bg)
            act.pack(side="left", padx=4)
            tk.Button(act, text="Edit", font=FONT_LABEL,
                      bg=tint(C["admin_accent"]), fg=C["admin_accent"],
                      relief="flat", cursor="hand2", padx=6, pady=2,
                      command=lambda u=uname: self._edit_student(u)).pack(side="left", padx=2)
            tk.Button(act, text="Delete", font=FONT_LABEL,
                      bg=tint(C["danger"]), fg=C["danger"],
                      relief="flat", cursor="hand2", padx=6, pady=2,
                      command=lambda u=uname: self._delete_student(u)).pack(side="left", padx=2)

            if idx < len(USERS) - 1:
                divider(tbl)
        return sf

    def _add_student(self):
        fields = [
            ("fullname", "Full Name",  None),
            ("username", "Username",   None),
            ("password", "Password",   "*"),
            ("major",    "Major",      None),
            ("year",     "Year",       None),
            ("gpa",      "GPA",        None),
        ]
        def save(vals):
            ok, err = admin_add_student(
                vals["fullname"], vals["username"], vals["password"],
                vals["major"], vals["year"], vals["gpa"])
            if ok:
                messagebox.showinfo("Added", "Student account created.")
                self._reload_page("Students")
            else:
                messagebox.showerror("Error", err)
        EditDialog(self, "Add Student", fields, save)

    def _edit_student(self, uname):
        info = USERS[uname]
        fields = [
            ("fullname", "Full Name",  None),
            ("major",    "Major",      None),
            ("year",     "Year",       None),
            ("gpa",      "GPA",        None),
            ("email",    "Email",      None),
        ]
        prefill = {k: info.get(k, "") for k in ("fullname","major","year","gpa","email")}
        def save(vals):
            for k, v in vals.items():
                admin_update_student(uname, k, v)
            messagebox.showinfo("Updated", "Student record updated.")
            self._reload_page("Students")
        EditDialog(self, f"Edit — {info['fullname']}", fields, save, prefill)

    def _delete_student(self, uname):
        if messagebox.askyesno("Confirm Delete",
            f"Delete student '{uname}'? This cannot be undone."):
            admin_delete_student(uname)
            self._reload_page("Students")

    # ── COURSES ─────────────────────────────────────
    def _page_courses(self):
        sf = ScrollFrame(self._content, bg=C["bg"])
        p = sf.inner
        self._page_header(p, "Course Management",
                          "Add, edit, and remove courses")

        tb = tk.Frame(p, bg=C["bg"])
        tb.pack(fill="x", padx=28, pady=(0, 14))
        self._action_btn(tb, "+ Add Course",
                         self._add_course).pack(side="left")

        tbl = card(p, padx=0, pady=0)
        tbl.pack(fill="x", padx=28, pady=(0, 28))

        hdr_bg = "#f9fafb"
        hdr = tk.Frame(tbl, bg=hdr_bg, pady=10)
        hdr.pack(fill="x")
        for col_text in ["CODE", "COURSE NAME", "LECTURER", "CREDITS", "ACTIONS"]:
            tk.Label(hdr, text=col_text, font=("Segoe UI", 8, "bold"),
                     fg=C["text_sub"], bg=hdr_bg, anchor="w").pack(
                side="left", padx=(20 if col_text=="CODE" else 8, 0))
        divider(tbl)

        for idx, course in enumerate(COURSES):
            code, name, lecturer, credits, color = course
            row_bg = C["card"] if idx % 2 == 0 else "#fafafa"
            row = tk.Frame(tbl, bg=row_bg, pady=10)
            row.pack(fill="x")

            # Code badge
            bc = tk.Frame(row, bg=tint(color), padx=6, pady=3)
            bc.pack(side="left", padx=(20, 8))
            tk.Label(bc, text=code, font=FONT_SMALL_B,
                     fg=color, bg=tint(color)).pack()

            # Name
            nc = tk.Frame(row, bg=row_bg, width=200)
            nc.pack(side="left")
            nc.pack_propagate(False)
            tk.Label(nc, text=name, font=FONT_BODY_B,
                     fg=C["text"], bg=row_bg, anchor="w").pack(fill="x")

            tk.Label(row, text=lecturer, font=FONT_SMALL,
                     fg=C["text_sub"], bg=row_bg, width=18, anchor="w").pack(
                side="left", padx=8)
            tk.Label(row, text=f"{credits} cr", font=FONT_SMALL_B,
                     fg=C["text"], bg=row_bg, width=6).pack(side="left", padx=8)

            act = tk.Frame(row, bg=row_bg)
            act.pack(side="left", padx=8)
            tk.Button(act, text="Edit", font=FONT_LABEL,
                      bg=tint(C["admin_accent"]), fg=C["admin_accent"],
                      relief="flat", cursor="hand2", padx=6, pady=2,
                      command=lambda i=idx: self._edit_course(i)).pack(side="left", padx=2)
            tk.Button(act, text="Delete", font=FONT_LABEL,
                      bg=tint(C["danger"]), fg=C["danger"],
                      relief="flat", cursor="hand2", padx=6, pady=2,
                      command=lambda i=idx: self._delete_course(i)).pack(side="left", padx=2)

            if idx < len(COURSES) - 1:
                divider(tbl)
        return sf

    def _add_course(self):
        fields = [("code","Course Code",None),("name","Course Name",None),
                  ("lecturer","Lecturer",None),("credits","Credit Hours",None)]
        def save(v):
            ok, err = admin_add_course(v["code"],v["name"],v["lecturer"],v["credits"] or "3")
            if ok:
                messagebox.showinfo("Added","Course added.")
                self._reload_page("Courses")
            else:
                messagebox.showerror("Error", err)
        EditDialog(self,"Add Course",fields,save)

    def _edit_course(self, idx):
        c = COURSES[idx]
        fields = [("code","Course Code",None),("name","Course Name",None),
                  ("lecturer","Lecturer",None),("credits","Credit Hours",None)]
        prefill = {"code":c[0],"name":c[1],"lecturer":c[2],"credits":str(c[3])}
        def save(v):
            admin_update_course(idx,v["code"],v["name"],v["lecturer"],v["credits"])
            messagebox.showinfo("Updated","Course updated.")
            self._reload_page("Courses")
        EditDialog(self,f"Edit — {c[1]}",fields,save,prefill)

    def _delete_course(self, idx):
        if messagebox.askyesno("Confirm","Delete this course?"):
            admin_delete_course(idx)
            self._reload_page("Courses")

    # ── RESULTS ─────────────────────────────────────
    def _page_results(self):
        sf = ScrollFrame(self._content, bg=C["bg"])
        p = sf.inner
        self._page_header(p, "Results Management",
                          "Add, edit, and remove academic results")

        tb = tk.Frame(p, bg=C["bg"])
        tb.pack(fill="x", padx=28, pady=(0, 14))
        self._action_btn(tb, "+ Add Result", self._add_result).pack(side="left")

        tbl = card(p, padx=0, pady=0)
        tbl.pack(fill="x", padx=28, pady=(0, 28))

        hdr_bg = "#f9fafb"
        hdr = tk.Frame(tbl, bg=hdr_bg, pady=10)
        hdr.pack(fill="x")
        for col_text in ["COURSE", "SEMESTER", "SCORE", "GRADE", "ACTIONS"]:
            tk.Label(hdr, text=col_text, font=("Segoe UI", 8, "bold"),
                     fg=C["text_sub"], bg=hdr_bg, anchor="w").pack(
                side="left", padx=(20 if col_text=="COURSE" else 8, 0))
        divider(tbl)

        for idx, (code, name, grade, score, sem) in enumerate(RESULTS):
            gc = grade_color(grade)
            row_bg = C["card"] if idx % 2 == 0 else "#fafafa"
            row = tk.Frame(tbl, bg=row_bg, pady=10)
            row.pack(fill="x")

            nc = tk.Frame(row, bg=row_bg, width=220)
            nc.pack(side="left", padx=(20, 0))
            nc.pack_propagate(False)
            tk.Label(nc, text=name, font=FONT_BODY_B,
                     fg=C["text"], bg=row_bg, anchor="w").pack(fill="x")
            tk.Label(nc, text=code, font=FONT_SMALL,
                     fg=C["text_sub"], bg=row_bg, anchor="w").pack(fill="x")

            tk.Label(row, text=sem, font=FONT_SMALL,
                     fg=C["text_sub"], bg=row_bg, width=18, anchor="w").pack(
                side="left", padx=8)

            pb_f = tk.Frame(row, bg=row_bg, width=90)
            pb_f.pack(side="left")
            pb_f.pack_propagate(False)
            progress_bar(pb_f, score, width=70, height=4,
                         fill_color=gc).pack(pady=(4, 0))
            tk.Label(pb_f, text=f"{score}%", font=FONT_LABEL,
                     fg=C["text_sub"], bg=row_bg).pack()

            gf = tk.Frame(row, bg=tint(gc), padx=8, pady=4)
            gf.pack(side="left", padx=8)
            tk.Label(gf, text=grade, font=FONT_SMALL_B,
                     fg=gc, bg=tint(gc)).pack()

            act = tk.Frame(row, bg=row_bg)
            act.pack(side="left", padx=8)
            tk.Button(act, text="Edit", font=FONT_LABEL,
                      bg=tint(C["admin_accent"]), fg=C["admin_accent"],
                      relief="flat", cursor="hand2", padx=6, pady=2,
                      command=lambda i=idx: self._edit_result(i)).pack(side="left", padx=2)
            tk.Button(act, text="Delete", font=FONT_LABEL,
                      bg=tint(C["danger"]), fg=C["danger"],
                      relief="flat", cursor="hand2", padx=6, pady=2,
                      command=lambda i=idx: self._delete_result(i)).pack(side="left", padx=2)
            if idx < len(RESULTS) - 1:
                divider(tbl)
        return sf

    def _add_result(self):
        fields = [("code","Course Code",None),("name","Course Name",None),
                  ("grade","Grade (A/B+/etc)",None),("score","Score (0-100)",None),
                  ("semester","Semester",None)]
        def save(v):
            admin_add_result(v["code"],v["name"],v["grade"],v["score"] or "0",v["semester"])
            messagebox.showinfo("Added","Result added.")
            self._reload_page("Results")
        EditDialog(self,"Add Result",fields,save)

    def _edit_result(self, idx):
        r = RESULTS[idx]
        fields = [("code","Course Code",None),("name","Course Name",None),
                  ("grade","Grade",None),("score","Score",None),("semester","Semester",None)]
        prefill = {"code":r[0],"name":r[1],"grade":r[2],"score":str(r[3]),"semester":r[4]}
        def save(v):
            admin_update_result(idx,v["code"],v["name"],v["grade"],v["score"],v["semester"])
            messagebox.showinfo("Updated","Result updated.")
            self._reload_page("Results")
        EditDialog(self,f"Edit Result — {r[0]}",fields,save,prefill)

    def _delete_result(self, idx):
        if messagebox.askyesno("Confirm","Delete this result?"):
            admin_delete_result(idx)
            self._reload_page("Results")

    # ── ATTENDANCE ──────────────────────────────────
    def _page_attendance(self):
        sf = ScrollFrame(self._content, bg=C["bg"])
        p = sf.inner
        self._page_header(p, "Attendance Management",
                          "Add, edit, and remove attendance records")

        tb = tk.Frame(p, bg=C["bg"])
        tb.pack(fill="x", padx=28, pady=(0, 14))
        self._action_btn(tb, "+ Add Record",
                         self._add_attendance).pack(side="left")

        tbl = card(p, padx=0, pady=0)
        tbl.pack(fill="x", padx=28, pady=(0, 28))

        hdr_bg = "#f9fafb"
        hdr = tk.Frame(tbl, bg=hdr_bg, pady=10)
        hdr.pack(fill="x")
        for col_text in ["COURSE", "ATTENDED", "TOTAL", "RATE", "STATUS", "ACTIONS"]:
            tk.Label(hdr, text=col_text, font=("Segoe UI", 8, "bold"),
                     fg=C["text_sub"], bg=hdr_bg, anchor="w").pack(
                side="left", padx=(20 if col_text=="COURSE" else 8, 0))
        divider(tbl)

        for idx, (code, name, att, total) in enumerate(ATTENDANCE):
            pct, status_key = course_attendance_status(att, total)
            fc = C[status_key]
            row_bg = C["card"] if idx % 2 == 0 else "#fafafa"
            row = tk.Frame(tbl, bg=row_bg, pady=10)
            row.pack(fill="x")

            nc = tk.Frame(row, bg=row_bg, width=200)
            nc.pack(side="left", padx=(20, 0))
            nc.pack_propagate(False)
            tk.Label(nc, text=name, font=FONT_BODY_B,
                     fg=C["text"], bg=row_bg, anchor="w").pack(fill="x")
            tk.Label(nc, text=code, font=FONT_SMALL,
                     fg=C["text_sub"], bg=row_bg, anchor="w").pack(fill="x")

            for val in [str(att), str(total), f"{pct}%"]:
                tk.Label(row, text=val, font=FONT_SMALL_B,
                         fg=C["text"], bg=row_bg, width=8).pack(side="left", padx=8)

            sf2 = tk.Frame(row, bg=tint(fc), padx=8, pady=3)
            sf2.pack(side="left", padx=4)
            tk.Label(sf2, text=status_key.upper(), font=FONT_LABEL,
                     fg=fc, bg=tint(fc)).pack()

            act = tk.Frame(row, bg=row_bg)
            act.pack(side="left", padx=8)
            tk.Button(act, text="Edit", font=FONT_LABEL,
                      bg=tint(C["admin_accent"]), fg=C["admin_accent"],
                      relief="flat", cursor="hand2", padx=6, pady=2,
                      command=lambda i=idx: self._edit_attendance(i)).pack(side="left", padx=2)
            tk.Button(act, text="Delete", font=FONT_LABEL,
                      bg=tint(C["danger"]), fg=C["danger"],
                      relief="flat", cursor="hand2", padx=6, pady=2,
                      command=lambda i=idx: self._delete_attendance(i)).pack(side="left", padx=2)
            if idx < len(ATTENDANCE) - 1:
                divider(tbl)
        return sf

    def _add_attendance(self):
        fields = [("code","Course Code",None),("name","Course Name",None),
                  ("attended","Classes Attended",None),("total","Total Classes",None)]
        def save(v):
            admin_add_attendance(v["code"],v["name"],v["attended"] or "0",v["total"] or "0")
            messagebox.showinfo("Added","Attendance record added.")
            self._reload_page("Attendance")
        EditDialog(self,"Add Attendance Record",fields,save)

    def _edit_attendance(self, idx):
        a = ATTENDANCE[idx]
        fields = [("code","Course Code",None),("name","Course Name",None),
                  ("attended","Classes Attended",None),("total","Total Classes",None)]
        prefill = {"code":a[0],"name":a[1],"attended":str(a[2]),"total":str(a[3])}
        def save(v):
            admin_update_attendance(idx,v["code"],v["name"],v["attended"],v["total"])
            messagebox.showinfo("Updated","Attendance updated.")
            self._reload_page("Attendance")
        EditDialog(self,f"Edit Attendance — {a[0]}",fields,save,prefill)

    def _delete_attendance(self, idx):
        if messagebox.askyesno("Confirm","Delete this attendance record?"):
            admin_delete_attendance(idx)
            self._reload_page("Attendance")

    # ── FINANCE ─────────────────────────────────────
    def _page_finance(self):
        sf = ScrollFrame(self._content, bg=C["bg"])
        p = sf.inner
        self._page_header(p, "Finance Management",
                          "Add, edit, and remove payment records")

        total, paid, balance, pct_paid = finance_summary()
        summ = tk.Frame(p, bg=C["bg"])
        summ.pack(fill="x", padx=28, pady=(0, 20))
        for val, lbl_txt, color in [
            (format_leones(total),   "Total Fees",  C["text_sub"]),
            (format_leones(paid),    "Collected",   C["success"]),
            (format_leones(balance), "Outstanding", C["danger"]),
        ]:
            sc = card(summ, padx=20, pady=18)
            sc.pack(side="left", expand=True, fill="x", padx=(0, 12))
            tk.Label(sc, text=lbl_txt.upper(),
                     font=("Segoe UI", 7, "bold"),
                     fg=C["text_sub"], bg=C["card"]).pack(anchor="w")
            tk.Label(sc, text=val, font=("Segoe UI", 16, "bold"),
                     fg=color, bg=C["card"]).pack(anchor="w", pady=(4, 0))

        tb = tk.Frame(p, bg=C["bg"])
        tb.pack(fill="x", padx=28, pady=(0, 14))
        self._action_btn(tb, "+ Add Transaction",
                         self._add_transaction).pack(side="left")

        tbl = card(p, padx=0, pady=0)
        tbl.pack(fill="x", padx=28, pady=(0, 28))

        hdr_bg = "#f9fafb"
        hdr = tk.Frame(tbl, bg=hdr_bg, pady=10)
        hdr.pack(fill="x")
        for col_text in ["DATE", "DESCRIPTION", "AMOUNT", "STATUS", "ACTIONS"]:
            tk.Label(hdr, text=col_text, font=("Segoe UI", 8, "bold"),
                     fg=C["text_sub"], bg=hdr_bg, anchor="w").pack(
                side="left", padx=(20 if col_text=="DATE" else 8, 0))
        divider(tbl)

        for idx, (date, desc, amt, status) in enumerate(TRANSACTIONS):
            pending = status == "due"
            color = C["warning"] if pending else C["success"]
            row_bg = C["card"] if idx % 2 == 0 else "#fafafa"
            row = tk.Frame(tbl, bg=row_bg, pady=10)
            row.pack(fill="x")

            tk.Label(row, text=date, font=FONT_SMALL,
                     fg=C["text_sub"], bg=row_bg, width=14, anchor="w").pack(
                side="left", padx=(20, 0))

            dc = tk.Frame(row, bg=row_bg, width=200)
            dc.pack(side="left", padx=8)
            dc.pack_propagate(False)
            tk.Label(dc, text=desc, font=FONT_BODY_B,
                     fg=C["text"], bg=row_bg, anchor="w").pack(fill="x")

            tk.Label(row, text=format_leones(amt), font=FONT_BODY_B,
                     fg=color, bg=row_bg, width=14).pack(side="left", padx=8)

            sf3 = tk.Frame(row, bg=tint(color), padx=8, pady=3)
            sf3.pack(side="left", padx=4)
            tk.Label(sf3, text=status.upper(), font=FONT_LABEL,
                     fg=color, bg=tint(color)).pack()

            act = tk.Frame(row, bg=row_bg)
            act.pack(side="left", padx=8)
            tk.Button(act, text="Edit", font=FONT_LABEL,
                      bg=tint(C["admin_accent"]), fg=C["admin_accent"],
                      relief="flat", cursor="hand2", padx=6, pady=2,
                      command=lambda i=idx: self._edit_transaction(i)).pack(side="left", padx=2)
            tk.Button(act, text="Delete", font=FONT_LABEL,
                      bg=tint(C["danger"]), fg=C["danger"],
                      relief="flat", cursor="hand2", padx=6, pady=2,
                      command=lambda i=idx: self._delete_transaction(i)).pack(side="left", padx=2)
            if idx < len(TRANSACTIONS) - 1:
                divider(tbl)
        return sf

    def _add_transaction(self):
        fields = [("date","Date (e.g. 01 Jan 2025)",None),
                  ("desc","Description",None),
                  ("amount","Amount in Leones",None),
                  ("status","Status (paid / due)",None)]
        def save(v):
            admin_add_transaction(v["date"],v["desc"],v["amount"] or "0",v["status"] or "due")
            messagebox.showinfo("Added","Transaction added.")
            self._reload_page("Finance")
        EditDialog(self,"Add Transaction",fields,save)

    def _edit_transaction(self, idx):
        t = TRANSACTIONS[idx]
        fields = [("date","Date",None),("desc","Description",None),
                  ("amount","Amount",None),("status","Status (paid/due)",None)]
        prefill = {"date":t[0],"desc":t[1],"amount":str(t[2]),"status":t[3]}
        def save(v):
            admin_update_transaction(idx,v["date"],v["desc"],v["amount"],v["status"])
            messagebox.showinfo("Updated","Transaction updated.")
            self._reload_page("Finance")
        EditDialog(self,f"Edit Transaction — {t[1]}",fields,save,prefill)

    def _delete_transaction(self, idx):
        if messagebox.askyesno("Confirm","Delete this transaction?"):
            admin_delete_transaction(idx)
            self._reload_page("Finance")

    # ── SETTINGS ────────────────────────────────────
    def _page_settings(self):
        sf = ScrollFrame(self._content, bg=C["bg"])
        p = sf.inner
        self._page_header(p, "Admin Settings")

        settings_card = card(p, padx=0, pady=0)
        settings_card.pack(fill="x", padx=28, pady=(0, 28))

        items = [
            ("Allow Student Self-Registration",
             "Let students create their own accounts", True),
            ("Email Notifications",
             "Send automatic email alerts for fee deadlines", True),
            ("Maintenance Mode",
             "Temporarily disable student login access", False),
            ("Audit Logging",
             "Record all admin actions for review", True),
        ]
        self._setting_vars = []
        for i, (name, desc, default) in enumerate(items):
            var = tk.BooleanVar(value=default)
            self._setting_vars.append(var)
            row = tk.Frame(settings_card, bg=C["card"], padx=24, pady=16)
            row.pack(fill="x")
            txt = tk.Frame(row, bg=C["card"])
            txt.pack(side="left", fill="x", expand=True)
            tk.Label(txt, text=name, font=FONT_BODY_B,
                     fg=C["text"], bg=C["card"]).pack(anchor="w")
            tk.Label(txt, text=desc, font=FONT_SMALL,
                     fg=C["text_sub"], bg=C["card"]).pack(anchor="w", pady=(2, 0))
            tk.Checkbutton(row, variable=var, bg=C["card"],
                           activebackground=C["card"],
                           selectcolor=C["admin_accent"],
                           relief="flat", cursor="hand2").pack(side="right")
            if i < len(items) - 1:
                divider(settings_card)

        btn_row = tk.Frame(p, bg=C["bg"])
        btn_row.pack(anchor="w", padx=28)
        tk.Button(btn_row, text="Save Settings",
                  font=FONT_BODY_B, bg=C["admin_accent"], fg=C["white"],
                  relief="flat", cursor="hand2", padx=16, pady=9,
                  activebackground="#4f46e5",
                  command=lambda: messagebox.showinfo(
                      "Saved", "Settings saved.", parent=self)).pack()
        return sf


# ─────────────────────────────────────────────
#  STUDENT DASHBOARD (unchanged)
# ─────────────────────────────────────────────
class Dashboard(tk.Frame):
    PAGES = [
        ("Dashboard",  Icon.dashboard),
        ("Courses",    Icon.book),
        ("Results",    Icon.chart),
        ("Attendance", Icon.attendance_icon),
        ("Finance",    Icon.wallet),
        ("Profile",    Icon.person),
        ("Settings",   Icon.gear),
    ]

    def __init__(self, parent, username, on_logout):
        super().__init__(parent, bg=C["bg"])
        self._user      = username
        self._info      = get_user(username)
        self._on_logout = on_logout
        self._active    = "Dashboard"
        self._nav_items = {}
        self._build()

    def _build(self):
        sb = tk.Frame(self, bg=C["sidebar"], width=220)
        sb.pack(side="left", fill="y")
        sb.pack_propagate(False)

        logo_frame = tk.Frame(sb, bg=C["green_dark"], pady=16)
        logo_frame.pack(fill="x")
        tk.Label(logo_frame, text="SALONE EDUPORTAL",
                 font=FONT_LOGO, fg=C["gold"],
                 bg=C["green_dark"]).pack(padx=16, anchor="w")
        tk.Label(logo_frame, text="Student Portal",
                 font=FONT_LOGO_SUB, fg="#86efac",
                 bg=C["green_dark"]).pack(padx=16, anchor="w", pady=(2, 0))

        tk.Frame(sb, bg="#1f2937", height=1).pack(fill="x")
        tk.Frame(sb, bg=C["sidebar"], height=10).pack()
        tk.Label(sb, text="NAVIGATION",
                 font=("Segoe UI", 7, "bold"),
                 fg="#4b5563", bg=C["sidebar"]).pack(anchor="w", padx=16, pady=(6, 4))

        for name, icon_fn in self.PAGES:
            item = NavItem(sb, name, icon_fn,
                           command=lambda n=name: self._switch(n),
                           active=(name == self._active))
            item.pack(fill="x")
            self._nav_items[name] = item

        tk.Frame(sb, bg=C["sidebar"]).pack(fill="y", expand=True)
        tk.Frame(sb, bg="#1f2937", height=1).pack(fill="x")

        user_strip = tk.Frame(sb, bg=C["sidebar"], pady=12)
        user_strip.pack(fill="x")
        av = tk.Canvas(user_strip, width=34, height=34,
                       bg=C["sidebar"], highlightthickness=0)
        av.pack(side="left", padx=(14, 8))
        av.create_oval(1, 1, 33, 33, fill=C["green"], outline="")
        initials = "".join(p[0] for p in self._info["fullname"].split())[:2].upper()
        av.create_text(17, 17, text=initials,
                       font=("Segoe UI", 11, "bold"), fill="white")
        u_info = tk.Frame(user_strip, bg=C["sidebar"])
        u_info.pack(side="left", fill="x", expand=True)
        tk.Label(u_info, text=self._info["fullname"].split()[0],
                 font=FONT_SMALL_B, fg=C["white"],
                 bg=C["sidebar"]).pack(anchor="w")
        tk.Label(u_info, text=f"@{self._user}",
                 font=FONT_LABEL, fg="#6b7280",
                 bg=C["sidebar"]).pack(anchor="w")

        tk.Button(sb, text="Sign Out", font=FONT_SMALL_B,
                  fg=C["danger"], bg="#1f2937", relief="flat",
                  cursor="hand2", activeforeground="#fca5a5",
                  activebackground="#1f2937",
                  command=self._on_logout, pady=8).pack(
            fill="x", padx=12, pady=(0, 12))

        self._content = tk.Frame(self, bg=C["bg"])
        self._content.pack(side="right", fill="both", expand=True)
        self._pages = {}
        self._load_page("Dashboard")

    def _switch(self, name):
        if name == self._active:
            return
        if self._active in self._pages:
            self._pages[self._active].pack_forget()
        self._nav_items[self._active].set_active(False)
        self._active = name
        self._nav_items[name].set_active(True)
        self._load_page(name)

    def _load_page(self, name):
        if name not in self._pages:
            builders = {
                "Dashboard":  self._page_dashboard,
                "Courses":    self._page_courses,
                "Results":    self._page_results,
                "Attendance": self._page_attendance,
                "Finance":    self._page_finance,
                "Profile":    self._page_profile,
                "Settings":   self._page_settings,
            }
            pg = builders[name]()
            self._pages[name] = pg
        self._pages[name].pack(fill="both", expand=True)

    def _page_header(self, parent, title, subtitle=None):
        hdr = tk.Frame(parent, bg=C["bg"], pady=0)
        hdr.pack(fill="x", padx=28, pady=(24, 4))
        label(hdr, title, font=("Segoe UI", 18, "bold"),
              fg=C["text"], bg=C["bg"]).pack(anchor="w")
        if subtitle:
            label(hdr, subtitle, font=FONT_SMALL,
                  fg=C["text_sub"], bg=C["bg"]).pack(anchor="w", pady=(2, 0))
        tk.Frame(parent, bg=C["border"], height=1).pack(fill="x", padx=28, pady=(8, 20))

    def _page_dashboard(self):
        sf = ScrollFrame(self._content, bg=C["bg"])
        sf.pack(fill="both", expand=True)
        p = sf.inner
        self._page_header(p,
            f"Welcome back, {self._info['fullname'].split()[0]}",
            f"{self._info['major']}  |  {self._info['year']}  |  {self._info['id']}")
        course_count, course_credits = course_load_summary()
        attendance_pct, _, _ = attendance_summary()
        stat_row = tk.Frame(p, bg=C["bg"])
        stat_row.pack(fill="x", padx=28, pady=(0, 20))
        stats = [
            ("Cumulative GPA",  self._info["gpa"], "Academic standing", C["green"]),
            ("Active Courses",  str(course_count),  f"{course_credits} credit hours", C["info"]),
            ("Attendance Rate", f"{attendance_pct}%","Above 75% required", C["gold"]),
            ("Fee Balance",     "Le 1,000,000",      "Due 15 Dec 2024",   C["danger"]),
        ]
        for i, (t, v, s, a) in enumerate(stats):
            sc = stat_card(stat_row, t, v, s, a)
            sc.grid(row=0, column=i, padx=(0, 12), sticky="nsew")
            stat_row.columnconfigure(i, weight=1)
        cols = tk.Frame(p, bg=C["bg"])
        cols.pack(fill="both", padx=28, pady=(0, 28))
        left_col = card(cols, padx=0, pady=0)
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 12))
        tk.Label(left_col, text="Recent Results", font=FONT_TITLE,
                 fg=C["text"], bg=C["card"]).pack(anchor="w", padx=20, pady=(18, 12))
        divider(left_col)
        for code, name, grade, score, _ in RESULTS[:4]:
            gc = grade_color(grade); gc_bg = tint(gc)
            row = tk.Frame(left_col, bg=C["card"])
            row.pack(fill="x", padx=20, pady=6)
            grade_box = tk.Frame(row, bg=gc_bg, width=36, height=36)
            grade_box.pack(side="left")
            grade_box.pack_propagate(False)
            tk.Label(grade_box, text=grade, font=FONT_SMALL_B,
                     fg=gc, bg=gc_bg).place(relx=0.5, rely=0.5, anchor="center")
            info_col = tk.Frame(row, bg=C["card"])
            info_col.pack(side="left", padx=10, fill="x", expand=True)
            tk.Label(info_col, text=name, font=FONT_BODY_B,
                     fg=C["text"], bg=C["card"]).pack(anchor="w")
            tk.Label(info_col, text=code, font=FONT_SMALL,
                     fg=C["text_sub"], bg=C["card"]).pack(anchor="w")
            tk.Label(row, text=f"{score}/100", font=FONT_SMALL_B,
                     fg=C["text_sub"], bg=C["card"]).pack(side="right")
            divider(left_col)
        right_col = tk.Frame(cols, bg=C["bg"], width=220)
        right_col.pack(side="right", fill="y")
        right_col.pack_propagate(False)
        nc = tk.Frame(right_col, bg=C["green_dark"], padx=18, pady=18)
        nc.pack(fill="x", pady=(0, 12))
        tk.Label(nc, text="NEXT CLASS", font=("Segoe UI", 7, "bold"),
                 fg="#86efac", bg=C["green_dark"]).pack(anchor="w")
        tk.Label(nc, text="CSC104", font=("Segoe UI", 20, "bold"),
                 fg=C["white"], bg=C["green_dark"]).pack(anchor="w")
        tk.Label(nc, text="Web Development", font=FONT_BODY,
                 fg="#d1fae5", bg=C["green_dark"]).pack(anchor="w")
        tk.Label(nc, text="Today  2:00 PM  Room B204",
                 font=FONT_SMALL, fg="#86efac",
                 bg=C["green_dark"]).pack(anchor="w", pady=(8, 0))
        sp = card(right_col, padx=18, pady=18)
        sp.pack(fill="x")
        tk.Label(sp, text="SEMESTER PROGRESS", font=("Segoe UI", 7, "bold"),
                 fg=C["text_sub"], bg=C["card"]).pack(anchor="w")
        tk.Label(sp, text="Week 11 of 16", font=FONT_TITLE,
                 fg=C["text"], bg=C["card"]).pack(anchor="w", pady=(4, 10))
        progress_bar(sp, 68, width=180, height=6,
                     fill_color=C["green"]).pack(anchor="w")
        tk.Label(sp, text="68% complete", font=FONT_SMALL,
                 fg=C["text_sub"], bg=C["card"]).pack(anchor="w", pady=(4, 0))
        return sf

    def _page_courses(self):
        sf = ScrollFrame(self._content, bg=C["bg"])
        p = sf.inner
        self._page_header(p, "Enrolled Courses",
                          "Semester 1, 2024  |  18 credit hours")
        grid = tk.Frame(p, bg=C["bg"])
        grid.pack(fill="x", padx=28)
        for i, (code, name, inst, cr, color) in enumerate(COURSES):
            col = i % 2; row_i = i // 2
            c_card = card(grid, padx=0, pady=0)
            c_card.grid(row=row_i, column=col,
                        padx=(0, 12 if col == 0 else 0), pady=(0, 14), sticky="nsew")
            grid.columnconfigure(col, weight=1)
            tk.Frame(c_card, bg=color, height=4).pack(fill="x")
            body = tk.Frame(c_card, bg=C["card"], padx=18, pady=16)
            body.pack(fill="both", expand=True)
            color_bg = tint(color)
            badge_f = tk.Frame(body, bg=color_bg, padx=8, pady=3)
            badge_f.pack(anchor="w")
            tk.Label(badge_f, text=code, font=FONT_SMALL_B,
                     fg=color, bg=color_bg).pack()
            tk.Label(body, text=name, font=FONT_BODY_B,
                     fg=C["text"], bg=C["card"]).pack(anchor="w", pady=(8, 2))
            tk.Label(body, text=f"Lecturer: {inst}", font=FONT_SMALL,
                     fg=C["text_sub"], bg=C["card"]).pack(anchor="w")
            tk.Label(body, text=f"{cr} Credit Hours", font=FONT_SMALL,
                     fg=C["text_muted"], bg=C["card"]).pack(anchor="w", pady=(2, 10))
            progress_bar(body, 60+i*5, width=260, height=4,
                         fill_color=color).pack(anchor="w")
            tk.Label(body, text="Course progress", font=FONT_LABEL,
                     fg=C["text_muted"], bg=C["card"]).pack(anchor="w", pady=(3, 0))
        return sf

    def _page_results(self):
        sf = ScrollFrame(self._content, bg=C["bg"])
        p = sf.inner
        self._page_header(p, "Academic Results",
                          f"Cumulative GPA: {self._info['gpa']}  |  Honour Roll")
        tbl = card(p, padx=0, pady=0)
        tbl.pack(fill="x", padx=28, pady=(0, 28))
        hdr_bg = "#f9fafb"
        hdr = tk.Frame(tbl, bg=hdr_bg, pady=10)
        hdr.pack(fill="x")
        for col_text, w in [("COURSE", 260), ("SEMESTER", 160),
                             ("SCORE", 100), ("GRADE", 80)]:
            tk.Label(hdr, text=col_text, font=("Segoe UI", 8, "bold"),
                     fg=C["text_sub"], bg=hdr_bg,
                     width=w//8, anchor="w").pack(
                side="left", padx=(20 if col_text=="COURSE" else 8, 0))
        divider(tbl)
        for idx, (code, name, grade, score, sem) in enumerate(RESULTS):
            gc = grade_color(grade)
            row_bg = C["card"] if idx % 2 == 0 else "#fafafa"
            row = tk.Frame(tbl, bg=row_bg, pady=10)
            row.pack(fill="x")
            c_col = tk.Frame(row, bg=row_bg, width=260)
            c_col.pack(side="left", padx=(20, 0))
            c_col.pack_propagate(False)
            tk.Label(c_col, text=name, font=FONT_BODY_B, fg=C["text"],
                     bg=row_bg, anchor="w").pack(fill="x")
            tk.Label(c_col, text=code, font=FONT_SMALL, fg=C["text_sub"],
                     bg=row_bg, anchor="w").pack(fill="x")
            tk.Label(row, text=sem, font=FONT_SMALL, fg=C["text_sub"],
                     bg=row_bg, width=18, anchor="w").pack(side="left", padx=8)
            sc_frame = tk.Frame(row, bg=row_bg, width=100)
            sc_frame.pack(side="left")
            sc_frame.pack_propagate(False)
            progress_bar(sc_frame, score, width=72, height=4, fill_color=gc).pack(pady=(2, 0))
            tk.Label(sc_frame, text=f"{score}%", font=FONT_LABEL,
                     fg=C["text_sub"], bg=row_bg).pack()
            g_frame = tk.Frame(row, bg=row_bg, width=80)
            g_frame.pack(side="left")
            gc_bg = tint(gc)
            gf = tk.Frame(g_frame, bg=gc_bg, padx=8, pady=4)
            gf.pack()
            tk.Label(gf, text=grade, font=FONT_SMALL_B, fg=gc, bg=gc_bg).pack()
            if idx < len(RESULTS) - 1:
                divider(tbl)
        return sf

    def _page_attendance(self):
        sf = ScrollFrame(self._content, bg=C["bg"])
        p = sf.inner
        self._page_header(p, "Attendance Record",
                          "Minimum required: 75% per course")
        overall_pct, attended_total, missed_total = attendance_summary()
        summ = tk.Frame(p, bg=C["bg"])
        summ.pack(fill="x", padx=28, pady=(0, 20))
        for val, lbl_txt, color in [
            (f"{overall_pct}%",     "Overall Attendance", C["green"]),
            (str(attended_total),   "Classes Attended",   C["info"]),
            (str(missed_total),     "Classes Missed",     C["danger"]),
        ]:
            sc = card(summ, padx=20, pady=16)
            sc.pack(side="left", expand=True, fill="x", padx=(0, 12))
            tk.Label(sc, text=val, font=("Segoe UI", 22, "bold"),
                     fg=color, bg=C["card"]).pack()
            tk.Label(sc, text=lbl_txt, font=FONT_SMALL,
                     fg=C["text_sub"], bg=C["card"]).pack()
        att_card = card(p, padx=24, pady=20)
        att_card.pack(fill="x", padx=28, pady=(0, 28))
        tk.Label(att_card, text="Per-Course Breakdown", font=FONT_TITLE,
                 fg=C["text"], bg=C["card"]).pack(anchor="w", pady=(0, 16))
        for code, name, att, total in ATTENDANCE:
            pct, status_key = course_attendance_status(att, total)
            fc = C[status_key]
            row = tk.Frame(att_card, bg=C["card"])
            row.pack(fill="x", pady=(0, 14))
            top = tk.Frame(row, bg=C["card"])
            top.pack(fill="x")
            tk.Label(top, text=f"{code}  {name}", font=FONT_BODY_B,
                     fg=C["text"], bg=C["card"]).pack(side="left")
            tk.Label(top, text=f"{att}/{total}  ({pct}%)", font=FONT_SMALL_B,
                     fg=fc, bg=C["card"]).pack(side="right")
            progress_bar(row, pct, width=500, height=7,
                         fill_color=fc).pack(anchor="w", pady=(5, 0))
        return sf

    def _page_finance(self):
        sf = ScrollFrame(self._content, bg=C["bg"])
        p = sf.inner
        self._page_header(p, "Fee & Finance",
                          "Academic Year 2024 - 2025  |  Currency: Leones (Le)")
        total, paid, balance, pct_paid = finance_summary()
        summ = tk.Frame(p, bg=C["bg"])
        summ.pack(fill="x", padx=28, pady=(0, 20))
        for val, lbl_txt, color in [
            (format_leones(total),   "Total Fees",  C["text_sub"]),
            (format_leones(paid),    "Amount Paid", C["success"]),
            (format_leones(balance), "Balance Due", C["danger"]),
        ]:
            sc = card(summ, padx=20, pady=18)
            sc.pack(side="left", expand=True, fill="x", padx=(0, 12))
            tk.Label(sc, text=lbl_txt.upper(), font=("Segoe UI", 7, "bold"),
                     fg=C["text_sub"], bg=C["card"]).pack(anchor="w")
            tk.Label(sc, text=val, font=("Segoe UI", 16, "bold"),
                     fg=color, bg=C["card"]).pack(anchor="w", pady=(4, 0))
        prog_card = card(p, padx=24, pady=20)
        prog_card.pack(fill="x", padx=28, pady=(0, 20))
        tk.Label(prog_card, text="Payment Progress", font=FONT_TITLE,
                 fg=C["text"], bg=C["card"]).pack(anchor="w", pady=(0, 12))
        progress_bar(prog_card, int(pct_paid), width=600, height=12,
                     fill_color=C["green"]).pack(anchor="w")
        row = tk.Frame(prog_card, bg=C["card"])
        row.pack(fill="x", pady=(6, 0))
        tk.Label(row, text=f"{format_leones(paid)} paid ({pct_paid}%)",
                 font=FONT_SMALL, fg=C["text_sub"], bg=C["card"]).pack(side="left")
        tk.Label(row, text=f"{format_leones(balance)} remaining",
                 font=FONT_SMALL, fg=C["danger"], bg=C["card"]).pack(side="right")
        hist_card = card(p, padx=0, pady=0)
        hist_card.pack(fill="x", padx=28, pady=(0, 28))
        tk.Label(hist_card, text="Payment History", font=FONT_TITLE,
                 fg=C["text"], bg=C["card"]).pack(anchor="w", padx=24, pady=(18, 12))
        divider(hist_card)
        for idx, (date, desc, amt, status) in enumerate(TRANSACTIONS):
            pending = status == "due"
            color = C["warning"] if pending else C["success"]
            row = tk.Frame(hist_card, bg=C["card"])
            row.pack(fill="x", padx=24, pady=10)
            dot = tk.Canvas(row, width=10, height=10,
                            bg=C["card"], highlightthickness=0)
            dot.create_oval(1, 1, 9, 9, fill=color, outline="")
            dot.pack(side="left", padx=(0, 12))
            info_f = tk.Frame(row, bg=C["card"])
            info_f.pack(side="left", fill="x", expand=True)
            tk.Label(info_f, text=desc, font=FONT_BODY_B,
                     fg=C["text"], bg=C["card"]).pack(anchor="w")
            tk.Label(info_f, text=date, font=FONT_SMALL,
                     fg=C["text_sub"], bg=C["card"]).pack(anchor="w")
            tk.Label(row, text=format_leones(amt), font=FONT_BODY_B,
                     fg=color, bg=C["card"]).pack(side="right", padx=(0, 8))
            if pending:
                due_lbl = tk.Frame(row, bg="#fef3c7", padx=6, pady=2)
                due_lbl.pack(side="right", padx=(0, 8))
                tk.Label(due_lbl, text="DUE", font=("Segoe UI", 7, "bold"),
                         fg="#92400e", bg="#fef3c7").pack()
            if idx < len(TRANSACTIONS) - 1:
                divider(hist_card)
        return sf

    def _page_profile(self):
        sf = ScrollFrame(self._content, bg=C["bg"])
        p = sf.inner
        self._page_header(p, "Student Profile")
        cols = tk.Frame(p, bg=C["bg"])
        cols.pack(fill="x", padx=28)
        av_card = card(cols, padx=24, pady=28, width=220)
        av_card.pack(side="left", fill="y", padx=(0, 20))
        av_card.pack_propagate(False)
        av = tk.Canvas(av_card, width=70, height=70,
                       bg=C["card"], highlightthickness=0)
        av.pack(pady=(0, 12))
        av.create_oval(2, 2, 68, 68, fill=C["green"], outline="")
        initials = "".join(p2[0] for p2 in self._info["fullname"].split())[:2].upper()
        av.create_text(35, 35, text=initials,
                       font=("Segoe UI", 22, "bold"), fill="white")
        tk.Label(av_card, text=self._info["fullname"], font=FONT_SUBHEAD,
                 fg=C["text"], bg=C["card"]).pack()
        tk.Label(av_card, text=f"@{self._user}", font=FONT_SMALL,
                 fg=C["text_sub"], bg=C["card"]).pack(pady=(2, 12))
        badge_f = tk.Frame(av_card, bg="#dcfce7", padx=10, pady=4)
        badge_f.pack()
        tk.Label(badge_f, text=self._info["year"], font=FONT_SMALL_B,
                 fg="#166534", bg="#dcfce7").pack()
        divider(av_card, pady=14)
        tk.Label(av_card, text=self._info["gpa"],
                 font=("Segoe UI", 26, "bold"),
                 fg=C["green"], bg=C["card"]).pack()
        tk.Label(av_card, text="Cumulative GPA", font=FONT_SMALL,
                 fg=C["text_sub"], bg=C["card"]).pack()
        det = card(cols, padx=24, pady=22)
        det.pack(side="left", fill="both", expand=True)
        tk.Label(det, text="Student Information", font=FONT_TITLE,
                 fg=C["text"], bg=C["card"]).pack(anchor="w", pady=(0, 14))
        divider(det)
        fields = [
            ("Student ID",       self._info["id"]),
            ("Major",            self._info["major"]),
            ("Year of Study",    self._info["year"]),
            ("Email",            self._info["email"]),
            ("Status",           "Active"),
            ("Academic Advisor", "Dr. A. Bangura"),
            ("Institution",      "University of Makeni (UNIMAK)"),
        ]
        for lbl_txt, val in fields:
            row = tk.Frame(det, bg=C["card"])
            row.pack(fill="x", pady=9)
            tk.Label(row, text=lbl_txt, font=FONT_SMALL, fg=C["text_sub"],
                     bg=C["card"], width=20, anchor="w").pack(side="left")
            tk.Label(row, text=val, font=FONT_SMALL_B, fg=C["text"],
                     bg=C["card"]).pack(side="left")
            divider(det)
        return sf

    def _page_settings(self):
        sf = ScrollFrame(self._content, bg=C["bg"])
        p = sf.inner
        self._page_header(p, "Settings & Preferences")
        settings_card = card(p, padx=0, pady=0)
        settings_card.pack(fill="x", padx=28, pady=(0, 28))
        items = [
            ("Enable Dark Mode",    "Switch the interface to a dark colour scheme", False),
            ("Push Notifications",  "Receive alerts for grades and announcements", True),
            ("Email Summaries",     "Get a weekly academic summary to your email", True),
            ("SMS Alerts",          "Receive fee reminders via SMS", False),
        ]
        self._setting_vars = []
        for i, (name, desc, default) in enumerate(items):
            var = tk.BooleanVar(value=default)
            self._setting_vars.append(var)
            row = tk.Frame(settings_card, bg=C["card"], padx=24, pady=16)
            row.pack(fill="x")
            txt = tk.Frame(row, bg=C["card"])
            txt.pack(side="left", fill="x", expand=True)
            tk.Label(txt, text=name, font=FONT_BODY_B,
                     fg=C["text"], bg=C["card"]).pack(anchor="w")
            tk.Label(txt, text=desc, font=FONT_SMALL,
                     fg=C["text_sub"], bg=C["card"]).pack(anchor="w", pady=(2, 0))
            tk.Checkbutton(row, variable=var, bg=C["card"],
                           activebackground=C["card"],
                           selectcolor=C["green"],
                           relief="flat", cursor="hand2").pack(side="right")
            if i < len(items) - 1:
                divider(settings_card)
        btn_row = tk.Frame(p, bg=C["bg"])
        btn_row.pack(anchor="w", padx=28)
        primary_btn(btn_row, "Save Preferences",
                    lambda: messagebox.showinfo("Saved","Your preferences have been saved.",
                                               parent=self), width=20).pack()
        return sf


# ─────────────────────────────────────────────
#  APPLICATION ROOT
# ─────────────────────────────────────────────
class SaloneEduPortal:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Salone EduPortal — Student Academic Portal")
        self.root.geometry("1180x720")
        self.root.minsize(960, 620)
        self.root.configure(bg=C["sidebar"])
        self.root.update_idletasks()
        w = self.root.winfo_width(); h = self.root.winfo_height()
        x = (self.root.winfo_screenwidth()  - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")
        self._current = None
        self._show_login()
        self.root.mainloop()

    def _clear(self):
        if self._current:
            self._current.pack_forget()
            self._current.destroy()
            self._current = None

    def _show_login(self):
        self._clear()
        scr = LoginScreen(self.root,
                          on_login=self._on_login,
                          on_register=self._show_register,
                          on_admin_login=self._show_admin_login)
        scr.pack(fill="both", expand=True)
        self._current = scr

    def _show_admin_login(self):
        self._clear()
        scr = AdminLoginScreen(self.root,
                               on_login=self._on_admin_login,
                               on_back=self._show_login)
        scr.pack(fill="both", expand=True)
        self._current = scr

    def _show_register(self):
        self._clear()
        scr = RegisterScreen(self.root,
                             on_back=self._show_login,
                             on_register=self._on_register)
        scr.pack(fill="both", expand=True)
        self._current = scr

    def _on_login(self, username):
        self._clear()
        dash = Dashboard(self.root, username, on_logout=self._show_login)
        dash.pack(fill="both", expand=True)
        self._current = dash

    def _on_admin_login(self, username):
        self._clear()
        dash = AdminDashboard(self.root, username, on_logout=self._show_login)
        dash.pack(fill="both", expand=True)
        self._current = dash

    def _on_register(self, *args):
        self._show_login()


if __name__ == "__main__":
    SaloneEduPortal()
