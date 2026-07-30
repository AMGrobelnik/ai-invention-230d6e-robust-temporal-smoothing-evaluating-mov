import json
import numpy as np
import os

def evaluate():
    data_path = '/ai-inventor/aii_data/runs/run_VmPZw2D1_DcZ/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/full_data_out.json'
    if not os.path.exists(data_path):
        data_path = '/ai-inventor/aii_data/runs/run_VmPZw2D1_DcZ/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/mini_data_out.json'

    with open(data_path, 'r') as f:
        data = json.load(f)

    datasets_output = []
    
    for ds in data['datasets']:
        ds_name = ds['dataset']
        examples_out = []
        
        for ex in ds['examples']:
            inp = json.loads(ex['input'])
            target = float(ex['output'])
            
            # Naive forecast: last value
            naive_pred = inp[-1]
            
            # Fixed MA (window=3)
            window = 3
            if len(inp) >= window:
                fixed_pred = np.mean(inp[-window:])
            else:
                fixed_pred = np.mean(inp)
            
            # Adaptive MA: adjust window based on recent volatility
            recent = inp[-5:] if len(inp) >= 5 else inp
            vol = np.var(recent) if len(recent) > 1 else 0.0
            
            if vol > 1.0:
                adap_window = 2
            elif vol < 0.2:
                adap_window = 6
            else:
                adap_window = 3
                
            if len(inp) >= adap_window:
                adap_pred = np.mean(inp[-adap_window:])
            else:
                adap_pred = np.mean(inp)
                
            ex_out = {
                "input": ex['input'],
                "output": str(target),
                "metadata_step": ex.get('metadata_step', 0),
                "metadata_noise_level": ex.get('metadata_noise_level', 0.0),
                "metadata_series_length": ex.get('metadata_series_length', len(inp)),
                "predict_naive": str(naive_pred),
                "predict_fixed_ma": str(fixed_pred),
                "predict_adaptive_ma": str(adap_pred)
            }
            examples_out.append(ex_out)
            
        datasets_output.append({
            "dataset": ds_name,
            "examples": examples_out
        })
        
    output = {
        "summary": "Adaptive moving average forecasting evaluation compared against naive and fixed MA across synthetic benchmarks.",
        "datasets": datasets_output
    }
    
    # Save full
    with open('/ai-inventor/aii_data/runs/run_VmPZw2D1_DcZ/3_invention_loop/iter_2/gen_art/gen_art_experiment_1/full_method_out.json', 'w') as f:
        json.dump(output, f, indent=2)
        
    # Save method_out.json as copy of full
    with open('/ai-inventor/aii_data/runs/run_VmPZw2D1_DcZ/3_invention_loop/iter_2/gen_art/gen_art_experiment_1/method_out.json', 'w') as f:
        json.dump(output, f, indent=2)
        
    # Save mini (first 3 datasets)
    mini_output = {
        "summary": output["summary"],
        "datasets": [
            {
                "dataset": ds["dataset"],
                "examples": ds["examples"][:3]
            }
            for ds in datasets_output[:3]
        ]
    }
    with open('/ai-inventor/aii_data/runs/run_VmPZw2D1_DcZ/3_invention_loop/iter_2/gen_art/gen_art_experiment_1/mini_method_out.json', 'w') as f:
        json.dump(mini_output, f, indent=2)
        
    # Save preview (1 dataset, 1 example)
    preview_output = {
        "summary": output["summary"],
        "datasets": [
            {
                "dataset": datasets_output[0]["dataset"],
                "examples": datasets_output[0]["examples"][:1]
            }
        ]
    }
    with open('/ai-inventor/aii_data/runs/run_VmPZw2D1_DcZ/3_invention_loop/iter_2/gen_art/gen_art_experiment_1/preview_method_out.json', 'w') as f:
        json.dump(preview_output, f, indent=2)
        
    print("Evaluation completed successfully and schema-compliant files generated.")

if __name__ == '__main__':
    evaluate()
