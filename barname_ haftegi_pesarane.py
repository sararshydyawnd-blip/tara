import tkinter as tk

# پنجره اصلی
root = tk.Tk()
root.title("☀️ برنامه هفتگی من ☀️")
root.geometry("1100x700")
root.configure(bg="#FFF3CD")

# رنگ‌ها
BG = "#FFF3CD"
DARK = "#7A3E00"
ORANGE = "#FF8C00"
LIGHT_ORANGE = "#FFA726"
YELLOW = "#FFD54F"
WHITE = "#FFFFFF"
TEXT = "#5D2E00"
CELL = "#FFF8E1"

# عنوان
title = tk.Label(
    root,
    text="☀️ برنامه‌ریزی هفتگی ☀️",
    font=("Tahoma", 25, "bold"),
    bg=BG,
    fg=ORANGE
)
title.pack(pady=20)

subtitle = tk.Label(
    root,
    text="🔥 هدف‌هات رو بنویس و هفته رو پرانرژی شروع کن!",
    font=("Tahoma", 12),
    bg=BG,
    fg=TEXT
)
subtitle.pack(pady=5)

# روزهای هفته
days = [
    "شنبه 🔥",
    "یکشنبه ☀️",
    "دوشنبه ⚡",
    "سه‌شنبه 🏀",
    "چهارشنبه 🚀",
    "پنجشنبه 🎯",
    "جمعه 😎"
]

times = [
    "صبح ☀️",
    "ظهر 🌞",
    "عصر 🔥",
    "شب 🌙"
]

# فریم جدول
table_frame = tk.Frame(root, bg=BG)
table_frame.pack(padx=20, pady=20)

# گوشه جدول
tk.Label(
    table_frame,
    text="زمان / روز",
    font=("Tahoma", 11, "bold"),
    bg=ORANGE,
    fg=WHITE,
    width=14,
    height=2
).grid(row=0, column=0, padx=3, pady=3)

# روزها
for col, day in enumerate(days, start=1):
    tk.Label(
        table_frame,
        text=day,
        font=("Tahoma", 11, "bold"),
        bg=DARK,
        fg=YELLOW,
        width=14,
        height=2
    ).grid(row=0, column=col, padx=3, pady=3)

# خانه‌های برنامه
for row, time in enumerate(times, start=1):

    tk.Label(
        table_frame,
        text=time,
        font=("Tahoma", 11, "bold"),
        bg=ORANGE,
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
            fg=TEXT,
            insertbackground=ORANGE,
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

# هدف هفته
goal = tk.Label(
    root,
    text="🎯 هدف این هفته:",
    font=("Tahoma", 13, "bold"),
    bg=BG,
    fg=ORANGE
)
goal.pack(pady=(10, 5))

goal_entry = tk.Entry(
    root,
    font=("Tahoma", 12),
    bg=WHITE,
    fg=TEXT,
    insertbackground=ORANGE,
    relief="flat",
    width=60,
    justify="center"
)
goal_entry.pack(ipady=8)

# پایین صفحه
footer = tk.Label(
    root,
    text="☀️ انرژی مثبت • تمرکز • تلاش • موفقیت 🔥",
    font=("Tahoma", 13, "bold"),
    bg=BG,
    fg=DARK
)
footer.pack(pady=20)

root.mainloop()



#(tara emami)