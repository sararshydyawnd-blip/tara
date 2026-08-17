import tkinter as tk
import math


# =========================
# تنظیمات
# =========================

root = tk.Tk()
root.title("🧮 ماشین حساب مهندسی PRO")
root.geometry("900x650")
root.configure(bg="#0b1020")
root.resizable(False, False)


# =========================
# متغیرها
# =========================

expression = ""
memory = 0
answer = 0
angle_mode = "DEG"


# =========================
# نمایشگر
# =========================

display = tk.Entry(
    root,
    font=("Consolas", 28, "bold"),
    bg="#151d35",
    fg="#00ffff",
    insertbackground="white",
    justify="right",
    relief="flat"
)

display.pack(
    fill="x",
    padx=20,
    pady=20,
    ipady=20
)


# =========================
# توابع
# =========================

def add(value):

    display.insert(
        tk.END,
        value
    )


def clear():

    display.delete(
        0,
        tk.END
    )


def backspace():

    text = display.get()

    display.delete(
        0,
        tk.END
    )

    display.insert(
        0,
        text[:-1]
    )


def calculate():

    global answer

    try:

        text = display.get()

        text = text.replace(
            "×",
            "*"
        )

        text = text.replace(
            "÷",
            "/"
        )

        text = text.replace(
            "^",
            "**"
        )

        result = eval(
            text,
            {
                "__builtins__": {}
            },
            {
                "pi": math.pi,
                "e": math.e,
                "sqrt": math.sqrt,
                "sin": math.sin,
                "cos": math.cos,
                "tan": math.tan,
                "log": math.log10,
                "ln": math.log,
                "abs": abs
            }
        )

        answer = result

        display.delete(
            0,
            tk.END
        )

        display.insert(
            0,
            str(result)
        )

    except:

        display.delete(
            0,
            tk.END
        )

        display.insert(
            0,
            "ERROR"
        )


def square():

    try:

        value = float(
            display.get()
        )

        result = value ** 2

        display.delete(
            0,
            tk.END
        )

        display.insert(
            0,
            str(result)
        )

    except:

        display.insert(
            tk.END,
            "**2"
        )


def sqrt_number():

    try:

        value = float(
            display.get()
        )

        result = math.sqrt(
            value
        )

        display.delete(
            0,
            tk.END
        )

        display.insert(
            0,
            str(result)
        )

    except:

        display.insert(
            tk.END,
            "sqrt("
        )


def factorial():

    try:

        value = int(
            float(
                display.get()
            )
        )

        result = math.factorial(
            value
        )

        display.delete(
            0,
            tk.END
        )

        display.insert(
            0,
            str(result)
        )

    except:

        display.insert(
            tk.END,
            "!"
        )


def sin():

    try:

        value = float(
            display.get()
        )

        if angle_mode == "DEG":

            value = math.radians(
                value
            )

        result = math.sin(
            value
        )

        display.delete(
            0,
            tk.END
        )

        display.insert(
            0,
            str(round(result, 10))
        )

    except:

        display.insert(
            tk.END,
            "sin("
        )


def cos():

    try:

        value = float(
            display.get()
        )

        if angle_mode == "DEG":

            value = math.radians(
                value
            )

        result = math.cos(
            value
        )

        display.delete(
            0,
            tk.END
        )

        display.insert(
            0,
            str(round(result, 10))
        )

    except:

        display.insert(
            tk.END,
            "cos("
        )


def tan():

    try:

        value = float(
            display.get()
        )

        if angle_mode == "DEG":

            value = math.radians(
                value
            )

        result = math.tan(
            value
        )

        display.delete(
            0,
            tk.END
        )

        display.insert(
            0,
            str(round(result, 10))
        )

    except:

        display.insert(
            tk.END,
            "tan("
        )


def change_mode():

    global angle_mode

    if angle_mode == "DEG":

        angle_mode = "RAD"

    else:

        angle_mode = "DEG"

    mode_button.config(
        text=angle_mode
    )


def memory_clear():

    global memory

    memory = 0


def memory_add():

    global memory

    try:

        memory += float(
            display.get()
        )

    except:
        pass


def memory_recall():

    display.delete(
        0,
        tk.END
    )

    display.insert(
        0,
        str(memory)
    )


def memory_subtract():

    global memory

    try:

        memory -= float(
            display.get()
        )

    except:
        pass


# =========================
# ساخت دکمه
# =========================

def button(
    parent,
    text,
    command,
    color="#18233d"
):

    return tk.Button(

        parent,

        text=text,

        command=command,

        bg=color,

        fg="white",

        activebackground="#34496e",

        activeforeground="white",

        font=(
            "Arial",
            13,
            "bold"
        ),

        relief="flat",

        bd=0,

        cursor="hand2"
    )


# =========================
# حالت زاویه
# =========================

top = tk.Frame(
    root,
    bg="#0b1020"
)

top.pack(
    fill="x",
    padx=20
)

mode_button = button(
    top,
    angle_mode,
    change_mode,
    "#3949ab"
)

mode_button.pack(
    side="right",
    ipadx=15,
    ipady=8
)


# =========================
# صفحه دکمه‌ها
# =========================

frame = tk.Frame(
    root,
    bg="#0b1020"
)

frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=15
)


buttons = [

    [
        ("MC", memory_clear, "#3949ab"),
        ("MR", memory_recall, "#3949ab"),
        ("M+", memory_add, "#3949ab"),
        ("M-", memory_subtract, "#3949ab"),
        ("C", clear, "#d32f2f"),
        ("⌫", backspace, "#d32f2f")
    ],

    [
        ("sin", sin, "#673ab7"),
        ("cos", cos, "#673ab7"),
        ("tan", tan, "#673ab7"),
        ("√", sqrt_number, "#673ab7"),
        ("x²", square, "#673ab7"),
        ("n!", factorial, "#673ab7")
    ],

    [
        ("π", lambda: add(str(math.pi)), "#00897b"),
        ("e", lambda: add(str(math.e)), "#00897b"),
        ("(", lambda: add("("), "#00897b"),
        (")", lambda: add(")"), "#00897b"),
        ("^", lambda: add("^"), "#ff8c00"),
        ("÷", lambda: add("÷"), "#ff8c00")
    ],

    [
        ("7", lambda: add("7")),
        ("8", lambda: add("8")),
        ("9", lambda: add("9")),
        ("×", lambda: add("×"), "#ff8c00"),
        ("%", lambda: add("%"), "#ff8c00"),
        ("log", lambda: add("log("), "#673ab7")
    ],

    [
        ("4", lambda: add("4")),
        ("5", lambda: add("5")),
        ("6", lambda: add("6")),
        ("-", lambda: add("-"), "#ff8c00"),
        ("+", lambda: add("+"), "#ff8c00"),
        ("ln", lambda: add("ln("), "#673ab7")
    ],

    [
        ("1", lambda: add("1")),
        ("2", lambda: add("2")),
        ("3", lambda: add("3")),
        (".", lambda: add(".")),
        ("Ans", lambda: add(str(answer)), "#3949ab"),
        ("=", calculate, "#00a88f")
    ],

    [
        ("0", lambda: add("0")),
        ("00", lambda: add("00")),
        ("(", lambda: add("(")),
        (")", lambda: add(")")),
        ("abs", lambda: add("abs("), "#673ab7"),
        ("AC", clear, "#d32f2f")
    ]

]


# =========================
# قرار دادن دکمه‌ها
# =========================

for r, row in enumerate(buttons):

    frame.rowconfigure(
        r,
        weight=1
    )

    for c in range(6):

        frame.columnconfigure(
            c,
            weight=1
        )

    for c, item in enumerate(row):

        text = item[0]

        command = item[1]

        color = (
            item[2]
            if len(item) == 3
            else "#18233d"
        )

        b = button(
            frame,
            text,
            command,
            color
        )

        b.grid(
            row=r,
            column=c,
            sticky="nsew",
            padx=4,
            pady=4
        )


# =========================
# کیبورد
# =========================

def keyboard(event):

    key = event.char

    if key in "0123456789.+-*/()":

        add(key)

    elif event.keysym == "Return":

        calculate()

    elif event.keysym == "BackSpace":

        backspace()

    elif event.keysym == "Escape":

        clear()


root.bind(
    "<Key>",
    keyboard
)


# =========================
# اجرا
# =========================

root.mainloop()



#(tara emami)