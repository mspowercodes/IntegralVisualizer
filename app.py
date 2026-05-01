import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Interactive Integral Visualizer")

# 1. User Input for the function
# We use eval() to turn text into a math function safely for simple inputs
func_text = st.sidebar.text_input("Enter a function of x", "x**2")
a = st.sidebar.number_input("Lower Bound (a)", value=-5.0)
b = st.sidebar.number_input("Upper Bound (b)", value=5.0)

# 2. Slider for number of rectangles
n = st.sidebar.slider("Number of Rectangles", 1, 100, 10)

# Define the function based on input
def f(x):
    return eval(func_text)

# 3. Create the Visualization
fig, ax = plt.subplots()

# Plot the smooth function curve
x_curve = np.linspace(-10, 10, 400)
y_curve = f(x_curve)
ax.plot(x_curve, y_curve, 'b', label=f'f(x) = {func_text}')

# Draw the Riemann Sum Rectangles
dx = (b - a) / n
x_rects = np.linspace(a, b - dx, n) # Left-hand Riemann sum
y_rects = f(x_rects)

ax.bar(x_rects, y_rects, width=dx, align='edge', 
       alpha=0.3, color='orange', edgecolor='black')

# Formatting the graph
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.axhline(0, color='black', linewidth=1)
ax.axvline(0, color='black', linewidth=1)
ax.set_title(f"Approximating Area with {n} Rectangles")
ax.legend()

# 4. Display in Streamlit
st.pyplot(fig)

# Show the calculated area approximation
approx_area = np.sum(y_rects * dx)
st.write(f"### Approximate Area: {approx_area:.4f}")

