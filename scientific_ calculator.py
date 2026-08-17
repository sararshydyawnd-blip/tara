import tkinter as tk
import math
import re


# ============================================================
#              SCIENTIFIC CALCULATOR PRO
# ============================================================

class ScientificCalculator:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "🧮 Scientific Calculator PRO"
        )

        self.root.geometry(
            "1050x720"
        )

        self.root.minsize(
            900,
            650
        )

        self.root.configure(
            bg="#0b1020"
        )

        # ----------------------------------------------------
        # VARIABLES
        # ----------------------------------------------------

        self.expression = ""

        self.result = ""

        self.memory = 0

        self.angle_mode = "DEG"

        self.history = []

        self.just_calculated = False

        # ----------------------------------------------------
        # COLORS
        # ----------------------------------------------------

        self.bg = "#0b1020"

        self.display_bg = "#111a2e"

        self.display_fg = "#ffffff"

        self.number_color = "#18243d"

        self.operator_color = "#ff8c42"

        self.function_color = "#673ab7"

        self.special_color = "#00897b"

        self.equal_color = "#00bfa5"

        self.danger_color = "#e53935"

        self.memory_color = "#3949ab"

        self.hover_color = "#263858"

        # ----------------------------------------------------
        # BUILD UI
        # ----------------------------------------------------

        self.create_header()

        self.create_display()

        self.create_main_area()

        self.create_history_panel()

        self.bind_keyboard()

    # ========================================================
    # HEADER
    # ========================================================

    def create_header(self):

        header = tk.Frame(
            self.root,
            bg=self.bg
        )

        header.pack(
            fill="x",
            padx=18,
            pady=(15, 5)
        )

        title = tk.Label(
            header,
            text="SCIENTIFIC CALCULATOR",
            bg=self.bg,
            fg="#00eaff",
            font=(
                "Arial",
                24,
                "bold"
            )
        )

        title.pack(
            side="left"
        )

        self.mode_button = tk.Button(
            header,
            text="DEG",
            command=self.change_angle_mode,
            bg="#3949ab",
            fg="white",
            activebackground="#5c6bc0",
            activeforeground="white",
            font=(
                "Arial",
                12,
                "bold"
            ),
            relief="flat",
            width=8,
            height=1,
            cursor="hand2"
        )

        self.mode_button.pack(
            side="right"
        )

    # ========================================================
    # DISPLAY
    # ========================================================

    def create_display(self):

        display_frame = tk.Frame(
            self.root,
            bg=self.display_bg,
            highlightbackground="#273653",
            highlightthickness=2
        )

        display_frame.pack(
            fill="x",
            padx=18,
            pady=10
        )

        self.display = tk.Label(
            display_frame,
            text="0",
            bg=self.display_bg,
            fg=self.display_fg,
            anchor="e",
            font=(
                "Consolas",
                32,
                "bold"
            ),
            padx=20,
            pady=18
        )

        self.display.pack(
            fill="x"
        )

        self.result_label = tk.Label(
            display_frame,
            text="",
            bg=self.display_bg,
            fg="#00eaff",
            anchor="e",
            font=(
                "Consolas",
                16
            ),
            padx=20,
            pady=(0, 12)
        )

        self.result_label.pack(
            fill="x"
        )

    # ========================================================
    # MAIN AREA
    # ========================================================

    def create_main_area(self):

        main = tk.Frame(
            self.root,
            bg=self.bg
        )

        main.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=5
        )

        # Calculator section

        calculator = tk.Frame(
            main,
            bg=self.bg
        )

        calculator.pack(
            side="left",
            fill="both",
            expand=True
        )

        # ----------------------------------------------------
        # MEMORY BUTTONS
        # ----------------------------------------------------

        memory_frame = tk.Frame(
            calculator,
            bg=self.bg
        )

        memory_frame.pack(
            fill="x",
            pady=5
        )

        memory_buttons = [
            ("MC", self.memory_clear),
            ("MR", self.memory_recall),
            ("M+", self.memory_add),
            ("M-", self.memory_subtract),
            ("MS", self.memory_store),
        ]

        for text, command in memory_buttons:

            self.create_button(
                memory_frame,
                text,
                command,
                self.memory_color,
                width=8
            ).pack(
                side="left",
                fill="x",
                expand=True,
                padx=3
            )

        # ----------------------------------------------------
        # BUTTON GRID
        # ----------------------------------------------------

        grid = tk.Frame(
            calculator,
            bg=self.bg
        )

        grid.pack(
            fill="both",
            expand=True
        )

        buttons = [

            # Row 1
            [
                ("sin", lambda: self.add_function("sin")),
                ("cos", lambda: self.add_function("cos")),
                ("tan", lambda: self.add_function("tan")),
                ("asin", lambda: self.add_function("asin")),
                ("acos", lambda: self.add_function("acos")),
                ("atan", lambda: self.add_function("atan")),
            ],

            # Row 2
            [
                ("sinh", lambda: self.add_function("sinh")),
                ("cosh", lambda: self.add_function("cosh")),
                ("tanh", lambda: self.add_function("tanh")),
                ("ln", lambda: self.add_function("ln")),
                ("log", lambda: self.add_function("log")),
                ("√", lambda: self.add_function("sqrt")),
            ],

            # Row 3
            [
                ("π", lambda: self.add_text("pi")),
                ("e", lambda: self.add_text("e")),
                ("x²", lambda: self.square()),
                ("xʸ", lambda: self.add_text("**")),
                ("1/x", lambda: self.inverse()),
                ("n!", lambda: self.factorial()),
            ],

            # Row 4
            [
                ("(", lambda: self.add_text("(")),
                (")", lambda: self.add_text(")")),
                ("%", lambda: self.add_text("%")),
                ("⌫", self.backspace, self.danger_color),
                ("C", self.clear, self.danger_color),
                ("÷", lambda: self.add_text("/"), self.operator_color),
            ],

            # Row 5
            [
                ("7", lambda: self.add_text("7")),
                ("8", lambda: self.add_text("8")),
                ("9", lambda: self.add_text("9")),
                ("×", lambda: self.add_text("*"), self.operator_color),
                ("mod", lambda: self.add_text("%"), self.operator_color),
                ("EXP", lambda: self.add_text("e"), self.operator_color),
            ],

            # Row 6
            [
                ("4", lambda: self.add_text("4")),
                ("5", lambda: self.add_text("5")),
                ("6", lambda: self.add_text("6")),
                ("−", lambda: self.add_text("-"), self.operator_color),
                ("abs", lambda: self.add_function("abs")),
                ("floor", lambda: self.add_function("floor")),
            ],

            # Row 7
            [
                ("1", lambda: self.add_text("1")),
                ("2", lambda: self.add_text("2")),
                ("3", lambda: self.add_text("3")),
                ("+", lambda: self.add_text("+"), self.operator_color),
                ("ceil", lambda: self.add_function("ceil")),
                ("round", lambda: self.add_function("round")),
            ],

            # Row 8
            [
                ("0", lambda: self.add_text("0")),
                (".", lambda: self.add_text(".")),
                ("±", self.toggle_sign),
                ("Ans", self.add_answer),
                ("=", self.calculate, self.equal_color),
                ("AC", self.clear, self.danger_color),
            ]
        ]

        for row_index, row in enumerate(buttons):

            grid.rowconfigure(
                row_index,
                weight=1
            )

            for col_index in range(6):

                grid.columnconfigure(
                    col_index,
                    weight=1
                )

            for col_index, item in enumerate(row):

                text = item[0]

                command = item[1]

                color = (
                    item[2]
                    if len(item) > 2
                    else self.number_color
                )

                button = self.create_button(
                    grid,
                    text,
                    command,
                    color
                )

                button.grid(
                    row=row_index,
                    column=col_index,
                    sticky="nsew",
                    padx=3,
                    pady=3
                )

    # ========================================================
    # HISTORY
    # ========================================================

    def create_history_panel(self):

        panel = tk.Frame(
            self.root,
            bg="#10182b",
            width=260
        )

        panel.pack(
            side="right",
            fill="y",
            padx=(0, 18),
            pady=10
        )

        title = tk.Label(
            panel,
            text="HISTORY",
            bg="#10182b",
            fg="#00eaff",
            font=(
                "Arial",
                15,
                "bold"
            )
        )

        title.pack(
            pady=10
        )

        self.history_list = tk.Listbox(
            panel,
            bg="#0b1020",
            fg="white",
            selectbackground="#3949ab",
            selectforeground="white",
            font=(
                "Consolas",
                10
            ),
            width=30,
            height=25,
            relief="flat"
        )

        self.history_list.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=5
        )

        clear_history = tk.Button(
            panel,
            text="Clear History",
            command=self.clear_history,
            bg=self.danger_color,
            fg="white",
            activebackground="#ef5350",
            activeforeground="white",
            relief="flat",
            font=(
                "Arial",
                10,
                "bold"
            ),
            cursor="hand2"
        )

        clear_history.pack(
            fill="x",
            padx=8,
            pady=8
        )

    # ========================================================
    # BUTTON CREATION
    # ========================================================

    def create_button(
        self,
        parent,
        text,
        command,
        color,
        width=5
    ):

        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg="white",
            activebackground=self.hover_color,
            activeforeground="white",
            font=(
                "Arial",
                11,
                "bold"
            ),
            relief="flat",
            bd=0,
            width=width,
            cursor="hand2"
        )

        button.bind(
            "<Enter>",
            lambda event:
            button.config(
                bg=self.hover_color
            )
        )

        button.bind(
            "<Leave>",
            lambda event:
            button.config(
                bg=color
            )
        )

        return button

    # ========================================================
    # DISPLAY
    # ========================================================

    def update_display(self):

        text = (
            self.expression
            if self.expression
            else "0"
        )

        self.display.config(
            text=text
        )

    # ========================================================
    # INPUT
    # ========================================================

    def add_text(
        self,
        text
    ):

        if self.just_calculated:

            if text in "+-*/":

                self.expression = (
                    self.result + text
                )

            else:

                self.expression = text

            self.just_calculated = False

        else:

            self.expression += text

        self.update_display()

    def add_function(
        self,
        function
    ):

        if self.just_calculated:

            self.expression = ""

            self.just_calculated = False

        self.expression += (
            function + "("
        )

        self.update_display()

    # ========================================================
    # SPECIAL OPERATIONS
    # ========================================================

    def square(self):

        if self.expression:

            self.expression += "**2"

            self.update_display()

    def inverse(self):

        if self.expression:

            self.expression = (
                "1/("
                + self.expression
                + ")"
            )

            self.update_display()

    def factorial(self):

        if self.expression:

            self.expression += "!"

            self.update_display()

    def toggle_sign(self):

        if not self.expression:
            return

        self.expression = (
            "-("
            + self.expression
            + ")"
        )

        self.update_display()

    def add_answer(self):

        if self.result:

            self.expression += (
                self.result
            )

            self.update_display()

    # ========================================================
    # CLEAR / BACKSPACE
    # ========================================================

    def clear(self):

        self.expression = ""

        self.result = ""

        self.just_calculated = False

        self.display.config(
            text="0"
        )

        self.result_label.config(
            text=""
        )

    def backspace(self):

        if self.expression:

            self.expression = (
                self.expression[:-1]
            )

            self.update_display()

    # ========================================================
    # ANGLE MODE
    # ========================================================

    def change_angle_mode(self):

        modes = [
            "DEG",
            "RAD",
            "GRAD"
        ]

        index = modes.index(
            self.angle_mode
        )

        self.angle_mode = modes[
            (index + 1) % len(modes)
        ]

        self.mode_button.config(
            text=self.angle_mode
        )

    # ========================================================
    # MEMORY
    # ========================================================

    def get_current_value(self):

        try:

            return self.evaluate(
                self.expression
            )

        except Exception:

            return 0

    def memory_clear(self):

        self.memory = 0

    def memory_recall(self):

        self.expression += str(
            self.memory
        )

        self.update_display()

    def memory_add(self):

        self.memory += (
            self.get_current_value()
        )

    def memory_subtract(self):

        self.memory -= (
            self.get_current_value()
        )

    def memory_store(self):

        self.memory = (
            self.get_current_value()
        )

    # ========================================================
    # CALCULATOR ENGINE
    # ========================================================

    def evaluate(
        self,
        expression
    ):

        expression = expression.replace(
            "×",
            "*"
        )

        expression = expression.replace(
            "÷",
            "/"
        )

        expression = expression.replace(
            "−",
            "-"
        )

        expression = expression.replace(
            "π",
            "pi"
        )

        # ----------------------------------------------------
        # FACTORIAL
        # ----------------------------------------------------

        factorial_pattern = (
            r"(\d+(?:\.\d+)?)!"
        )

        while re.search(
            factorial_pattern,
            expression
        ):

            match = re.search(
                factorial_pattern,
                expression
            )

            number = float(
                match.group(1)
            )

            if number < 0:
                raise ValueError(
                    "Invalid factorial"
                )

            value = math.factorial(
                int(number)
            )

            expression = (
                expression[:match.start()]
                + str(value)
                + expression[match.end():]
            )

        # ----------------------------------------------------
        # ANGLE FUNCTIONS
        # ----------------------------------------------------

        def sin_func(x):

            if self.angle_mode == "DEG":

                x = math.radians(x)

            elif self.angle_mode == "GRAD":

                x = x * math.pi / 200

            return math.sin(x)

        def cos_func(x):

            if self.angle_mode == "DEG":

                x = math.radians(x)

            elif self.angle_mode == "GRAD":

                x = x * math.pi / 200

            return math.cos(x)

        def tan_func(x):

            if self.angle_mode == "DEG":

                x = math.radians(x)

            elif self.angle_mode == "GRAD":

                x = x * math.pi / 200

            return math.tan(x)

        def asin_func(x):

            value = math.asin(x)

            if self.angle_mode == "DEG":

                return math.degrees(value)

            if self.angle_mode == "GRAD":

                return value * 200 / math.pi

            return value

        def acos_func(x):

            value = math.acos(x)

            if self.angle_mode == "DEG":

                return math.degrees(value)

            if self.angle_mode == "GRAD":

                return value * 200 / math.pi

            return value

        def atan_func(x):

            value = math.atan(x)

            if self.angle_mode == "DEG":

                return math.degrees(value)

            if self.angle_mode == "GRAD":

                return value * 200 / math.pi

            return value

        allowed = {

            "sin": sin_func,
            "cos": cos_func,
            "tan": tan_func,

            "asin": asin_func,
            "acos": acos_func,
            "atan": atan_func,

            "sinh": math.sinh,
            "cosh": math.cosh,
            "tanh": math.tanh,

            "ln": math.log,
            "log": math.log10,

            "sqrt": math.sqrt,

            "abs": abs,

            "floor": math.floor,
            "ceil": math.ceil,
            "round": round,

            "pi": math.pi,
            "e": math.e,

            "pow": pow
        }

        # ----------------------------------------------------
        # SAFE EVALUATION
        # ----------------------------------------------------

        code = compile(
            expression,
            "<calculator>",
            "eval"
        )

        for name in code.co_names:

            if name not in allowed:

                raise ValueError(
                    f"Unknown function: {name}"
                )

        return eval(
            code,
            {
                "__builtins__":
                {}
            },
            allowed
        )

    # ========================================================
    # CALCULATE
    # ========================================================

    def calculate(self):

        if not self.expression:

            return

        try:

            value = self.evaluate(
                self.expression
            )

            if isinstance(
                value,
                float
            ):

                if value.is_integer():

                    value = int(
                        value
                    )

                else:

                    value = round(
                        value,
                        12
                    )

            self.result = str(
                value
            )

            history_text = (
                f"{self.expression} = "
                f"{self.result}"
            )

            self.history.insert(
                0,
                history_text
            )

            self.history_list.insert(
                0,
                history_text
            )

            self.result_label.config(
                text="= " + self.result
            )

            self.expression = self.result

            self.just_calculated = True

            self.update_display()

        except ZeroDivisionError:

            self.show_error(
                "Division by zero"
            )

        except Exception as error:

            self.show_error(
                "Invalid expression"
            )

    # ========================================================
    # ERROR
    # ========================================================

    def show_error(
        self,
        message
    ):

        self.result_label.config(
            text="⚠ " + message,
            fg="#ff5252"
        )

        self.root.after(
            1500,
            lambda:
            self.result_label.config(
                fg="#00eaff"
            )
        )

    # ========================================================
    # HISTORY
    # ========================================================

    def clear_history(self):

        self.history.clear()

        self.history_list.delete(
            0,
            tk.END
        )

    # ========================================================
    # KEYBOARD
    # ========================================================

    def bind_keyboard(self):

        self.root.bind(
            "<Key>",
            self.keyboard_input
        )

    def keyboard_input(
        self,
        event
    ):

        key = event.keysym

        char = event.char

        if char in "0123456789":

            self.add_text(
                char
            )

        elif char in "+-*/().":

            self.add_text(
                char
            )

        elif key == "Return":

            self.calculate()

        elif key == "BackSpace":

            self.backspace()

        elif key == "Escape":

            self.clear()

        elif char == "^":

            self.add_text(
                "**"
            )


# ============================================================
# MAIN
# ============================================================

def main():

    root = tk.Tk()

    app = ScientificCalculator(
        root
    )

    root.mainloop()


if __name__ == "__main__":

    main()