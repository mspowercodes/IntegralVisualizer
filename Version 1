import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Define the function
def f(x):
    return (x + 1) * (x - 2) * (x + 3)

# User-provided domain interval
a = float(input("Enter start of interval (e.g., -4): "))
b = float(input("Enter end of interval (e.g., 3): "))

# Initial setup for the graph
initial_n = 5
x_vals = np.linspace(a, b, 400)
y_vals = f(x_vals)

fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.25)  # Make room for the slider

# Plot the continuous function
line, = ax.plot(x_vals, y_vals, 'k', lw=2, label='f(x) = (x+1)(x-2)(x+3)')
rect_container = []

def update(val):
    # Remove previous rectangles
    for r in rect_container:
        r.remove()
    rect_container.clear()
    
    n = int(slider.val)
    dx = (b - a) / n
    # Use left-endpoint Riemann sum for rectangle positions
    x_rects = np.linspace(a, b - dx, n)
    y_rects = f(x_rects)
    
    # Draw new rectangles
    new_rects = ax.bar(x_rects, y_rects, width=dx, align='edge', 
                       alpha=0.3, color='skyblue', edgecolor='blue')
    rect_container.extend(new_rects)
    
    # Calculate and display the sum
    riemann_sum = np.sum(y_rects * dx)
    ax.set_title(f"Riemann Sum (n={n}): {riemann_sum:.4f}")
    fig.canvas.draw_idle()

# Create the slider axes and widget
ax_slider = plt.axes([0.2, 0.1, 0.6, 0.03])
slider = Slider(ax_slider, 'Rectangles', 1, 100, valinit=initial_n, valstep=1)

# Connect the slider to the update function
slider.on_changed(update)

# Initial call to populate rectangles
update(initial_n)

ax.axhline(0, color='black', lw=1)
ax.legend()
plt.show()
