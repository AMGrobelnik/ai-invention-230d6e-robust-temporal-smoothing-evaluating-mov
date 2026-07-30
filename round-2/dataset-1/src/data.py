import os
import json
import numpy as np

os.makedirs("temp/datasets", exist_ok=True)
dataset_names = [
    "synth_trend_season_3",
    "synth_regime_shift_1",
    "synth_random_walk_2",
    "synth_trend_season_6",
    "synth_regime_shift_4"
]

datasets_data = []
np.random.seed(42)

for name in dataset_names:
    n_samples = 250
    t = np.linspace(0, 50, n_samples)
    if "trend_season" in name:
        signal = 0.5 * t + np.sin(t) + np.random.normal(0, 0.2, n_samples)
    elif "regime_shift" in name:
        signal = np.sin(t) + np.random.normal(0, 0.1, n_samples)
        signal[125:] += 4.0
    else:
        signal = np.cumsum(np.random.normal(0.05, 0.5, n_samples))
        
    examples = []
    for idx in range(3, n_samples):
        past_vals = signal[idx-3:idx].tolist()
        curr_val = signal[idx]
        examples.append({
            "input": json.dumps({"past_values": past_vals}),
            "output": str(curr_val),
            "metadata_fold": int(idx % 5),
            "metadata_feature_names": ["lag_1", "lag_2", "lag_3"],
            "metadata_task_type": "regression",
            "metadata_row_index": int(idx)
        })
    datasets_data.append({"dataset": name, "examples": examples})

output = {"datasets": datasets_data}
with open("full_data_out.json", "w") as f:
    json.dump(output, f, indent=2)

mini_datasets = [{"dataset": ds["dataset"], "examples": ds["examples"][:20]} for ds in datasets_data]
with open("mini_data_out.json", "w") as f:
    json.dump({"datasets": mini_datasets}, f, indent=2)

preview_datasets = [{"dataset": ds["dataset"], "examples": ds["examples"][:10]} for ds in datasets_data]
with open("preview_data_out.json", "w") as f:
    json.dump({"datasets": preview_datasets}, f, indent=2)

print("Generated 5 datasets successfully.")
