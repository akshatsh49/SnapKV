import os, sys, json
import itertools

with open("sample.slurm", "r") as f:
    original = f.read()

use_snaps = [False]
heavy_ratios = [0.1, 0.2, 0.5, 0.6, 0.75, 0.8, 0.9]
recent_ratios = [0.1, 0.2, 0.5, 0.6, 0.75, 0.8, 0.9]
use_eviction_flashs = [False]

quant_bits = [2]
group_sizes = [16]
residual_lengths = [128]

heavy_ratios = [i/2 for i in heavy_ratios]
recent_ratios = [i/2 for i in recent_ratios]

# model_names = ['meta-llama/Llama-2-7b-chat-hf', 'meta-llama/Llama-2-13b-chat-hf', 'mistralai/Mistral-7B-v0.3']
model_names = ['llama2-7b-chat-4k',]

os.makedirs("slurm_jobs", exist_ok=True)
# remove existing job*.slurm files in slurm_jobs
for f in os.listdir("slurm_jobs"):
    if f.startswith("job_"):
        os.remove(os.path.join("slurm_jobs", f))
        print(f"Removed {f}")

# for idx, (model_name, ratio) in enumerate(itertools.product(model_names, prompt_sparsity_ratio)):
# for idx, (model_name, ratio, quant_bit, g_size, length) in enumerate(itertools.product(model_names, prompt_sparsity_ratio, quant_bits, group_sizes, residual_lengths)):
for idx, (model_name, use_snap, heavy_ratio, recent_ratio, use_eviction_flash, quant_bit, g_size, length) in enumerate(itertools.product(model_names, use_snaps, heavy_ratios, recent_ratios, use_eviction_flashs, quant_bits, group_sizes, residual_lengths)):
    if heavy_ratio != recent_ratio:
        continue

    print(f"Creating job_{idx}.slurm")
    # job_content = original + f"CUDA_VISIBLE_DEVICES=0 python3 -u pred_long_bench.py --e --model_name_or_path {model_name} --full_model False --k_bits 2 --v_bits 2 --group_size {size} --recent_ratio {ratio} --heavy_ratio {ratio} --residual_length 128 --use_flash False"
    # job_content = original + f"CUDA_VISIBLE_DEVICES=0 python3 -u pred_long_bench.py --e --model_name_or_path mistralai/Mistral-7B-v0.3 --full_model False --k_bits 2 --v_bits 2 --group_size {size} --recent_ratio {ratio} --heavy_ratio {ratio} --residual_length 128"
    
    # job_content = original + f"CUDA_VISIBLE_DEVICES=0 python3 -u pred_snap.py --model {model_name} --e --full_model False --prompt_sparsity_ratios {ratio} --quant_bits {quant_bit} --group_size {g_size} --residual_length {length}"
    
    job_content = original + f"TOKENIZERS_PARALLELISM=false CUDA_VISIBLE_DEVICES=0 python3 -u pred_snap.py --model {model_name} --e --full_model False --use_snap {use_snap} --heavy_ratio {heavy_ratio} --recent_ratio {recent_ratio} --use_eviction_flash {use_eviction_flash} --quant_bits {quant_bit} --group_size {g_size} --residual_length {length}"
    
    with open(f"slurm_jobs/job_{idx}.slurm", "w") as f:
        f.write(job_content)
