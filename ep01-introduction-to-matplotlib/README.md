# EP1 — Introduction to Matplotlib

Welcome to the first episode of the **Python Data Visualization with Matplotlib** series.

## Objectives

After completing this episode, you will be able to:
- Explain the role of Matplotlib in Python
- Create and manage Figure and Axes objects
- Build your first Line Plot
- Display multiple data series in a single chart
- Customize colors and line styles
- Configure axis ranges
- Add titles, axis labels, and legends
- Understand the Figure–Axes architecture

## Prerequisites

- Python 3
- NumPy
- Matplotlib
- VS Code
- WSL Ubuntu (recommended)

## Install

```bash
python3 -m pip install matplotlib numpy
```

## Example 1 — First Line Plot

```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0,10,500)
y = np.sin(x)

fig, ax = plt.subplots()
ax.plot(x,y)
ax.set_title("Sine Wave")
plt.show()
```

## Figure vs Axes

- **Figure**: the overall canvas.
- **Axes**: the plotting area where charts are drawn.

A single figure may contain one or many axes.

## Multiple Lines

```python
ax.plot(x,np.sin(x),label="sin(x)")
ax.plot(x,np.cos(x),label="cos(x)")
ax.legend()
```

## Styling

Try changing:
- color
- linestyle
- linewidth
- marker

Example:
```python
ax.plot(x,np.sin(x),color="royalblue",linestyle="--",linewidth=2)
```

## Axis Configuration

```python
ax.set_xlim(0,10)
ax.set_ylim(-1.2,1.2)
```

## Labels

```python
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("Simple Plot")
```

## Exercises

1. Plot y=x².
2. Plot sin(x) and cos(x) together.
3. Change colors and line styles.
4. Add labels and legends.
5. Export the chart as PNG.

## Challenge

Create a chart with three mathematical functions and make it presentation-ready.

## Folder Structure

```text
ep01-introduction-to-matplotlib/
├── README.md
├── source-code/
│   ├── first_plot.py
│   ├── multiple_lines.py
│   └── styling.py
```

## Next Episode

**EP2 — Creating Scatter Plots**
