import json
import os

# Read results/method_out.json
with open('/ai-inventor/aii_data/runs/run_VmPZw2D1_DcZ/3_invention_loop/iter_2/gen_art/gen_art_experiment_1/results/method_out.json', 'r') as f:
    data = json.load(f)

# Save full_method_out.json
with open('/ai-inventor/aii_data/runs/run_VmPZw2D1_DcZ/3_invention_loop/iter_2/gen_art/gen_art_experiment_1/results/full_method_out.json', 'w') as f:
    json.dump(data, f, indent=2)

# Save mini_method_out.json (first 3 results)
mini_data = data.copy()
mini_data['results'] = data['results'][:3]
with open('/ai-inventor/aii_data/runs/run_VmPZw2D1_DcZ/3_invention_loop/iter_2/gen_art/gen_art_experiment_1/results/mini_method_out.json', 'w') as f:
    json.dump(mini_data, f, indent=2)

# Save preview_method_out.json (first 1 result)
preview_data = data.copy()
preview_data['results'] = data['results'][:1]
with open('/ai-inventor/aii_data/runs/run_VmPZw2D1_DcZ/3_invention_loop/iter_2/gen_art/gen_art_experiment_1/results/preview_method_out.json', 'w') as f:
    json.dump(preview_data, f, indent=2)

print("Generated full, mini, and preview JSON files successfully.")
