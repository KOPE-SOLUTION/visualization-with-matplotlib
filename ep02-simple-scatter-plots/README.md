# EP2 — Creating Scatter Plots with Matplotlib

Welcome to Episode 2 of the **Python Data Visualization with Matplotlib** series.

## Learning Objectives

- Understand what a scatter plot is
- Create scatter plots with `plot()` and `scatter()`
- Customize marker style, size, and color
- Use transparency (`alpha`)
- Apply colormaps
- Know when to use `plot()` or `scatter()`

## Example 1

```python
import numpy as np
import matplotlib.pyplot as plt

x=np.linspace(0,10,30)
y=np.sin(x)

plt.scatter(x,y)
plt.show()
```

A scatter plot represents every observation as an individual point.

## Example 2

```python
plt.scatter(
    x,
    y,
    marker="o",
    color="royalblue",
    s=80
)
```

Customize:
- marker
- color
- size

## Example 3

```python
plt.scatter(
    x,
    y,
    alpha=0.5
)
```

Transparency helps visualize overlapping points.

## Example 4

```python
rng=np.random.default_rng(0)

x=rng.normal(size=100)
y=rng.normal(size=100)
sizes=rng.uniform(20,200,100)
colors=rng.random(100)

plt.scatter(
    x,
    y,
    s=sizes,
    c=colors,
    cmap="viridis",
    alpha=0.7
)
plt.colorbar()
```

## plot() vs scatter()

Use `plot()` for connected lines and very large datasets with identical markers.

Use `scatter()` when marker size or color should represent additional information.

## Exercises

1. Plot y=x² using scatter.
2. Change marker styles.
3. Change point colors.
4. Add a title.
5. Add axis labels.

## Mini Challenge

Create a presentation-ready scatter chart using random data.

## Next Episode

EP3 — Visualizing Error Bars
