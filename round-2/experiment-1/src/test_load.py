import json
import numpy as np

# Load mini dataset first to test
with open('/ai-inventor/aii_data/runs/run_VmPZw2D1_DcZ/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/mini_data_out.json', 'r') as f:
    data = json.load(f)

print("Loaded datasets:", len(data['datasets']))
