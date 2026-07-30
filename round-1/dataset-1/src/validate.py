# /// script
# dependencies = ["pydantic"]
# ///
import json

def main():
    path = "/ai-inventor/aii_data/runs/run_VmPZw2D1_DcZ/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/full_data_out.json"
    with open(path, "r") as f:
        data = json.load(f)
    
    assert "datasets" in data, "Missing 'datasets' key"
    for ds in data["datasets"]:
        assert "dataset" in ds, "Missing 'dataset' name"
        assert "examples" in ds, "Missing 'examples'"
        for ex in ds["examples"]:
            assert "input" in ex, "Missing 'input'"
            assert "output" in ex, "Missing 'output'"
            for k in ex.keys():
                if k.startswith("metadata_"):
                    pass # valid
                elif k in ["input", "output"]:
                    pass # valid
                else:
                    raise AssertionError(f"Invalid field: {k}")

    # Generate mini and preview versions
    mini_data = {
        "datasets": [
            {
                "dataset": ds["dataset"],
                "examples": ds["examples"][:3]
            }
            for ds in data["datasets"][:5]
        ]
    }
    with open("/ai-inventor/aii_data/runs/run_VmPZw2D1_DcZ/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/mini_data_out.json", "w") as f:
        json.dump(mini_data, f, indent=2)

    with open("/ai-inventor/aii_data/runs/run_VmPZw2D1_DcZ/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/preview_data_out.json", "w") as f:
        json.dump(mini_data, f, indent=2)

    print("Schema validation successful! Mini and preview datasets generated.")

if __name__ == "__main__":
    main()
