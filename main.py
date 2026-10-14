
import tkinter as tk
import sympy as sp
import threading
import base64
import subprocess
from openai import OpenAI

# =========================================================
# MAIN WINDOW
# =========================================================

root = tk.Tk()
root.title("AI Engineering Calculator")
root.geometry("320x480")
root.configure(bg="#151515")

content = tk.Frame(root, bg="#151515")
content.pack(fill="both", expand=True)

expression = tk.StringVar()
angle_mode = tk.StringVar(value="DEG")

client = OpenAI()

# =========================================================
# GENERAL
# =========================================================

def clear_screen():
    for widget in content.winfo_children():
        widget.destroy()


def make_home_button(text, command):
    button = tk.Button(
        content,
        text=text,
        command=command,
        font=("Arial", 14, "bold"),
        width=16,
        height=1
    )
    button.pack(pady=6)


# =========================================================
# HOME
# =========================================================

def show_home():
    clear_screen()

    tk.Label(
        content,
        text="AI ENGINEERING\nCALCULATOR",
        font=("Arial", 20, "bold"),
        fg="white",
        bg="#151515"
    ).pack(pady=(20, 8))

    tk.Label(
        content,
        text="SELECT MODE",
        font=("Arial", 11),
        fg="gray",
        bg="#151515"
    ).pack(pady=(0, 10))

    make_home_button("CALC", show_calc)
    make_home_button("AI", show_ai)
    make_home_button("CAMERA", show_camera)
    make_home_button("ENGINEERING", show_engineering)


# =========================================================
# CALCULATOR
# =========================================================

def insert_value(value):
    expression.set(expression.get() + value)


def clear_calc():
    expression.set("")


def backspace():
    expression.set(expression.get()[:-1])


def toggle_angle():
    if angle_mode.get() == "DEG":
        angle_mode.set("RAD")
    else:
        angle_mode.set("DEG")

    show_calc()


def calculate():
    try:
        text = expression.get()

        text = text.replace("^", "**")
        text = text.replace("×", "*")
        text = text.replace("÷", "/")

        if angle_mode.get() == "DEG":

            def sin_func(x):
                return sp.sin(sp.pi * x / 180)

            def cos_func(x):
                return sp.cos(sp.pi * x / 180)

            def tan_func(x):
                return sp.tan(sp.pi * x / 180)

        else:
            sin_func = sp.sin
            cos_func = sp.cos
            tan_func = sp.tan

        functions = {
            "sin": sin_func,
            "cos": cos_func,
            "tan": tan_func,
            "sqrt": sp.sqrt,
            "log": lambda x: sp.log(x, 10),
            "ln": sp.log,
            "pi": sp.pi,
            "e": sp.E
        }

        result = sp.sympify(text, locals=functions)

        if result.is_number:
            result = sp.N(result, 12)

        expression.set(str(result))

    except Exception:
        expression.set("ERROR")


def show_calc():
    clear_screen()

    top = tk.Frame(content, bg="#151515")
    top.pack(fill="x", padx=10, pady=10)

    tk.Button(
        top,
        text="HOME",
        command=show_home,
        font=("Arial", 11, "bold")
    ).pack(side="left")

    tk.Label(
        top,
        text="CALC",
        font=("Arial", 18, "bold"),
        fg="white",
        bg="#151515"
    ).pack(side="left", padx=30)

    tk.Button(
        top,
        text=angle_mode.get(),
        command=toggle_angle,
        font=("Arial", 11, "bold")
    ).pack(side="right")

    tk.Entry(
        content,
        textvariable=expression,
        font=("Arial", 18),
        justify="right",
        bd=5
    ).pack(
        fill="x",
        padx=15,
        pady=(5, 8),
        ipady=7
    )

    keypad = tk.Frame(content, bg="#151515")
    keypad.pack()

    buttons = [
        ("sin(", 0, 0),
        ("cos(", 0, 1),
        ("tan(", 0, 2),
        ("⌫", 0, 3),

        ("log(", 1, 0),
        ("ln(", 1, 1),
        ("sqrt(", 1, 2),
        ("C", 1, 3),

        ("(", 2, 0),
        (")", 2, 1),
        ("^", 2, 2),
        ("÷", 2, 3),

        ("7", 3, 0),
        ("8", 3, 1),
        ("9", 3, 2),
        ("×", 3, 3),

        ("4", 4, 0),
        ("5", 4, 1),
        ("6", 4, 2),
        ("-", 4, 3),

        ("1", 5, 0),
        ("2", 5, 1),
        ("3", 5, 2),
        ("+", 5, 3),

        ("pi", 6, 0),
        ("0", 6, 1),
        (".", 6, 2),
        ("=", 6, 3)
    ]

    for text, row, column in buttons:

        if text == "=":
            command = calculate

        elif text == "C":
            command = clear_calc

        elif text == "⌫":
            command = backspace

        else:
            command = lambda value=text: insert_value(value)

        tk.Button(
            keypad,
            text=text,
            command=command,
            font=("Arial", 11, "bold"),
            width=5,
            height=1
        ).grid(
            row=row,
            column=column,
            padx=2,
            pady=2
        )


# =========================================================
# ENGINEERING FORMULA DATA
# =========================================================

engineering_data = {

    "CIRCUITS": """
OHM'S LAW

V = I R
I = V / R
R = V / I


POWER

P = V I
P = I² R
P = V² / R


VOLTAGE DIVIDER

Vout = Vin(R2 / (R1 + R2))


CURRENT DIVIDER

I1 = Itotal(R2 / (R1 + R2))


CAPACITOR

Q = C V

Zc = 1 / (jωC)

Xc = 1 / (2πfC)


INDUCTOR

V = L(di/dt)

Zl = jωL

Xl = 2πfL


RC TIME CONSTANT

τ = R C


RL TIME CONSTANT

τ = L / R


RC CUTOFF FREQUENCY

fc = 1 / (2πRC)


RLC RESONANCE

f0 = 1 / (2π√LC)
""",

    "ELECTRONICS": """
IDEAL OP-AMP

V+ ≈ V-

Input current ≈ 0


INVERTING AMPLIFIER

Av = -Rf / Rin


NON-INVERTING AMPLIFIER

Av = 1 + (Rf / R1)


VOLTAGE FOLLOWER

Av = 1


BJT

Ic ≈ β Ib

Ie = Ic + Ib

VBE ≈ 0.7 V
for silicon transistor


MOSFET

Cutoff:
VGS < VTH

Triode:
VGS > VTH
VDS < VGS - VTH

Saturation:
VGS > VTH
VDS ≥ VGS - VTH
""",

    "SIGNALS": """
ANGULAR FREQUENCY

ω = 2πf


PERIOD

T = 1 / f


SINUSOID

x(t) = A cos(ωt + φ)


EULER'S FORMULA

e^(jθ) = cos(θ) + j sin(θ)


COMPLEX EXPONENTIAL

cos(θ) = (e^(jθ) + e^(-jθ)) / 2


ENERGY SIGNAL

E = ∫ |x(t)|² dt


AVERAGE POWER

P = lim
T→∞

1/(2T) ∫ |x(t)|² dt
""",

    "ELECTROMAGNETICS": """
COULOMB'S LAW

F = (1 / 4πε) (q1q2 / r²)


ELECTRIC FIELD

E = F / q


ELECTRIC POTENTIAL

V = -∫ E · dl


CAPACITANCE

C = Q / V


GAUSS'S LAW

∮ D · dS = Qenc


ELECTRIC FLUX DENSITY

D = εE


MAGNETIC FLUX

Φ = ∫ B · dS


FARADAY'S LAW

V = -dΦ/dt


WAVE SPEED

v = 1 / √(με)
""",

    "RF / ANTENNAS": """
WAVELENGTH

λ = v / f


FREE SPACE

λ = c / f

c ≈ 3 × 10⁸ m/s


WAVENUMBER

β = 2π / λ


FREE-SPACE IMPEDANCE

η0 ≈ 377 Ω


POWER IN DECIBELS

dB = 10 log10(P2 / P1)


VOLTAGE IN DECIBELS

dB = 20 log10(V2 / V1)


HALF-WAVE DIPOLE

L ≈ λ / 2


QUARTER-WAVE ANTENNA

L ≈ λ / 4
""",

    "PROBABILITY": """
COMPLEMENT

P(Aᶜ) = 1 - P(A)


CONDITIONAL PROBABILITY

P(A|B) = P(A ∩ B) / P(B)


MULTIPLICATION RULE

P(A ∩ B)
= P(A|B)P(B)


BAYES' THEOREM

P(A|B)
=
P(B|A)P(A) / P(B)


INDEPENDENT EVENTS

P(A ∩ B)
=
P(A)P(B)


BERNOULLI / BINOMIAL

P(X = k)
=
C(n,k)p^k(1-p)^(n-k)


EXPECTED VALUE

E[X] = Σ xP(X=x)


VARIANCE

Var(X)
=
E[X²] - (E[X])²
""",

    "CONSTANTS": """
SPEED OF LIGHT

c = 299,792,458 m/s


ELECTRON CHARGE

q = 1.602 × 10⁻¹⁹ C


VACUUM PERMITTIVITY

ε0 = 8.854 × 10⁻¹² F/m


VACUUM PERMEABILITY

μ0 ≈ 1.257 × 10⁻⁶ H/m


FREE-SPACE IMPEDANCE

η0 ≈ 376.73 Ω


BOLTZMANN CONSTANT

k = 1.381 × 10⁻²³ J/K


PLANCK CONSTANT

h = 6.626 × 10⁻³⁴ J·s
"""
}


# =========================================================
# ENGINEERING MODE
# =========================================================

def show_engineering():
    clear_screen()

    top = tk.Frame(content, bg="#151515")
    top.pack(fill="x", padx=10, pady=10)

    tk.Button(
        top,
        text="HOME",
        command=show_home,
        font=("Arial", 11, "bold")
    ).pack(side="left")

    tk.Label(
        top,
        text="ENGINEERING",
        font=("Arial", 16, "bold"),
        fg="white",
        bg="#151515"
    ).pack(side="left", padx=15)

    tk.Label(
        content,
        text="FORMULA LIBRARY",
        font=("Arial", 11),
        fg="gray",
        bg="#151515"
    ).pack(pady=(5, 8))

    categories = [
        "CIRCUITS",
        "ELECTRONICS",
        "SIGNALS",
        "ELECTROMAGNETICS",
        "RF / ANTENNAS",
        "PROBABILITY",
        "CONSTANTS"
    ]

    for category in categories:
        tk.Button(
            content,
            text=category,
            command=lambda c=category: show_formula_sheet(c),
            font=("Arial", 11, "bold"),
            width=20,
            height=1
        ).pack(pady=3)


def show_formula_sheet(category):
    clear_screen()

    top = tk.Frame(content, bg="#151515")
    top.pack(fill="x", padx=10, pady=10)

    tk.Button(
        top,
        text="← BACK",
        command=show_engineering,
        font=("Arial", 11, "bold")
    ).pack(side="left")

    tk.Label(
        top,
        text=category,
        font=("Arial", 16, "bold"),
        fg="white",
        bg="#151515"
    ).pack(side="left", padx=20)

    formula_frame = tk.Frame(content)
    formula_frame.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    scrollbar = tk.Scrollbar(formula_frame)
    scrollbar.pack(side="right", fill="y")

    text_box = tk.Text(
        formula_frame,
        font=("Arial", 15),
        wrap="word",
        bg="#eeeeee",
        fg="black",
        padx=15,
        pady=15,
        yscrollcommand=scrollbar.set
    )

    text_box.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.config(command=text_box.yview)

    text_box.insert("1.0", engineering_data[category])

    text_box.config(state="disabled")


# =========================================================
# AI / CAMERA PLACEHOLDERS
# =========================================================

def show_basic_mode(title, message):
    clear_screen()

    tk.Label(
        content,
        text=title,
        font=("Arial", 26, "bold"),
        fg="white",
        bg="#151515"
    ).pack(pady=(80, 30))

    tk.Label(
        content,
        text=message,
        font=("Arial", 16),
        fg="white",
        bg="#151515",
        wraplength=400
    ).pack(pady=20)

    tk.Button(
        content,
        text="← BACK",
        command=show_home,
        font=("Arial", 16, "bold"),
        width=12,
        height=2
    ).pack(pady=50)


def show_ai():
    show_basic_mode(
        "AI MODE",
        "Wi-Fi AI assistant coming soon."
    )


def show_camera():
    clear_screen()

    top = tk.Frame(content, bg="#151515")
    top.pack(fill="x", padx=10, pady=10)

    tk.Button(
        top,
        text="HOME",
        command=show_home,
        font=("Arial", 11, "bold")
    ).pack(side="left")

    tk.Label(
        top,
        text="CAMERA MODE",
        font=("Arial", 16, "bold"),
        fg="white",
        bg="#151515"
    ).pack(side="left", padx=15)

    tk.Label(
        content,
        text="Point camera at the problem",
        font=("Arial", 11),
        fg="white",
        bg="#151515"
    ).pack(pady=6)

    answer_box = tk.Text(
        content,
        font=("Arial", 11),
        height=13,
        wrap="word",
        padx=6,
        pady=5
    )

    answer_box.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=4
    )

    def scan_problem():

        scan_button.config(
            state="disabled",
            text="CAPTURING..."
        )

        answer_box.delete("1.0", "end")
        answer_box.insert("1.0", "Taking picture...")

        def camera_worker():

            try:

                image_path = (
                    "/home/n_kevin123/AI_Calculator/"
                    "camera_capture.jpg"
                )

                subprocess.run(
                    [
                        "rpicam-still",
                        "-n",
                        "--timeout",
                        "1000",
                        "-o",
                        image_path
                    ],
                    check=True
                )

                answer_box.after(
                    0,
                    lambda: (
                        answer_box.delete("1.0", "end"),
                        answer_box.insert(
                            "1.0",
                            "Reading problem..."
                        )
                    )
                )

                with open(image_path, "rb") as image_file:

                    image_data = base64.b64encode(
                        image_file.read()
                    ).decode("utf-8")

                camera_prompt = """
You are an engineering calculator tutor.

Carefully read the problem in the image.

Solve the problem using PLAIN TEXT ONLY.

Never use Markdown or LaTeX.
Never use # headings.
Never use backslash math commands.

Use normal engineering symbols:
π
Ω
µ
×
÷
√

For numerical problems, use this exact style:

Given:
List known values and units.

Formula:
Write the formula.

Convert:
Show unit conversions if necessary.

Substitute:
Insert the numbers.

Solve:
Show the important calculation.

Answer:
Give the final answer with units.

Keep everything short and easy to read.

If any part of the image cannot be read clearly,
say what is unclear instead of guessing.
"""

                response = client.responses.create(
                    model="gpt-6-astra",
                    input=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "input_text",
                                    "text": camera_prompt
                                },
                                {
                                    "type": "input_image",
                                    "image_url":
                                        "data:image/jpeg;base64,"
                                        + image_data,
                                    "detail": "high"
                                }
                            ]
                        }
                    ]
                )

                answer = response.output_text

            except Exception as error:

                answer = (
                    "CAMERA ERROR:\n\n"
                    + str(error)
                )

            def update_camera_screen():

                answer_box.delete("1.0", "end")
                answer_box.insert("1.0", answer)

                scan_button.config(
                    state="normal",
                    text="TAKE PHOTO & SOLVE"
                )

            root.after(
                0,
                update_camera_screen
            )

        threading.Thread(
            target=camera_worker,
            daemon=True
        ).start()

    scan_button = tk.Button(
        content,
        text="TAKE PHOTO & SOLVE",
        command=scan_problem,
        font=("Arial", 12, "bold"),
        height=1
    )

    scan_button.pack(
        fill="x",
        padx=10,
        pady=6
    )

def show_ai():
    clear_screen()

    top = tk.Frame(content, bg="#151515")
    top.pack(fill="x", padx=10, pady=10)

    tk.Button(
        top,
        text="HOME",
        command=show_home,
        font=("Arial", 11, "bold")
    ).pack(side="left")

    tk.Label(
        top,
        text="AI MODE",
        font=("Arial", 16, "bold"),
        fg="white",
        bg="#151515"
    ).pack(side="left", padx=22)

    tk.Label(
        content,
        text="ASK AI",
        font=("Arial", 11),
        fg="gray",
        bg="#151515"
    ).pack(pady=(3, 2))

    question_box = tk.Text(
        content,
        font=("Arial", 12),
        height=3,
        wrap="word",
        padx=6,
        pady=5
    )

    question_box.pack(
        fill="x",
        padx=10,
        pady=4
    )

    tk.Label(
        content,
        text="RESPONSE",
        font=("Arial", 10, "bold"),
        fg="white",
        bg="#151515"
    ).pack(pady=(3, 2))

    answer_box = tk.Text(
        content,
        font=("Arial", 11),
        height=8,
        wrap="word",
        padx=6,
        pady=5
    )

    answer_box.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=3
    )

    def ask_ai():

        question = question_box.get(
            "1.0",
            "end"
        ).strip()

        if not question:
            return

        answer_box.delete("1.0", "end")
        answer_box.insert("1.0", "Thinking...")

        ask_button.config(
            state="disabled",
            text="THINKING..."
        )


        def worker():

            try:

                prompt = rf"""
You are an engineering calculator tutor.

IMPORTANT:
Your response is displayed on a small calculator screen.

USE PLAIN TEXT ONLY.

Never use Markdown or LaTeX.
Never use # headings.
Never use **bold**.
Never use \frac, \text, \(, \), \[, or \].

Use normal engineering symbols:
π
Ω
µ
×
÷
√

For numerical problems, use this format:

Given:
List the known values and units.

Formula:
Write the formula in normal calculator notation.

Convert:
Show unit conversions if needed.

Substitute:
Insert the numbers into the formula.

Solve:
Show the important calculation.

Answer:
Give the final answer with units.

Keep everything short and easy to read.
Do not use long paragraphs.

Question:
{question}
"""

                response = client.responses.create(
                    model="gpt-6-astra",
                    input=prompt
                )

                answer = response.output_text

            except Exception as error:
                answer = "AI ERROR:\n\n" + str(error)

            def update():

                answer_box.delete("1.0", "end")
                answer_box.insert("1.0", answer)

                ask_button.config(
                    state="normal",
                    text="ASK AI"
                )

            root.after(0, update)

        threading.Thread(
            target=worker,
            daemon=True
        ).start()

    ask_button = tk.Button(
        content,
        text="ASK AI",
        command=ask_ai,
        font=("Arial", 12, "bold"),
        height=1
    )

    ask_button.pack(
        fill="x",
        padx=10,
        pady=4
    )

    def clear_ai():

        question_box.delete("1.0", "end")
        answer_box.delete("1.0", "end")

    tk.Button(
        content,
        text="CLEAR",
        command=clear_ai,
        font=("Arial", 10, "bold")
    ).pack(pady=3)

# =========================================================
# START
# =========================================================

show_home()

root.mainloop()
