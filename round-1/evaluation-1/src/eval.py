import json
import numpy as np
from scipy import stats

def main():
    # Load full method output from experiment 1
    exp_path = "/ai-inventor/aii_data/runs/run_VmPZw2D1_DcZ/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/full_method_out.json"
    with open(exp_path, 'r') as f:
        data = json.load(f)

    examples = data["datasets"][0]["examples"]

    actuals = []
    naive_preds = []
    ma_preds = []

    for ex in examples:
        actuals.append(float(ex["output"]))
        naive_preds.append(float(ex["predict_naive"]))
        ma_preds.append(float(ex["predict_moving_average"]))

    actuals = np.array(actuals)
    naive_preds = np.array(naive_preds)
    ma_preds = np.array(ma_preds)

    naive_errors = (naive_preds - actuals) ** 2
    ma_errors = (ma_preds - actuals) ** 2

    naive_mse = float(np.mean(naive_errors))
    ma_mse = float(np.mean(ma_errors))

    naive_rmse = float(np.sqrt(naive_mse))
    ma_rmse = float(np.sqrt(ma_mse))

    # Paired t-test and Wilcoxon signed-rank test on squared errors
    t_stat, p_value_t = stats.ttest_rel(naive_errors, ma_errors)
    wilcoxon_stat, p_value_w = stats.wilcoxon(naive_errors, ma_errors)

    metrics = {
        "naive_mse": naive_mse,
        "moving_average_mse": ma_mse,
        "naive_rmse": naive_rmse,
        "moving_average_rmse": ma_rmse,
        "paired_t_statistic": float(t_stat),
        "paired_t_p_value": float(p_value_t),
        "wilcoxon_statistic": float(wilcoxon_stat),
        "wilcoxon_p_value": float(p_value_w),
        "num_samples": len(actuals)
    }

    output = {
        "evaluation": {
            "dataset": "synthetic_noisy_timeseries",
            "metrics": metrics
        }
    }

    with open('/ai-inventor/aii_data/runs/run_VmPZw2D1_DcZ/3_invention_loop/iter_1/gen_art/gen_art_evaluation_1/eval_out.json', 'w') as f:
        json.dump(output, f, indent=2)

    print("Evaluation completed successfully.")
    print(json.dumps(output, indent=2))

if __name__ == '__main__':
    main()
