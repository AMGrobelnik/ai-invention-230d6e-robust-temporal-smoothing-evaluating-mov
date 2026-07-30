import numpy as np
import json

def main():
    examples = []
    for seed in range(100):
        np.random.seed(seed)
        t = np.arange(50)
        series = 0.1 * t + np.sin(t * 0.2) + np.random.normal(0, 0.5, size=50)
        
        for i in range(3, len(series)):
            naive_pred = float(series[i-1])
            ma_pred = float(np.mean(series[i-3:i]))
            actual = float(series[i])
            
            examples.append({
                "input": f"Series values up to index {i-1}, seed {seed}",
                "output": str(actual),
                "metadata_seed": seed,
                "metadata_timestep": i,
                "predict_naive": str(naive_pred),
                "predict_moving_average": str(ma_pred)
            })

    output = {
        "datasets": [
            {
                "dataset": "synthetic_noisy_timeseries",
                "examples": examples
            }
        ]
    }

    with open('full_method_out.json', 'w') as f:
        json.dump(output, f, indent=2)

    with open('method_out.json', 'w') as f:
        json.dump(output, f, indent=2)

    preview_output = {
        "datasets": [
            {
                "dataset": "synthetic_noisy_timeseries",
                "examples": examples[:10]
            }
        ]
    }
    with open('preview_method_out.json', 'w') as f:
        json.dump(preview_output, f, indent=2)

    mini_output = {
        "datasets": [
            {
                "dataset": "synthetic_noisy_timeseries",
                "examples": examples[:2]
            }
        ]
    }
    with open('mini_method_out.json', 'w') as f:
        json.dump(mini_output, f, indent=2)

    print("Successfully generated schema-compliant JSON outputs.")

if __name__ == '__main__':
    main()
