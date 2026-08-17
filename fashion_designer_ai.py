import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import ImageGrab


# ==========================================
# پنجره اصلی
# ==========================================

root = tk.Tk()
root.title("👗 دستیار طراحی و دوخت لباس")
root.geometry("1200x750")
root.configure(bg="#FFF3E0")


# ==========================================
# رنگ‌ها
# ==========================================

BG = "#FFF3E0"
ORANGE = "#F57C00"
DARK_ORANGE = "#E65100"
YELLOW = "#FFB300"
WHITE = "#FFFFFF"
TEXT = "#4E342E"
PINK = "#EC407A"
BLUE = "#42A5F5"


# ==========================================
# عنوان
# ==========================================

title = tk.Label(
    root,
    text="👗✨ دستیار طراحی و دوخت لباس ✨👗",
    font=("Tahoma", 24, "bold"),
    bg=BG,
    fg=DARK_ORANGE
)

title.pack(pady=15)


subtitle = tk.Label(
    root,
    text="ایده لباس خودت را بنویس و طرح و نکات دوخت بگیر!",
    font=("Tahoma", 12),
    bg=BG,
    fg=TEXT
)

subtitle.pack()


# ==========================================
# قسمت وارد کردن ایده
# ==========================================

input_frame = tk.Frame(root, bg=BG)
input_frame.pack(pady=15)


idea_label = tk.Label(
    input_frame,
    text="💡 ایده لباس:",
    font=("Tahoma", 13, "bold"),
    bg=BG,
    fg=DARK_ORANGE
)

idea_label.grid(row=0, column=0, padx=10)


idea_entry = tk.Entry(
    input_frame,
    font=("Tahoma", 12),
    width=65,
    justify="right",
    bg=WHITE,
    fg=TEXT,
    relief="solid"
)

idea_entry.grid(row=0, column=1, padx=10, ipady=8)


# ==========================================
# بدنه اصلی
# ==========================================

main_frame = tk.Frame(root, bg=BG)
main_frame.pack(fill="both", expand=True, padx=20, pady=10)


# ==========================================
# قسمت طراحی
# ==========================================

draw_frame = tk.Frame(
    main_frame,
    bg=WHITE,
    highlightbackground=ORANGE,
    highlightthickness=3
)

draw_frame.pack(
    side="left",
    fill="both",
    expand=True,
    padx=10
)


draw_title = tk.Label(
    draw_frame,
    text="🎨 طرح لباس",
    font=("Tahoma", 16, "bold"),
    bg=WHITE,
    fg=ORANGE
)

draw_title.pack(pady=8)


canvas = tk.Canvas(
    draw_frame,
    width=500,
    height=480,
    bg="#FAFAFA",
    highlightthickness=0
)

canvas.pack(padx=10, pady=5)


# ==========================================
# قسمت نکات
# ==========================================

tips_frame = tk.Frame(
    main_frame,
    bg="#FFF8E1",
    width=400,
    highlightbackground=YELLOW,
    highlightthickness=3
)

tips_frame.pack(
    side="right",
    fill="both",
    padx=10
)


tips_title = tk.Label(
    tips_frame,
    text="🧵 نکات طراحی و دوخت",
    font=("Tahoma", 16, "bold"),
    bg="#FFF8E1",
    fg=DARK_ORANGE
)

tips_title.pack(pady=10)


tips_text = tk.Text(
    tips_frame,
    font=("Tahoma", 11),
    bg="#FFF8E1",
    fg=TEXT,
    wrap="word",
    relief="flat"
)

tips_text.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=10
)


# ==========================================
# تشخیص نوع لباس
# ==========================================

def detect_type(idea):

    idea = idea.lower()

    if "پیراهن" in idea or "dress" in idea:
        return "dress"

    if "دامن" in idea:
        return "skirt"

    if "شلوار" in idea:
        return "pants"

    if "کت" in idea or "مانتو" in idea or "jacket" in idea:
        return "jacket"

    if "بلوز" in idea or "تاپ" in idea or "shirt" in idea:
        return "top"

    return "dress"


# ==========================================
# تشخیص رنگ
# ==========================================

def detect_color(idea):

    colors = {
        "مشکی": "#212121",
        "سفید": "#FFFFFF",
        "قرمز": "#E53935",
        "آبی": "#1E88E5",
        "سبز": "#43A047",
        "زرد": "#FDD835",
        "نارنجی": "#FB8C00",
        "صورتی": "#EC407A",
        "بنفش": "#8E24AA",
        "قهوه‌ای": "#6D4C41"
    }

    for name, color in colors.items():

        if name in idea:
            return color

    return "#FFB74D"


# ==========================================
# پاک کردن طرح
# ==========================================

def clear_canvas():

    canvas.delete("all")


# ==========================================
# رسم سر و بدن مانکن
# ==========================================

def draw_body():

    # سر
    canvas.create_oval(
        210, 30,
        290, 110,
        outline="#555555",
        width=3
    )

    # گردن
    canvas.create_line(
        230, 105,
        230, 135,
        fill="#555555",
        width=3
    )

    canvas.create_line(
        270, 105,
        270, 135,
        fill="#555555",
        width=3
    )

    # بدن
    canvas.create_line(
        230, 135,
        185, 240,
        fill="#555555",
        width=3
    )

    canvas.create_line(
        270, 135,
        315, 240,
        fill="#555555",
        width=3
    )


# ==========================================
# رسم پیراهن
# ==========================================

def draw_dress(color, idea):

    # بالاتنه
    canvas.create_polygon(
        230, 125,
        270, 125,
        315, 240,
        185, 240,
        fill=color,
        outline="#333333",
        width=3
    )

    # دامن
    canvas.create_polygon(
        185, 235,
        315, 235,
        390, 440,
        110, 440,
        fill=color,
        outline="#333333",
        width=3
    )

    # کمر
    canvas.create_line(
        185, 235,
        315, 235,
        fill="#333333",
        width=4
    )

    # یقه
    if "یقه قلبی" in idea:

        canvas.create_arc(
            225, 120,
            275, 160,
            start=180,
            extent=180,
            style="arc",
            outline="#333333",
            width=3
        )

    elif "یقه گرد" in idea:

        canvas.create_arc(
            225, 115,
            275, 155,
            start=180,
            extent=180,
            style="arc",
            outline="#333333",
            width=3
        )

    else:

        canvas.create_line(
            230, 130,
            250, 150,
            270, 130,
            fill="#333333",
            width=3
        )

    # آستین پفی
    if "پفی" in idea:

        canvas.create_oval(
            175, 135,
            225, 205,
            fill=color,
            outline="#333333",
            width=3
        )

        canvas.create_oval(
            275, 135,
            325, 205,
            fill=color,
            outline="#333333",
            width=3
        )

    # آستین بلند
    elif "آستین بلند" in idea:

        canvas.create_line(
            190, 145,
            140, 230,
            fill=color,
            width=25
        )

        canvas.create_line(
            310, 145,
            360, 230,
            fill=color,
            width=25
        )

    # کمربند
    if "کمربند" in idea:

        canvas.create_rectangle(
            180, 225,
            320, 245,
            fill="#222222"
        )


# ==========================================
# رسم دامن
# ==========================================

def draw_skirt(color):

    canvas.create_polygon(
        190, 170,
        310, 170,
        380, 440,
        120, 440,
        fill=color,
        outline="#333333",
        width=3
    )

    canvas.create_line(
        190, 170,
        310, 170,
        fill="#333333",
        width=5
    )


# ==========================================
# رسم شلوار
# ==========================================

def draw_pants(color):

    canvas.create_polygon(
        190, 160,
        310, 160,
        300, 300,
        280, 440,
        250, 440,
        245, 280,
        220, 440,
        190, 440,
        200, 300,
        fill=color,
        outline="#333333",
        width=3
    )


# ==========================================
# تولید نکات دوخت
# ==========================================

def make_tips(idea, clothing_type):

    tips = []

    tips.append("✂️ نکات عمومی طراحی و دوخت")
    tips.append("--------------------------------")
    tips.append("• قبل از برش، اندازه‌های بدن را دقیق بگیرید.")
    tips.append("• الگو را ابتدا روی کاغذ اصلاح و کنترل کنید.")
    tips.append("• قبل از برش پارچه اصلی، نمونه اولیه تهیه کنید.")
    tips.append("• جهت راه پارچه را حتماً روی الگو مشخص کنید.")
    tips.append("• جای دوخت را متناسب با نوع درز در نظر بگیرید.")
    tips.append("")

    if clothing_type == "dress":

        tips.append("👗 نکات مخصوص پیراهن")
        tips.append("• ابتدا خط کمر و سینه را کنترل کنید.")
        tips.append("• برای پارچه‌های لیز مثل ساتن، برش دقیق اهمیت زیادی دارد.")
        tips.append("• برای دامن بلند، قد نهایی را با کفش موردنظر کنترل کنید.")

    elif clothing_type == "skirt":

        tips.append("👗 نکات مخصوص دامن")
        tips.append("• اندازه کمر و باسن را دقیق بگیرید.")
        tips.append("• خط باسن و مقدار آزادی را کنترل کنید.")
        tips.append("• برای دامن فون، میزان بازشدگی پایین را قبل از برش مشخص کنید.")

    elif clothing_type == "pants":

        tips.append("👖 نکات مخصوص شلوار")
        tips.append("• اندازه دور کمر، باسن و قد شلوار مهم است.")
        tips.append("• فاق جلو و پشت باید با اندازه بدن هماهنگ باشد.")
        tips.append("• قبل از دوخت نهایی، پرو انجام دهید.")

    elif clothing_type == "jacket":

        tips.append("🧥 نکات مخصوص کت و مانتو")
        tips.append("• آزادی لباس را بر اساس نوع پارچه تعیین کنید.")
        tips.append("• محل جیب‌ها را قبل از برش مشخص کنید.")
        tips.append("• لایی مناسب برای قسمت‌های حساس استفاده کنید.")

    if "ساتن" in idea:

        tips.append("")
        tips.append("✨ پارچه ساتن")
        tips.append("• از سوزن ظریف استفاده کنید.")
        tips.append("• هنگام برش، پارچه را ثابت نگه دارید.")
        tips.append("• اتوکاری با حرارت مناسب انجام شود.")

    if "تور" in idea:

        tips.append("")
        tips.append("✨ پارچه تور")
        tips.append("• هنگام برش با دقت بیشتری کار کنید.")
        tips.append("• لبه‌ها را متناسب با نوع تور تمیزکاری کنید.")

    if "مخمل" in idea:

        tips.append("")
        tips.append("✨ پارچه مخمل")
        tips.append("• جهت خواب پارچه در تمام قطعات یکسان باشد.")
        tips.append("• قبل از برش، قطعات الگو را از نظر جهت خواب بررسی کنید.")

    if "پفی" in idea:

        tips.append("")
        tips.append("🎀 آستین پفی")
        tips.append("• برای حجم آستین باید مقدار اضافه مناسبی در تاج آستین ایجاد شود.")
        tips.append("• چین‌ها را به صورت یکنواخت تقسیم کنید.")

    tips.append("")
    tips.append("📏 یادآوری مهم:")
    tips.append("طرح نهایی قبل از برش پارچه اصلی حتماً پرو و اصلاح شود.")

    return "\n".join(tips)


# ==========================================
# ساخت طرح
# ==========================================

def generate_design():

    idea = idea_entry.get().strip()

    if not idea:

        messagebox.showwarning(
            "⚠️ توجه",
            "اول ایده لباس را بنویس!"
        )

        return

    clear_canvas()

    clothing_type = detect_type(idea)

    color = detect_color(idea)

    draw_body()

    if clothing_type == "dress":

        draw_dress(color, idea)

    elif clothing_type == "skirt":

        draw_skirt(color)

    elif clothing_type == "pants":

        draw_pants(color)

    elif clothing_type == "jacket":

        draw_dress(color, idea)

    elif clothing_type == "top":

        draw_dress(color, idea)

    tips_text.delete("1.0", tk.END)

    tips_text.insert(
        tk.END,
        make_tips(idea, clothing_type)
    )


# ==========================================
# ذخیره طرح
# ==========================================

def save_design():

    filename = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[
            ("PNG Image", "*.png")
        ]
    )

    if not filename:
        return

    x = root.winfo_rootx() + canvas.winfo_x()
    y = root.winfo_rooty() + canvas.winfo_y()
    x2 = x + canvas.winfo_width()
    y2 = y + canvas.winfo_height()

    image = ImageGrab.grab(
        bbox=(x, y, x2, y2)
    )

    image.save(filename)

    messagebox.showinfo(
        "✅ ذخیره شد",
        "طرح لباس با موفقیت ذخیره شد!"
    )


# ==========================================
# دکمه‌ها
# ==========================================

button_frame = tk.Frame(
    root,
    bg=BG
)

button_frame.pack(pady=10)


generate_button = tk.Button(
    button_frame,
    text="✨ طراحی کن",
    font=("Tahoma", 12, "bold"),
    bg=ORANGE,
    fg=WHITE,
    activebackground=DARK_ORANGE,
    activeforeground=WHITE,
    relief="flat",
    padx=25,
    pady=10,
    command=generate_design
)

generate_button.grid(
    row=0,
    column=0,
    padx=10
)


save_button = tk.Button(
    button_frame,
    text="💾 ذخیره طرح",
    font=("Tahoma", 12, "bold"),
    bg=YELLOW,
    fg=TEXT,
    activebackground="#FFA000",
    relief="flat",
    padx=25,
    pady=10,
    command=save_design
)

save_button.grid(
    row=0,
    column=1,
    padx=10
)


clear_button = tk.Button(
    button_frame,
    text="🗑️ پاک کردن",
    font=("Tahoma", 12, "bold"),
    bg="#EF5350",
    fg=WHITE,
    relief="flat",
    padx=25,
    pady=10,
    command=clear_canvas
)

clear_button.grid(
    row=0,
    column=2,
    padx=10
)


# ==========================================
# اجرای برنامه
# ==========================================

root.mainloop()



