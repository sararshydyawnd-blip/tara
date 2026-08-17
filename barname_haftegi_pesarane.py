import tkinter as tk

# -------------------------------
# پنجره اصلی
# -------------------------------
root = tk.Tk()
root.title("⚡ برنامه هفتگی من ⚡")
root.geometry("1100x700")
root.configure(bg="#0B1220")

# -------------------------------
# رنگ‌ها
# -------------------------------
BG = "#0B1220"
DARK = "#111827"
BLUE = "#2563EB"
LIGHT_BLUE = "#60A5FA"
WHITE = "#F8FAFC"
GRAY = "#94A3B8"
CELL = "#172033"

# -------------------------------
# عنوان
# -------------------------------
title = tk.Label(
    root,
    text="⚡ برنامه‌ریزی هفتگی ⚡",
    font=("Tahoma", 25, "bold"),
    bg=BG,
    fg=LIGHT_BLUE
)
title.pack(pady=20)

subtitle = tk.Label(
    root,
    text="🎯 هدف‌هات رو بنویس و هفته رو قوی شروع کن!",
    font=("Tahoma", 12),
    bg=BG,
    fg=GRAY
)
subtitle.pack(pady=5)

# -------------------------------
# روزهای هفته
# -------------------------------
days = [
    "شنبه 🔥",
    "یکشنبه ⚡",
    "دوشنبه 🎮",
    "سه‌شنبه 🏀",
    "چهارشنبه 🚀",
    "پنجشنبه 🎯",
    "جمعه 😎"
]

times = [
    "صبح ☀️",
    "ظهر 🌤️",
    "عصر 🌆",
    "شب 🌙"
]

# -------------------------------
# فریم جدول
# -------------------------------
table_frame = tk.Frame(root, bg=BG)
table_frame.pack(padx=20, pady=20)

# گوشه جدول
tk.Label(
    table_frame,
    text="زمان / روز",
    font=("Tahoma", 11, "bold"),
    bg=BLUE,
    fg=WHITE,
    width=14,
    height=2
).grid(row=0, column=0, padx=3, pady=3)

# -------------------------------
# عنوان ستون‌ها
# -------------------------------
for col, day in enumerate(days, start=1):
    tk.Label(
        table_frame,
        text=day,
        font=("Tahoma", 11, "bold"),
        bg=DARK,
        fg=LIGHT_BLUE,
        width=14,
        height=2
    ).grid(row=0, column=col, padx=3, pady=3)

# -------------------------------
# ساخت خانه‌های برنامه
# -------------------------------
for row, time in enumerate(times, start=1):

    tk.Label(
        table_frame,
        text=time,
        font=("Tahoma", 11, "bold"),
        bg=BLUE,
        fg=WHITE,
        width=14,
        height=4
    ).grid(row=row, column=0, padx=3, pady=3)

    for col in range(1, 8):

        entry = tk.Entry(
            table_frame,
            font=("Tahoma", 10),
            justify="center",
            bg=CELL,
            fg=WHITE,
            insertbackground=LIGHT_BLUE,
            relief="flat",
            width=16
        )

        entry.grid(
            row=row,
            column=col,
            padx=3,
            pady=3,
            ipady=14
        )

# -------------------------------
# بخش هدف هفتگی
# -------------------------------
goal = tk.Label(
    root,
    text="🎯 هدف این هفته:",
    font=("Tahoma", 13, "bold"),
    bg=BG,
    fg=LIGHT_BLUE
)
goal.pack(pady=(10, 5))

goal_entry = tk.Entry(
    root,
    font=("Tahoma", 12),
    bg=DARK,
    fg=WHITE,
    insertbackground=WHITE,
    relief="flat",
    width=60,
    justify="center"
)
goal_entry.pack(ipady=8)

# -------------------------------
# متن پایین
# -------------------------------
footer = tk.Label(
    root,
    text="💪 تمرکز کن • تلاش کن • موفق شو 🔥",
    font=("Tahoma", 13, "bold"),
    bg=BG,
    fg=GRAY
)
footer.pack(pady=20)

# -------------------------------
# اجرای برنامه
# -------------------------------
root.mainloop()

