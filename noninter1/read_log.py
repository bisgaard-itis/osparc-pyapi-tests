import pathlib as pl

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

exitcode_map = {0: 0, 1: 1, 2: 2, 12: 502, 14: 504}
error_string = {
    0: "Success",
    1: "Unknown error",
    2: "Job FAILING",
    502: "Error 502",
    504: "Error 504",
}


def main():
    log_file_path = pl.Path("./test.log")
    log_content = pd.read_csv(log_file_path, delimiter="\t")
    print(log_content)

    exitvals = log_content["Exitval"]
    exitvals = exitvals.replace(exitcode_map)
    bins = np.arange(
        start=exitvals.min() - 0.5, stop=exitvals.max() + 1.5, step=1
    )

    counts, bin_edges = np.histogram(exitvals, bins=bins)
    # ax = exitvals.hist(bins=bin_edges, grid=False, align="mid", rwidth=0.1)
    filtered_counts = counts[counts > 0]
    filtered_bin_edges = bin_edges[:-1][counts > 0]
    filtered_bin_labels = [
        error_string[int(x)] for x in filtered_bin_edges + 0.5
    ]
    ticks = range(len(filtered_counts))
    fig, ax = plt.subplots()

    ax.bar(
        ticks,
        filtered_counts,
        color="black",
        width=0.5,
        align="center",
        zorder=2,
    )
    ax.grid(zorder=1)

    ax.set_xlabel("Exit value")
    ax.set_ylabel(f"Number (out of {len(exitvals)})")
    ax.set_ylim(0, len(exitvals))
    ax.set_yticks(range(0, len(exitvals) + 1, 5))
    ax.set_xticks(ticks)
    ax.set_xticklabels(filtered_bin_labels)
    ax.set_title("Exit code histogram")

    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
