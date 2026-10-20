
import tkinter as tk
import sympy as sp
import threading
import base64
import subprocess
import queue
import time
import serial
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

active_scroll_widget = None

client = OpenAI()


def friendly_error(error, source="ai"):
    """Turn technical Python/API errors into simple user messages."""

    error_text = str(error).lower()
    error_type = type(error).__name__.lower()

    # Physical camera capture problem
    if source == "camera":
        return (
            "Camera unavailable.\n\n"
            "Check the camera connection and try again."
        )

    # API key / authentication problem
    if (
        "authentication" in error_type
        or "api key" in error_text
        or "incorrect api key" in error_text
        or "401" in error_text
    ):
        return (
            "API key problem.\n\n"
            "Check your OpenAI API key."
        )

    # Internet / connection problem
    if (
        "connection" in error_type
        or "connection" in error_text
        or "network" in error_text
        or "dns" in error_text
        or "timed out" in error_text
        or "timeout" in error_text
    ):
        return (
            "No internet connection.\n\n"
            "Check Wi-Fi and try again."
        )

    # API credit, quota, or rate-limit problem
    if (
        "rate" in error_type
        or "429" in error_text
        or "quota" in error_text
        or "billing" in error_text
        or "insufficient_quota" in error_text
    ):
        return (
            "API limit reached.\n\n"
            "Check your API balance or try again later."
        )

    # Anything unexpected
    return (
        "Something went wrong.\n\n"
        "Please try again."
    )

# =========================================================
# GENERAL
# =========================================================

def clear_screen():
    global active_scroll_widget

    active_scroll_widget = None

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
            value = float(sp.N(result, 12))
            display_result = f"{value:.12g}"
        else:
            display_result = str(result)

        expression.set(display_result)

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

    global active_scroll_widget
    active_scroll_widget = text_box


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

    image_paths = []

    status_label = tk.Label(
        content,
        text="Problem images: 0 / 3",
        font=("Arial", 11, "bold"),
        fg="white",
        bg="#151515"
    )
    status_label.pack(pady=(4, 2))

    tk.Label(
        content,
        text="Take up to 3 photos for one problem",
        font=("Arial", 10),
        fg="white",
        bg="#151515"
    ).pack(pady=(0, 6))

    answer_box = tk.Text(
        content,
        font=("Arial", 11),
        height=11,
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

    global active_scroll_widget
    active_scroll_widget = answer_box

    answer_box.insert(
        "1.0",
        "Use TAKE / ADD PHOTO to capture one problem.\n\n"
        "If the problem continues onto another page or picture, "
        "add the next photo, then press SOLVE ALL PHOTOS."
    )

    button_row = tk.Frame(content, bg="#151515")
    button_row.pack(fill="x", padx=10, pady=(2, 4))

    def update_camera_ui():
        count = len(image_paths)

        status_label.config(
            text=f"Problem images: {count} / 3"
        )

        if count == 0:
            take_button.config(
                text="TAKE / ADD PHOTO",
                state="normal"
            )
            solve_button.config(
                text="SOLVE ALL PHOTOS",
                state="disabled"
            )
            clear_button.config(
                state="disabled"
            )

        elif count < 3:
            take_button.config(
                text="ADD PHOTO",
                state="normal"
            )
            solve_button.config(
                text="SOLVE ALL PHOTOS",
                state="normal"
            )
            clear_button.config(
                state="normal"
            )

        else:
            take_button.config(
                text="MAX 3 PHOTOS",
                state="disabled"
            )
            solve_button.config(
                text="SOLVE ALL PHOTOS",
                state="normal"
            )
            clear_button.config(
                state="normal"
            )

    def take_photo():

        if len(image_paths) >= 3:
            return

        take_button.config(
            state="disabled",
            text="CAPTURING..."
        )
        solve_button.config(state="disabled")
        clear_button.config(state="disabled")

        next_index = len(image_paths) + 1

        answer_box.delete("1.0", "end")
        answer_box.insert(
            "1.0",
            f"Taking photo {next_index}..."
        )

        def capture_worker():

            try:
                image_path = (
                    f"/home/n_kevin123/AI_Calculator/"
                    f"camera_capture_{next_index}.jpg"
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

                def capture_done():
                    image_paths.append(image_path)

                    answer_box.delete("1.0", "end")
                    answer_box.insert(
                        "1.0",
                        f"Captured photo {next_index} successfully.\n\n"
                        "Add another photo if the problem continues,\n"
                        "or press SOLVE ALL PHOTOS."
                    )

                    update_camera_ui()

                root.after(0, capture_done)

            except Exception as error:
                error_message = friendly_error(error, "camera")

                def capture_error():
                    answer_box.delete("1.0", "end")
                    answer_box.insert(
                        "1.0",
                        error_message
                    )
                    update_camera_ui()

                root.after(0, capture_error)

        threading.Thread(
            target=capture_worker,
            daemon=True
        ).start()

    def solve_all_photos():

        if not image_paths:
            return

        take_button.config(state="disabled")
        solve_button.config(
            state="disabled",
            text="SOLVING..."
        )
        clear_button.config(state="disabled")

        answer_box.delete("1.0", "end")
        answer_box.insert(
            "1.0",
            "Reading all photos..."
        )

        def solve_worker():

            try:
                content_items = [
                    {
                        "type": "input_text",
                        "text": """
You are an engineering calculator tutor.

These images belong to ONE continuous engineering or math problem.

IMPORTANT:
- Read the images in the exact order provided.
- The problem may continue from one image to the next.
- Combine all information across the images before solving.
- Do not treat them as separate problems.

USE PLAIN TEXT ONLY.

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

If part of the problem is unclear or missing,
say exactly what is unclear instead of guessing.
"""
                    }
                ]

                for image_path in image_paths:
                    with open(image_path, "rb") as image_file:
                        image_data = base64.b64encode(
                            image_file.read()
                        ).decode("utf-8")

                    content_items.append(
                        {
                            "type": "input_image",
                            "image_url":
                                "data:image/jpeg;base64," + image_data,
                            "detail": "high"
                        }
                    )

                response = client.responses.create(
                    model="gpt-6-astra",
                    input=[
                        {
                            "role": "user",
                            "content": content_items
                        }
                    ]
                )

                answer = response.output_text

            except Exception as error:
                answer = friendly_error(error)

            def solve_done():
                answer_box.delete("1.0", "end")
                answer_box.insert("1.0", answer)
                update_camera_ui()

            root.after(0, solve_done)

        threading.Thread(
            target=solve_worker,
            daemon=True
        ).start()

    def clear_photos():
        image_paths.clear()
        answer_box.delete("1.0", "end")
        answer_box.insert(
            "1.0",
            "Use TAKE / ADD PHOTO to capture one problem.\n\n"
            "If the problem continues onto another page or picture, "
            "add the next photo, then press SOLVE ALL PHOTOS."
        )
        update_camera_ui()

    take_button = tk.Button(
        button_row,
        text="TAKE / ADD PHOTO",
        command=take_photo,
        font=("Arial", 10, "bold"),
        height=1
    )
    take_button.pack(
        side="left",
        expand=True,
        fill="x",
        padx=(0, 4)
    )

    solve_button = tk.Button(
        button_row,
        text="SOLVE ALL PHOTOS",
        command=solve_all_photos,
        font=("Arial", 10, "bold"),
        height=1
    )
    solve_button.pack(
        side="left",
        expand=True,
        fill="x",
        padx=(4, 0)
    )

    clear_button = tk.Button(
        content,
        text="CLEAR PHOTOS",
        command=clear_photos,
        font=("Arial", 10, "bold"),
        height=1
    )
    clear_button.pack(
        fill="x",
        padx=10,
        pady=(0, 6)
    )

    update_camera_ui()

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

    global active_scroll_widget
    active_scroll_widget = answer_box

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
                answer = friendly_error(error)

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
# ESP32 PHYSICAL KEYPAD
# =========================================================

esp32_key_queue = queue.Queue()


def handle_esp32_key(message):
    if message == "KEY:UP":
        if active_scroll_widget is not None:
            active_scroll_widget.yview_scroll(-3, "units")
        return

    if message == "KEY:DOWN":
        if active_scroll_widget is not None:
            active_scroll_widget.yview_scroll(3, "units")
        return

    # Mode / navigation keys
    if message == "KEY:HOME":
        show_home()
        return

    if message == "KEY:AI":
        show_ai()
        return

    if message == "KEY:CAMERA":
        show_camera()
        return

    if message == "KEY:ENG":
        show_engineering()
        return

    # Calculator control keys
    if message == "KEY:ENTER":
        calculate()
        return

    if message == "KEY:CLEAR":
        clear_calc()
        return

    if message == "KEY:BACK":
        backspace()
        return

    if message == "KEY:ANGLE":
        toggle_angle()
        return

    # Calculator entry keys
    key_map = {
        "KEY:7": "7",
        "KEY:8": "8",
        "KEY:9": "9",
        "KEY:DIV": "÷",

        "KEY:4": "4",
        "KEY:5": "5",
        "KEY:6": "6",
        "KEY:MUL": "×",

        "KEY:1": "1",
        "KEY:2": "2",
        "KEY:3": "3",
        "KEY:SUB": "-",

        "KEY:0": "0",
        "KEY:DOT": ".",
        "KEY:ADD": "+",

        "KEY:LPAREN": "(",
        "KEY:RPAREN": ")",
        "KEY:SQRT": "sqrt(",
        "KEY:POW": "^",

        "KEY:SIN": "sin(",
        "KEY:COS": "cos(",
        "KEY:TAN": "tan(",
        "KEY:LOG": "log(",
        "KEY:LN": "ln(",
        "KEY:PI": "pi",
        "KEY:E": "e"
    }

    value = key_map.get(message)

    if value is not None:
        insert_value(value)


def esp32_serial_worker():
    ports = [
        "/dev/ttyACM0",
        "/dev/ttyUSB0"
    ]

    while True:
        connection = None

        for port in ports:
            try:
                connection = serial.Serial(
                    port,
                    115200,
                    timeout=1
                )
                break
            except Exception:
                pass

        if connection is None:
            time.sleep(2)
            continue

        try:
            while True:
                line = connection.readline().decode(
                    errors="ignore"
                ).strip()

                if line.startswith("KEY:"):
                    esp32_key_queue.put(line)

        except Exception:
            try:
                connection.close()
            except Exception:
                pass

            time.sleep(2)


def poll_esp32_keys():
    try:
        while True:
            message = esp32_key_queue.get_nowait()
            handle_esp32_key(message)

    except queue.Empty:
        pass

    root.after(50, poll_esp32_keys)


# =========================================================
# START
# =========================================================

show_home()

threading.Thread(
    target=esp32_serial_worker,
    daemon=True
).start()

poll_esp32_keys()

root.mainloop()
