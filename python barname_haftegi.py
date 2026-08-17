import tkinter as tk
from tkinter import ttk

# پنجره اصلی
root = tk.Tk()
root.title("🌸 برنامه‌ریزی هفتگی من 🌸")
root.geometry("1000x650")
root.configure(bg="#FFF0F6")

# عنوان
title = tk.Label(
    root,
    text="🌷 برنامه‌ریزی هفتگی من 🌷",
    font=("Tahoma", 24, "bold"),
    bg="#FFF0F6",
    fg="#D63384"
)
title.pack(pady=20)

# روزهای هفته
days = [
    "شنبه 🌸",
    "یکشنبه 🌼",
    "دوشنبه 🌷",
    "سه‌شنبه 🌺",
    "چهارشنبه 🌻",
    "پنجشنبه 🌹",
    "جمعه 💐"
]

# ساعت‌ها
times = [
    "صبح ☀️",
    "ظهر 🌤️",
    "عصر 🌸",
    "شب 🌙"
]

# فریم جدول
frame = tk.Frame(root, bg="#FFF0F6")
frame.pack(padx=20, pady=10, fill="both", expand=True)

# خانه گوشه جدول
tk.Label(
    frame,
    text="زمان / روز",
    font=("Tahoma", 12, "bold"),
    bg="#F8BBD0",
    fg="#6A1B4D",
    width=14,
    height=2
).grid(row=0, column=0, padx=2, pady=2)

# ساخت ستون روزها
for col, day in enumerate(days, start=1):
    tk.Label(
        frame,
        text=day,
        font=("Tahoma", 11, "bold"),
        bg="#F48FB1",
        fg="white",
        width=14,
        height=2
    ).grid(row=0, column=col, padx=2, pady=2)

# ساخت جدول
colors = ["#FFF5F8", "#FFF0F5", "#FCE4EC", "#FFF8E1"]

for row, time in enumerate(times, start=1):

    tk.Label(
        frame,
        text=time,
        font=("Tahoma", 11, "bold"),
        bg="#F8BBD0",
        fg="#6A1B4D",
        width=14,
        height=4
    ).grid(row=row, column=0, padx=2, pady=2)

    for col in range(1, 8):

        entry = tk.Entry(
            frame,
            font=("Tahoma", 10),
            justify="center",
            bg=colors[row - 1],
            fg="#7B1E57",
            relief="flat",
            width=16
        )

        entry.grid(
            row=row,
            column=col,
            padx=2,
            pady=2,
            ipady=12
        )

# متن پایین
footer = tk.Label(
    root,
    text="🌸 هر روز یک قدم کوچک به سمت هدف‌هایت 🌸",
    font=("Tahoma", 13, "bold"),
    bg="#FFF0F6",
    fg="#C2185B"
)
footer.pack(pady=15)

root.mainloop()