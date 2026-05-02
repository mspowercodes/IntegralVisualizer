import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import re
from scipy.integrate import quad

# Page config
st.set_page_config(page_title="Integral Visualizer")
st.title("Interactive Integral Visualizer")

# --- Function Preprocessing ---
def preprocess_function(text):
    text = text.replace('^', '**')
    text = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', text)
    text = re.sub(r'([a-zA-Z\)])(\d)', r'\1*\2', text)
    text = re.sub(r'([xX\d\)])(\()', r'\1*\2', text)
    text = re.sub(r'(\))([xX\d])', r'\1*\2', text)
    return text

# --- Formatting Helper ---
def format_num(val):
    return f"{val:g}"

# --- Sidebar Inputs ---
st.sidebar.header("Parameters")
raw_func = st.sidebar.text_input("Function f(x):", "x^2")
func_text = preprocess_function(raw_func)

# The "%g" format tells Streamlit to hide trailing zeros in the box
a = st.sidebar.number_input("Lower Bound (a)", value=0.0, step=0.1, format="%g")
b = st.sidebar.number_input("Upper Bound (b)", value=4.0, step=0.1, format="%g")
n = st.sidebar.slider("Number of Rectangles/Steps", 1, 100, 10)

method = st.sidebar.selectbox(
    "Approximation Method",
    ("Left Endpoint", "Right Endpoint", "Midpoint", "Trapezoid")
)

a_disp = f"{a:g}"
b_disp = f"{b:g}"

# --- Math Logic ---
def f(x):
    if not func_text.strip(): return np.zeros_like(x)
    try:
        allowed_names = {
            "x": x, "np": np, "sin": np.sin, "cos": np.cos, 
            "tan": np.tan, "exp": np.exp, "sqrt": np.sqrt, "pi": np.pi
        }
        return eval(func_text, {"__builtins__": {}}, allowed_names)
    except:
        return None

# Helper for scipy integration (needs scalar input)
def f_scalar(x):
    try:
        return eval(func_text, {"__builtins__": {}}, {"x": x, "np": np, "sin": np.sin, "cos": np.cos, "tan": np.tan, "exp": np.exp, "sqrt": np.sqrt, "pi": np.pi})
    except:
        return 0

# --- Calculations ---
dx = (b - a) / n
x_vals = np.linspace(a, b, n + 1)
approx_area = 0

# 1. Exact Area Calculation
try:
    exact_area, error = quad(f_scalar, a, b)
except:
    exact_area = 0

# 2. Prepare Display Columns ABOVE graph
col1, col2 = st.columns(2)

# --- Plotting Logic ---
fig, ax = plt.subplots()
padding = max(abs(b - a) * 0.2, 1)
x_curve = np.linspace(a - padding, b + padding, 400)
y_curve = f(x_curve)

if y_curve is not None:
    ax.plot(x_curve, y_curve, 'b', lw=2, label=f'f(x) = {raw_func}')

    if method == "Left Endpoint":
        y_left = f(x_vals[:-1])
        ax.bar(x_vals[:-1], y_left, width=dx, align='edge', alpha=0.3, color='orange', edgecolor='black')
        approx_area = np.sum(y_left * dx)
    elif method == "Right Endpoint":
        y_right = f(x_vals[1:])
        ax.bar(x_vals[:-1], y_right, width=dx, align='edge', alpha=0.3, color='green', edgecolor='black')
        approx_area = np.sum(y_right * dx)
    elif method == "Midpoint":
        x_mid = (x_vals[:-1] + x_vals[1:]) / 2
        y_mid = f(x_mid)
        ax.bar(x_vals[:-1], y_mid, width=dx, align='edge', alpha=0.3, color='purple', edgecolor='black')
        approx_area = np.sum(y_mid * dx)
    elif method == "Trapezoid":
        y_vals = f(x_vals)
        for i in range(n):
            ax.fill([x_vals[i], x_vals[i+1], x_vals[i+1], x_vals[i]], [0, 0, y_vals[i+1], y_vals[i]], 'red', alpha=0.2, edgecolor='black')
        approx_area = (dx / 2) * (y_vals[0] + 2 * np.sum(y_vals[1:-1]) + y_vals[-1])

    # Show results in columns at the top
col1.metric("Approximate Area", f"{round(approx_area, 2):g}")
col2.metric("Exact Area", f"{round(exact_area, 2):g}", f"{round(approx_area - exact_area, 2):g} (Error)")

    ax.axhline(0, color='black', lw=1)
    ax.axvline(0, color='black', lw=1)
    ax.set_title(f"{method} from {a_disp} to {b_disp}")
    ax.grid(True, linestyle=':', alpha=0.6)
    st.pyplot(fig)
else:
    st.error(f"**Check your function!** Python couldn't read '{raw_func}'.")
