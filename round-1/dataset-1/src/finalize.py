# /// script
# dependencies = []
# ///
import json

def main():
    with open("/ai-inventor/aii_data/runs/run_VmPZw2D1_DcZ/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/full_data_out.json", "r") as f:
        data = json.load(f)
    
    # Keep top 10 datasets
    top_10 = data["datasets"][:10]
    final_data = {"datasets": top_10}
    
    with open("/ai-inventor/aii_data/runs/run_VmPZw2D1_DcZ/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/full_data_out.json", "w") as f:
        json.dump(final_data, f, indent=2)
    print("Filtered to top 10 datasets successfully.")

if __name__ == "__main__":
    main()
