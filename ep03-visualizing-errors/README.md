# EP3 — Visualizing Errors with Matplotlib

Welcome to Episode 3 of the Python Data Visualization with Matplotlib series.

## Learning Objectives

- Understand why uncertainty matters
- Create error bars with `plt.errorbar()`
- Customize error bars
- Create confidence bands using `fill_between()`
- Learn best practices for presenting measurement uncertainty

## Example 1 — Basic Error Bars

```python
import numpy as np
import matplotlib.pyplot as plt

x=np.linspace(0,10,20)
y=np.sin(x)
err=0.2

plt.errorbar(x,y,yerr=err,fmt='o',capsize=4)
plt.show()
```

## Example 2 — Styled Error Bars

```python
plt.errorbar(
    x,
    y,
    yerr=err,
    fmt='o',
    color='royalblue',
    ecolor='gray',
    elinewidth=2,
    capsize=6
)
```

## Example 3 — Confidence Band

```python
plt.plot(x,y)
plt.fill_between(
    x,
    y-err,
    y+err,
    alpha=0.2
)
```

`fill_between()` shades the uncertainty region around a curve.

## Best Practices

- Label your axes.
- Explain what the error represents.
- Keep colors subtle.
- Avoid clutter.

## Exercises

1. Create vertical error bars.
2. Add horizontal error bars.
3. Customize colors.
4. Replace error bars with a confidence band.

## Mini Challenge

Create a presentation-ready chart that includes:

- Data
- Error bars
- Title
- Axis labels
- Grid

## Next Episode

EP4 — Density and Contour Plots
