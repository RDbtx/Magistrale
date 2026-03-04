import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def eps_value(eps_key: str) -> float:
    """
    Convert an epsilon key (like: 8/255) into a numeric float value.

    Input:
    - eps_key: epsilon key (string or number).

    Output:
    - eps: epsilon as a float.

    """
    num, den = eps_key.split('/')
    return float(num) / float(den)

def generate_x_axis(df_acc: pd.DataFrame) -> np.ndarray:
    """
    Uses the epsilon values listed in the dataframe to generate the x-axis values
    of accuracy vs epsilons plots.

    Input:
    - df_acc: pandas DataFrame containing accuracy values.
    Output:
    - x_axis: x-axis values.

    """
    x_axis = []
    for eps in df_acc.columns:
        x_axis.append(eps_value(eps))
    return np.array(x_axis, dtype=float)


def plot_acc_vs_eps(df_acc: pd.DataFrame, savepath: str, title: str = "Robust accuracy vs ε") -> None:
    """
    Plot robust accuracy vs epsilon for each model and save the figure.

    Inputs:
    - df_acc: DataFrame with models as rows, eps keys as columns, and robust accuracies as values.
    - savepath: output path for the saved PNG figure.
    - title: plot title.

    """
    x = generate_x_axis(df_acc)

    plt.figure()
    for m in df_acc.index:
        plt.plot(x, df_acc.loc[m].values.astype(float), marker="o", label=m)

    plt.xlabel("ε")
    plt.ylabel("Robust accuracy")
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(savepath, dpi=200)
    plt.show()
    plt.close()


def plot_rank_vs_eps(df_acc: pd.DataFrame, savepath: str, title: str = "Rank position vs ε") -> None:
    """
    Plot model rank vs epsilon and save the figure. For each epsilon column, models are ranked by robust accuracy,
    where rank 1 is best.

    Inputs:
    - df_acc: DataFrame with models as rows, eps keys as columns, and robust accuracies as values.
    - savepath: output path for the saved PNG figure.
    - title: plot title.

    """
    df_rank = df_acc.rank(axis=0, ascending=False, method="average")
    x = generate_x_axis(df_acc)

    plt.figure()
    for m in df_rank.index:
        plt.plot(x, df_rank.loc[m].values.astype(float), marker="o", label=m)

    plt.xlabel("ε")
    plt.ylabel("Rank (1 = best)")
    plt.title(title)
    plt.gca().invert_yaxis()
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(savepath, dpi=200)
    plt.show()
    plt.close()


def plot_heatmap_acc(df_acc: pd.DataFrame, savepath: str, title: str = "Robust Accuracy Heatmap ") -> None:
    """
    Plot a heatmap of robust accuracies across models and epsilons.
    Models are ordered by their average rank across epsilons (best on top).

    Inputs:
    - df_acc: DataFrame with models as rows, eps keys as columns, and robust accuracies as values.
    - savepath: output path for the saved PNG figure.
    - title: plot title.

    """
    df_rank = df_acc.rank(axis=0, ascending=False, method="average")
    order = df_rank.mean(axis=1).sort_values().index
    df_plot = df_acc.loc[order]

    plt.figure()
    plt.imshow(df_plot.values.astype(float), aspect="auto")
    plt.colorbar(label="Robust accuracy")
    plt.yticks(range(df_plot.shape[0]), df_plot.index, fontsize=8)
    plt.xticks(range(df_plot.shape[1]), df_plot.columns, rotation=45, ha="right")
    plt.xlabel("ε")
    plt.ylabel("Model")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(savepath, dpi=200)
    plt.show()
    plt.close()


def plot_acc_vs_eps_with_rb_points(df_acc: pd.DataFrame, rb_acc: dict, savepath: str, rb_eps: str = "8/255",
                                   title: str = "Robust accuracy vs ε + RobustBench point") -> None:
    """
    Plot robust accuracy vs epsilon and overlay RobustBench point estimates.
    For each model, the function plots the robust accuracy curve from `df_acc`.
    If `rb_acc` contains an entry for the model, it overlays a marker at `rb_eps`.

    Inputs:
    - df_acc: DataFrame with models as rows, eps keys as columns, and robust accuracies as values.
    - rb_acc: dictionary mapping model name -> RobustBench robust accuracy (at `rb_eps`).
    - savepath: output path for the saved PNG figure.
    - rb_eps: epsilon key for RobustBench reference (default "8/255").
    - title: plot title.

    """
    x = generate_x_axis(df_acc)
    x_rb = eps_value(rb_eps)

    plt.figure()
    for m in df_acc.index:
        plt.plot(x, df_acc.loc[m].values.astype(float), marker="o", label=m)
        if m in rb_acc and rb_acc[m] is not None:
            plt.scatter([x_rb], [float(rb_acc[m])], marker="x")

    plt.xlabel("ε")
    plt.ylabel("Robust accuracy")
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(savepath, dpi=200)
    plt.show()
    plt.close()


def plot_rb_vs_ours_at_eps(df_acc: pd.DataFrame, rb_acc: dict, savepath: str, rb_eps: str = "8/255",
                           title: str = "RobustBench vs AutoAttack robust accuracy") -> None:
    """
    Compare RobustBench accuracy vs our AutoAttack accuracy at a selected epsilon.

    Inputs:
    - df_acc: DataFrame with models as rows, eps keys as columns, and robust accuracies as values.
    - rb_acc: dictionary mapping model name -> RobustBench robust accuracy (at `rb_eps`).
    - savepath: output path for the saved PNG figure.
    - rb_eps: RobustBench epsilon key (default "8/255").
    - title: plot title.

    """
    col = rb_eps if rb_eps in df_acc.columns else min(
        df_acc.columns,
        key=lambda c: abs(eps_value(c) - eps_value(rb_eps))
    )

    models = list(rb_acc.keys())
    rb_vals = [float(rb_acc[m]) for m in models]
    our_vals = [float(df_acc.loc[m, col]) for m in models]

    x = np.arange(len(models))
    w = 0.38

    plt.figure()
    plt.bar(x - w / 2, rb_vals, w, label="RobustBench")
    plt.bar(x + w / 2, our_vals, w, label="Ours")

    plt.xticks(x, models, rotation=45, ha="right", fontsize=8)
    plt.ylabel("Robust accuracy")
    plt.title(f"{title}\n(ours at ε={col}, RB at ε={rb_eps})")
    plt.grid(True, axis="y", alpha=0.3)
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(savepath, dpi=200)
    plt.show()
    plt.close()


def make_all_plots(result_csv_filename: str = "results.csv", rb_acc: dict = None) -> None:
    """
    Generate and save all plots from a results CSV.
    The function loads the robust accuracy table from `./results/<result_csv_filename>`
    and writes plots to `./plots`.

    Plots generated:
    - robust accuracy vs epsilon (with optional RobustBench overlay point)
    - rank vs epsilon
    - accuracy heatmap (models ordered by average rank)

    If `rb_acc` is provided, the function also generates:
    - robust accuracy vs epsilon with RobustBench markers at `rb_eps`
    - RobustBench vs ours bar chart at eps = 8/255

    Inputs:
    - result_csv_filename: name of the results CSV inside `./results`.
    - rb_acc: optional dict mapping model name -> RobustBench robust accuracy (at `rb_eps`).

    """
    out_dir = "./plots"
    results_dir = "./results"
    rb_eps = "8/255"

    name = result_csv_filename.replace(".csv", "")
    os.makedirs(out_dir, exist_ok=True)

    df_acc = pd.read_csv(os.path.join(results_dir, result_csv_filename), index_col=0)

    if rb_acc:
        plot_acc_vs_eps_with_rb_points(
            df_acc, rb_acc, os.path.join(out_dir, f"{name}_acc_vs_eps_with_rb.png"),
            rb_eps=rb_eps
        )
        plot_rb_vs_ours_at_eps(
            df_acc, rb_acc, os.path.join(out_dir, f"{name}_rb_vs_ours.png"),
            rb_eps=rb_eps
        )
    else:
        plot_acc_vs_eps(
            df_acc,
            os.path.join(out_dir, f"{name}_acc_vs_eps.png"),
            title="Robust accuracy vs AutoAttack ε "
        )

    plot_rank_vs_eps(df_acc, os.path.join(out_dir, f"{name}_rank_vs_eps.png"))
    plot_heatmap_acc(df_acc, os.path.join(out_dir, f"{name}_heatmap_acc.png"))
