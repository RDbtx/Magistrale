import json
from src.autoattacks_utils import compute_autoattacks
from src.results_analysis_utils import make_all_plots
from src.results_processing_utils import compute_results_average

# RobustBench models to re-evaluate with AutoAttack.
# Values are the RobustBench reported robust accuracies.
robust_bench_models = {
    "Peng2023Robust": 0.7107,
    "Rebuffi2021Fixing_70_16_cutmix_ddpm": 0.6420,
    "Wang2020Improving": 0.5629,
    "Rice2020Overfitting": 0.5342,
    "Chen2024Data_WRN_34_20": 0.5809
}

if __name__ == "__main__":
    # main AutoAttack analysis
    compute_autoattacks(
        models=robust_bench_models,
        samples=150,
        seeds=0,
        batch_size=50,
        mode="fast targeted",
        steps=[1, 4, 8, 12, 16],
        out_file_name="targeted_results"
    )

    # Generate plots from the produced CSV and compare against RobustBench accuracies numbers if specified.
    make_all_plots("targeted_untargeted_averaged.csv", rb_acc=robust_bench_models)
