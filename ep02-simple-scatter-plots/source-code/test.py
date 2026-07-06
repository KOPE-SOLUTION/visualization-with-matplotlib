import numpy as np
import matplotlib.pyplot as plt

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


plt.show()
