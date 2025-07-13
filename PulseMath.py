import customtkinter as ctk
import tkinter as tk
from math import sqrt
import pygame
import matplotlib.pyplot as plt

class PulseMathCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("PulseMath | Powered by Y7X 💗")
        self.root.geometry("720x860")
        self.root.resizable(False, False)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        pygame.mixer.init()
        self.click_sound_path = "/System/Library/Sounds/Pop.aiff"

        self.current_input = "0"
        self.previous_input = ""
        self.operation = None
        self.reset_input = False
        self.history = []

        self.build_layout()

    def build_layout(self):
        self.main_frame = ctk.CTkFrame(self.root, fg_color="#000000")  # AMOLED
        self.main_frame.pack(fill="both", expand=True)

        self.display_and_buttons_frame = ctk.CTkFrame(self.main_frame, fg_color="#000000")
        self.display_and_buttons_frame.pack(side="top", fill="both", expand=True, padx=10, pady=(10, 5))

        self.sidebar_frame = ctk.CTkFrame(self.main_frame, fg_color="#000000")
        self.sidebar_frame.pack(side="top", fill="x", padx=10, pady=(5, 10))

        self.footer_label = ctk.CTkLabel(
            self.main_frame,
            text="🎯 PulseMath — Powered by Y7X 💗",
            font=("Poppins", 14, "bold"),
            text_color="#ff0000"
        )
        self.footer_label.pack(pady=(0, 10))

        self.build_display()
        self.build_buttons()
        self.build_sidebar()

    def build_display(self):
        self.display_var = ctk.StringVar()
        self.display_var.set(self.current_input)

        self.display = ctk.CTkEntry(
            self.display_and_buttons_frame,
            textvariable=self.display_var,
            font=("Poppins", 28),
            justify="right",
            height=60,
            corner_radius=15,
            fg_color="#000000",
            text_color="#ff0000"
        )
        self.display.pack(pady=20, padx=10, fill="x")

    def play_click(self):
        try:
            pygame.mixer.music.load(self.click_sound_path)
            pygame.mixer.music.play()
        except:
            pass

    def build_buttons(self):
        button_frame = ctk.CTkFrame(self.display_and_buttons_frame, fg_color="transparent")
        button_frame.pack(expand=True, fill="both", padx=10, pady=10)

        buttons = [
            ["%", "CE", "C", "÷"],
            ["1/x", "x²", "√", "×"],
            ["7", "8", "9", "-"],
            ["4", "5", "6", "+"],
            ["1", "2", "3", "="],
            ["±", "0", ".", "💥"]
        ]

        for r, row in enumerate(buttons):
            for c, label in enumerate(row):
                btn = ctk.CTkButton(
                    button_frame,
                    text=label,
                    font=("Poppins", 20),
                    text_color="#ffffff",
                    fg_color="#000000",
                    border_color="#ff0000",
                    border_width=2,
                    hover_color="#1a1a1a",
                    corner_radius=30,
                    height=60,
                    width=150,
                    command=lambda l=label: self.handle_click(l)
                )
                btn.grid(row=r, column=c, padx=8, pady=8, sticky="nsew")

        for i in range(6):
            button_frame.rowconfigure(i, weight=1)
        for i in range(4):
            button_frame.columnconfigure(i, weight=1)

    def handle_click(self, label):
        self.play_click()
        actions = {
            "C": self.clear_all,
            "CE": self.clear_entry,
            "±": self.toggle_sign,
            "%": self.percent,
            "1/x": self.reciprocal,
            "x²": self.square,
            "√": self.square_root,
            "=": self.calculate,
            "+": lambda: self.set_operation("+"),
            "-": lambda: self.set_operation("-"),
            "×": lambda: self.set_operation("*"),
            "÷": lambda: self.set_operation("/"),
            ".": lambda: self.add_digit("."),
            "💥": lambda: self.display_var.set("💥 Boom!")
        }
        actions.get(label, lambda: self.add_digit(label))()

    def add_digit(self, digit):
        if self.reset_input:
            self.current_input = "0"
            self.reset_input = False

        if digit == "." and "." in self.current_input:
            return

        if self.current_input == "0" and digit != ".":
            self.current_input = digit
        else:
            self.current_input += digit

        self.display_var.set(self.current_input)

    def clear_entry(self):
        self.current_input = "0"
        self.display_var.set(self.current_input)

    def clear_all(self):
        self.current_input = "0"
        self.previous_input = ""
        self.operation = None
        self.display_var.set(self.current_input)

    def toggle_sign(self):
        if self.current_input != "0":
            if self.current_input.startswith("-"):
                self.current_input = self.current_input[1:]
            else:
                self.current_input = "-" + self.current_input
            self.display_var.set(self.current_input)

    def percent(self):
        try:
            value = float(self.current_input) / 100
            self.current_input = str(value)
            self.display_var.set(self.current_input)
        except:
            self.display_var.set("Error")
            self.current_input = "0"

    def reciprocal(self):
        try:
            value = 1 / float(self.current_input)
            self.current_input = str(value)
            self.display_var.set(self.current_input)
        except:
            self.display_var.set("Error")
            self.current_input = "0"

    def square(self):
        try:
            value = float(self.current_input) ** 2
            self.current_input = str(value)
            self.display_var.set(self.current_input)
        except:
            self.display_var.set("Error")
            self.current_input = "0"

    def square_root(self):
        try:
            value = sqrt(float(self.current_input))
            self.current_input = str(value)
            self.display_var.set(self.current_input)
        except:
            self.display_var.set("Error")
            self.current_input = "0"

    def set_operation(self, op):
        if self.operation and not self.reset_input:
            self.calculate()

        self.previous_input = self.current_input
        self.operation = op
        self.reset_input = True

    def calculate(self):
        if not self.operation:
            return

        try:
            a = float(self.previous_input)
            b = float(self.current_input)

            if self.operation == "+":
                result = a + b
            elif self.operation == "-":
                result = a - b
            elif self.operation == "*":
                result = a * b
            elif self.operation == "/":
                result = a / b

            full_expr = f"{self.previous_input} {self.operation} {self.current_input} = {result}"
            self.history.append(full_expr)

            self.current_input = str(result)
            self.display_var.set(self.current_input)
            self.operation = None
            self.reset_input = True
        except:
            self.display_var.set("Error")
            self.current_input = "0"
            self.operation = None

    def build_sidebar(self):
        title_label = ctk.CTkLabel(self.sidebar_frame, text="🔧 Tools", font=("Poppins", 18, "bold"), text_color="#ff0000")
        title_label.pack(pady=(10, 0))

        btn_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=10)

        btns = [
            ("📜 History", self.show_history),
            ("📁 Export", self.export_history),
            ("📊 Graph", self.plot_expression),
            ("🤖 Explain", self.explain_result),
        ]

        for i, (label, cmd) in enumerate(btns):
            btn = ctk.CTkButton(
                btn_frame,
                text=label,
                command=cmd,
                corner_radius=12,
                height=45,
                width=160,
                text_color="#ffffff",
                fg_color="#000000",
                border_color="#ff0000",
                border_width=2,
                hover_color="#1c1c1c"
            )
            btn.grid(row=0, column=i, padx=10, pady=5, sticky="nsew")

        for i in range(len(btns)):
            btn_frame.columnconfigure(i, weight=1)

    def show_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("📜 Calculation History")
        history_text = tk.Text(history_window, wrap="word", font=("Poppins", 12))
        history_text.pack(expand=True, fill="both")
        history_text.insert("1.0", "\n".join(self.history))
        history_text.configure(state="disabled")

    def export_history(self):
        with open("calculation_history.txt", "w") as f:
            f.write("\n".join(self.history))
        self.display_var.set("📁 Exported")

    def plot_expression(self):
        try:
            expr = self.display_var.get().replace("^", "**").replace("x", "*x")
            x = [i for i in range(-10, 11)]
            y = [eval(expr.replace("x", str(i))) for i in x]
            plt.plot(x, y, marker='o')
            plt.title("Graph of: " + self.display_var.get())
            plt.grid(True)
            plt.show()
        except:
            self.display_var.set("\u26a0\ufe0f Invalid Expr")

    def explain_result(self):
        try:
            last_expr = self.history[-1] if self.history else ""
            if not last_expr:
                self.display_var.set("No calc yet")
                return

            parts = last_expr.split()
            if len(parts) >= 3:
                a, op, b = parts[0], parts[1], parts[2]
                explanation = f"{a} {op} {b} means:\n"

                match op:
                    case "+":
                        explanation += f"Add {a} and {b}"
                    case "-":
                        explanation += f"Subtract {b} from {a}"
                    case "*":
                        explanation += f"Multiply {a} by {b}"
                    case "/":
                        explanation += f"Divide {a} by {b}"
                    case _:
                        explanation += "Operation not recognized"

                self.display_var.set(explanation)
            else:
                self.display_var.set("Can't explain")
        except:
            self.display_var.set("❌ Error")

if __name__ == "__main__":
    root = ctk.CTk()
    app = PulseMathCalculator(root)
    root.mainloop()
