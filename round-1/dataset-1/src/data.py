# /// script
# dependencies = ["numpy", "pydantic"]
# ///
import json
import os
import numpy as np

def main():
    input_path = "/ai-inventor/aii_data/runs/run_VmPZw2D1_DcZ/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/temp/datasets/data_out.json"
    with open(input_path, "r") as f:
        raw_datasets = json.load(f)

    datasets_output = []
    
    # Exactly top 10 datasets
    for ds in raw_datasets[:10]:
        ds_id = ds["id"]
        length = ds["length"]
        noise_level = ds["noise_level"]
        series = ds["series"]
        
        examples = []
        for t in range(2, length):
            history = series[:t]
            target = series[t]
            examples.append({
                "input": json.dumps(history),
                "output": str(target),
                "metadata_step": t,
                "metadata_noise_level": noise_level,
                "metadata_series_length": length
            })
            
        datasets_output.append({
            "dataset": f"synthetic_ts_{ds_id}",
            "examples": examples
        })

    output_data = {
        "datasets": datasets_output
    }

    full_path = "/ai-inventor/aii_data/runs/run_VmPZw2D1_DcZ/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/full_data_out.json"
    with open(full_path, "w") as f:
        json.dump(output_data, f, indent=2)

    # Mini dataset (3 examples per dataset)
    mini_data = {
        "datasets": [
            {
                "dataset": ds["dataset"],
                "examples": ds["examples"][:3]
            }
            for ds in datasets_output
        ]
    }
    with open("/ai-inventor/aii_data/runs/run_VmPZw2D1_DcZ/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/mini_data_out.json", "w") as f:
        json.dump(mini_data, f, indent=2)

    # Preview dataset (10 examples per dataset or all if less)
    preview_data = {
        "datasets": [
            {
                "dataset": ds["dataset"],
                "examples": ds["examples"][:10]
            }
            for ds in datasets_output
        ]
    }
    with open("/ai-inventor/aii_data/runs/run_VmPZw2D1_DcZ/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/preview_data_out.json", "w") as f:
        json.dump(preview_data, f, indent=2)

    print("Successfully generated full, mini, and preview datasets.")

if __name__ == "__main__":
    main()

