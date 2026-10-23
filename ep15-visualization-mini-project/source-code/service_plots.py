"""Four reusable Axes-level plots; none creates or shows a Figure."""

import matplotlib.ticker as mticker
import seaborn as sns

from service_data import HOURS, SERVICE_ORDER, SERVICE_COLORS, WAIT_BINS, WAIT_TARGET


def format_hour_axis(ax):
    ax.set_xticks(HOURS)
    ax.xaxis.set_major_formatter(mticker.StrMethodFormatter("{x:02.0f}:00"))
    ax.set_xlim(HOURS[0] - 0.4, HOURS[-1] + 0.4)


def plot_intake(ax, hourly_jobs):
    ax.plot(hourly_jobs.index, hourly_jobs.values, color="0.25", marker="o", linewidth=2)
    ax.set(title="Check-ins by Hour", xlabel="Check-in hour (bucket start)",
           ylabel="Number of jobs", ylim=(0, max(5, hourly_jobs.max() + 1)))
    format_hour_axis(ax)
    ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    ax.grid(axis="y", alpha=0.25)


def plot_service_time(ax, mean_service):
    # An absent category has no mean, not a mean of zero minutes.
    values = mean_service.dropna()
    bars = ax.barh(values.index, values.values,
                   color=[SERVICE_COLORS[name] for name in values.index])
    ax.invert_yaxis()
    ax.bar_label(bars, fmt="%.1f", padding=4)
    ax.set(title="Mean Service Time", xlabel="Service time (min)",
           xlim=(0, max(75, values.max() * 1.2)))
    ax.grid(axis="x", alpha=0.20)
    ax.set_axisbelow(True)


def plot_wait_distribution(ax, jobs, wait_target=WAIT_TARGET):
    if not jobs["wait_min"].between(WAIT_BINS[0], WAIT_BINS[-1]).all():
        raise ValueError("Waiting times exceed WAIT_BINS; extend the bin edges before plotting.")
    ax.hist(jobs["wait_min"], bins=WAIT_BINS, color="slategray", edgecolor="white")
    ax.axvline(wait_target, color="crimson", linestyle="--",
               label=f"Example target: {wait_target:g} min")
    ax.set(title="Waiting Time Distribution", xlabel="Waiting time (min)",
           ylabel="Number of jobs", xticks=WAIT_BINS,
           xlim=(0, max(WAIT_BINS[-1], wait_target + 5)))
    ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    ax.grid(axis="y", alpha=0.20)
    ax.legend(fontsize=9)


def plot_wait_by_hour(ax, jobs, wait_target=WAIT_TARGET):
    sns.scatterplot(data=jobs, x="hour", y="wait_min", hue="service_type",
                    hue_order=SERVICE_ORDER, palette=SERVICE_COLORS, s=65, ax=ax)
    ax.axhline(wait_target, color="crimson", linestyle="--",
               label=f"Example target: {wait_target:g} min")
    # idxmax returns the index label; loc retrieves that row. Ties select the first row.
    longest = jobs.loc[jobs["wait_min"].idxmax()]
    ax.annotate(
        f"{longest['job_id']}: {longest['wait_min']:g} min",
        xy=(longest["hour"], longest["wait_min"]),
        xytext=(0, 12), textcoords="offset points", ha="center", fontsize=9,
        arrowprops={"arrowstyle": "->", "color": "0.2"},
    )
    ax.set(title="Waiting Time by Check-in Hour", xlabel="Check-in hour (bucket start)",
           ylabel="Waiting time (min)", ylim=(0, max(60, jobs["wait_min"].max() + 15, wait_target + 15)))
    format_hour_axis(ax)
    ax.grid(alpha=0.20)
    ax.legend(title="Service / reference", loc="upper left", fontsize=8, title_fontsize=9)
