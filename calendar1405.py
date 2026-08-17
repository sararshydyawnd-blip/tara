import tkinter as tk
from tkinter import messagebox
import calendar


# =========================================================
# تقویم شمسی ۱۴۰۵
# =========================================================

root = tk.Tk()

root.title("🌸 تقویم زیبای ۱۴۰۵ 🌸")
root.geometry("1050x750")
root.configure(bg="#0d1326")
root.resizable(False, False)


# =========================================================
# رنگ‌ها
# =========================================================

BG = "#0d1326"
CARD = "#151e38"
CARD2 = "#1d2948"

WHITE = "#ffffff"
TEXT = "#dbe7ff"

BLUE = "#42a5f5"
CYAN = "#00e5ff"
PURPLE = "#9c6cff"

GREEN = "#26d07c"
RED = "#ff5370"
YELLOW = "#ffd166"

HOVER = "#30446f"


# =========================================================
# اطلاعات ماه‌های سال ۱۴۰۵
# =========================================================

months = [
    "فروردین",
    "اردیبهشت",
    "خرداد",
    "تیر",
    "مرداد",
    "شهریور",
    "مهر",
    "آبان",
    "آذر",
    "دی",
    "بهمن",
    "اسفند"
]


# تعداد روزهای ماه‌ها
days_in_month = [
    31, 31, 31, 31, 31, 31,
    30, 30, 30, 30, 30, 29
]


# =========================================================
# مناسبت‌های مهم
# =========================================================

events = {

    "1-1": "نوروز 🎉",
    "2-1": "نوروز 🎉",
    "3-1": "نوروز 🎉",
    "4-1": "نوروز 🎉",

    "12-1": "روز جمهوری اسلامی 🇮🇷",

    "13-1": "روز طبیعت 🌿",

    "14-1": "روز هنر انقلاب",

    "22-1": "روز فناوری هسته‌ای",

    "1-2": "روز سعدی",

    "25-2": "روز فردوسی",

    "3-3": "فتح خرمشهر",

    "14-3": "روز اهدای خون",

    "1-4": "روز تبلیغ",

    "7-4": "روز قوه قضائیه",

    "8-4": "روز مبارزه با مواد مخدر",

    "10-4": "روز صنعت و معدن",

    "16-4": "روز مالیات",

    "26-4": "روز کارآفرینی",

    "1-5": "روز کارگر",

    "25-5": "روز گل و گیاه",

    "1-6": "روز پزشک",

    "5-6": "روز داروساز",

    "13-6": "روز تعاون",

    "1-7": "روز بزرگداشت مولانا",

    "20-7": "روز حافظ",

    "10-8": "روز مجلس",

    "30-8": "روز کتاب",

    "1-9": "روز دانشجو",

    "16-9": "روز دانشجو",

    "30-9": "شب یلدا 🍉",

    "1-10": "روز میلاد خورشید",

    "29-10": "روز هوای پاک",

    "12-11": "دهه فجر",

    "22-11": "پیروزی انقلاب اسلامی",

    "5-12": "روز مهندسی",

    "15-12": "روز درختکاری 🌳",

    "29-12": "روز ملی شدن صنعت نفت"

}


# =========================================================
# متغیرها
# =========================================================

current_month = 0

selected_day = None


# =========================================================
# عنوان
# =========================================================

title_frame = tk.Frame(
    root,
    bg=BG
)

title_frame.pack(
    fill="x",
    pady=(18, 5)
)


title = tk.Label(
    title_frame,
    text="🌸 تقویم زیبای سال ۱۴۰۵ 🌸",
    bg=BG,
    fg=CYAN,
    font=("Tahoma", 28, "bold")
)

title.pack()


subtitle = tk.Label(
    title_frame,
    text="تقویم شمسی | سال ۱۴۰۵",
    bg=BG,
    fg=TEXT,
    font=("Tahoma", 13)
)

subtitle.pack(
    pady=5
)


# =========================================================
# کنترل ماه
# =========================================================

control = tk.Frame(
    root,
    bg=BG
)

control.pack(
    pady=10
)


def previous_month():

    global current_month

    current_month -= 1

    if current_month < 0:
        current_month = 11

    draw_calendar()


def next_month():

    global current_month

    current_month += 1

    if current_month > 11:
        current_month = 0

    draw_calendar()


def today():

    global current_month

    current_month = 0

    draw_calendar()


prev_button = tk.Button(
    control,
    text="◀ ماه قبل",
    command=previous_month,
    bg=PURPLE,
    fg=WHITE,
    activebackground=HOVER,
    activeforeground=WHITE,
    font=("Tahoma", 11, "bold"),
    relief="flat",
    cursor="hand2",
    padx=20,
    pady=8
)

prev_button.pack(
    side="left",
    padx=10
)


month_label = tk.Label(
    control,
    text="فروردین",
    bg=CARD,
    fg=YELLOW,
    font=("Tahoma", 18, "bold"),
    width=15,
    pady=8
)

month_label.pack(
    side="left",
    padx=10
)


next_button = tk.Button(
    control,
    text="ماه بعد ▶",
    command=next_month,
    bg=PURPLE,
    fg=WHITE,
    activebackground=HOVER,
    activeforeground=WHITE,
    font=("Tahoma", 11, "bold"),
    relief="flat",
    cursor="hand2",
    padx=20,
    pady=8
)

next_button.pack(
    side="left",
    padx=10
)


# =========================================================
# کارت تقویم
# =========================================================

calendar_card = tk.Frame(
    root,
    bg=CARD,
    highlightbackground="#26385f",
    highlightthickness=2
)

calendar_card.pack(
    padx=35,
    pady=10,
    fill="both",
    expand=True
)


# =========================================================
# نام روزهای هفته
# =========================================================

weekdays = [
    "شنبه",
    "یکشنبه",
    "دوشنبه",
    "سه‌شنبه",
    "چهارشنبه",
    "پنجشنبه",
    "جمعه"
]


# =========================================================
# تبدیل روز اول ماه
# =========================================================

def first_day_offset(month):

    # شروع تقریبی ماه‌های سال شمسی
    # برای نمایش تقویم زیبا

    offsets = [
        0, 3, 6, 2, 4, 0,
        3, 5, 1, 3, 6, 1
    ]

    return offsets[month]


# =========================================================
# انتخاب روز
# =========================================================

def select_day(day):

    global selected_day

    selected_day = day

    key = f"{day}-{current_month + 1}"

    event = events.get(
        key,
        "برای این روز مناسبتی ثبت نشده است."
    )

    messagebox.showinfo(
        f"{months[current_month]} {day}",
        f"📅 {months[current_month]} {day} ۱۴۰۵\n\n"
        f"✨ {event}"
    )


# =========================================================
# رسم تقویم
# =========================================================

def draw_calendar():

    for widget in calendar_card.winfo_children():

        widget.destroy()


    month_label.config(
        text=months[current_month]
    )


    # ---------------------------------
    # روزهای هفته
    # ---------------------------------

    for col, day_name in enumerate(weekdays):

        label = tk.Label(
            calendar_card,
            text=day_name,
            bg="#202d4c",
            fg=(
                RED
                if day_name == "جمعه"
                else CYAN
            ),
            font=("Tahoma", 12, "bold"),
            pady=10
        )

        label.grid(
            row=0,
            column=col,
            sticky="nsew",
            padx=3,
            pady=3
        )


    # ---------------------------------
    # تنظیم ستون‌ها
    # ---------------------------------

    for col in range(7):

        calendar_card.columnconfigure(
            col,
            weight=1
        )


    for row in range(1, 7):

        calendar_card.rowconfigure(
            row,
            weight=1
        )


    # ---------------------------------
    # روزها
    # ---------------------------------

    total_days = days_in_month[current_month]

    offset = first_day_offset(
        current_month
    )


    for day in range(
        1,
        total_days + 1
    ):

        position = (
            offset + day - 1
        )

        row = (
            position // 7
        ) + 1

        col = (
            position % 7
        )


        key = f"{day}-{current_month + 1}"

        has_event = (
            key in events
        )


        if col == 6:

            color = "#54243a"

            text_color = "#ff7b96"

        elif has_event:

            color = "#293b63"

            text_color = YELLOW

        else:

            color = CARD2

            text_color = WHITE


        button = tk.Button(
            calendar_card,
            text=str(day),
            command=lambda d=day:
                select_day(d),
            bg=color,
            fg=text_color,
            activebackground=HOVER,
            activeforeground=WHITE,
            font=(
                "Tahoma",
                15,
                "bold"
            ),
            relief="flat",
            cursor="hand2"
        )


        button.grid(
            row=row,
            column=col,
            sticky="nsew",
            padx=4,
            pady=4
        )


        # نقطه برای مناسبت

        if has_event:

            event_label = tk.Label(
                calendar_card,
                text="●",
                bg=color,
                fg=YELLOW,
                font=("Arial", 8)
            )

            event_label.place(
                relx=(
                    col / 7
                ) + 0.08,
                rely=(
                    row / 7
                ) + 0.08
            )


# =========================================================
# پایین صفحه
# =========================================================

footer = tk.Frame(
    root,
    bg=BG
)

footer.pack(
    fill="x",
    pady=10
)


legend1 = tk.Label(
    footer,
    text="🟡 مناسبت",
    bg=BG,
    fg=YELLOW,
    font=("Tahoma", 10, "bold")
)

legend1.pack(
    side="left",
    padx=25
)


legend2 = tk.Label(
    footer,
    text="🔴 جمعه",
    bg=BG,
    fg=RED,
    font=("Tahoma", 10, "bold")
)

legend2.pack(
    side="left",
    padx=25
)


legend3 = tk.Label(
    footer,
    text="💡 روی هر روز کلیک کن",
    bg=BG,
    fg=TEXT,
    font=("Tahoma", 10)
)

legend3.pack(
    side="right",
    padx=25
)


# =========================================================
# شروع
# =========================================================

draw_calendar()

root.mainloop()





#(tara emami)