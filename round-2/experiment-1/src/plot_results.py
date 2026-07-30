import json
import matplotlib.pyplot as plt
import numpy as np

with open('/ai-inventor/aii_data/runs/run_VmPZw2D1_DcZ/3_invention_loop/iter_2/gen_art/gen_art_experiment_1/results/method_out.json', 'r') as f:
    data = json.load(f)

datasets = [r['dataset'] for r in data['results']]
naive_mse = [r['metrics']['naive_mse'] for r in data['results']]
fixed_mse = [r['metrics']['fixed_ma_mse'] for r in data['results']]
adaptive_mse = [r['metrics']['adaptive_ma_mse'] for r in data['results']]

x = np.arange(len(datasets))
width = 0.25

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(x - width, naive_mse, width, label='Naive')
ax.bar(x, fixed_mse, width, label='Fixed MA (3)')
ax.bar(x + width, adaptive_mse, width, label='Adaptive MA')

ax.set_ylabel('Mean Squared Error (MSE)')
ax.set_title('Comparison of Forecasting Methods Across Synthetic Datasets')
ax.set_xticks(x)
ax.set_xticklabels(datasets, rotation=45)
ax.legend()

plt.tight_layout()
plt.savefig('/ai-inventor/aii_data/runs/run_VmPZw2D1_DcZ/3_invention_loop/iter_2/gen_art/gen_art_experiment_1/results/forecast_comparison.png')
print("Plot saved successfully.")
