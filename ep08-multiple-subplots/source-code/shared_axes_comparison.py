import matplotlib.pyplot as plt

from factory_data import create_shift_data


data = create_shift_data()
shift_hour = data["shift_hour"]

fig, axes = plt.subplots(
    3,
    1,
    figsize=(10, 7),
    sharex=True,
    sharey=True,
    layout="constrained",
)

line_series = [
    (data["line_a"], "Line A", "tab:blue"),
    (data["line_b"], "Line B", "tab:orange"),
    (data["line_c"], "Line C", "tab:green"),
]

for ax, (values, label, color) in zip(
    axes,
    line_series,
):
    ax.plot(
        shift_hour,
        values,
        color=color,
        linewidth=2,
    )
    ax.axhline(
        90,
        color="gray",
        linestyle="--",
        linewidth=1.2,
    )
    ax.set_ylabel(label)
    ax.grid(alpha=0.25)

axes[-1].set_xlabel("Shift hour")
fig.suptitle("Output Rate by Production Line")

plt.show()
