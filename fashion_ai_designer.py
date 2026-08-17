import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
from openai import OpenAI
import base64
import io
import os
import threading


# =====================================================
# تنظیم API
# =====================================================

# بهتر است API Key را به صورت متغیر محیطی قرار بدهی:
# Windows:
# set OPENAI_API_KEY=YOUR_API_KEY

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("OPENAI_API_KEY پیدا نشد.")
    print("ابتدا API Key را به صورت متغیر محیطی تنظیم کن.")

client = OpenAI(api_key=api_key) if api_key else None


# =====================================================
# پنجره
# =====================================================

root = tk.Tk()
root.title("👗 Fashion AI Designer")
root.geometry("1250x800")
root.configure(bg="#FFF4E6")


# =====================================================
# رنگ‌ها
# =====================================================

BG = "#FFF4E6"
ORANGE = "#F57C00"
DARK = "#4E2600"
YELLOW = "#FFB300"
WHITE = "#FFFFFF"
LIGHT = "#FFF8EF"
PINK = "#E91E63"


# =====================================================
# عنوان
# =====================================================

title = tk.Label(
    root,
    text="👗✨ FASHION AI DESIGNER ✨👗",
    font=("Tahoma", 25, "bold"),
    bg=BG,
    fg=ORANGE
)

title.pack(pady=15)


subtitle = tk.Label(
    root,
    text="ایده لباس را بنویس؛ هوش مصنوعی آن را طراحی می‌کند!",
    font=("Tahoma", 13),
    bg=BG,
    fg=DARK
)

subtitle.pack()


# =====================================================
# ورودی ایده
# =====================================================

input_frame = tk.Frame(root, bg=BG)
input_frame.pack(pady=15)


tk.Label(
    input_frame,
    text="💡 ایده لباس:",
    font=("Tahoma", 13, "bold"),
    bg=BG,
    fg=DARK
).pack(side="right", padx=10)


idea_entry = tk.Entry(
    input_frame,
    font=("Tahoma", 13),
    width=75,
    justify="right",
    bg=WHITE,
    fg=DARK,
    relief="solid"
)

idea_entry.pack(side="right", ipady=8)


# =====================================================
# فریم اصلی
# =====================================================

main_frame = tk.Frame(root, bg=BG)
main_frame.pack(fill="both", expand=True, padx=20)


# =====================================================
# سمت تصویر
# =====================================================

image_frame = tk.Frame(
    main_frame,
    bg=WHITE,
    highlightbackground=ORANGE,
    highlightthickness=3
)

image_frame.pack(
    side="left",
    fill="both",
    expand=True,
    padx=10
)


tk.Label(
    image_frame,
    text="🎨 طرح تولیدشده",
    font=("Tahoma", 16, "bold"),
    bg=WHITE,
    fg=ORANGE
).pack(pady=10)


image_label = tk.Label(
    image_frame,
    text="هنوز طرحی ساخته نشده است\n\nایده خودت را وارد کن 👗",
    font=("Tahoma", 14),
    bg=WHITE,
    fg=DARK
)

image_label.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=20
)


# =====================================================
# سمت نکات
# =====================================================

tips_frame = tk.Frame(
    main_frame,
    bg=LIGHT,
    highlightbackground=YELLOW,
    highlightthickness=3
)

tips_frame.pack(
    side="right",
    fill="both",
    expand=True,
    padx=10
)


tk.Label(
    tips_frame,
    text="🧵 اطلاعات طراحی و دوخت",
    font=("Tahoma", 16, "bold"),
    bg=LIGHT,
    fg=DARK
).pack(pady=10)


tips_text = tk.Text(
    tips_frame,
    font=("Tahoma", 11),
    bg=LIGHT,
    fg=DARK,
    wrap="word",
    relief="flat"
)

tips_text.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=10
)


# =====================================================
# پرامپت طراحی لباس
# =====================================================

def make_image_prompt(idea):

    return f"""
Create a professional fashion design sketch based on this idea:

{idea}

The result must be a professional clothing design concept.

Show:
- full body fashion figure
- front view
- complete garment
- accurate silhouette
- neckline
- sleeves
- skirt or pants shape
- garment details
- fabric appearance
- realistic colors
- elegant fashion illustration
- clean studio background

The clothing design must be the main focus.

Do not add text, labels, logos or watermarks.
"""


# =====================================================
# گرفتن نکات طراحی و دوخت
# =====================================================

def get_fashion_tips(idea):

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"""
تو یک طراح لباس و متخصص الگو و دوخت هستی.

برای این ایده لباس:

{idea}

یک راهنمای کوتاه و کاربردی به زبان فارسی بده.

حتماً این بخش‌ها را داشته باش:

👗 جزئیات طراحی
🧵 پارچه پیشنهادی
📐 نکات الگو
✂️ نکات برش
🪡 نکات دوخت
📏 نکات اندازه‌گیری و پرو
⚠️ نکات مهم

پاسخ را برای کسی بنویس که می‌خواهد این لباس را واقعاً طراحی و دوخت کند.
"""
    )

    return response.output_text


# =====================================================
# تولید تصویر
# =====================================================

def generate_image(idea):

    prompt = make_image_prompt(idea)

    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024"
    )

    image_data = base64.b64decode(
        result.data[0].b64_json
    )

    return Image.open(
        io.BytesIO(image_data)
    )


# =====================================================
# اجرای عملیات در Thread
# =====================================================

def generate():

    idea = idea_entry.get().strip()

    if not idea:
        messagebox.showwarning(
            "توجه",
            "اول ایده لباس را بنویس 👗"
        )
        return

    if not client:
        messagebox.showerror(
            "API Key",
            "OPENAI_API_KEY تنظیم نشده است."
        )
        return

    generate_button.config(
        state="disabled",
        text="⏳ در حال طراحی..."
    )

    image_label.config(
        text="🎨 هوش مصنوعی در حال طراحی لباس است...",
        image=""
    )

    tips_text.delete("1.0", tk.END)

    def work():

        try:

            # تولید تصویر
            image = generate_image(idea)

            # گرفتن نکات
            tips = get_fashion_tips(idea)

            # نمایش در Tkinter
            image.thumbnail((520, 520))

            photo = ImageTk.PhotoImage(image)

            def update():

                image_label.config(
                    image=photo,
                    text=""
                )

                image_label.image = photo

                tips_text.insert(
                    tk.END,
                    tips
                )

                generate_button.config(
                    state="normal",
                    text="✨ طراحی لباس"
                )

            root.after(0, update)

        except Exception as e:

            def error():

                messagebox.showerror(
                    "خطا",
                    f"مشکلی پیش آمد:\n\n{e}"
                )

                generate_button.config(
                    state="normal",
                    text="✨ طراحی لباس"
                )

            root.after(0, error)

    threading.Thread(
        target=work,
        daemon=True
    ).start()


# =====================================================
# ذخیره تصویر
# =====================================================

last_image = None


def save_image():

    if not hasattr(image_label, "image"):

        messagebox.showwarning(
            "توجه",
            "اول یک طرح تولید کن."
        )

        return

    filename = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[
            ("PNG Image", "*.png")
        ]
    )

    if not filename:
        return

    image = image_label.image

    image._PhotoImage__photo.write(
        filename,
        format="png"
    )

    messagebox.showinfo(
        "ذخیره شد",
        "طرح با موفقیت ذخیره شد! 💾"
    )


# =====================================================
# دکمه‌ها
# =====================================================

button_frame = tk.Frame(
    root,
    bg=BG
)

button_frame.pack(pady=15)


generate_button = tk.Button(
    button_frame,
    text="✨ طراحی لباس",
    font=("Tahoma", 13, "bold"),
    bg=ORANGE,
    fg=WHITE,
    activebackground=DARK,
    activeforeground=WHITE,
    relief="flat",
    padx=30,
    pady=10,
    command=generate
)

generate_button.pack(
    side="left",
    padx=10
)


save_button = tk.Button(
    button_frame,
    text="💾 ذخیره طرح",
    font=("Tahoma", 13, "bold"),
    bg=YELLOW,
    fg=DARK,
    activebackground=ORANGE,
    relief="flat",
    padx=30,
    pady=10,
    command=save_image
)

save_button.pack(
    side="left",
    padx=10
)


# =====================================================
# اجرای برنامه
# =====================================================

root.mainloop()