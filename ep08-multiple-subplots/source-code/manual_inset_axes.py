import matplotlib.pyplot as plt

from factory_data import create_shift_data


data = create_shift_data()
shift_hour = data["shift_hour"]

fig = plt.figure(figsize=(11, 6))

main_ax = fig.add_axes(
    [0.09, 0.13, 0.82, 0.77]
)
inset_ax = fig.add_axes(
    [0.61, 0.57, 0.25, 0.24]
)

main_ax.plot(
    shift_hour,
    data["line_a"],
    color="tab:blue",
    linewidth=2.5,
)
main_ax.axhline(
    90,
    color="gray",
    linestyle="--",
    linewidth=1.2,
)
main_ax.set(
    title="Line A Output Rate",
    xlabel="Shift hour",
    ylabel="Output rate (units/min)",
)
main_ax.grid(alpha=0.25)

inset_ax.plot(
    shift_hour,
    data["defect_rate"],
    color="tab:red",
)
inset_ax.set_title(
    "Defect Rate",
    fontsize=10,
)
inset_ax.tick_params(labelsize=8)
inset_ax.grid(alpha=0.2)

plt.show()
