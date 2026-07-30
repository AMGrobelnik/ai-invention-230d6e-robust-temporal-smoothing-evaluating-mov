import json
import os

with open('method_out.json', 'r') as f:
    data = json.load(f)

# Full output
with open('full_method_out.json', 'w') as f:
    json.dump(data, f, indent=2)

# Preview output (first 5 details)
preview_data = data.copy()
preview_data['details'] = data['details'][:5]
with open('preview_method_out.json', 'w') as f:
    json.dump(preview_data, f, indent=2)

# Mini output (summary only, no details)
mini_data = data.copy()
mini_data.pop('details', None)
with open('mini_method_out.json', 'w') as f:
    json.dump(mini_data, f, indent=2)

print("Generated full, preview, and mini versions successfully.")
