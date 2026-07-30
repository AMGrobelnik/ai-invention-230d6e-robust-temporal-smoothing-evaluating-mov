import json
import numpy as np
from scipy import stats
import os

def main():
    print("Loading full experiment results...")
    data_path = "/ai-inventor/aii_data/runs/run_VmPZw2D1_DcZ/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/full_method_out.json"
    with open(data_path, "r") as f:
        data = json.load(f)
    
    examples = data["datasets"][0]["examples"]
    
    y_true = []
    y_naive = []
    y_ma = []
    seeds = []
    timesteps = []
    
    for ex in examples:
        y_true.append(float(ex["output"]))
        y_naive.append(float(ex["predict_naive"]))
        y_ma.append(float(ex["predict_moving_average"]))
        seeds.append(int(ex["metadata_seed"]))
        timesteps.append(int(ex["metadata_timestep"]))
        
    y_true = np.array(y_true)
    y_naive = np.array(y_naive)
    y_ma = np.array(y_ma)
    seeds = np.array(seeds)
    timesteps = np.array(timesteps)
    
    # Compute overall metrics
    mse_naive = float(np.mean((y_true - y_naive) ** 2))
    mae_naive = float(np.mean(np.abs(y_true - y_naive)))
    mse_ma = float(np.mean((y_true - y_ma) ** 2))
    mae_ma = float(np.mean(np.abs(y_true - y_ma)))
    
    # Per-seed analysis to get paired samples across seeds
    unique_seeds = np.unique(seeds)
    seed_mse_naive = []
    seed_mse_ma = []
    
    for s in unique_seeds:
        mask = (seeds == s)
        t_s = y_true[mask]
        n_s = y_naive[mask]
        m_s = y_ma[mask]
        seed_mse_naive.append(np.mean((t_s - n_s) ** 2))
        seed_mse_ma.append(np.mean((t_s - m_s) ** 2))
        
    seed_mse_naive = np.array(seed_mse_naive)
    seed_mse_ma = np.array(seed_mse_ma)
    
    # Statistical tests on per-seed MSE
    t_stat, p_value_t = stats.ttest_rel(seed_mse_naive, seed_mse_ma)
    wilcoxon_stat, p_value_w = stats.wilcoxon(seed_mse_naive - seed_mse_ma)
    
    win_rate = float(np.mean(seed_mse_ma < seed_mse_naive))
    
    # Build examples with eval metrics per example
    eval_examples = []
    for i in range(len(examples)):
        err_naive = float((y_true[i] - y_naive[i]) ** 2)
        err_ma = float((y_true[i] - y_ma[i]) ** 2)
        eval_examples.append({
            "input": examples[i]["input"],
            "output": examples[i]["output"],
            "metadata_seed": int(seeds[i]),
            "metadata_timestep": int(timesteps[i]),
            "predict_naive": float(examples[i]["predict_naive"]),
            "predict_moving_average": float(examples[i]["predict_moving_average"]),
            "eval_mse_naive": float(err_naive),
            "eval_mse_ma": float(err_ma)
        })
        
    metrics_agg = {
        "overall_mse_naive": mse_naive,
        "overall_mse_ma": mse_ma,
        "overall_mae_naive": mae_naive,
        "overall_mae_ma": mae_ma,
        "paired_t_test_stat": float(t_stat),
        "paired_t_test_pvalue": float(p_value_t),
        "wilcoxon_stat": float(wilcoxon_stat),
        "wilcoxon_pvalue": float(p_value_w),
        "seed_win_rate": win_rate
    }
    
    full_output = {
        "metrics_agg": metrics_agg,
        "datasets": [
            {
                "dataset": "synthetic_noisy_timeseries_evaluated",
                "examples": eval_examples
            }
        ]
    }
    
    # Save full
    with open("full_eval_out.json", "w") as f:
        json.dump(full_output, f, indent=2)
        
    # Save mini (~3 examples)
    mini_output = {
        "metrics_agg": metrics_agg,
        "datasets": [
            {
                "dataset": "synthetic_noisy_timeseries_evaluated",
                "examples": eval_examples[:3]
            }
        ]
    }
    with open("mini_eval_out.json", "w") as f:
        json.dump(mini_output, f, indent=2)
        
    # Save preview (~1 example)
    preview_output = {
        "metrics_agg": metrics_agg,
        "datasets": [
            {
                "dataset": "synthetic_noisy_timeseries_evaluated",
                "examples": eval_examples[:1]
            }
        ]
    }
    with open("preview_eval_out.json", "w") as f:
        json.dump(preview_output, f, indent=2)
        
    print("Evaluation files (full, mini, preview) generated successfully adhering to exp_eval_sol_out.json schema!")

if __name__ == "__main__":
    main()
